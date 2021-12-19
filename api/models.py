import uuid
import jwt
from flask import Blueprint, jsonify, session, make_response, request, current_app as app
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from api import mongo

auth_blueprint = Blueprint("auth_blueprint", __name__)


class BlacklistToken:
    """
    Token Model for storing JWT tokens
    """

    def __init__(self, token):

        self.token = token
        self.listed_on = datetime.now()
        self._token = {"listed_on": self.listed_on, "token": self.token}

    def __repr__(self):
        return "<id: token: {}".format(self.token)

    def insert(self, db):
        db.deletedTokens.insert_one(self._token)

    @staticmethod
    def check_blacklist(auth_token, db):
        # check whether auth token has been blacklisted
        res = db.deletedTokens.find_one({"token": auth_token})
        if res:
            return True
        else:
            return False


class User:
    def __init__(self, key=app.secret_key, db=mongo.db) -> None:

        self.key = key
        self.db = db
        self.data = request.get_json()

    @staticmethod
    def encode_auth_token(user, key) -> str:
        """
        Generate and encode the Auth Token and returns a string
        """
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
                "iat": datetime.utcnow(),
                "sub": user["_id"],
            }
            return jwt.encode(payload, key, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token, key, db):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token, db)
            if is_blacklisted_token:
                return "Token blacklisted. Please log in again."
            else:
                return payload["sub"]
        except jwt.ExpiredSignatureError:
            return 401
        except jwt.InvalidTokenError:
            return 402

    def start_session(self):
        print("inside session")
        self.user.pop("password")
        session["logged_in"] = True
        session["user"] = self.user
        try:
            session["token"] = self.encode_auth_token(user=self.user, key=self.key)
            responseObject = {"ok": 1, "res": "user logged in", "session": session}
            print (responseObject)
            return make_response(responseObject, 201)

        except Exception as e:
            responseObject = {"status": "fail", "message": e}
            return make_response(jsonify(responseObject)), 500

    def signup(self):

        if not self.db.users.find_one({"email": self.data["email"]}):

            try:
                self.user = {
                    "_id": uuid.uuid4().hex,
                    "name": self.data["fullname"],
                    "username": self.data["username"],
                    "email": self.data["email"],
                    "password": pbkdf2_sha256.encrypt(self.data["password"]),
                }
                self.db.users.insert_one(self.user)
                return self.start_session()

            except Exception as e:
                responseObject = {"status": "fail", "message": "Some error occurred. Please try again."}
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                "status": "fail",
                "message": "User already exists. Please Log in.",
            }
            return make_response(jsonify(responseObject)), 202

    def logout(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = self.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    # mark the token as blacklisted
                    BlacklistToken(token=auth_token).insert(db=self.db)
                    session.clear()
                    responseObject = {"status": "success", "message": "Successfully logged out."}
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {"status": "fail", "message": e}
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {"status": "fail", "message": resp}
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {"status": "fail", "message": "Provide a valid auth token."}
            return make_response(jsonify(responseObject)), 403

    def login(self):

        for item in ["email", "username"]:
            self.user = self.db.users.find_one({item: self.data["identity"]})

            if self.user and pbkdf2_sha256.verify(self.data["password"], self.user["password"]):
                return self.start_session()

            responseObject = {"status": "fail", "message": "Invalid user or password."}
        return make_response(jsonify(responseObject)), 401


class UserAPI(MethodView):
    """
    User Resource
    """

    def get(self):
        # get the auth token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {"status": "fail", "message": "Bearer token malformed."}
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ""
        if auth_token:
            resp = User.decode_auth_token(auth_token, app.config["SECRET_KEY"], mongo.db)
            if isinstance(resp, str):
                user = mongo.db.users.find_one({"_id": resp})
                print(user)
                responseObject = {
                    "status": "success",
                    "data": {
                        "_id": user["_id"],
                        "name": user["name"],
                        "username": user["username"],
                        "email": user["email"],
                    },
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {"status": "fail", "message": resp}
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {"status": "fail", "message": "Provide a valid auth token."}
            return make_response(jsonify(responseObject)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    # mark the token as blacklisted
                    BlacklistToken(token=auth_token).insert(mongo.db)
                    responseObject = {"status": "success", "message": "Successfully logged out."}
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {"status": "fail", "message": e}
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {"status": "fail", "message": resp}
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {"status": "fail", "message": "Provide a valid auth token."}
            return make_response(jsonify(responseObject)), 403


# define the API resources
user_view = UserAPI.as_view("user_api")
logout_view = LogoutAPI.as_view("logout_api")

auth_blueprint.add_url_rule("/auth/status", view_func=user_view, methods=["GET"])
auth_blueprint.add_url_rule("/auth/logout/", view_func=logout_view, methods=["POST"])

from flask import jsonify, json, request, session, make_response
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
import uuid
import jwt


class User:

    def __init__ (
            self, 
            key=None, 
            db=None )-> None:

        self.key = key
        self.db = db

    def encode_auth_token(self)-> str:
        """
        Generate and encode the Auth Token and returns a string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, seconds=600),
                'iat': datetime.utcnow(),
                'sub': self.user['_id']
            }
            return jwt.encode(
                payload,
                self.key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, self.key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def start_session(self):
        self.user.pop("password")
        session['logged_in'] = True
        session['user'] = self.user
        auth_token = self.encode_auth_token()
        # responseObject = {
        #     'status': 'success',
        #     'message': 'Successfully registered.',
        #     'auth_token': auth_token.decode()
        # }
        # return make_response(jsonify(responseObject)), 201
        if auth_token:
            session['token'] = auth_token.decode()
        return make_response(
                jsonify({
                    "ok" : 1, 
                    "res": "user logged in",
                    "session": session})), 201
    
    def signout(self):
        session.clear()
        return jsonify({
                "ok" : 1, 
                "res": "user logged out"}), 200

    def signup(self):

        # load request 
        data = request.get_json()

        # Create User Object
        self.user = {
            "_id":      uuid.uuid4().hex,
            "name":     data['fullname'],
            "username": data['username'],
            "email":    data['email'],
            "password": data['password']
        }

        # ecrypt the password
        self.user["password"] = pbkdf2_sha256.encrypt(self.user["password"])

        # check duplicates  (move this validation prior to submission)
        if self.db.users.find_one({"email": self.user['email']}):
            return jsonify({"error" : "Email address already in use"}), 400

        if self.db.users.find_one({"username": data['username']}):
            return jsonify({"error" : "Username address already in use"}), 400

        # Add user
        if self.db.users.insert_one(self.user):
            return self.start_session()

        return jsonify({"ok": 0, "err" : "Signup failed"}), 400
    
    def login(self):

        #load request
        data = json.loads(request.data)
        for item in ['email', 'username']:
            self.user = self.db.users.find_one({item: data['identity']})

            if self.user and pbkdf2_sha256.verify(data['password'], self.user['password']):
                return self.start_session()

        return jsonify({"error" : "Invalid user or password"}), 401



class Field:

    def validate(self, db):

        # Create User Object
        data = json.loads(request.data)

        # check duplicates  (move this validation prior to submission)
        if db.users.find_one({"email": data}):
            return jsonify({"error" : "Email address already in use"}), 400

        elif db.users.find_one({"username": data}):
            return jsonify({"error" : "Username address already in use"}), 400
        else:
            return 200

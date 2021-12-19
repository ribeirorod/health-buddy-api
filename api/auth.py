from functools import wraps
from flask import Blueprint, request, jsonify, current_app as app
from .models import User, UserAPI, LogoutAPI

from api import mongo

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})
        try:
            payload = User.decode_auth_token(token, app.secret_key)
            current_user = mongo.db.users.find_one({"_id": payload["_id"]})
        except:
            return jsonify({"message": "token is invalid"})
        return f(current_user, *args, **kwargs)

    return wrap

@bp.route("/signup", methods=["POST"])
def signup():
    return User().signup()

@bp.route("/login", methods=["POST"])
def login():
    return User().login()

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()


# define the API resources
user_view = UserAPI.as_view("user_api")
logout_view = LogoutAPI.as_view("logout_api")

bp.add_url_rule("/status", view_func=user_view, methods=["GET"])
bp.add_url_rule("/logout", view_func=logout_view, methods=["POST"])

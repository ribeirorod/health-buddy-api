from flask import current_app as app, jsonify, request, make_response
from functools import wraps

from models import User, auth_blueprint
from config import DevelopmentConfig

from api import mongo



# decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    token = None
    if 'x-access-tokens' in request.headers:
        token = request.headers['x-access-tokens']
        
    if not token:
        return jsonify({'message': 'a valid token is missing'})
    try:
        payload = User.decode_auth_token(token, app.secret_key)
        current_user = mongo.db.users.find_one({'_id': payload['_id']})
    except:
        return jsonify({'message': 'token is invalid'})
    return f(current_user, *args, **kwargs)
  return wrap


@app.route('/auth/signup', methods=['POST'])
def signup():
  return User(key=app.secret_key, db=mongo.db).signup()

@app.route('/auth/login', methods=['POST'])
def login():
  return User(key=app.secret_key, db=mongo.db).login()



from bson import ObjectId



#projection={'_id': True}

# '/auth/status' '/auth/logout/'
app.register_blueprint(auth_blueprint)

# @app.route('/user/logout')
# def logout():
#   return User().logout()

# @app.route('/loginstatus')
# def loginstatus():
#     status = 1 if 'logged_in' in session else 0
#     return jsonify({'logged_in': status})

# @app.route('/user/refresh')
# def refresh(*args):
#   print(arg for arg in args)
#   return session

if __name__ == '__main__':
    app.run(debug=True)


"""
curl localhost:5000/auth/login -d '{"identity": "rodtest", "password":"12345"}' -H 'Content-Type: application/json'
"""
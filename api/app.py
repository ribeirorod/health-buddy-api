from flask import Flask, session, jsonify, request, make_response
from functools import wraps
from flask_pymongo import PyMongo
from models import User, auth_blueprint

app = Flask(__name__)
app.secret_key = b'X\x8aW\xa8\x18z\xba\r\xe53Y\xeb\xc7e\x89{'

# Mongo database
app.config['MONGO_DBNAME'] = "corpus"
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/corpus"
mongo = PyMongo(app)
db = mongo.db

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
        payload = User.decode_auth_token(token, app.config['SECRET_KEY'])
        current_user = db.users.find_one({'_id': payload['_id']})
    except:
        return jsonify({'message': 'token is invalid'})
    return f(current_user, *args, **kwargs)
  return wrap


@app.route('/auth/signup', methods=['POST'])
def signup():
  return User(key=app.secret_key, db=db).signup()

@app.route('/auth/login', methods=['POST'])
def login():
  return User(key=app.secret_key, db=db).login()


import re
from bson import ObjectId

@app.route('/food',methods= ['GET'])
def food():
  response = []
  search = request.args.get('search')
  if isinstance(search, str):
      query = '.+'.join(search.split())
      # for s in search.split():
      #   query =  f'(?=.*?\{s}\b)'
      print(query)
      cursor= list(db.data.find({'description':\
        {"$regex":re.compile(query, re.IGNORECASE)}},\
          {'_id':True, 'description':True }, max_time_ms=1000, limit=20))

      for item in cursor:
        item['_id'] = str(item['_id'])
        response.append(item)

      return make_response(
        jsonify({
          "ok" : 1, 
          "data": response})), 201   
  else:
    return None

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
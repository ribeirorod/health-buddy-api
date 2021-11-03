# backend/api/__init__.py
from flask_pymongo import PyMongo
from flask import Flask
import models
from api.auth.views import auth_blueprint

app = Flask(__name__)
app.secret_key = b'X\x8aW\xa8\x18z\xba\r\xe53Y\xeb\xc7e\x89{'
app.config['MONGO_DBNAME'] = "corpus"
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/corpus"
mongo = PyMongo(app)
db = mongo.db

@app.route('/api')
def home():
    return "This is an example app"

app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(debug=True)



    
    





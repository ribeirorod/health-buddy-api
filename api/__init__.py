from flask import Flask, jsonify
from flask_pymongo import PyMongo
#from flask_restx import Api



def create_app(env=None):
    from api.config import config_by_name
    #from api.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    mongo = PyMongo(app)
    db = mongo.db

    #api = Api(app, title="Flaskerific API", version="0.1.0")

    register_routes(app)
    #db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app

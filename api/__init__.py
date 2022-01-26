import os
from flask import Flask
from flask_pymongo import PyMongo
from api.config import config_by_name

mongo = PyMongo()

def create_app(test_config=None, env="dev"):

    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_by_name[env or "test"])

    # initialize MongoDB
    mongo.init_app(app)

    # ensures the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        # Include our Routes
        from . import models

        # Register Blueprints
        from . import auth, food
        app.register_blueprint(auth.bp)
        app.register_blueprint(food.bp)

    return app

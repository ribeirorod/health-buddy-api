import os
from flask import Flask
from api.config import config_by_name

print(config_by_name)

def create_app(test_config=None, env="dev"):

    app = Flask(__name__, instance_relative_config=True)



    app.config.from_object(config_by_name[env or "test"])
    print(app.instance_path)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app

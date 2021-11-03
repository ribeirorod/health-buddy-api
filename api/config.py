import os
basedir = os.path.abspath(os.path.dirname(__file__))

mongodb_local_base = "mongodb://localhost:27017/corpus"
db_name = 'corpus'

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    #BCRYPT_LOG_ROUNDS = 13
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    MONGO_DBNAME = db_name
    MONGO_URI = mongodb_local_base + db_name

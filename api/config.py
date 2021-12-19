import os
from typing import List, Type

#basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    CONFIG_NAME = "base"
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEVELOPMENT = True
    CONFIG_NAME = "dev"
    SECRET_KEY = b'X\x8aW\xa8\x18z\xba\r\xe53Y\xeb\xc7e\x89{' #os.environ.get("SECRET_KEY")
    DEBUG = True
    MONGO_DBNAME = "corpus"
    MONGO_URI = "mongodb://127.0.0.1:27017/corpus"


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    SECRET_KEY = os.environ.get("TEST_SECRET_KEY", "Thanos did nothing wrong")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "production"
    SECRET_KEY = os.environ.get("PROD_SECRET_KEY", "I'm Ron Burgundy?")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    MONGO_URI = os.environ.get("MONGO_URI")


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}

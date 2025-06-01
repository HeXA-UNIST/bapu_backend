import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SESSION_TYPE = os.getenv("SESSION_TYPE")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./development_db.db"
    SESSION_TYPE = "filesystem"
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test_db.sqlite3"
    SESSION_TYPE = "filesystem"
    TESTING = True


mode = os.getenv("FLASK_ENV", "development")
config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestConfig,
}[mode]
print(f"Running with {mode} mode")

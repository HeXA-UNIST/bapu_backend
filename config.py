import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SESSION_TYPE = os.getenv("SESSION_TYPE")
    SESSION_REDIS = Redis(os.getenv("SESSION_REDIS_HOST"), int(os.getenv("SESSION_REDIS_PORT")))


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./development_db.sqlite3"
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

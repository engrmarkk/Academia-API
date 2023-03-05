import os
from decouple import config
from datetime import timedelta

# This is the base directory for the application
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# This is the configuration object that will be used by the application
class Config:
    # This is the secret key for the application
    SECRET_KEY = config("SECRET_KEY", "secret")
    # This is the expiration minutes for the jwt access token
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    # This is the expiration days for the jwt refresh token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # This is the secret key for the jwt
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True


class AppConfig(Config):
    # This is the debug mode for the application
    DEBUG = True
    # This is the testing mode for the application
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This is the database URI for the application
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "quiz.sqlite3")


class TestConfig(Config):
    # TESTING = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = "sqlite://"
    pass


# This is the dictionary that contains the configuration object
config_object = {"appcon": AppConfig,
                 "testcon": TestConfig}

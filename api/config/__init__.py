import os
from decouple import config
from datetime import timedelta

# This is the base directory for the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# db_name = 'academia'
#
# default_uri = "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', db_name)
#
# uri = os.getenv('DATABASE_URL', default_uri)
# if uri.startswith('postgres://'):
#     uri = uri.replace('postgres://', 'postgresql://', 1)


# This is the configuration object that will be used by the application
class Config:
    # This is the secret key for the application
    SECRET_KEY = config("SECRET_KEY", "secretkey")
    # This is the expiration minutes for the jwt access token
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    # This is the expiration days for the jwt refresh token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    # This is the secret key for the jwt
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", "secret")
    API_TITLE = 'Student Management System'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_JSON_PATH = 'openapi.json'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    OPENAPI_SWAGGER_UI_VERSION = '3.23.11'
    OPENAPI_SWAGGER_UI_JSONEDITOR = True
    PROPAGATE_EXCEPTIONS = True
    API_SPEC_OPTIONS = {
        'security': [{"bearerAuth": []}],
        'components': {
            "securitySchemes":
                {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
        }
    }


class AppConfig(Config):
    # This is the debug mode for the application
    DEBUG = True
    # This is the testing mode for the application
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This is the database URI for the application
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "academia.sqlite3")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    DEBUG = False


class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI = uri
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DEBUG = config('DEBUG', False, cast=bool)
    pass


# This is the dictionary that contains the configuration object
config_object = {"appcon": AppConfig,
                 "testcon": TestConfig,
                 "prodcon": ProdConfig}


"""

"""
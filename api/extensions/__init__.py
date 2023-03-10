from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api()

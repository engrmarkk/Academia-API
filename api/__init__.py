from .extensions import db, migrate, jwt, app, api
from .config import config_object
from .models import Course, Staff, Student, CourseRegistered
# from .auth import user_namespace
from .resources import *
from flask import jsonify
from http import HTTPStatus


# This is the function that creates the app
def create_app(configure=config_object["appcon"]):
    # This line of code configures the application using the configuration object specified.
    # The configuration object contains settings that will be used by the application.
    app.config.from_object(configure)

    # This line of code initializes the extensions imported above
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    api.add_namespace(user_namespace, path="/user")
    api.add_namespace(question_namespace)
    api.add_namespace(option_namespace)
    api.add_namespace(answer_namespace)
    # api.add_namespace(answer_namespace)

    @jwt.expired_token_loader
    def handle_expired_token_error(expired_token, func):
        return jsonify({"message": "Token has expired"}), HTTPStatus.UNAUTHORIZED

    @jwt.unauthorized_loader
    def handle_unauthorized_error(unauthorized_error):
        return jsonify({"message": "Authorization header is missing"}), HTTPStatus.UNAUTHORIZED

    # This line of code imports the routes from the routes package
    @app.shell_context_processor
    # This function returns the database, Question, Options, and Answer models
    def make_shell_context():
        # This returns the database, Question, Options, and Answer models
        return {
                "db": db,
                "Question": Question,
                "Options": Options,
                "Answer": Answer,
                "Users": Users,
                "Is_answered": Is_answered
                }

    return app

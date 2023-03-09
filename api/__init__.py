from .extensions import db, migrate, jwt, app, api
from .config import config_object
from .models import Course, Admin, Student, CourseRegistered
from .auth import blb as AuthBlueprint
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

    # This line of code registers the blueprint imported above
    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(admin_blp)
    app.register_blueprint(student_blp)
    app.register_blueprint(super_admin_blp)

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
        # This returns the database, Staff, Student, Course and CourseRegistered models
        return {
                "db": db,
                "Admin": Admin,
                "Student": Student,
                "Course": Course,
                "CourseRegistered": CourseRegistered
                }

    return app

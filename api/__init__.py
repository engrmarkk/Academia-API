from .extensions import db, migrate, jwt, api
from .config import config_object
from .models import Course, Admin, Student, CourseRegistered
from .auth import blb as AuthBlueprint
from .resources.student import blp as student_blp
from .resources.admin import blp as admin_blp
from flask import jsonify, Flask
from .blocklist import BLOCKLIST


# This is the function that creates the app
def create_app(configure=config_object["appcon"]):

    app = Flask(__name__)

    app.config.from_object(configure)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     return  BlockliskModel.query.filter_by(jwt=jwt_payload["jti"] ).first()

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_additional_claims(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # this is going to check the BLOCKLIST set if the token you're trying to use exist in the set
    # if the token is present in the set, it will return a 'token revoked' message
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # with app.app_context():
    #     #     db.create_all()
    api.register_blueprint(admin_blp)
    api.register_blueprint(student_blp)
    api.register_blueprint(AuthBlueprint)

    @app.shell_context_processor
    def make_shell_context():
        return {"db": db,
                "Admin": Admin,
                "Student": Student,
                "Course": Course,
                "CourseRegistered": CourseRegistered
                }

    return app

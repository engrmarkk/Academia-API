# import all dependencies
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from ..schemas import *
from ..models import Student, Admin
from ..extensions import db
from ..utils import validate_email
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from ..blocklist import BLOCKLIST
# from sqlalchemy import or_
from datetime import timedelta

# create an instance of the Blueprint imported from flask_smorest
blb = Blueprint("auth", __name__, description="auth api")


# # generate a random token for resetting the password
# reset_token = random.randint(0000, 9999)


# use the instance to create a route
# this is the route to register a user
@blb.route("/register")
class Register(MethodView):
    # the argument schema, the input for this registration should have the fields from the schema
    # go to the schema.py file and see the fields in the plainUserSchema
    @blb.arguments(UserRegisterSchema)
    @blb.response(201, plainAdminSchema)
    @blb.doc(description="Register a new user",
             summary="Register a new user")
    def post(self, admin_data):
        if not validate_email(admin_data["email"]):
            abort(400, message="Invalid email address")
        # query the database to check if the username or email already exist in the database
        if Admin.query.filter(Admin.email == admin_data["email"].lower()).first():
            # if any of those details already exist in the database, abort the registration process with
            # a status code of 409
            abort(409, message="An admin with that username or email already exists.")
        if len(admin_data["password"]) < 6:
            abort(400, message="Password must be at least 6 characters long")
        # if the email and username does not exist in the database, then add and commit the user into the database
        admin = Admin(
            first_name=admin_data["first_name"].lower(),
            last_name=admin_data["last_name"].lower(),
            email=admin_data["email"].lower(),
            password=pbkdf2_sha256.hash(admin_data["password"]),
        )
        db.session.add(admin)
        db.session.commit()
        # after a successful registration, return this message to the user
        return admin


# this is an endpoint that uses the refresh token to generate a new access token
@blb.route("/refresh")
class TokenRefresh(MethodView):
    # jwt_required simply means a token will be required to access this route
    # for you to generate a token, you need too login first
    @blb.doc(description="Refresh an access token",
             summary="Refresh an access token using a refresh token")
    @jwt_required(refresh=True)
    def post(self):
        # get the current user's id, use it as an identity to create a new access token using the refresh token
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, expires_delta=timedelta(hours=2)
        )

        # return the new generated token
        return {"access_token": new_token}


# the login route
@blb.route("/login")
class UserLogin(MethodView):
    # the data to be provided during the login process should follow this schema's convention
    @blb.arguments(plainUserLoginSchema)
    @blb.doc(description="Login a user",
             summary="Login a user after providing a valid user_id and password:"
                     "user_id is stud_id for students and adm_id for admins",)
    def post(self, user_data):
        if user_data["user_id"].startswith('ADMIN'):
            # query the database to check if the username exist
            admin = Admin.query.filter(Admin.adm_id == user_data["user_id"]).first()

            # if the username exist, verify if the password matches
            # if the password is valid, create an access token along with s refresh token
            if admin:
                if pbkdf2_sha256.verify(user_data["password"], admin.password):
                    access_token = create_access_token(fresh=True, identity=admin.adm_id)
                    refresh_token = create_refresh_token(identity=admin.adm_id)
                    # return the created tokens
                    return {"access_token": access_token, "refresh_token": refresh_token}
                    # if the username and the password are invalid, abort with a status code of 404
                else:
                    abort(404, message="invalid password")
            else:
                abort(
                    404,
                    message="user not found , invalid adm_id",
                )
        elif user_data["user_id"].startswith('ACA'):
            # query the database to check if the username exist
            student = Student.query.filter(Student.stud_id == user_data["user_id"]).first()

            # if the username exist, verify if the password matches
            # if the password is valid, create an access token along with s refresh token
            if student:
                if pbkdf2_sha256.verify(user_data["password"], student.password):
                    access_token = create_access_token(fresh=True, identity=student.stud_id)
                    refresh_token = create_refresh_token(identity=student.stud_id)
                    # return the created tokens
                    return {"access_token": access_token, "refresh_token": refresh_token}
                else:
                    abort(404, message="Invalid password")
            else:
                # if the username and the password are invalid, abort with a status user_id of 404
                abort(
                    404,
                    message="student not found , invalid stud_id",
                )
        else:
            abort(404, message="Invalid user_id")


@blb.route("/logout")
class UserLogin(MethodView):
    # the jwt_required indicates that the access token will be required to log out
    @blb.doc(description="Logout a user",
             summary="Logout a user after providing a valid access token")
    @jwt_required()
    def post(self):
        # get the current user's token
        jti = get_jwt()["jti"]
        # send the token to the BLOCKLIST set in the blocklist/__init__.py file
        # this will revoke the token. A new access token will be created for you when you log in again
        BLOCKLIST.add(jti)
        # return this message for a successful logout
        return {"message": "Successfully logged out"}

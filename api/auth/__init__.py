# import all dependencies
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from ..schemas import (
    plainStudentSchema,
    plainStaffSchema,
    plainUserLoginSchema
)
from ..models import Student, Staff
from ..extensions import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from ..blocklist import BLOCKLIST
from sqlalchemy import or_
from datetime import timedelta
# from flask_mail import Message
# import random

# create an instance of the Blueprint imported from flask_smorest
blb = Blueprint("user", __name__, description="user api")


# # generate a random token for resetting the password
# reset_token = random.randint(0000, 9999)


# use the instance to create a route
# this is the route to register a user
@blb.route("/student/register")
class StudentRegister(MethodView):
    # the argument schema, the input for this registration should have the fields from the schema
    # go to the schema.py file and see the fields in the plainUserSchema
    @blb.arguments(plainStudentSchema)
    def post(self, student_data):
        # query the database to check if the username and email already exist in the database
        if Student.query.filter(
                or_(
                    Student.username == student_data["username"], Student.email == student_data["email"]
                )
        ).first():
            # if any of those details already exist in the database, abort the registration process with
            # a status code of 409
            abort(409, message="A student with that username or email already exists.")

        # if the email and username does not exist in the database, then add and commit the user into the database
        student = Student(
            first_name=student_data["first_name"],
            last_name=student_data["last_name"],
            username=student_data["username"],
            email=student_data["email"],
            password=pbkdf2_sha256.hash(student_data["password"]),
        )
        db.session.add(student)
        db.session.commit()
        # after a successful registration, return this message to the user
        return {"message": "user created successfully"}


# use the instance to create a route
# this is the route to register a user
@blb.route("/staff/register")
class StaffRegister(MethodView):
    # the argument schema, the input for this registration should have the fields from the schema
    # go to the schema.py file and see the fields in the plainUserSchema
    @blb.arguments(plainStaffSchema)
    def post(self, staff_data):
        # query the database to check if the username and email already exist in the database
        if Staff.query.filter(
                or_(
                    Staff.username == staff_data["username"], Staff.email == staff_data["email"]
                )
        ).first():
            # if any of those details already exist in the database, abort the registration process with
            # a status code of 409
            abort(409, message="A staff with that username or email already exists.")

        # if the email and username does not exist in the database, then add and commit the user into the database
        staff = Staff(
            first_name=staff_data["first_name"].lower(),
            last_name=staff_data["last_name"].lower(),
            username=staff_data["username"].lower(),
            email=staff_data["email"].lower(),
            password=pbkdf2_sha256.hash(staff_data["password"]),
        )
        db.session.add(staff)
        db.session.commit()
        # after a successful registration, return this message to the user
        return {"message": "Staff created successfully"}


# this is an endpoint that uses the refresh token to generate a new access token
@blb.route("/refresh")
class TokenRefresh(MethodView):
    # jwt_required simply means a token will be required to access this route
    # for you to generate a token, you need too login first
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
@blb.route("/user/login")
class UserLogin(MethodView):
    # the data to be provided during the login process should follow this schema's convention
    @blb.arguments(plainUserLoginSchema)
    def post(self, user_data):
        if user_data["user_type"].lower() == "staff":
            # query the database to check if the username exist
            staff = Staff.query.filter(Staff.username == user_data["username"].lower()).first()

            # if the username exist, verify if the password matches
            # if the password is valid, create an access token along with s refresh token
            if staff:
                if pbkdf2_sha256.verify(user_data["password"], staff.password):
                    access_token = create_access_token(fresh=True, identity=staff.id)
                    refresh_token = create_refresh_token(identity=staff.id)
                    # return the created tokens
                    return {"access_token": access_token, "refresh_token": refresh_token}
                    # if the username and the password are invalid, abort with a status code of 404
                else:
                    abort(404, message="invalid password")
            else:
                abort(
                    404,
                    message="staff not found , check if username is correct",
                )
        elif user_data["user_type"].lower() == "student":
            # query the database to check if the username exist
            student = Student.query.filter(Student.username == user_data["username"].lower()).first()

            # if the username exist, verify if the password matches
            # if the password is valid, create an access token along with s refresh token
            if student:
                if pbkdf2_sha256.verify(user_data["password"], student.password):
                    access_token = create_access_token(fresh=True, identity=student.id)
                    refresh_token = create_refresh_token(identity=student.id)
                    # return the created tokens
                    return {"access_token": access_token, "refresh_token": refresh_token}
                else:
                    abort(404, message="Invalid password")
            else:
                # if the username and the password are invalid, abort with a status code of 404
                abort(
                    404,
                    message="student not found , check if username is correct",
                )
        else:
            abort(404, message="You have to be a student or staff to login")


@blb.route("/user/logout")
class UserLogin(MethodView):
    # the jwt_required indicates that the access token will be required to log out
    @jwt_required()
    def post(self):
        # get the current user's token
        jti = get_jwt()["jti"]
        # send the token to the BLOCKLIST set in the blocklist/__init__.py file
        # this will revoke the token. A new access token will be created for you when you log in again
        BLOCKLIST.add(jti)
        # return this message for a successful logout
        return {"message": "Successfully logged out"}

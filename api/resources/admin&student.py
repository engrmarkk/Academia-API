from flask_smorest import Blueprint, abort, Api
from flask.views import MethodView
from ..schemas import *
from ..models import Student, Course, \
    admin_required, student_default_password, CourseRegistered, Admin
from http import HTTPStatus
from ..extensions import db
from ..utils import calculate_gpa
from flask_jwt_extended import jwt_required

blp = Blueprint("admin and student", __name__, description="admin and student accessible endpoints")


from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import jsonify
from ..models import Student, student_required, Course, CourseRegistered
from http import HTTPStatus
from ..extensions import db
from ..schemas import *
from ..utils import available_departments
from flask_jwt_extended import get_jwt_identity
from passlib.hash import pbkdf2_sha256

blp = Blueprint("user", __name__, description="user api")


@blp.route("/check-departments")
class CheckDepartment(MethodView):
    def get(self):
        return jsonify(available_departments), HTTPStatus.OK


@blp.route("/student-profile")
class StudentProfile(MethodView):
    @blp.response(plainStudentSchema)
    @student_required
    def get(self):
        student = Student.query.filter_by(email=get_jwt_identity()).first()
        return student, HTTPStatus.OK

    @blp.arguments(UpdatePasswordByStudentSchema)
    @student_required
    def patch(self, student_data):
        student = Student.query.get(get_jwt_identity())

        if student_data["new_password"] and student_data["new_password"] < 6:
            abort(403, message="Password must be at least 6 characters"), HTTPStatus.FORBIDDEN

        if student_data["old_password"]:
            if student_data["new_password"]:
                if student_data["confirm_password"]:
                    if student_data["new_password"] != student_data["confirm_password"]:
                        abort(403, message="Password does not match"), HTTPStatus.FORBIDDEN
                else:
                    abort(403, message="Confirm password is required"), HTTPStatus.FORBIDDEN
            else:
                abort(403, message="New password is required"), HTTPStatus.FORBIDDEN
        else:
            abort(403, message="Old password is required"), HTTPStatus.FORBIDDEN

        if pbkdf2_sha256.verify(student_data["old_password"], student.password):
            hashed_password = pbkdf2_sha256.hash(student_data["new_password"])
            student.password = hashed_password
            db.session.commit()
            return {"message": "Password updated successfully"}, HTTPStatus.OK
        else:
            abort(403, message="Incorrect password"), HTTPStatus.FORBIDDEN


@blp.route("/student-courses")
class StudentCourses(MethodView):
    @blp.response(plainCourseSchema(many=True))
    @student_required
    def get(self):
        student = Student.query.get(get_jwt_identity())
        courses = Course.query.filter_by(department=student.department).all()
        return courses, HTTPStatus.OK


@blp.route("/register-course")
class RegisterCourse(MethodView):

    def get(self):
        pass

    @blp.arguments(plainCourseSchema)
    @student_required
    def post(self, course_data):
        student = Student.query.get(get_jwt_identity())
        course = Course.query.filter_by(code=course_data["code"]).first()
        if not course:
            abort(404, message="Course not found"), HTTPStatus.NOT_FOUND
        if course.department != student.department:
            abort(403, message="You are not allowed to register for this course"), HTTPStatus.FORBIDDEN
        if course in student.courses:
            abort(403, message="You have already registered for this course"), HTTPStatus.FORBIDDEN
        course_registered = CourseRegistered(
            student_id=student.id,
            course_id=course.id,
            course_code=course.course_code,
            course_title=course.title,
            course_unit=course.course_unit,
            matric_code=student.matric_code
        )
        db.session.add(course_registered)
        db.session.commit()
        return {"message": "Course registered successfully"}, HTTPStatus.CREATED

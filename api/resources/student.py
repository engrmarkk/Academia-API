from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models import Student, student_required, Course, CourseRegistered
from http import HTTPStatus
from ..extensions import db
from ..schemas import *
from flask_jwt_extended import get_jwt_identity
from passlib.hash import pbkdf2_sha256

blp = Blueprint("user", __name__, description="user api")


@blp.route("/get-student-id/<string:email>")
class GetStudentId(MethodView):
    @blp.response(plainStudentID)
    def get(self, email):
        student = Student.query.filter_by(email=email).first()
        if not student:
            abort(404, message="Student not found, contact admin"), HTTPStatus.NOT_FOUND
        return student, HTTPStatus.OK


@blp.route("/student-profile")
class StudentProfile(MethodView):
    @blp.response(plainStudentSchema)
    @student_required
    def get(self):
        student = Student.query.get(get_jwt_identity())
        return student, HTTPStatus.OK

    @blp.arguments(UpdatePasswordByStudentSchema)
    @student_required
    def patch(self, password_data):
        student = Student.query.get(get_jwt_identity())

        if password_data["new_password"] and password_data["new_password"] < 6:
            abort(403, message="Password must be at least 6 characters"), HTTPStatus.FORBIDDEN
        if student.changed_password:
            abort(403, message="Contact the admin to reset your password"), HTTPStatus.FORBIDDEN
        if password_data["new_password"]:
            if password_data["confirm_password"]:
                if password_data["new_password"] != password_data["confirm_password"]:
                    abort(403, message="Password does not match"), HTTPStatus.FORBIDDEN
            else:
                abort(403, message="Confirm password is required"), HTTPStatus.FORBIDDEN
        else:
            abort(403, message="New password is required"), HTTPStatus.FORBIDDEN

        hashed_password = pbkdf2_sha256.hash(password_data["new_password"])
        student.password = hashed_password
        student.changed_password = True
        db.session.commit()
        return {"message": "Password updated successfully",
                "note": "You need to contact your admin for subsequent change of password"}, HTTPStatus.OK


@blp.route("/available-courses")
class StudentCourses(MethodView):
    @blp.response(plainCourseSchema(many=True))
    def get(self):
        courses = Course.query.all()
        return courses, HTTPStatus.OK


@blp.route("/register-course")
class RegisterCourse(MethodView):
    @blp.arguments(plainCourseSchema)
    @student_required
    def post(self, course_data):
        student = Student.query.get(get_jwt_identity())
        course = Course.query.filter_by(code=course_data["code"]).first()
        if not course:
            abort(404, message="Course not found"), HTTPStatus.NOT_FOUND
        if course in student.registered_courses:
            abort(403, message="You have already registered for this course"), HTTPStatus.FORBIDDEN
        course_registered = CourseRegistered(
            student_id=student.id,
            course_id=course.id,
            course_code=course.course_code,
            course_title=course.title,
            course_unit=course.course_unit,
            stud_id=student.stud_id
        )
        db.session.add(course_registered)
        db.session.commit()
        return {"message": f"<Course: {course_data['code']}> registered successfully"}, HTTPStatus.CREATED

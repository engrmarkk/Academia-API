from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..schemas import *
from ..models import Student, Admin, Course, admin_required, student_default_password
from http import HTTPStatus
from ..utils import available_departments
from flask_jwt_extended import get_jwt_identity
from ..extensions import db

blp = Blueprint("admin", __name__, description="admin api")


@blp.route("/students/<string:department>")
class AllStudents(MethodView):
    @blp.response(plainStudentSchema(many=True))
    @admin_required
    def get(self, department):
        if department.lower() not in available_departments:
            abort(403, message="Department not available, access the check-department endpoint to check your department"), HTTPStatus.FORBIDDEN
        if department.lower() != Admin.query.get(get_jwt_identity()).department:
            abort(403, message="You are not allowed to view students in this department"), HTTPStatus.FORBIDDEN
        else:
            students = Student.query.filter_by(department=department.lower()).all()
            return students, HTTPStatus.OK
        if Admin.query.get(get_jwt_identity()).is_super_admin:
            students = Student.query.filter_by(department=department.lower()).all()
            return students, HTTPStatus.OK


@blp.route("/create-student/<string:department>")
class CreateStudent(MethodView):
    @blp.arguments(plainStudentSchema)
    @admin_required
    def post(self, student_data, department: str):
        student = Student.query.filter_by(email=student_data["email"]).first()
        if student:
            abort(409, message="Student already exist"), HTTPStatus.CONFLICT
        if department.lower() != Admin.query.get(get_jwt_identity()).department:
            abort(403, message="You are not allowed to add student to this department"), HTTPStatus.FORBIDDEN
        if department.lower() not in available_departments:
            abort(403, message="Department not available, access the check-department endpoint to check your department"), HTTPStatus.FORBIDDEN
        student = Student(
            first_name=student_data["first_name"].lower(),
            last_name=student_data["last_name"].lower(),
            department=department.lower(),
            email=student_data["email"].lower(),
        )
        db.session.add(student)
        db.session.commit()
        return student, HTTPStatus.CREATED


@blp.route("/student/<string:matric_code>")
class EachStudent(MethodView):
    @blp.response(plainStudentSchema)
    @admin_required
    def get(self, matric_code):
        student = Student.query.filter_by(matric_code).first()
        if not student:
            abort(404, message="Student not found/Invalid code"), HTTPStatus.NOT_FOUND
        if Admin.query.get(get_jwt_identity()).department != student.department:
            abort(403, message="You are not allowed to view this student"), HTTPStatus.FORBIDDEN
        else:
            return student, HTTPStatus.OK
        if Admin.query.get(get_jwt_identity()).is_super_admin:
            return student, HTTPStatus.OK

    def put(self, student_data, matric_code: str):
        student = Student.query.filter_by(matric_code).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        if student_data["first_name"]:
            student.first_name = student_data["first_name"].lower()
        if student_data["last_name"]:
            student.last_name = student_data["last_name"].lower()
        if student_data["email"]:
            student.email = student_data["email"].lower()
        if student_data["department"]:
            student.department = student_data["department"].lower()
        db.session.commit()
        return student, HTTPStatus.OK

    def delete(self, matric_code):
        student = Student.query.filter_by(matric_code).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}, HTTPStatus.OK


@blp.route("/reset-student-password/<string:matric_code>")
class ResetStudentPassword(MethodView):
    @admin_required
    def patch(self, matric_code):
        student = Student.query.filter_by(matric_code).first()
        if not student:
            abort(404, message="Student not found/Invalid code"), HTTPStatus.NOT_FOUND
        if Admin.query.get(get_jwt_identity()).department != student.department:
            abort(403, message="You are not allowed to reset this student password"), HTTPStatus.FORBIDDEN
        student.password = student_default_password('academia')
        db.session.commit()
        return {"message": "Password reset successfully"}, HTTPStatus.OK


@blp.route("/create-course/<string:department>")
class CreateCourse(MethodView):
    @blp.arguments(plainCourseSchema)
    @admin_required
    def post(self, course_data, department: str):
        # errors = plainCourseSchema().validate(request.json)
        # if errors:
        #     abort(400, errors=errors)
        if department.lower() not in available_departments:
            abort(403, message="Department not available, access the check-department endpoint to check your department"), HTTPStatus.FORBIDDEN

        if department != Admin.query.get(get_jwt_identity()).department:
            abort(403, message="You are not allowed to add course to this department"), HTTPStatus.FORBIDDEN

        if Course.query.filter_by(course_code=course_data["course_code"]).first():
            abort(409, message="Course already exist"), HTTPStatus.CONFLICT

        course = Course(
            course_code=course_data["course_code"].upper(),
            course_title=course_data["course_title"].lower(),
            course_unit=course_data["course_unit"],
            semester=course_data["semester"],
            teacher=course_data["teacher"].lower(),
            department=course_data["department"].lower(),
        )
        db.session.add(course)
        db.session.commit()
        return course, HTTPStatus.CREATED

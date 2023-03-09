from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import jsonify, request
from ..models import Student, Admin, admin_required, Course, CourseRegistered, super_admin_required
from http import HTTPStatus
from ..extensions import db
from ..schemas import *
from ..utils import available_departments
from flask_jwt_extended import get_jwt_identity

blp = Blueprint("user", __name__, description="user api")


@blp.route("/students")
class AllStudents(MethodView):
    @blp.response(plainStudentSchema)
    @admin_required
    def get(self):
        students = Student.query.all()
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


@blp.route("/check-departments")
class CheckDepartment(MethodView):
    def get(self):
        return jsonify(available_departments), HTTPStatus.OK


@blp.route("/student/<string:matric_code>")
class EachStudent(MethodView):
    @blp.response(plainStudentSchema)
    @admin_required
    def get(self, matric_code):
        student = Student.query.filter_by(matric_code).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
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
        if student_data["password"]:
            student.password = student_data["password"]
        if student_data["gpa"]:
            student.gpa = student_data["gpa"]
        db.session.commit()
        return student, HTTPStatus.OK

    def delete(self, matric_code):
        student = Student.query.filter_by(matric_code).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}, HTTPStatus.OK


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


@blp.route("/departments-courses/<string:department>")
class DepartmentCourses(MethodView):

    @blp.response(plainCourseSchema)
    @super_admin_required
    def get(self, department):
        if department.lower() not in available_departments:
            abort(403, message="Department not available, access the check-department endpoint to check your department"), HTTPStatus.FORBIDDEN
        courses = Course.query.filter_by(department=department.lower()).all()
        return courses, HTTPStatus.OK


@blp.route("/all-student")
class AllStudent(MethodView):
    def get(self):
        student = Student.query.all()
        return student, HTTPStatus.OK

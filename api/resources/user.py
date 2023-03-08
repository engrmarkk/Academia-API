from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import jsonify
from ..models import Student, Admin, admin_required
from http import HTTPStatus
from ..extensions import db
from ..schemas import *
from ..utils import available_departments

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
        if department != student_data["department"].lower():
            abort(403, message="You are not allowed to add student to this department"), HTTPStatus.FORBIDDEN
        if student_data["department"].lower() not in available_departments:
            abort(403, message="Department not available, access the check-department endpoint to check your department"), HTTPStatus.FORBIDDEN
        student = Student(
            first_name=student_data["first_name"].lower(),
            last_name=student_data["last_name"].lower(),
            department=student_data["department"].lower(),
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

    def patch(self):
        pass

    def delete(self, user_id):
        student = Student.query.get_or_404(user_id)
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}, HTTPStatus.OK


class EachStaff(MethodView):
    def get(self):
        pass

    def patch(self):
        pass

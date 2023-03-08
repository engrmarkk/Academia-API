from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models import Student, Admin
from http import HTTPStatus
from ..extensions import db

blp = Blueprint("user", __name__, description="user api")


@blp.route("/students")
class AllStudents(MethodView):
    def get(self):
        students = Student.query.all()
        return students, HTTPStatus.OK


@blp.route("/student/<int:user_id>")
class EachStudent(MethodView):
    def get(self, user_id):
        student = Student.query.get_or_404(user_id)
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

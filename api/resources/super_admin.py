from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..schemas import *
from ..models import Student, Admin, Course, super_admin_required
from http import HTTPStatus
from ..utils import available_departments

blp = Blueprint("super-admin", __name__, description="super-admin api")


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
    @blp.response(plainStudentSchema(many=True))
    @super_admin_required
    def get(self):
        student = Student.query.all()
        return student, HTTPStatus.OK


@blp.route("/all-admins")
class AllAdmins(MethodView):
    @blp.response(plainAdminSchema(many=True))
    @super_admin_required
    def get(self):
        admins = Admin.query.all()
        return admins, HTTPStatus.OK

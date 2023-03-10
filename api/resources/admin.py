from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..schemas import *
from ..models import Student, Course, \
    admin_required, student_default_password, CourseRegistered
from http import HTTPStatus
from ..extensions import db
from ..utils import calculate_gpa

blp = Blueprint("admin", __name__, description="admin api")


@blp.route("/students")
class AllStudents(MethodView):
    @blp.response(plainStudentSchema(many=True))
    @admin_required
    def get(self):
        students = Student.query.all()
        return students, HTTPStatus.OK


@blp.route("/create-student")
class CreateStudent(MethodView):
    @blp.arguments(plainStudentSchema)
    @admin_required
    def post(self, student_data):
        student = Student.query.filter_by(email=student_data["email"]).first()
        if student:
            abort(409, message="Student already exist"), HTTPStatus.CONFLICT
        student = Student(
            first_name=student_data["first_name"].lower(),
            last_name=student_data["last_name"].lower(),
            email=student_data["email"].lower(),
        )
        db.session.add(student)
        db.session.commit()
        return student, HTTPStatus.CREATED


@blp.route("/student/<string:stud_id>")
class EachStudent(MethodView):
    @blp.response(plainStudentSchema)
    @admin_required
    def get(self, stud_id):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid code"), HTTPStatus.NOT_FOUND
        return student, HTTPStatus.OK

    def put(self, student_data, stud_id: str):
        student = Student.query.filter_by(stud_id).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        if student_data["first_name"]:
            student.first_name = student_data["first_name"].lower()
        if student_data["last_name"]:
            student.last_name = student_data["last_name"].lower()
        if student_data["email"]:
            student.email = student_data["email"].lower()
        db.session.commit()
        return student, HTTPStatus.OK

    def delete(self, stud_id):
        student = Student.query.filter_by(stud_id).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}, HTTPStatus.OK


@blp.route("/reset-student-password/<string:stud_id>")
class ResetStudentPassword(MethodView):
    @admin_required
    def patch(self, stud_id):
        student = Student.query.filter_by(stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid code"), HTTPStatus.NOT_FOUND
        student.password = student_default_password('academia')
        student.password_changed = False
        db.session.commit()
        return {"message": "Password reset successfully"}, HTTPStatus.OK


@blp.route("/create-course/<string:department>")
class CreateCourse(MethodView):
    @blp.arguments(plainCourseSchema)
    @admin_required
    def post(self, course_data):
        # errors = plainCourseSchema().validate(request.json)
        # if errors:
        #     abort(400, errors=errors)

        if Course.query.filter_by(course_code=course_data["course_code"]).first():
            abort(409, message="Course already exist"), HTTPStatus.CONFLICT

        course = Course(
            course_code=course_data["course_code"].upper(),
            course_title=course_data["course_title"].lower(),
            course_unit=course_data["course_unit"],
            teacher=course_data["teacher"].lower(),
        )
        db.session.add(course)
        db.session.commit()
        return course, HTTPStatus.CREATED


@blp.route("/upload-grade/<string:stud_id>/<string:course_code>")
class UploadGrade(MethodView):
    @blp.arguments(plainGradeSchema)
    @admin_required
    def put(self, grade_data, stud_id: str, course_code: str):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid code"), HTTPStatus.NOT_FOUND
        course = Course.query.filter_by(course_code=course_code).first()
        if not course:
            abort(404, message="Course not found/Invalid code"), HTTPStatus.NOT_FOUND
        course_registered = CourseRegistered.query.filter_by(
            stud_id=stud_id, course_code=course_code
        ).first()
        if not course_registered:
            abort(404, message="Student not registered for this course"), HTTPStatus.NOT_FOUND
        course_registered.grade = grade_data["grade"]
        db.session.commit()
        return course_registered, HTTPStatus.OK


@blp.route("/calculate-gpa/<string:stud_id>")
class CalculateGPA(MethodView):
    @admin_required
    def patch(self, stud_id):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid code"), HTTPStatus.NOT_FOUND
        student_grade = student.course_registered.grade
        units = student.course_registered.course.course_unit
        if not student_grade:
            abort(404, message="Student has no grade(s)"), HTTPStatus.NOT_FOUND
        gpa = calculate_gpa(student_grade, units)
        student.gpa = gpa
        db.session.commit()
        return {"message": f"Student GPA is : {gpa}"}, HTTPStatus.OK

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..schemas import *
from ..models import Student, Course, \
    admin_required, student_default_password, CourseRegistered, Admin
from http import HTTPStatus
from ..extensions import db
from ..utils import calculate_gpa
from flask_jwt_extended import jwt_required

blp = Blueprint("admin", __name__, description="admin accessible endpoints")


@blp.route("/students")
class AllStudents(MethodView):
    @blp.response(200, plainStudentSchema(many=True))
    @blp.doc(description='Get all students',
             summary='Get all registered students with their registered courses')
    @jwt_required()
    @admin_required
    def get(self):
        students = Student.query.all()
        return students


@blp.route("/create-student")
class CreateStudent(MethodView):
    @blp.arguments(plainStudentID)
    @blp.response(201, plainStudentID)
    @blp.doc(description='Create a student',
             summary='Create students')
    @jwt_required()
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
        return student


@blp.route("/student/<string:stud_id>")
class EachStudent(MethodView):
    @blp.response(200, plainStudentSchema)
    @blp.doc(description='Get a student by stud_id',
             summary='Get a student\'s details')
    @jwt_required()
    @admin_required
    def get(self, stud_id):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        return student

    @blp.arguments(UpdateStudentDetails)
    @blp.response(200, UpdateStudentDetails)
    @blp.doc(description='Update a student by stud_id',
             summary='Update a student\'s details')
    @jwt_required()
    @admin_required
    def put(self, student_data, stud_id: str):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND

        first_name = student_data.get("first_name", None)
        if first_name:
            student.first_name = student_data["first_name"].lower()

        last_name = student_data.get("last_name", None)
        if last_name:
            student.last_name = student_data["last_name"].lower()

        email = student_data.get("email", None)
        if email:
            student.email = student_data["email"].lower()
        db.session.commit()
        return student

    @blp.doc(description='Delete a student by stud_id',
             summary='Delete a student from the system')
    @jwt_required()
    @admin_required
    def delete(self, stud_id):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}, HTTPStatus.OK


@blp.route("/reset-student-password/<string:stud_id>")
class ResetStudentPassword(MethodView):

    @blp.doc(description='Reset student password',
             summary='Reset student password to default')
    @jwt_required()
    @admin_required
    def patch(self, stud_id):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        student.password = student_default_password('academia')
        student.changed_password = False
        db.session.commit()
        return {"message": "Password reset successfully"}, HTTPStatus.OK


@blp.route("/create-course")
class CreateCourse(MethodView):
    @blp.arguments(plainCourseSchema)
    @blp.response(201, plainCourseSchema)
    @blp.doc(description='Create a course',
             summary='Create courses for the system')
    @jwt_required()
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
        return course


@blp.route("/course/<string:course_code>")
class CreateCourse(MethodView):
    @blp.arguments(UpdateCourseSchema)
    @blp.response(200, UpdateCourseSchema)
    @blp.doc(description='Update a course',
             summary='Update an available course')
    @jwt_required()
    @admin_required
    def put(self, course_data, course_code: str):
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND

        course_title = course_data.get("course_title", None)
        if course_title:
            course.course_title = course_title.lower()

        course_unit = course_data.get("course_unit", None)
        if course_unit is not None:
            course.course_unit = course_unit

        teacher = course_data.get("teacher", None)
        if teacher:
            course.teacher = teacher.lower()

        db.session.commit()
        return course

    @blp.doc(description='Delete a course',
             summary='Delete an available course')
    @jwt_required()
    @admin_required
    def delete(self, course_code: str):
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND
        db.session.delete(course)
        db.session.commit()
        return {"message": f"Course<{course_code}> deleted"}, HTTPStatus.OK


@blp.route("/upload-grade/<string:stud_id>/<string:course_code>")
class UploadGrade(MethodView):
    @blp.arguments(plainGradeSchema)
    @blp.response(200, plainCourseRegisteredSchema)
    @blp.doc(description='Upload grade for a student',
             summary='Upload grade for a student using stud_id (i.e matric number) and course_code')
    @jwt_required()
    @admin_required
    def put(self, grade_data, stud_id: str, course_code: str):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND
        course_registered = CourseRegistered.query.filter_by(
            stud_id=stud_id, course_code=course_code.upper()
        ).first()
        # if course_registered and course_registered.grade:
        #     abort(409, message="Grade already uploaded"), HTTPStatus.CONFLICT
        if not course_registered:
            abort(404, message="Student not registered for this course"), HTTPStatus.NOT_FOUND
        if grade_data["grade"] < 1 or grade_data["grade"] > 100:
            abort(400, message="Grade must be between 1 and 100"), HTTPStatus.BAD_REQUEST
        # if not grade_data["grade"]:
        #     abort(400, message="Grade cannot be empty"), HTTPStatus.BAD_REQUEST
        course_registered.grade = grade_data["grade"]
        db.session.commit()
        return course_registered


@blp.route("/calculate-gpa/<string:stud_id>")
class CalculateGPA(MethodView):

    @blp.doc(description='Calculate student GPA',
             summary='Calculate student GPA using stud_id (i.e matric number)')
    @jwt_required()
    @admin_required
    def patch(self, stud_id):
        student = Student.query.filter_by(stud_id=stud_id).first()
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND

        course_registered_records = CourseRegistered.query.filter_by(stud_id=stud_id).all()
        student_grades = [record.grade for record in course_registered_records]

        course_registered_records = CourseRegistered.query.filter_by(stud_id=stud_id).all()
        student_units = [record.course_unit for record in course_registered_records]

        if not student_grades:
            abort(404, message="Student has no grade(s)"), HTTPStatus.NOT_FOUND
        gpa = calculate_gpa(student_grades, student_units)
        student.gpa = gpa
        db.session.commit()
        return {"message": f"Uploaded successfully, student GPA is : {gpa}"}, HTTPStatus.OK


@blp.route("/get-admins")
class GetAdmin(MethodView):
    @blp.response(200, plainAdminSchema(many=True))
    @blp.doc(description='Get all admins',
             summary='Get all registered admins')
    def get(self):
        admin = Admin.query.all()
        return admin


@blp.route("/courses-students")
class GetCoursesStudents(MethodView):
    @blp.response(200, ListCoursesWithStudentSchema(many=True))
    @blp.doc(description='Get all courses and students registered for each course',
             summary='Get all courses and students registered for each course')
    @jwt_required()
    @admin_required
    def get(self):
        all_course = Course.query.all()
        return all_course

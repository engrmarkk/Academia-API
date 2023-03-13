from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models import Student, student_required, Course, CourseRegistered, check_if_registered
from http import HTTPStatus
from ..extensions import db
from ..schemas import *
from flask_jwt_extended import get_jwt_identity, jwt_required
from passlib.hash import pbkdf2_sha256

blp = Blueprint("student", __name__, description="student accessible endpoints")


@blp.route("/get-student-id/<string:email>")
class GetStudentId(MethodView):
    @blp.response(200, plainStudentID)
    @blp.doc(description='Get a student\'s stud_id (i.e matric number) by email',
             summary='Get a student\'s stud_id: This will fetch the student\'s matric '
                     'number that will be used to login')
    def get(self, email):
        student = Student.query.filter_by(email=email).first()
        if not student:
            abort(404, message="Student not found, contact admin"), HTTPStatus.NOT_FOUND
        return student


@blp.route("/student-profile")
class StudentProfile(MethodView):
    @blp.response(200, plainStudentSchema)
    @blp.doc(description='Get a student\'s profile',
             summary='Get an authenticated student\'s profile')
    @jwt_required()
    @student_required
    def get(self):
        student = Student.query.filter_by(stud_id=get_jwt_identity()).first()
        return student

    @blp.arguments(UpdatePasswordByStudentSchema)
    @blp.doc(description='Update a student\'s password',
             summary='Change the student\'s password, this can only be done once')
    @jwt_required()
    @student_required
    def patch(self, password_data):
        student = Student.query.filter_by(stud_id=get_jwt_identity()).first()

        if password_data["new_password"] and len(password_data["new_password"]) < 6:
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


# This endpoint can also be accessed by the admin
@blp.route("/available-courses")
class StudentCourses(MethodView):
    @blp.response(200, plainCourseSchema(many=True))
    @blp.doc(description='Get all available courses',
             summary='Get all available courses with their respective course codes,'
                     ' course titles, course units and course lecturers,'
                     'this will enable the student to know the correct course code to register')
    def get(self):
        courses = Course.query.all()
        return courses


@blp.route("/register-course")
class RegisterCourse(MethodView):
    @blp.arguments(RegisterACourseSchema)
    @blp.doc(description='Register a course',
             summary='Register a course by providing the valid course code')
    @jwt_required()
    @student_required
    def post(self, course_data):
        student = Student.query.filter_by(stud_id=get_jwt_identity()).first()
        course = Course.query.filter_by(course_code=course_data["course_code"].upper()).first()
        if not course:
            abort(404, message="Course not found"), HTTPStatus.NOT_FOUND
        if check_if_registered(course_data["course_code"].upper()):
            abort(403, message="Course already registered"), HTTPStatus.FORBIDDEN
        course_registered = CourseRegistered(
            student_id=student.id,
            course_id=course.id,
            course_code=course.course_code,
            course_title=course.course_title,
            course_unit=course.course_unit,
            first_name=student.first_name,
            last_name=student.last_name,
            stud_id=student.stud_id
        )
        db.session.add(course_registered)
        db.session.commit()
        return {"message": f"<Course: {course_data['course_code'].upper()}> registered successfully"}, HTTPStatus.CREATED

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..models import Student, student_required, Course, CourseRegistered, check_if_registered
from http import HTTPStatus
from ..extensions import db
from ..schemas import *
from flask_jwt_extended import get_jwt_identity, jwt_required
from passlib.hash import pbkdf2_sha256

# create an instance of the Blueprint imported from flask_smorest
blp = Blueprint("student", __name__, description="student accessible endpoints")


@blp.route("/get-student-id/<string:email>")
class GetStudentId(MethodView):
    @blp.response(200, plainStudentID)
    @blp.doc(description='Get a student\'s stud_id (i.e matric number) by email',
             summary='Get a student\'s stud_id: This will fetch the student\'s matric '
                     'number that will be used to login')
    # get the student's id (i.e. matric number) by email
    def get(self, email):
        # query the database to check if the student exist
        student = Student.query.filter_by(email=email).first()
        # if the student does not exist, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found, contact admin"), HTTPStatus.NOT_FOUND
        # if the student exist, return the student's id
        return student


@blp.route("/student-profile")
class StudentProfile(MethodView):
    @blp.response(200, plainStudentSchema)
    @blp.doc(description='Get a student\'s profile',
             summary='Get an authenticated student\'s profile')
    @jwt_required()
    @student_required
    # get the student's profile
    def get(self):
        # query the database for the authenticated student's profile
        student = Student.query.filter_by(stud_id=get_jwt_identity()).first()
        # return the student's profile
        return student

    @blp.arguments(UpdatePasswordByStudentSchema)
    @blp.doc(description='Update a student\'s password',
             summary='Change the student\'s password, this can only be done once')
    @jwt_required()
    @student_required
    # update the student's password
    def patch(self, password_data):
        # query the database for the authenticated student's profile
        student = Student.query.filter_by(stud_id=get_jwt_identity()).first()
        # check if a new password was provided and if the password is less than 6 characters
        # if the password is less than 6 characters, abort the process with a status code of 403
        if password_data["new_password"] and len(password_data["new_password"]) < 6:
            abort(403, message="Password must be at least 6 characters"), HTTPStatus.FORBIDDEN
        # check if the student has changed their password before
        # if the student has changed their password before, abort the process with a status code of 403
        if student.changed_password:
            abort(403, message="Contact the admin to reset your password"), HTTPStatus.FORBIDDEN
        # if new password and confirm password are provided, check if they match
        # if the new password is provided and the confirm password is not provided, abort the process with a status code of 403
        # if the new password is not provided and the confirm password is provided, abort the process with a status code of 403
        # if the new password is provided and the confirm password is provided, check if they match
        # if the new password is provided and the confirm password is provided but they do not match, abort the process with a status code of 403
        # if the new password is provided and the confirm password is provided and they match, hash the new password and update the student's password
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
    # get all available courses
    def get(self):
        # query the database for all available courses
        courses = Course.query.all()
        # return all available courses
        return courses


@blp.route("/register-course")
class RegisterCourse(MethodView):
    @blp.arguments(RegisterACourseSchema)
    @blp.doc(description='Register a course',
             summary='Register a course by providing the valid course code')
    @jwt_required()
    @student_required
    # register a course
    def post(self, course_data):
        # query the database for the authenticated student's profile
        student = Student.query.filter_by(stud_id=get_jwt_identity()).first()
        # query the database for the course to be registered, check if the course exist
        course = Course.query.filter_by(course_code=course_data["course_code"].upper()).first()
        # if the course does not exist, abort the process with a status code of 404
        if not course:
            abort(404, message="Course not found"), HTTPStatus.NOT_FOUND
        # check if the student has registered for the course before by passing the course code into the check_if_registered function
        # the check_if_registered function will return True if the student has registered for the course before
        # if the student has registered for the course before, abort the process with a status code of 403
        if check_if_registered(course_data["course_code"].upper()):
            abort(403, message="Course already registered"), HTTPStatus.FORBIDDEN
        # if the student has not registered for the course before, register the student for the course
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
        # add the course to the database and commit the changes
        db.session.add(course_registered)
        db.session.commit()
        # return a success message
        return {"message": f"<Course: {course_data['course_code'].upper()}> registered successfully"}, HTTPStatus.CREATED


# @blp.route("/delete-course/<string:course_code>")
# class RegisterCourse(MethodView):
#     @blp.doc(description='Delete a registered course',
#              summary='Delete a registered course by providing the valid course code')
#     @jwt_required()
#     @student_required
#     def delete(self, course_code):
#         course = Course.query.filter_by(course_code=course_code).first()
#         if not course:
#             abort(404, message="Course not found"), HTTPStatus.NOT_FOUND
#         if course and not check_if_registered(course_code):
#             abort(404, message="Course not registered"), HTTPStatus.NOT_FOUND
#         course_registered = CourseRegistered.query.filter_by(course_code=course_code,
#                                                              stud_id=get_jwt_identity()).first()
#         if course_registered.score:
#             abort(403, message='You cannot delete a graded course')
#         db.session.delete(course_registered)
#         db.session.commit()
#         return {"message": f"<Course: {course_code}> deleted successfully"}, HTTPStatus.OK

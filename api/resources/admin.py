from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..schemas import *
from ..models import Student, Course, \
    admin_required, student_default_password, CourseRegistered, Admin
from http import HTTPStatus
from ..extensions import db
from ..utils import calculate_gpa, get_grade, validate_email
from flask_jwt_extended import jwt_required

# create an instance of the Blueprint imported from flask_smorest
blp = Blueprint("admin", __name__, description="admin accessible endpoints")


# use the instance to create a route
@blp.route("/students")
class AllStudents(MethodView):
    @blp.response(200, plainStudentSchema(many=True))
    @blp.doc(description='Get all students',
             summary='Get all registered students with their registered courses')
    @jwt_required()
    @admin_required
    def get(self):
        # get all the students from the database
        students = Student.query.all()
        # return the students
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
        # check if the email of the student you want to create follows the email format
        # this is done by calling the validate_email function from the utils.py file and passing the student's email
        if not validate_email(student_data["email"]):
            # if not, abort the process with a status code of 403
            abort(403, message="Invalid email"), HTTPStatus.FORBIDDEN
        # check if the student already exist in the database using the email
        student = Student.query.filter_by(email=student_data["email"]).first()
        # if the student already exist in the database, abort the process with a status code of 409
        if student:
            abort(409, message="Student already exist"), HTTPStatus.CONFLICT
        # if the student does not exist in the database, create the student
        student = Student(
            first_name=student_data["first_name"].lower(),
            last_name=student_data["last_name"].lower(),
            email=student_data["email"].lower(),
        )
        # add the student to the database
        db.session.add(student)
        # commit the changes
        db.session.commit()
        # return the student
        return student


@blp.route("/student/<string:stud_id>")
class EachStudent(MethodView):
    @blp.response(200, plainStudentSchema)
    @blp.doc(description='Get a student by stud_id',
             summary='Get a student\'s details')
    @jwt_required()
    @admin_required
    # get the student's details
    def get(self, stud_id):
        # get the student from the database using the stud_id
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        # if the student exist in the database, return the student
        return student

    @blp.arguments(UpdateStudentDetails)
    @blp.response(200, UpdateStudentDetails)
    @blp.doc(description='Update a student by stud_id',
             summary='Update a student\'s details')
    @jwt_required()
    @admin_required
    # update the student's details
    def put(self, student_data, stud_id: str):
        # get the student from the database using the student's id which is the matric number
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        # if the student exist in the database, update the student's details
        # check if the student's first name is in the student_data dictionary
        # if it is, update the student's first name, if not, leave it as it is
        first_name = student_data.get("first_name", None)
        if first_name:
            student.first_name = student_data["first_name"].lower()

        # check if the student's last name is in the student_data dictionary
        # if it is, update the student's last name, if not, leave it as it is
        last_name = student_data.get("last_name", None)
        if last_name:
            student.last_name = student_data["last_name"].lower()

        # check if the student's email is in the student_data dictionary
        # if it is, update the student's email, if not, leave it as it is
        email = student_data.get("email", None)
        if email:
            student.email = student_data["email"].lower()
        # commit the changes
        db.session.commit()
        # return the student
        return student

    @blp.doc(description='Delete a student by stud_id',
             summary='Delete a student from the system')
    @jwt_required()
    @admin_required
    # delete a student
    def delete(self, stud_id):
        # get the student from the database using the student's id which is the matric number
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found"), HTTPStatus.NOT_FOUND
        # if the student exist in the database, delete the student
        db.session.delete(student)
        # commit the changes
        db.session.commit()
        # return a message that the student has been deleted
        return {"message": "Student deleted"}, HTTPStatus.OK


@blp.route("/reset-student-password/<string:stud_id>")
class ResetStudentPassword(MethodView):

    @blp.doc(description='Reset student password',
             summary='Reset student password to default')
    @jwt_required()
    @admin_required
    # reset student password
    def patch(self, stud_id):
        # get the student from the database using the student's id which is the matric number
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        # if the student exist in the database, reset the student's password
        # set the student's password to the default password
        student.password = student_default_password('academia')
        # set the student's password_changed to False
        # this is to enable the student to change the password on the next login
        student.changed_password = False
        # commit the changes
        db.session.commit()
        # return a message that the student's password has been reset
        return {"message": "Password reset successfully"}, HTTPStatus.OK


@blp.route("/create-course")
class CreateCourse(MethodView):
    @blp.arguments(plainCourseSchema)
    @blp.response(201, plainCourseSchema)
    @blp.doc(description='Create a course',
             summary='Create courses for the system')
    @jwt_required()
    @admin_required
    # create a course
    def post(self, course_data):
        # errors = plainCourseSchema().validate(request.json)
        # if errors:
        #     abort(400, errors=errors)

        # check if the course already exist in the database
        # if it does, abort the process with a status code of 409
        if Course.query.filter_by(course_code=course_data["course_code"]).first():
            abort(409, message="Course already exist"), HTTPStatus.CONFLICT

        # if the course does not exist in the database, create the course
        course = Course(
            course_code=course_data["course_code"].upper(),
            course_title=course_data["course_title"].lower(),
            course_unit=course_data["course_unit"],
            teacher=course_data["teacher"].lower(),
        )
        # commit the changes
        db.session.add(course)
        # commit the changes
        db.session.commit()
        # return the course
        return course


@blp.route("/course/<string:course_code>")
class CreateCourse(MethodView):
    @blp.arguments(UpdateCourseSchema)
    @blp.response(200, UpdateCourseSchema)
    @blp.doc(description='Update a course',
             summary='Update an available course')
    @jwt_required()
    @admin_required
    # update a course
    def put(self, course_data, course_code: str):
        # check if the course exist in the database
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        # if the course does not exist in the database, abort the process with a status code of 404
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND

        # if the course exist in the database, update the course's details
        # check if the course's title is in the course_data dictionary
        # if it is, update the course's title, if not, leave it as it is
        course_title = course_data.get("course_title", None)
        if course_title:
            course.course_title = course_title.lower()

        # check if the course's unit is in the course_data dictionary
        # if it is, update the course's unit, if not, leave it as it is
        course_unit = course_data.get("course_unit", None)
        if course_unit:
            course.course_unit = course_unit

        # check if the course's teacher is in the course_data dictionary
        # if it is, update the course's teacher, if not, leave it as it is
        teacher = course_data.get("teacher", None)
        if teacher:
            course.teacher = teacher.lower()
        # commit the changes
        db.session.commit()
        # return the course
        return course

    @blp.doc(description='Delete a course',
             summary='Delete an available course')
    @jwt_required()
    @admin_required
    # delete a course
    def delete(self, course_code: str):
        # check if the course exist in the database
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        # if the course does not exist in the database, abort the process with a status code of 404
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND
        # if the course exist in the database, delete the course
        db.session.delete(course)
        # commit the changes
        db.session.commit()
        # return a message that the course has been deleted
        return {"message": f"Course<{course_code}> deleted"}, HTTPStatus.OK


@blp.route("/get-grade/<string:stud_id>/<string:course_code>")
class GetGradeOfEachStudent(MethodView):
    @blp.response(200, GetStudentGradeSchema)
    @blp.doc(description='Get grade of a student',
             summary='Get grade of a student using stud_id (i.e matric number) and course_code')
    @jwt_required()
    @admin_required
    # get grade of a student
    def get(self, stud_id: str, course_code: str):
        # check if the student exist in the database
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        # check if the course exist in the database
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        # if the course does not exist in the database, abort the process with a status code of 404
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND
        # check if the student is registered for the course
        course_registered = CourseRegistered.query.filter_by(student_id=student.id, course_id=course.id).first()
        # if the student is not registered for the course, abort the process with a status code of 404
        if not course_registered:
            abort(404, message="Student not registered for this course"), HTTPStatus.NOT_FOUND
        # if the student is registered for the course, return the student's grade
        return course_registered


@blp.route("/upload-score/<string:stud_id>/<string:course_code>")
class UploadScore(MethodView):
    @blp.arguments(plainscoreSchema)
    @blp.response(200, plainCourseRegisteredSchema)
    @blp.doc(description='Upload score for a student',
             summary='Upload score for a student using stud_id (i.e matric number) and course_code')
    @jwt_required()
    @admin_required
    # upload score for a student
    def put(self, score_data, stud_id: str, course_code: str):
        # check if the student exist in the database
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND
        # check if the course exist in the database
        course = Course.query.filter_by(course_code=course_code.upper()).first()
        # if the course does not exist in the database, abort the process with a status code of 404
        if not course:
            abort(404, message="Course not found/Invalid course_code"), HTTPStatus.NOT_FOUND
        # check if the student is registered for the course
        course_registered = CourseRegistered.query.filter_by(
            stud_id=stud_id, course_code=course_code.upper()
        ).first()

        # if the student is not registered for the course, abort the process with a status code of 404
        if not course_registered:
            abort(404, message="Student not registered for this course"), HTTPStatus.NOT_FOUND
        # if the score is not between 1 and 100, abort the process with a status code of 400
        if score_data["score"] < 1 or score_data["score"] > 100:
            abort(400, message="score must be between 1 and 100"), HTTPStatus.BAD_REQUEST
        # if not score_data["score"]:
        #     abort(400, message="score cannot be empty"), HTTPStatus.BAD_REQUEST
        # if the student is registered for the course, update the student's score
        course_registered.score = score_data["score"]
        # update the student's grade
        # the get_grade function is in the utils.py file, it returns the grade based on the score
        course_registered.grade = get_grade(score_data["score"])
        # commit the changes
        db.session.commit()
        # return the student's score and grade
        return course_registered


@blp.route("/calculate-gpa/<string:stud_id>")
class CalculateGPA(MethodView):

    @blp.doc(description='Calculate student GPA',
             summary='Calculate student GPA using stud_id (i.e matric number)')
    @jwt_required()
    @admin_required
    # calculate student GPA
    def patch(self, stud_id):
        # check if the student exist in the database
        student = Student.query.filter_by(stud_id=stud_id).first()
        # if the student does not exist in the database, abort the process with a status code of 404
        if not student:
            abort(404, message="Student not found/Invalid stud_id"), HTTPStatus.NOT_FOUND

        # query the database to get the student's details from the course_registered table
        course_registered_records = CourseRegistered.query.filter_by(stud_id=stud_id).all()
        # get the student's score by looping through the course_registered_records and getting the score
        student_scores = [record.score for record in course_registered_records]

        course_registered_records = CourseRegistered.query.filter_by(stud_id=stud_id).all()
        # get the student's course unit by looping through the course_registered_records and getting the course_unit
        student_units = [record.course_unit for record in course_registered_records]

        # if the student has no score, abort the process with a status code of 404
        if not student_scores:
            abort(404, message="Student has no score(s)"), HTTPStatus.NOT_FOUND
        # calculate the student's GPA by calling the calculate_gpa function in the utils.py file and passing in the student's score and course unit
        gpa = calculate_gpa(student_scores, student_units)
        # update the student's GPA in the database
        student.gpa = gpa
        # commit the changes
        db.session.commit()
        # return the student's GPA
        return {"message": f"Uploaded successfully, student GPA is : {gpa}"}, HTTPStatus.OK


@blp.route("/get-admins")
class GetAdmin(MethodView):
    @blp.response(200, plainAdminSchema(many=True))
    @blp.doc(description='Get all admins',
             summary='Get all registered admins')
    # get all admins
    def get(self):
        # query the database to get all admins
        admin = Admin.query.all()
        # return all admins
        return admin


@blp.route("/courses-students")
class GetCoursesStudents(MethodView):
    @blp.response(200, ListCoursesWithStudentSchema(many=True))
    @blp.doc(description='Get all courses and students registered for each course',
             summary='Get all courses and students registered for each course')
    @jwt_required()
    @admin_required
    # get all courses and students registered for each course
    def get(self):
        # query the database to get all courses and students registered for each course
        all_course = Course.query.all()
        # return all courses and students registered for each course
        return all_course

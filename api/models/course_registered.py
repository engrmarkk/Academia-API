from ..extensions import db
from flask_jwt_extended import get_jwt_identity


# This is the model for the registered courses by students
class CourseRegistered(db.Model):
    __tablename__ = 'course_registered'
    # The id column is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # The score column is not nullable with a default value of 0.0
    score = db.Column(db.Float, nullable=False, default=0.0)
    # The grade column is not nullable with a default value of N/A
    grade = db.Column(db.String(10), default='N/A')
    # The course_code column is not nullable, this is the course code
    course_code = db.Column(db.String(80), nullable=False)
    # The course_title column is not nullable, this is the course title
    course_title = db.Column(db.String(100), nullable=False)
    # The stud_id column is not nullable, this is the student id
    stud_id = db.Column(db.String(80), nullable=False)
    # The course_unit column is not nullable, this is the course unit
    course_unit = db.Column(db.Integer, nullable=False)
    # the first_name of the student
    first_name = db.Column(db.String(50), nullable=False)
    # the last_name of the student
    last_name = db.Column(db.String(50), nullable=False)
    # the student's id, it is a foreign key linked to the students table
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    # the course's id, it is a foreign key linked to the courses table
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return '<CourseRegistered %r>' % self.id


# This function checks if a course is registered by a student
def check_if_registered(course_code):
    # query the course_registered table to check if the course is registered by the student
    course = CourseRegistered.query.filter_by(
        course_code=course_code, stud_id=get_jwt_identity()
    ).first()
    # if the course is registered, return True
    if course:
        return True
    # if the course is not registered, return False
    return False

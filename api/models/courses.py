from ..extensions import db
from datetime import datetime


# This is the model for the courses
class Course(db.Model):
    __tablename__ = 'courses'
    # The id column is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # the course_title column
    course_title = db.Column(db.String(100), nullable=False)
    # the course_code column
    course_code = db.Column(db.String(80), unique=True, nullable=False)
    # the year column, it takes the current year as the default value
    year = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    # the course unit column
    course_unit = db.Column(db.Integer, nullable=False)
    # the created_at column, it takes the current date as the default value
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now().date())
    # the teacher column
    teacher = db.Column(db.String(150), nullable=False)
    # the registered_courses column, it is a relationship with the CourseRegistered model
    registered_courses = db.relationship('CourseRegistered', backref='course', lazy=True, cascade="all, delete")
    # the student_registered column, it is also a relationship with the CourseRegistered model
    # the viewonly=True makes it a read-only relationship
    # the overlaps="course,registered_courses" makes it a read-only relationship
    student_registered = db.relationship('CourseRegistered', viewonly=True, overlaps="course,registered_courses", backref='student_')

    def __repr__(self):
        return '<Course %r>' % self.name

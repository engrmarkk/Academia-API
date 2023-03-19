from functools import wraps
from flask_jwt_extended import get_jwt_identity
from ..extensions import db
from flask_smorest import abort
from passlib.hash import pbkdf2_sha256
import random
from datetime import datetime


# function to hash the default password
# it takes the default password as an argument
def student_default_password(default_password):
    # hash the default password
    pass_word = pbkdf2_sha256.hash(default_password)
    # return the hashed password
    return pass_word


# function to generate a unique code
def code_generator(prefix: str):
    # generate a random number
    unique_code = random.randint(100000, 999999)
    # convert the random number to a string
    unique_code = str(unique_code)
    # concatenate the prefix and the random number
    # the prefix is an argument passed to the function
    mat_num = prefix + unique_code
    # return the unique code
    return mat_num


# This is the model for the students
class Student(db.Model):
    __tablename__ = 'students'
    # The id column is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # the first_name column
    first_name = db.Column(db.String(80), nullable=False)
    # the last_name column
    last_name = db.Column(db.String(80), nullable=False)
    # the email column is unique and not nullable
    email = db.Column(db.String(120), unique=True, nullable=False)
    # student_id column is unique and not nullable, this is the student's matriculation number
    # the default value is a function that generates a unique code with the prefix 'ACA' and the current year
    stud_id = db.Column(db.String(50), unique=True, nullable=False,
                        default=code_generator(f'ACA-{datetime.now().year}-'))
    # the gpa column is not nullable, the default value is 0.00
    gpa = db.Column(db.Float, nullable=False, default=0.00)
    # the password column is not nullable, the default value is a function that hashes the default password
    # the default password is the argument passed to the function
    password = db.Column(db.Text, nullable=False,
                         default=student_default_password('academia'))
    # the changed_password column is not nullable, the default value is False
    # this column is used to check if the student has changed the default password
    changed_password = db.Column(db.Boolean, nullable=False, default=False)
    # the registered_courses column is a relationship with the CourseRegistered model
    registered_courses = db.relationship('CourseRegistered',
                                         cascade="all, delete", backref='student', lazy=True)

    # The __repr__ method is used to print the object
    def __repr__(self):
        return '<User %r>' % self.email


# This decorator is used to check if the logged-in user is a student
def student_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the logged-in user
        logged_user = get_jwt_identity()
        # Check if the logged-in user is a student
        if not logged_user.startswith('ACA'):
            # If not, return an error
            abort(401, message="This is students arena")
        return func(*args, **kwargs)
    return wrapper

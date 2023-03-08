from ..extensions import db
from passlib.hash import pbkdf2_sha256


def student_default_password(default_password):
    pass_word = pbkdf2_sha256.hash(default_password)
    return pass_word


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    faculty = db.Column(db.String(70), nullable=False)
    department = db.Column(db.String(70), nullable=False)
    matric_code = db.Column(db.String(50), unique=True, nullable=False)
    gpa = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.Text, nullable=False,
                         default=student_default_password('academia'))
    registered_courses = db.relationship('CourseRegistered',
                                         cascade="all, delete", backref='student', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

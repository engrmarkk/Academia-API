from ..extensions import db


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    matric_number = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(80), nullable=False)
    registered_courses = db.relationship('CourseRegistered', cascade="all, delete", backref='student', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

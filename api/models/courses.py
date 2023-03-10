from ..extensions import db
from datetime import datetime


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    course_unit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    teacher = db.Column(db.String(150), nullable=False)
    registered_courses = db.relationship('CourseRegistered', backref='course', lazy=True)

    def __repr__(self):
        return '<Course %r>' % self.name

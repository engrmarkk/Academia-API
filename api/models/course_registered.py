from ..extensions import db
from flask_jwt_extended import get_jwt_identity


class CourseRegistered(db.Model):
    __tablename__ = 'course_registered'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False, default=0.0)
    grade = db.Column(db.String(10), default='N/A')
    course_code = db.Column(db.String(80), nullable=False)
    course_title = db.Column(db.String(100), nullable=False)
    stud_id = db.Column(db.String(80), nullable=False)
    course_unit = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return '<CourseRegistered %r>' % self.id


def check_if_registered(course_code):
    course = CourseRegistered.query.filter_by(
        course_code=course_code, stud_id=get_jwt_identity()
    ).first()
    if course:
        return True
    return False

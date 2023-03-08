from ..extensions import db


class CourseRegistered(db.Model):
    __tablename__ = 'course_registered'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float, default=0.00, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_code = db.Column(db.String(80), nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __repr__(self):
        return '<CourseRegistered %r>' % self.id

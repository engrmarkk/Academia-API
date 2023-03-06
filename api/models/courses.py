from ..extensions import db
from datetime import datetime


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(80), unique=True, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False, default=datetime.now().year)
    unit = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    tutor_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)

    def __repr__(self):
        return '<Course %r>' % self.name

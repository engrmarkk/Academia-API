from ..extensions import db
from enum import Enum


class Role(Enum):
    TEACHER = 'teacher'
    ICT = 'ict'


class Staff(db.Model):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(80), nullable=False)
    courses = db.relationship('Course', cascade="all, delete", backref='tutor', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

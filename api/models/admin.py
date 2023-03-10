from ..extensions import db
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from .students import code_generator
from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    adm_id = db.Column(db.String(50), unique=True, nullable=False,
                       default=code_generator(f'ADMIN-{datetime.now().year}-')
                       )
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.email


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logged_user = get_jwt_identity()
        if not logged_user.startswith('ADMIN'):
            abort(401, message="Admin access required")
        return func(*args, **kwargs)
    return wrapper

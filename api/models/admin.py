from ..extensions import db
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(70), nullable=False)
    admin_code = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.email


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin = Admin.query.get(get_jwt_identity())
        if not admin:
            abort(401, "Admin access required")
        return func(*args, **kwargs)
    return wrapper

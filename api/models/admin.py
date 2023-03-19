from ..extensions import db
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from .students import code_generator
from datetime import datetime


class Admin(db.Model):
    __tablename__ = 'admin'
    # The id column is the primary key
    id = db.Column(db.Integer, primary_key=True)
    # the first_name and last_name columns are not nullable
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # the adm_id column is unique and not nullable
    # the default value is a function that generates a unique code
    adm_id = db.Column(db.String(50), unique=True, nullable=False,
                       default=code_generator(f'ADMIN-{datetime.now().year}-')
                       )
    # the email column is unique and not nullable
    email = db.Column(db.String(120), unique=True, nullable=False)
    # the password column is not nullable
    password = db.Column(db.Text, nullable=False)

    # The __repr__ method is used to print the object
    def __repr__(self):
        return '<Admin %r>' % self.email


# This decorator is used to check if the logged-in user is an admin
def admin_required(func):
    # This wraps the function to be decorated
    @wraps(func)
    # This is the wrapper function
    def wrapper(*args, **kwargs):
        # Get the logged-in user
        logged_user = get_jwt_identity()
        # Check if the logged-in user is an admin
        if not logged_user.startswith('ADMIN'):
            # If not, return an error
            abort(401, message="Admin access required")
        return func(*args, **kwargs)
    return wrapper

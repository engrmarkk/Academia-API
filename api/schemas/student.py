from marshmallow import Schema, fields
from .course import plainCourseRegisteredSchema


class plainStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    stud_id = fields.Str(required=True, dump_only=True)
    email = fields.Str(required=True)
    gpa = fields.Float(required=True)
    # the registered_courses will return a list of courses registered by the student
    registered_courses = fields.Nested(plainCourseRegisteredSchema(), many=True)


class UpdatePasswordByStudentSchema(Schema):
    new_password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)


class plainStudentID(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    stud_id = fields.Str(dump_only=True)


class UpdateStudentDetails(Schema):
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    email = fields.Str(required=False)


"""
Student Model

    id
    first_name
    last_name
    email
    faculty
    department
    stud_id
    gpa
    password
    registered_courses : relationship
"""

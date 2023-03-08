from marshmallow import fields, Schema


"""
Admin Model

    id
    first_name
    last_name
    department
    admin_code
    email
    password
"""


"""
Student Model

    id
    first_name
    last_name
    email
    faculty
    department
    matric_code
    gpa
    password
    registered_courses : relationship
"""

"""
Course fields

    id
    name
    course_code
    semester
    year
    unit
    created_at
    teacher
    department : foreignKey

"""

"""
Registered Course fields

    id
    grade
    name
    matric_code
    unit
    student_id
    course_id
"""


class plainCourseRegisteredSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Float(dump_only=True)
    name = fields.Str()
    matric_code = fields.Str()
    unit = fields.Int()
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)


class plainStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    matric_code = fields.Str(required=True, dump_only=True)
    email = fields.Str(required=True)
    department = fields.Str(required=True)
    gpa = fields.Float(required=True)
    password = fields.Str(required=True, load_only=True)
    registered_courses = fields.Nested(plainCourseRegisteredSchema(), many=True)


class plainCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    code = fields.Str(required=True)
    description = fields.Str(required=True)
    semester = fields.Int(required=True)
    year = fields.Int(required=True)
    unit = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    tutor_id = fields.Int(required=True)


class plainAdminSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    department = fields.Str(required=True)
    admin_code = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class plainUserLoginSchema(Schema):
    code = fields.Str(required=True)
    password = fields.Str(required=True)


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    department = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

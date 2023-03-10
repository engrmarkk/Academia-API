from marshmallow import fields, Schema


"""
Admin Model

    id
    first_name
    last_name
    department
    adm_id
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
    stud_id
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

"""

"""
Registered Course fields

    id
    grade
    name
    stud_id
    unit
    stud_id
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
    matric_id = fields.Str(required=True, dump_only=True)
    email = fields.Str(required=True)
    gpa = fields.Float(required=True)
    password = fields.Str(required=True, load_only=True)
    registered_courses = fields.Nested(plainCourseRegisteredSchema(), many=True)


class plainCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    course_title = fields.Str(required=True)
    course_code = fields.Str(required=True)
    year = fields.Int(dump_only=True)
    course_unit = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    teacher = fields.Str(required=True)


class plainAdminSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    admin_id = fields.Str()
    email = fields.Str(required=True)
    password = fields.Str(load_only=True)


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


class UpdatePasswordByStudentSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)


class plainGradeSchema(Schema):
    grade = fields.Float(required=True)


class plainStudentID(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    stud_id = fields.Str(required=True)

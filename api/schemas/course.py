from marshmallow import Schema, fields


class plainCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    course_title = fields.Str(required=True)
    course_code = fields.Str(required=True)
    year = fields.Int(dump_only=True)
    course_unit = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    teacher = fields.Str(required=True)


class plainCourseRegisteredSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Float(dump_only=True)
    name = fields.Str()
    matric_code = fields.Str()
    unit = fields.Int()
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)


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

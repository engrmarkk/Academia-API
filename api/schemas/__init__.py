from marshmallow import fields, Schema


class plainCourseRegisteredSchema(Schema):
    id = fields.Int(dump_only=True)
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)


class plainStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    grade = fields.Int(required=True)
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


class plainStaffSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)
    is_admin = fields.Bool(required=True)
    password = fields.Str(required=True, load_only=True)
    courses = fields.Nested(plainCourseSchema(), many=True)

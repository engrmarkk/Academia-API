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
    grade = fields.Str(dump_only=True)
    score = fields.Float(dump_only=True)
    course_code = fields.Str(required=True)
    course_title = fields.Str(required=True)
    course_unit = fields.Int(required=True)
    stud_id = fields.Str(required=True)


class StudentWhoRegisteredACourseSchema(Schema):
    stud_id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    grade = fields.Float(dump_only=True)


class CourseRegisteredStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Float(dump_only=True)
    course_code = fields.Str(required=True)
    course_title = fields.Str(required=True)
    stud_id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    # student_id = fields.Int()
    # course_id = fields.Int()


class ListCoursesWithStudentSchema(Schema):
    id = fields.Int(dump_only=True)
    course_title = fields.Str(required=True)
    course_code = fields.Str(required=True)
    year = fields.Int(dump_only=True)
    course_unit = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    teacher = fields.Str(required=True)
    student_registered = fields.Nested(StudentWhoRegisteredACourseSchema(), many=True)


class RegisterACourseSchema(Schema):
    course_code = fields.Str(required=True)


class UpdateCourseSchema(Schema):
    course_title = fields.Str(required=False)
    course_code = fields.Str(dump_only=True)
    course_unit = fields.Int(required=False)
    teacher = fields.Str(required=False)


"""
Registered Course fields

    id
    score
    name
    stud_id
    unit
    stud_id
    course_id
"""

"""
Course fields

    id
    course_title
    course_code
    year
    course_unit
    created_at
    teacher
    registered_courses

"""

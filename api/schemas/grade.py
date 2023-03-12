from marshmallow import Schema, fields


class plainGradeSchema(Schema):
    grade = fields.Float(required=True)

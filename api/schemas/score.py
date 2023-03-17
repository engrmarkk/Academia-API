from marshmallow import Schema, fields


class plainscoreSchema(Schema):
    score = fields.Float(required=True)

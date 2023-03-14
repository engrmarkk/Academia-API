from marshmallow import Schema, fields


class plainUserLoginSchema(Schema):
    user_id = fields.Str(required=True)
    password = fields.Str(required=True)


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

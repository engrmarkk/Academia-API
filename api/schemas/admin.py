from marshmallow import Schema, fields


class plainAdminSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    adm_id = fields.Str(required=True, dump_only=True)
    password = fields.Str(required=True, load_only=True)


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

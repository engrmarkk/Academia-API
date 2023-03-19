from marshmallow import Schema, fields


# this is the schema for the user registration response
class plainAdminSchema(Schema):
    # the id is dump only, meaning it will not be required when registering a user
    id = fields.Int(dump_only=True)
    # the first name is required
    first_name = fields.Str(required=True)
    # the last name is required
    last_name = fields.Str(required=True)
    # the email is required and must be a valid email
    email = fields.Str(required=True)
    # the adm_id is dump only, meaning it will not be required when registering a user, it will be generated automatically
    adm_id = fields.Str(required=True, dump_only=True)
    # the password is load only, meaning it will not be returned when a user is queried
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

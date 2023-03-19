from marshmallow import Schema, fields


# this is the schema for the user login arguments
class plainUserLoginSchema(Schema):
    # the user_id is required
    user_id = fields.Str(required=True)
    # the password is required
    password = fields.Str(required=True)


# this is the schema for the user registration arguments
class UserRegisterSchema(Schema):
    # the id is dump only, meaning it will not be required when registering a user
    # it will be generated automatically
    id = fields.Int(dump_only=True)
    # the first name is required
    first_name = fields.Str(required=True)
    # the last name is required
    last_name = fields.Str(required=True)
    # the email is required and must be a valid email
    email = fields.Str(required=True)
    # the password is load only, meaning it will not be returned when a user is queried
    password = fields.Str(required=True, load_only=True)

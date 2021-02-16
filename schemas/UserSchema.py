from models.User import User
from main import mar
from marshmallow.validate import Length

class UserSchema (mar.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]

    username = mar.String(required=True, validate=Length(min=3))
    password = mar.String(required=True, validate=Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many = True)

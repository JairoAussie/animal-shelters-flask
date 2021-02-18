from main import mar
from models.Shelter import Shelter
from schemas.UserSchema import UserSchema

class ShelterSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = Shelter
    user =  mar.Nested(UserSchema)
shelter_schema = ShelterSchema()
shelters_schema = ShelterSchema(many=True)
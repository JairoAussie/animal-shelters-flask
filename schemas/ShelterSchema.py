from main import mar
from models.Shelter import Shelter

class ShelterSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = Shelter

shelter_schema = ShelterSchema()
shelters_schema = ShelterSchema(many=True)
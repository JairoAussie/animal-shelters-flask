from main import mar
from models.Animal import Animal
from schemas.ShelterSchema import ShelterSchema
class AnimalSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = Animal
        #include_fk = True
    shelter =  mar.Nested(ShelterSchema)
animalSchema = AnimalSchema()
animalsSchema = AnimalSchema(many=True)

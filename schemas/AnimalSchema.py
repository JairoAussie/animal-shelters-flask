from main import mar

from models.Animal import Animal

class AnimalSchema(mar.SQLAlchemyAutoSchema):
    class Meta:
        model = Animal
        include_fk = True

animalSchema = AnimalSchema()
animalsSchema = AnimalSchema(many=True)

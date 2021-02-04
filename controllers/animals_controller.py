from models.Animal import Animal

from main import db
from schemas.AnimalSchema import animalSchema, animalsSchema
from flask import Blueprint, request, jsonify
animals = Blueprint('animals', __name__, url_prefix="/animals")

@animals.route("/", methods=["GET"])
def animal_index():
    animals = Animal.query.all()
    return jsonify(animalsSchema.dump(animals))

@animals.route("/", methods=["POST"])
def animal_create():
    animal_fields = animalSchema.load(request.json)

    new_Animal = Animal()
    new_Animal.name = animal_fields["name"]
    new_Animal.kind = animal_fields["kind"]
    new_Animal.breed = animal_fields["breed"]
    new_Animal.age = animal_fields["age"]
    new_Animal.shelter_id = animal_fields["shelter_id"]

    db.session.add(new_Animal)
    db.session.commit()
    return jsonify(animalSchema.dump(new_Animal))

@animals.route("/<int:id>", methods=["GET"])
def animal_show(id):
    animal = Animal.query.get(id)
    return jsonify(animalSchema.dump(animal))


@animals.route("/<int:id>", methods=["DELETE"])
def animal_delete(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify(animalSchema.dump(animal))

@animals.route("/<int:id>", methods=["PUT", "PATCH"])
def animal_update(id):
    animals = Animal.query.filter_by(id=id)
    animal_fields = animalSchema.load(request.json)
    animals.update(animal_fields)

    db.session.commit()
    return jsonify(animalSchema.dump(animals[0]))
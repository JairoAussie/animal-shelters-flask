from models.Animal import Animal
from models.Shelter import Shelter

from main import db
from schemas.AnimalSchema import animalSchema, animalsSchema
from flask import Blueprint, request, jsonify, render_template, abort
from flask_jwt_extended import jwt_required
from services.auth_service import verify_user
animals = Blueprint('animals', __name__, url_prefix="/animals")

@animals.route("/", methods=["GET"])
def animal_index():
    animals = Animal.query.all()
    return jsonify(animalsSchema.dump(animals))
    #return render_template("animals_index.html", anims = animals)

@animals.route("/", methods=["POST"])
@jwt_required
@verify_user
def animal_create(user=None):
    shelter = Shelter.query.filter_by(user_id=user.id).first()

    if not shelter:
        return abort(400, description= "Not authorised, you need to create a shelter first")

    animal_fields = animalSchema.load(request.json)

    new_Animal = Animal()
    new_Animal.name = animal_fields["name"]
    new_Animal.kind = animal_fields["kind"]
    new_Animal.breed = animal_fields["breed"]
    new_Animal.age = animal_fields["age"]
    new_Animal.shelter_id = shelter.id

    db.session.add(new_Animal)
    db.session.commit()
    return jsonify(animalSchema.dump(new_Animal))

@animals.route("/<int:id>", methods=["GET"])
def animal_show(id):
    animal = Animal.query.get(id)
    return jsonify(animalSchema.dump(animal))
    #return render_template("animal.html", anim = animal )

@animals.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def animal_delete(id, user=None):

    animal = Animal.query.get(id)

    shelter = Shelter.query.filter_by(id=animal.shelter_id, user_id=user.id).first()

    if not shelter:
        return abort(400, description= "Not authorised, this animal does not belong to your shelter")

    
    db.session.delete(animal)
    db.session.commit()
    return jsonify(animalSchema.dump(animal))

@animals.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
@verify_user
def animal_update(id, user=None):
    animal = Animal.query.get(id)

    shelter = Shelter.query.filter_by(id=animal.shelter_id, user_id=user.id).first()

    if not shelter:
        return abort(400, description= "Not authorised, this animal does not belong to your shelter")

    animals = Animal.query.filter_by(id=id)
    animal_fields = animalSchema.load(request.json)
    animals.update(animal_fields)

    db.session.commit()
    return jsonify(animalSchema.dump(animals[0]))
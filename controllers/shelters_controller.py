from models.Shelter import Shelter
from models.Animal import Animal
from main import db
from schemas.ShelterSchema import shelter_schema, shelters_schema
from schemas.AnimalSchema import animalSchema, animalsSchema
from flask import Blueprint, request, jsonify

shelters = Blueprint('shelters',__name__, url_prefix="/shelters")

@shelters.route("/", methods=["GET"])
def shelter_index():
    shelters = Shelter.query.all()
    return jsonify(shelters_schema.dump(shelters))
    #rs = db.engine.execute('SELECT * FROM shelters')
    #return jsonify(shelters_schema.dump(rs))

@shelters.route("/", methods=["POST"])
def shelter_create():

    shelter_fields = shelter_schema.load(request.json)
    #create a new Shelter object, with the data received in the request
    new_shelter = Shelter()
    new_shelter.name = shelter_fields["name"]
    new_shelter.email = shelter_fields["email"]
    new_shelter.phone = shelter_fields["phone"]
    new_shelter.address = shelter_fields["address"]
    new_shelter.city = shelter_fields["city"]

    #add a new shelter to the db
    db.session.add(new_shelter)
    db.session.commit()

    return jsonify(shelter_schema.dump(new_shelter))

@shelters.route("/<int:id>", methods=["GET"])
def shelter_show(id):
    #SELECT * FROM SHELTERS WHERE ID = id
    shelter = Shelter.query.get(id)
    return jsonify(shelter_schema.dump(shelter))

@shelters.route("/<int:id>/animals", methods=["GET"])
def shelter_animals_show(id):
    #SELECT * FROM ANIMALS WHERE SHELTER_ID = id
    animals = Animal.query.filter_by(shelter_id=id)

    return jsonify(animalsSchema.dump(animals))

@shelters.route("/<int:id>", methods=["DELETE"])
def shelter_delete(id):
    shelter = Shelter.query.get(id)
    db.session.delete(shelter)
    db.session.commit()
    return jsonify(shelter_schema.dump(shelter))

@shelters.route("/<int:id>", methods=["PUT","PATCH"])
def shelter_update(id):
    shelters = Shelter.query.filter_by(id=id)
    shelter_fields = shelter_schema.load(request.json)
    shelters.update(shelter_fields)
    db.session.commit()
    return jsonify(shelter_schema.dump(shelters[0]))
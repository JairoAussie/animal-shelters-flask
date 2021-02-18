from models.Shelter import Shelter
from models.Animal import Animal
from models.User import User
from main import db
from schemas.ShelterSchema import shelter_schema, shelters_schema
from schemas.AnimalSchema import animalSchema, animalsSchema
from flask import Blueprint, request, jsonify, render_template, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import verify_user

shelters = Blueprint('shelters',__name__, url_prefix="/shelters")

@shelters.route("/", methods=["GET"])
def shelter_index():
    shelters = Shelter.query.all()
    return jsonify(shelters_schema.dump(shelters))
    #return render_template("shelters_index.html", shelters = shelters)
    #rs = db.engine.execute('SELECT * FROM shelters')
    #return jsonify(shelters_schema.dump(rs))

@shelters.route("/", methods=["POST"])
@jwt_required
@verify_user
def shelter_create(user=None):

    shelter = Shelter.query.filter_by(user_id=user.id).first()
    #print (shelter)
    if shelter:
        return abort(400, description= "Not authorised to create more than one shelter")
    print(request.json)
    shelter_fields = shelter_schema.load(request.json)
    #create a new Shelter object, with the data received in the request
    new_shelter = Shelter()
    new_shelter.name = shelter_fields["name"]
    new_shelter.email = shelter_fields["email"]
    new_shelter.phone = shelter_fields["phone"]
    new_shelter.address = shelter_fields["address"]
    new_shelter.city = shelter_fields["city"]
    new_shelter.user_id = user.id

    #add a new shelter to the db
    db.session.add(new_shelter)
    db.session.commit()

    return jsonify(shelter_schema.dump(new_shelter))

@shelters.route("/<int:id>", methods=["GET"])
def shelter_show(id):
    #SELECT * FROM SHELTERS WHERE ID = id
    shelter = Shelter.query.get(id)
    return jsonify(shelter_schema.dump(shelter))
    #return render_template("shelter.html", shelt = shelter )

@shelters.route("/<int:id>/animals", methods=["GET"])
def shelter_animals_show(id):
    #SELECT * FROM ANIMALS WHERE SHELTER_ID = id
    animals = Animal.query.filter_by(shelter_id=id)
    #return render_template("animals_index.html", anims = animals)
    return jsonify(animalsSchema.dump(animals))

@shelters.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def shelter_delete(id, user=None):
    # user_id = get_jwt_identity()
    # user = User.query.get(user_id)

    # if not user:
    #     return abort(401, description="Invalid user")


    #shelter = Shelter.query.get(id)
    shelter = Shelter.query.filter_by(id=id, user_id=user.id).first()
    if not shelter:
        return abort(400, description="Not authorized to delete other people's shelters")

    db.session.delete(shelter)
    db.session.commit()
    return jsonify(shelter_schema.dump(shelter))

@shelters.route("/<int:id>", methods=["PUT","PATCH"])
@jwt_required
@verify_user
def shelter_update(id, user=None):
    shelter = Shelter.query.filter_by(id=id, user_id=user.id).first()
    #shelters = Shelter.query.filter_by(id=id)
    shelter_fields = shelter_schema.load(request.json)
    shelters.update(shelter_fields)
    db.session.commit()
    return jsonify(shelter_schema.dump(shelters[0]))
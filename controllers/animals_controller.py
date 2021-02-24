from models.Animal import Animal
from models.Shelter import Shelter

from main import db
from schemas.AnimalSchema import animalSchema, animalsSchema
from flask import Blueprint, request, jsonify, render_template, abort, redirect, url_for
# from flask_jwt_extended import jwt_required
# from services.auth_service import verify_user
from flask_login import login_required, current_user
animals = Blueprint('animals', __name__, url_prefix="/animals")

@animals.route("/", methods=["GET"])
def animal_index():
    animals = Animal.query.all()
    #return jsonify(animalsSchema.dump(animals))
    return render_template("animals_index.html", anims = animals)

@animals.route("/", methods=["POST"])
@login_required
def animal_create():
    shelter = Shelter.query.filter_by(user_id=current_user.id).first()

    if not shelter:
        return abort(400, description= "Not authorised, you need to create a shelter first")

    #animal_fields = animalSchema.load(request.json)

    new_Animal = Animal()
    new_Animal.name = request.form.get("name")
    new_Animal.kind = request.form.get("kind")
    new_Animal.breed = request.form.get("breed")
    new_Animal.age = request.form.get("age")
    new_Animal.shelter_id = shelter.id

    db.session.add(new_Animal)
    db.session.commit()
    #return jsonify(animalSchema.dump(new_Animal))
    return redirect(url_for('animals.animal_index'))


@animals.route("/<int:id>", methods=["GET"])
def animal_show(id):
    animal = Animal.query.get(id)
    #return jsonify(animalSchema.dump(animal))
    return render_template("animal.html", anim = animal )

@animals.route("/delete/<int:id>", methods=["GET"])
@login_required
def animal_delete(id):

    animal = Animal.query.get(id)

    shelter = Shelter.query.filter_by(id=animal.shelter_id, user_id=current_user.id).first()

    if not shelter:
        return abort(400, description= "Not authorised, this animal does not belong to your shelter")

    
    db.session.delete(animal)
    db.session.commit()
    #return jsonify(animalSchema.dump(animal))
    return redirect(url_for('animals.animal_index'))

@animals.route("/update/<int:id>", methods=["POST"])
@login_required
def animal_update(id):
    animal = Animal.query.get(id)

    shelter = Shelter.query.filter_by(id=animal.shelter_id, user_id=current_user.id).first()

    if not shelter:
        return abort(400, description= "Not authorised, this animal does not belong to your shelter")

    #start updating the values of the shelter according to the form
    animal.name = request.form.get("name")
    animal.kind = request.form.get("kind")
    animal.breed = request.form.get("breed")
    animal.age = request.form.get("age")
    shelter.user_id = current_user.id
    #save the changes
    db.session.commit()
    return redirect(url_for('animals.animal_index'))

@animals.route("/new", methods=["GET"])
def new_animal():
    return render_template("new_animal.html")

@animals.route("/modify/<int:id>", methods=["GET"])
def modify_animal(id):
    animal = Animal.query.get(id)
    return render_template("modify_animal.html", anim=animal)
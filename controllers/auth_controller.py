from models.User import User
from schemas.UserSchema import user_schema
from main import db
from flask import Blueprint, request, jsonify, abort
from main import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def auth_register():
    user_fields = user_schema.load(request.json)

    #avoid to create a user that already exists
    user = User.query.filter_by(username=user_fields["username"]).first()

    if user:
        return abort(400, description="user already exists")

    user = User()
    user.username = user_fields["username"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))

@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)

    
    user = User.query.filter_by(username=user_fields["username"]).first()
    # don't login if the user doesn't exist
    if not user: 
        return abort(401, description="Incorrect username")
    if not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    return jsonify({"token": access_token})
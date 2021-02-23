from models.User import User
from schemas.UserSchema import user_schema, users_schema
from main import db
from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for
from main import bcrypt
from flask_jwt_extended import create_access_token
from flask_login import login_user, current_user, logout_user, login_required
from datetime import timedelta
auth = Blueprint('auth', __name__,)

@auth.route("/auth/register", methods=["POST"])
def auth_register():
    username = request.form.get('username')
    password = request.form.get('password')
    #print(username)
    #print(password)

    #user_fields = user_schema.load(request.json)

    #avoid to create a user that already exists
    #user = User.query.filter_by(username=user_fields["username"]).first()
    user = User.query.filter_by(username=username).first()
    if user:
        return abort(400, description="user already exists")
    user = User()
    #user.username = user_fields["username"]
    #user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    user.username = username
    user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    #return jsonify(user_schema.dump(user))
    return redirect(url_for('auth.login'))

@auth.route("/auth/login", methods=["POST"])
def auth_login():
    username = request.form.get('username')
    password = request.form.get('password')
    # print(username)
    # print(password)
    # user_fields = user_schema.load(request.json)

    
    # user = User.query.filter_by(username=user_fields["username"]).first()
    user = User.query.filter_by(username=username).first()
    # don't login if the user doesn't exist
    if not user: 
        return abort(401, description="Incorrect username")
    if not bcrypt.check_password_hash(user.password, password):
        return abort(401, description="Incorrect password")
    #print(current_user.username)
    login_user(user)
    #expiry = timedelta(days=1)
    #access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    #return jsonify({"token": access_token})
    return redirect(url_for('shelters.shelter_index'))

@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('shelters.shelter_index'))

# @auth.route("/users", methods=["GET"])
# def users_index():
#     users = User.query.all()
#     return jsonify(users_schema.dump(users))
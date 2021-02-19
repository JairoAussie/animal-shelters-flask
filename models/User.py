from main import db
from flask_login import UserMixin

def get_user(user_id):
    user=User.query.filter_by(id=user_id).first()
    return user

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    shelters = db.relationship("Shelter", backref="user")
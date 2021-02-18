from main import db
from flask import Blueprint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def create_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_db():
    from main import bcrypt
    from models.Shelter import Shelter
    from models.Animal import Animal
    from models.User import User

    u1 = User()
    u1.username = "Jairo"
    u1.password = bcrypt.generate_password_hash("123456").decode("utf-8")
    db.session.add(u1)

    u2 = User()
    u2.username = "Ignacio"
    u2.password = bcrypt.generate_password_hash("123456").decode("utf-8")
    db.session.add(u2)

    db.session.commit()
    
    s1 = Shelter()
    s1.name = "Brisbane Shelter"
    s1.address = "100 Main st "
    s1.email = "brisbaneshelter@gmail.com"
    s1.city = "Brisbane"
    s1.phone = "1800011122"
    s1.user_id = 1
    db.session.add(s1)

    s2 = Shelter()
    s2.name = "Sydney Shelter"
    s2.address = "100 Adelaide st "
    s2.email = "sydneyshelter@gmail.com"
    s2.city = "Sydney"
    s2.phone = "180024135122"
    s2.user_id = 2
    db.session.add(s2)

    db.session.commit()    

    a1 = Animal()
    a1.name = "Rusty"
    a1.kind = "Dog"
    a1.breed = "Jack Russell"
    a1.age = "10 years"
    a1.shelter_id = 1
    db.session.add(a1)

    a2 = Animal()
    a2.name = "Kubernetes"
    a2.kind = "Koala"
    a2.age = "2 years"
    a2.shelter_id = 1
    db.session.add(a2)

    a3 = Animal()
    a3.name = "Flask"
    a3.kind = "Snake"
    a3.breed = "Python"
    a3.age = "1 year"
    a3.shelter_id = 2
    db.session.add(a3)

    a4 = Animal()
    a4.name = "Docker"
    a4.kind = "Kangaroo"
    a4.age = "2 years"
    a4.shelter_id = 2
    db.session.add(a4)

    db.session.commit()
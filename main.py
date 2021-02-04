from flask import Flask 
app = Flask(__name__)

from database import init_db
db = init_db(app)

from flask_marshmallow import Marshmallow
mar = Marshmallow(app)

from commands import db_commands
app.register_blueprint(db_commands)

from controllers import registerable_controllers

for controller in registerable_controllers:
    app.register_blueprint(controller)





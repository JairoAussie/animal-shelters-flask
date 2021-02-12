from flask_sqlalchemy import SQLAlchemy 

def init_db(app):
    
    db = SQLAlchemy(app)
    #print("db connected")
    return db
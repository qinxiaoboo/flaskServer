from flaskServer.config.connect import db

class User(db.Model):
    __tablename__  = "t_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


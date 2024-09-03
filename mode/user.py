from flaskServer.config.connect import db
import datetime

class User(db.Model):
    __tablename__  = "t_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    groups = db.Column(db.String(120), unique=True, nullable=True)
    token = db.Column(db.String(120), unique=True, nullable=True)
    updatetime = db.Column(db.DateTime, default=datetime.datetime.now(),comment="更新时间")
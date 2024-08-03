from dataclasses import dataclass

from dataclasses_json import dataclass_json

from flaskServer.config.connect import db

@dataclass_json
@dataclass
class SpacePoints(db.Model):
    __tablename__ = "t_space_points"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    alia = db.Column(db.String(120), unique=False, nullable=False)
    env_name = db.Column(db.String(120), unique=True, nullable=False)
    points = db.Column(db.Integer, unique=True, nullable=True)
    ranking = db.Column(db.Integer, unique=True, nullable=True)
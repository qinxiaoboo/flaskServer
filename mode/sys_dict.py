from flaskServer.config.connect import db

class SysDict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    key = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), unique=True, nullable=False)
    def to_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'key':self.key,
            'value':self.value
        }


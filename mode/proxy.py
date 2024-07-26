from flaskServer.config.connect import db

class Proxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=False, nullable=False)
    pwd = db.Column(db.String(120), unique=False, nullable=False)
    ip = db.Column(db.String(120), unique=True, nullable=False)
    port = db.Column(db.String(120), unique=False, nullable=False)


    def to_json(self):
        return {
            'id':self.id,
            'user':self.name,
            'ip':self.key,
            'port':self.value,
            'pwd': self.pwd

        }


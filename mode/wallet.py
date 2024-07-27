from flaskServer.config.connect import db

class Wallet(db.Model):
    __tablename__ = "t_wallet"
    id = db.Column(db.Integer, primary_key=True)
    word_pass = db.Column(db.String(255), unique=False, nullable=True)
    address = db.Column(db.String(80), unique=False, nullable=True)
    type = db.Column(db.String(80), unique=False, nullable=True)
    env = db.Column(db.String(80), unique=False, nullable=True)


    def to_json(self):
        return {
            'id':self.id,
            'user':self.word_pass,
            'type': self.type,
            'address': self.address,

        }


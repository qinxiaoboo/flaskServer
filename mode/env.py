from flaskServer.config.connect import db

class Env(db.Model):
    __tablename__  = "t_env"

    id = db.Column(db.Integer, primary_key=True)
    t_proxy_id = db.Column(db.Integer, unique=False, nullable=True)
    tw_id = db.Column(db.Integer, unique=True, nullable=True)
    discord_id = db.Column(db.Integer, unique=True, nullable=True)
    outlook_id = db.Column(db.Integer, unique=True, nullable=True)
    okx_id = db.Column(db.Integer, unique=True, nullable=True)
    init_id = db.Column(db.Integer, unique=True, nullable=True)
    bitlight_id = db.Column(db.Integer, unique=True, nullable=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    group = db.Column(db.String(120), unique=False, nullable=False)
    port = db.Column(db.String(120), unique=True, nullable=False)
    cookies = db.Column(db.String(120), unique=False, nullable=True)
    user_agent = db.Column(db.String(80), unique=False, nullable=False)


    def to_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'group':self.group,
            'port':self.port
        }


from flaskServer.config.connect import db

class Account(db.Model):
    __tablename__ = "t_account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    pwd = db.Column(db.String(120), unique=False, nullable=False)
    email_name = db.Column(db.String(120), unique=True, nullable=False)
    email_pass = db.Column(db.String(120), unique=False, nullable=False)
    fa2 = db.Column(db.String(120), unique=False, nullable=False)
    type = db.Column(db.String(120), unique=False, nullable=False)
    token = db.Column(db.String(250), unique=False, nullable=True)
    # 0: 未登录 1：登录异常 2：登录成功
    status = db.Column(db.Integer, unique=False, nullable=False)
    error = db.Column(db.String(120), unique=False, nullable=False)


    def to_json(self):
        return {
            'id':self.id,
            'user':self.name,
            'pwd':self.pwd,
            'fa2':self.fa2,
            'type': self.type

        }


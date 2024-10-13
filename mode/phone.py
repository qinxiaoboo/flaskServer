from flaskServer.config.connect import db,app
class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    country_id = db.Column(db.String(256), nullable=True)
    country_code = db.Column(db.String(256), nullable=True)
    requestId = db.Column(db.String(256), nullable=True)
    # 0待释放，1已释放
    status = db.Column(db.Integer, unique=False, nullable=True)
    # platefrom = db.Column(db.String(256), nullable=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
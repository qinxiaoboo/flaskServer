from flaskServer.config.connect import db,app
class DataDictionary(db.Model):
    __tablename__ = 'data_dictionary'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'code': self.code,
            'value': self.value,
            'description': self.description
        }
if __name__ == '__main__':

    # Create the database and table
    with app.app_context():
        db.create_all()
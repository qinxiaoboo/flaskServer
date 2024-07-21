from flaskServer.config.connect import db,app
from user import User

if __name__ == '__main__':

    with app.app_context():
        new_user = User(username="proxyu",password="proxy_pass")
        db.session.add(new_user)
        db.session.commit()

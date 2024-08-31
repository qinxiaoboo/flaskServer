import datetime
import secrets
from flaskServer.mode.user import User
from flaskServer.config.connect import db,app
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64, aesCbcPbkdf2EncryptToBase64
from sqlalchemy import and_


def getUserByName(name):
    with app.app_context():
        user = User.query.filter_by(username=name).first()
    return user

def getUserByToken(token):
    with app.app_context():
        thirty_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)
        user = User.query.filter(and_(User.updatetime >= thirty_minutes_ago, User.token == token)).first()
    return user

def getAllUser():
    LIST = []
    with app.app_context():
        users = User.query.all()
        for user in users:
            if user.username!="admin":
                LIST.append({"name":user.username, "groups": user.groups, "id": user.id})
    return LIST

def updateUser(name, password, groups):
    user = getUserByName(name)
    if user:
        if password and aesCbcPbkdf2DecryptFromBase64(user.password) != password and password != "undefined":
            user.password = aesCbcPbkdf2EncryptToBase64(password)
        if groups and user.groups != groups:
            user.groups = groups
    else:
        user = User(username=name,password=aesCbcPbkdf2EncryptToBase64(password),groups=groups)
    db.session.add(user)
    db.session.commit()

def deleteUserById(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

def generate_api_token(length=32):
    return secrets.token_hex(length)

def loginUser(name, password):
    user = getUserByName(name)
    if user:
        if password and aesCbcPbkdf2DecryptFromBase64(user.password) == password:
            user.token = generate_api_token()
            user.updatetime = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            return user

# 检查token是否存在
def checkToken(token):
    return getUserByToken(token)


def updateToken(token):
    user = checkToken(token)
    if user:
        with app.app_context():
            user.updatetime = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            return True
    return False



if __name__ == '__main__':
    print(updateToken("12354123"))
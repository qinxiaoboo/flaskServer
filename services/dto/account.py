from flaskServer.mode.account import Account
from flaskServer.config.connect import db,app
from sqlalchemy import and_
from flaskServer.utils.crypt import aesCbcPbkdf2EncryptToBase64

# 获取账号信息，通过环境名称和账号类型，TW，OUTLOOK，DISCORD
def getAccount(name,type):
    with app.app_context():
        account = Account.query.filter(and_(Account.name==name,Account.type==type)).first()
        return account

# 获取账号通过账号ID
def getAccountById(id):
    with app.app_context():
        return Account.query.filter_by(id=id).first()

# 更新账号信息
def updateAccount(name,pwd,fa2,type,email_name=None,email_pass=None):
    pwd = aesCbcPbkdf2EncryptToBase64(pwd)
    fa2 = aesCbcPbkdf2EncryptToBase64(fa2)
    account = getAccount(name,type)
    with app.app_context():
        if account:
            if account.pwd != pwd:
                account.pwd = pwd
            if account.email_name != email_name and email_name:
                account.email_name = email_name
            if account.email_pass != email_pass and email_pass:
                account.email_pass = email_pass
            if account.fa2 != fa2 and fa2:
                account.fa2 = fa2
        else:
            account = Account(name=name,pwd=pwd,email_name=email_name,email_pass=email_pass,fa2=fa2,type=type)
        db.session.add(account)
        db.session.commit()
        print("新增一条账号信息，id: ",account.id)
        return account

if __name__ == '__main__':
    name,pwd,fa2 = "brown_laur21244:VwiuMLt8lPqirZ4:".split(":")
    acc = updateAccount(name,pwd,fa2,"TW")
    print(acc.to_json())
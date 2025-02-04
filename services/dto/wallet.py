from flaskServer.mode.wallet import Wallet
from flaskServer.config.connect import db,app
from sqlalchemy import and_
from flaskServer.utils.crypt import aesCbcPbkdf2EncryptToBase64

# 获取钱包信息，通过助记词
def getWalletByWord(env,t):
    with app.app_context():
        wallet = Wallet.query.filter(and_(Wallet.env==env,Wallet.type==t)).first()
        return wallet

# 获取钱包信息通过钱包ID
def getWalletByID(_id):
    with app.app_context():
        wallet = Wallet.query.filter_by(id=_id).first()
        return wallet

# 更新钱包信息
def updateWallt(env,word,address,t):
    word = aesCbcPbkdf2EncryptToBase64(word)
    wallet = getWalletByWord(env,t)
    with app.app_context():
        if wallet:
            if wallet.address != address:
                wallet.address = address
            if wallet.word_pass != word:
                wallet.word_pass = word
        else:
            wallet = Wallet(env=env,word_pass=word,address=address,type=t)
        db.session.add(wallet)
        db.session.commit()
        print(f"钱包信息，环境名称：{env}, 地址：{address}，id：", wallet.id)
        return wallet

if __name__ == '__main__':
    updateWallt("Q-1","","","INIT")

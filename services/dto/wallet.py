from flaskServer.mode.wallet import Wallet
from flaskServer.config.connect import db,app
from sqlalchemy import and_
from flaskServer.utils.crypt import aesCbcPbkdf2EncryptToBase64

def getWalletByWord(env,t):
    with app.app_context():
        wallet = Wallet.query.filter(and_(Wallet.env==env,Wallet.type==t)).first()
        return wallet

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
        print("新增一条钱包信息，id：",wallet.id)
        return wallet

if __name__ == '__main__':
    updateWallt("Q-1","drip secret frown define acid goose tenant into beyond memory horn pear","init1z2900y05r38nxfrxygmg43606hlynwu64n5u6d","INIT")
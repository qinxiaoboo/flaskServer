from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.mode.account import Account
from eth_account import Account as ETHAccount
from flaskServer.dao.galxeAccount import AccountInfo
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64

def getAccountByEnv(env:Env):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        if proxy:
            proxy = f"http://{proxy.user}:{proxy.pwd}@{proxy.ip}:{proxy.port}"
        wallet = Wallet.query.filter_by(id=env.okx_id).first()
        email = Account.query.filter_by(id=env.outlook_id).first()
        ETHAccount.enable_unaudited_hdwallet_features()
        wallet_pri = ETHAccount.from_mnemonic(aesCbcPbkdf2DecryptFromBase64(wallet.word_pass)).key.hex()
        account = AccountInfo(idx=env.name, evm_address=wallet.address, evm_private_key= wallet_pri, proxy=proxy, email_username=email.name, user_agent=env.user_agent)
        return account

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-0").first()
        account = getAccountByEnv(env)
        print(account)


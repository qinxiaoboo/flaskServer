from eth_account import Account as ETHAccount

from flaskServer.config.connect import app, db
from flaskServer.entity.galxeAccount import AccountInfo
from flaskServer.mode.account import Account
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.space_points import SpacePoints
from flaskServer.mode.wallet import Wallet
from flaskServer.utils.envutil import to_be_exclude
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.dto.env import getAllEnvs


# 获取银河账号信息，通过ENV
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

def getGaxlesInfo():
    datas = []
    env_names = []
    for env in getAllEnvs():
        env_names.append(env.name)
    with app.app_context():
        ts = db.session.query(SpacePoints).filter(SpacePoints.env_name.in_(env_names)).order_by(SpacePoints.env_name.asc()).all()
        points = {}
        for t in ts:
            if t.env_name in points:
                points[t.env_name].append({f"{t.alia}":f"{t.points}:{t.ranking}"})
            else:
                points[t.env_name] = [{f"{t.alia}":f"{t.points}:{t.ranking}"}]
        for key,value in points.items():
            dicts = dict()
            dicts["环境"] = key
            for data in value:
                for name,vv in data.items():
                    if to_be_exclude(name):
                        continue
                    dicts[f"{name}"] = f"{vv}"
            datas.append(dicts)
    return datas

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-0").first()
        account = getAccountByEnv(env)
        print(account)


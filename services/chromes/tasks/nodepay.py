import asyncio

from flaskServer.services.internal.tls.client import TLSClient
from flaskServer.entity.galxeAccount import AccountInfo
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.account import Account
from flaskServer.config.connect import app

token = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMjkzMjE1MzQ2NjUxNTYxOTg0IiwiaWF0IjoxNzI4NDc3NDQ1LCJleHAiOjE3Mjk2ODcwNDV9.PVA7RDdsTH_8UflzBMIQhHRPBwP229C6bxSG9FL78KhniY6d8iUvpg5ywIOuhH43gO8GIHOP14NwUkqsiWE7Kw"

def toKeep(token,proxy,env_name,username):
    custom_headers = {
            "authorization": token,
             "origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm"
        }
    account = AccountInfo(idx=env_name,proxy=proxy,email_username=username)
    client = TLSClient(account, custom_headers)
    request = asyncio.run(client.post("https://api.nodepay.org/api/auth/session", {}))
    print(request)



if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-0").first()
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        account = Account.query.filter_by(id=env.outlook_id).first()
        if proxy:
            toKeep(token, proxy.user+":" +proxy.pwd+"@"+proxy.ip+":"+proxy.port, env.name, account.name)
        else:
            toKeep(token, "", env.name, account.name)


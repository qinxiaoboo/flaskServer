
import time
import asyncio
import requests
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger
from flaskServer.services.chromes.mail.factory import Email
from flaskServer.config.config import WALLET_PASSWORD
from flaskServer.config.connect import app
from flaskServer.entity.galxeAccount import AccountInfo
from flaskServer.mode.account import Account
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.utils.chrome import getChrome,get_Custome_Tab, quitChrome
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.content import Content
from flaskServer.services.dto.proxy import getProxyByID
from flaskServer.services.dto.account import updateAccountStatus,updateAccountToken
from flaskServer.services.internal.twitter.twitter import Twitter




if __name__ == '__main__':
    # with app.app_context():
    #     envs = Env.query.filter_by(group="qinxiaobo").all()
    #     for env in envs:
    #         tw = Account.query.filter_by(id=env.tw_id).first()
    #         discord = Account.query.filter_by(id=env.discord_id).first()
    #         if tw:
    #             print(tw.name)
    #         if discord:
    #             print(discord.token)

    # with app.app_context():
    #     envs = Env.query.all()
    #     for env in envs:
    #         tw = Account.query.filter_by(id=env.tw_id).first()
    #         discord = Account.query.filter_by(id=env.discord_id).first()
    #         if tw:
    #             print(tw.name)
    #         if discord:
    #             print(discord.token)

    with app.app_context():
        envs = Env.query.filter_by(name="test-2").all()
        for env in envs:
            tw = Account.query.filter_by(id=env.tw_id).first()
            discord = Account.query.filter_by(id=env.discord_id).first()

            print(f"环境编号：{env.name} | Tw_Name: @{tw.name} | Discord_Token: {discord.token}")
            print(f"{env.name}|@{tw.name}|{discord.token}")

            # if tw:
            #     print(f"Tw_Name: @{tw.name}")
            # if discord:
            #     print(f"Discord_Token: {discord.token}")
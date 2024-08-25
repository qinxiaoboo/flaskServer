import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
import random
# 连接数据库
from flaskServer.config.connect import app
#数据库信息
from flaskServer.mode.env import Env
import time
#配置代理
from flaskServer.mode.proxy import Proxy
#创建浏览器
from flaskServer.services.chromes.worker import submit
#变量
from flaskServer.services.content import Content
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.dto.account import getAccountById
from pprint import pprint
from flaskServer.config.connect import db
from flaskServer.mode.account import Account
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.chromes.login import tw2faV
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
from threading import Thread
from flaskServer.services.chromes.login import LoginDiscord
from flaskServer.utils.chrome import wait_captcha_page


url = "https://sepolia-faucet.pk910.de/#/"


def Faucet(chrome,env):
    tab = chrome.new_tab(url)
    # with open('C:/Users/Toka/Desktop/eth.txt', mode='r', encoding='utf-8') as f:
    #     addr = f.readline()
    #     line = addr[1:]
    chrome.wait(3,4)
    wait_captcha_page(tab, env)

    print("验证结束")











def Oneness(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            Faucet(chrome, env)

            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
            #chrome.quit()
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            if chrome:
                chrome.quit()

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="ZLL-22").first()
        Oneness(env)
    # submit(Oneness,getAllEnvs())

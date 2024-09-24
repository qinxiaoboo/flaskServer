import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
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
from flaskServer.utils.chrome import quitChrome
from flaskServer.utils.decorator import chrome_retry
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.services.chromes.login import LoginTW
import time
import string



#项目名称
name = 'now chain'

#项目邀请链接
now_chain_url = 'https://testnet.nowchain.co/testnet/point-system?referral=0xECB41b49D74D7d13bB51f9603Fd2360557647504/'


okx_url = '''let button  =
document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-announced-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet:nth-child(1)");
button.click();'''

def exe_okx(chrome):
    try:
        chrome.wait(3, 4)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
    except Exception as e:
        print("取的ele不对")
        logger.error(e)
    return

def getCount(chrome, env):
    try:
        taskData = getTaskObject(env, name)

    except Exception as e:
        logger.error(e)

def getChck_in(chrome,env):
    tab = chrome.new_tab(url=now_chain_url)
    time.sleep(5)
    #登录钱包
    try:
        if tab.s_ele('Connect Wallet'):
            tab.ele('Connect Wallet').click()
            time.sleep(2)
            tab.run_js(okx_url)
            time.sleep(2)
            exe_okx(chrome)
            time.sleep(2)




    except Exception as e:
        logger.error(e)






def nowchain(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)

            getChck_in(chrome,env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)
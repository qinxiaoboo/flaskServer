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
from flaskServer.utils.chrome import quitChrome
from flaskServer.utils.decorator import chrome_retry
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.services.chromes.login import LoginTW

start_url = "https://points.absinthe.network/hemi/start"
dashboard_url = "https://points.absinthe.network/hemi/d/dashboard"
brige_url = "https://app.hemi.xyz/en/tunnel/?operation=deposit"
swap_url = "https://swap.hemi.xyz/"
safe_url = "https://safe.hemi.xyz/welcome/accounts"

refcode = "b5fc3684"


def getHemi(chrome, env):
    tab = chrome.new_tab(start_url)

    # 登录钱包
    logger.info(f"{env.name}: 连接钱包")
    if tab.s_ele("Switch Wallet"):
        tab.refresh()
    if tab.s_ele("Connected",index=1):
        logger.info(f"{env.name}: 钱包已连接")
    else:
        tab.ele('Connect Wallet').click()
        tab.ele('Phantom').click()
        chrome.wait(10,15)
        if chrome.get_tab(title="Phantom Wallet").ele("@type=submit"):
            chrome.get_tab(title="Phantom Wallet").ele("@type=submit").click()
        chrome.wait(4,6)
        chrome.get_tab(title="Phantom Wallet").ele("@type=button",index=2).click()
        if tab.s_ele("Connected",index=1):
            logger.info(f"{env.name}: 钱包已连接")

    #输入邀请码
    if tab.s_ele("@class=lucide lucide-check"):
        logger.info(f"{env.name}: 邀请码已绑定")
    else:
        logger.info(f"{env.name}: 输入邀请码: {refcode}")
        tab.ele("@placeholder=<refcode>").input(refcode)
        tab.ele("@class=flex-shrink-0 w-10 h-10 flex items-center justify-center transition ease-in-out duration-150 css-1mepe94").click()
        if tab.s_ele("@class=lucide lucide-check"):
            logger.info(f"{env.name}: 邀请码绑定完成：{refcode}")

    #连接推特
    logger.info(f"{env.name}: 连接推特")
    if tab.s_ele("Connected", index=2):
        logger.info(f"{env.name}: 已连接")
    else:
        # tw_tab = tab.ele("@class=text-sm font-semibold max-w-full justify-center transition duration-150 ease-in-out disabled:cursor-not-allowed css-ds9w7p").click.for_new_tab()
        tab.ele("@class=text-sm font-semibold max-w-full justify-center transition duration-150 ease-in-out disabled:cursor-not-allowed css-ds9w7p").click()
        chrome.wait(12, 15)
        tw_tab = chrome.get_tab(url="twitter")
        if "login" in tw_tab.url:
            logger.info(f"{env.name}: 推特未登录,尝试重新登录")
            with app.app_context():
                tw: Account = Account.query.filter_by(id=env.tw_id).first()
                if tw:
                    tw_tab.ele("@autocomplete=username").input(tw.name)
                    tw_tab.ele("@@type=button@@text()=Next").click()
                    tw_tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
                    tw_tab.ele("@@type=button@@text()=Log in").click()
                    fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                    if "login" in tab.url and len(fa2) > 10:
                        tw2faV(tab, fa2)
                    chrome.wait(5, 8)
                    tw_tab.ele("Authorize app").click()
                else:
                    raise Exception(f"{env.name}: 没有导入TW的账号信息")

        else:
            tw_tab.ele("Authorize app").click()
        if tab.s_ele("Your X account has been connected successfully"):
            logger.info(f"{env.name}: Your X account has been connected successfully")
        else:
            logger.info(f"{env.name}: 推特授权失败")

    # #进入主页
    # tab = chrome.new_tab(start_url)
    #
    # tab.ele("Jumpstart the Pilot Program").click()





def Hemi(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getHemi(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            pass
            # quitChrome(env, chrome)

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="SYL-2").first()
        Hemi(env)



















































































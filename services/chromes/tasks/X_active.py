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


def getTab(chrome, env):
    tab = chrome.new_tab(url='https://x.com/home')

    tw_tab = tab
    if "login" in tw_tab.url:
        logger.info(f"{env.name}: 推特未登录,尝试重新登录")
        with app.app_context():
            tw: Account = Account.query.filter_by(id=env.tw_id).first()
        if tw:
            tw_tab.ele("@autocomplete=username").input(tw.name, clear=True)
            tw_tab.ele("@@type=button@@text()=Next").click()
            tab.ele("t:span@text():Password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd), clear=True)
            tw_tab.ele("@@type=button@@text()=Log in").click()
            fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
            if "login" in tab.url and len(fa2) > 10:
                tw2faV(tab, fa2)
            chrome.wait(25, 30)
        else:
            logger.info(f"{env.name}   推特被封或者需要重新登录")
            raise Exception(f"{env.name}: 没有导入TW的账号信息")

    if tab.s_ele("@@type=submit@@value=Start") or tab.ele("@@type=submit@@value=Continue to X"):

        try:
            tab.ele("@@type=submit@@value=Start").click()
        except Exception as e:
            pass
        chrome.wait(5, 10)

        try:
            tab.ele("@@type=submit@@value=Continue to X").click()
        except Exception as e:
            pass
        chrome.wait(5, 10)

        try:
            tab.ele("@@type=submit@@value=Start").click()
        except Exception as e:
            pass
        chrome.wait(5, 10)

    if tab.s_ele("@@type=submit@@value=Send email"):
        logger.info(f"{env.name}   推特被封或者需要重新登录")
        return

    if tab.ele('t:span@text():Got it'):
        tab.ele('t:span@text():Got it').click()

    if tab.ele('t:span@text():Turn on personalized ads'):
        tab.ele('t:span@text():Turn on personalized ads').click()

    if tab.ele('t:span@text():Got it'):
        tab.ele('t:span@text():Got it').click()

    for _ in range(20):
        tab.scroll.up(2)
        time.sleep(1)

    tab.ele('@class=css-175oi2r r-18kxxzh r-1wron08 r-onrtq4 r-1awozwy', index=5).click()
    chrome.wait(3, 6)
    tab.ele('@data-testid=like').click()
    chrome.wait(1)
    tab.ele('@data-testid=retweet').click()
    chrome.wait(1)
    tab.ele('@data-testid=retweetConfirm').click()
    chrome.wait(1)

    if tab.ele('@data-testid=unlike') and tab.ele('@data-testid=unretweet'):
        tab.ele('@class=css-175oi2r r-dnmrzs r-1559e4e').click()
        tab.ele('@role=presentation', index=2).click.multi()
        for _ in range(10):
            tab.scroll.up(2)
            time.sleep(1)
        tab.ele('@class=css-175oi2r r-18kxxzh r-1wron08 r-onrtq4 r-1awozwy', index=3).click()

        for _ in range(10):
            tab.scroll.up(2)
            time.sleep(1)
    else:
        logger.info(f"{env.name}   推特被封或者需要重新登录")
        return

    return

def x_active(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getTab(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)


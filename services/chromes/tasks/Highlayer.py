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
import requests
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger

from flaskServer.config.config import WALLET_PASSWORD
from flaskServer.config.connect import app
from flaskServer.mode.account import Account
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.utils.chrome import getChrome,get_Custome_Tab, quitChrome
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.content import Content
from flaskServer.services.dto.account import updateAccountStatus
name = 'Highlayer'
click_wallet_js = """
                const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > wui-list-wallet:nth-child(3)").shadowRoot.querySelector("button > wui-text").shadowRoot.querySelector("slot");
                return button
                """
click_wallet_js2 = """
                const button = document.querySelector("#root > div.dashboard-container > div.dashboard-profile-container.justify-center.hide-on-mobile > w3m-button").shadowRoot.querySelector("w3m-connect-button").shadowRoot.querySelector("wui-connect-button").shadowRoot.querySelector("button > wui-text").shadowRoot.querySelector("slot");                
                return button
                """

def getTab(chrome, env):
    rw = RandomWords()
    random_word = rw.random_word()
    taskData = getTaskObject(env, name)
    env_name = env.name
    outlook: Account = Account.query.filter_by(id=env.outlook_id).first()
    tab = chrome.new_tab(url="https://dashboard.highlayer.io/?referral=TOKATO")
    try:
        logger.info(f"{env.name}    连接钱包选择OKX")
        tab.run_js(click_wallet_js2).click()
        chrome.wait(2, 4)
        tab.run_js(click_wallet_js).click()
        chrome.wait(4, 8)
    except Exception as e:
        logger.info(f"{env.name}    该环境钱包已登录")

    if chrome.get_tab(title="OKX Wallet"):
        chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        chrome.wait(3, 6)

    if tab.ele('Create account'):
        tab.ele('Create account').click()
        chrome.wait(10, 15)

    try:
        tab.ele('@name=username').input(random_word, clear=True)
        logger.info(f"{env.name}    输入用户名")
        chrome.wait(3, 6)
        tab.ele('@name=email').input(outlook.name, clear=True)
        logger.info(f"{env.name}    输入邮箱")
        chrome.wait(3, 6)
        tab.ele('@class=cta-link profile-form-button').click()
        logger.info(f"{env.name}    点击更新资料按钮")
        chrome.wait(4, 8)
    except Exception as e:
        logger.info(f"{env.name}    该环境已经更新过用户资料")

    tab = chrome.new_tab(url="https://dashboard.highlayer.io/socials")
    chrome.wait(3, 6)
    if tab.ele('t:div@text():Connect new handle'):
        tab.ele('t:div@text():Connect new handle').click()
        logger.info(f"{env.name}    点击推特授权")
    else:
        tab.refresh()
        chrome.wait(3, 6)
        try:
            tab.ele('t:div@text():Connect new handle').click()
            logger.info(f"{env.name}    点击推特授权")
        except Exception as e:
            pass

    chrome.wait(10, 15)

    try:
        tw_tab = chrome.get_tab(url="twitter")
        if tw_tab:
            if "login" in tw_tab.url:
                logger.info(f"{env.name}: 推特未登录,尝试重新登录")
                with app.app_context():
                    tw: Account = Account.query.filter_by(id=env.tw_id).first()
                    if tw:
                        tw_tab.ele("@autocomplete=username").input(tw.name)
                        tw_tab.ele("@@type=button@@text()=Next").click()
                        tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
                        tw_tab.ele("@@type=button@@text()=Log in").click()
                        fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                        if "login" in tab.url and len(fa2) > 10:
                            tw2faV(tab, fa2)
                        chrome.wait(20, 25)
                    else:
                        raise Exception(f"{env.name}: 没有导入TW的账号信息")
    except Exception as e:
        logger.info(f"y{env.name}: 推特登陆失败")
        return

    try:
        if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Send email"):
            logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
            quitChrome(env, chrome)
    except Exception as e:
        pass

    try:
        if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Start"):
            chrome.get_tab(url='https://twitter.com/').ele("@@type=submit@@value=Start").click()
            chrome.wait(10, 15)
            if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Send email"):
                logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
                quitChrome(env, chrome)
            chrome.wait(25, 30)
    except Exception as e:
        pass

    try:
        if chrome.get_tab(url='https://twitter.com/').ele("@@type=submit@@value=Continue to X"):
            chrome.get_tab(url='https://twitter.com/').ele("@@type=submit@@value=Continue to X").click()
            chrome.wait(20, 25)
        if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Start"):
            chrome.get_tab(url='https://twitter.com/').ele("@@type=submit@@value=Start").click()
            chrome.wait(10, 15)
        if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Send email"):
            logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
            quitChrome(env, chrome)
    except Exception as e:
        pass

    try:
        chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
        logger.info(f"{env.name}    授权 X 完成")
        chrome.wait(10, 15)

    except Exception as e:
                max_attempts = 5
                attempt = 0
                while attempt < max_attempts:
                        tab.close()
                        tab = chrome.new_tab(url="https://dashboard.highlayer.io/socials")
                        tab.refresh()

                        if tab.ele('t:div@text():Connect new handle'):
                            tab.ele('t:div@text():Connect new handle').click()
                            logger.info(f"{env.name}    点击推特授权2")
                            chrome.wait(10, 15)
                        try:
                            chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
                            logger.info(f"{env.name}    授权 X 完成")
                            chrome.wait(10, 15)
                            break
                        except Exception as e:
                            pass
                        attempt += 1


    tab = chrome.new_tab(url="https://dashboard.highlayer.io/daily")

    if tab.ele('@class=cta-link dashboard-button cta-button-bottom fw-300 ls-1 xs'):
        chrome.wait(5, 10)
        tab.ele('@class=cta-link dashboard-button cta-button-bottom fw-300 ls-1 xs', index=1).click()
        logger.info(f"{env.name}    加入discord")
        chrome.wait(10, 15)
        try:
            tab.ele('t:div@text():Visit telegram group').click()
            chrome.wait(3, 5)
            logger.info(f"{env.name}    加入tg")
        except Exception as e:
            logger.info(f"{env.name}    加入tg失败")

        try:
            tab.ele('@class=cta-link dashboard-button cta-button-bottom fw-300 ls-1 xs', index=3).click()
            chrome.wait(3, 5)
            logger.info(f"{env.name}    加入X")
        except Exception as e:
            logger.info(f"{env.name}    加入X失败")

        try:
            tab.ele('t:div@text():Visit blog and learn').click()
            chrome.wait(3, 5)
            logger.info(f"{env.name}    Visit blog")
        except Exception  as e:
            logger.info(f"{env.name}    Visit blog失败")

        try:
            tab.ele('t:div@text():Visit website').click()
            chrome.wait(3, 5)
            logger.info(f"{env.name}    Visit website")
            chrome.wait(10, 15)
        except Exception as e:
            logger.info(f"{env.name}    Visit website失败")

        logger.info(f"{env.name}    每日任务已完成！")

    else:
        logger.info(f"{env.name}    推特授权失败，每日任务失败")
        return

    logger.info(f"{env.name}    统计总分")
    tab = chrome.new_tab(url="https://dashboard.highlayer.io/?referral=TOKATO")
    tab.refresh()
    chrome.wait(3, 4)
    total = tab.ele('@class=stat-value', index=6).text
    taskData.Total = total
    updateTaskRecord(env.name, name, taskData, 1)

    return

def highlayer(env):
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
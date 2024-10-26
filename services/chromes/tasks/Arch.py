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
name = "Arch"

def getTab(chrome, env):
    tab = chrome.new_tab(url="https://dashboard.arch.network?referralCode=f9c6ab90-03a4-4724-9cbd-080a192f74d2")
    rw = RandomWords()
    random_word = rw.random_word()
    taskData = getTaskObject(env, name)
    env_name = env.name
    tab.set.window.max()
    chrome.wait(2, 3)

    if tab.ele('t:button@text():Connect Wallet'):
        logger.info(f"{env.name}   链接钱包选择OKX")
        tab.ele('t:button@text():Connect Wallet').click()
        chrome.wait(3, 6)
        tab.ele('OKX').click()
        chrome.wait(10, 15)

        if chrome.get_tab(title="OKX Wallet"):
            logger.info(f"{env.name}   OKX钱包授权")
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            chrome.wait(10, 15)

    for _ in range(3):
        if tab.ele('t:button@text():Sign'):
            logger.info(f"{env.name}   登录")
            tab.ele('t:button@text():Sign').click()
            chrome.wait(10, 15)
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            chrome.wait(15, 20)

    if tab.ele('t:span@text():START MISSIONS'):
        logger.info(f"{env.name}   主页登录成功")
    else:
        logger.info(f"{env.name}   主页登录失败")
        return

    logger.info(f"{env.name}   进入任务页面")
    tab.ele('t:span@text():START MISSIONS').click()
    chrome.wait(2, 3)
    tab.ele('t:div@text():DAILY MISSIONS').click()
    chrome.wait(6, 9)

    if tab.ele('t:button@text():Start'):
        logger.info(f"{env.name}   推特授权成功")
    else:
        logger.info(f"{env.name}   推特授权")
        tab.ele('t:button@text():Authorize').click()
        chrome.wait(20, 25)

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
                            tab.ele("@type=password").click().input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
                            tw_tab.ele("@@type=button@@text()=Log in").click()
                            fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                            if "login" in tab.url and len(fa2) > 10:
                                tw2faV(tab, fa2)
                            chrome.wait(25, 30)
                        else:
                            raise Exception(f"{env.name}: 没有导入TW的账号信息")
        except Exception as e:
            logger.info(f"{env.name}: 推特登陆失败")
            return

        if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Send email"):
            logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
            return

        if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Start"):
            chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Start").click(by_js=True)
            chrome.wait(10, 15)
            if chrome.get_tab(url='https://twitter.com/').s_ele("@@type=submit@@value=Send email"):
                logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
                return
            chrome.wait(25, 30)

        if chrome.get_tab(url='https://twitter.com/').ele("@@type=submit@@value=Continue to X"):
            chrome.get_tab(url='https://twitter.com/').ele("@@type=submit@@value=Continue to X").click()
            chrome.wait(20, 25)

        if chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button"):
            chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
            logger.info(f"{env.name}   推特授权成功")
            chrome.wait(15, 20)
        else:
            tab = chrome.new_tab(url="https://dashboard.arch.network/missions")
            tab.ele('t:div@text():DAILY MISSIONS').click()
            chrome.wait(2, 4)

            if tab.ele('t:button@text():Start'):
                logger.info(f"{env.name}   推特授权成功")
            else:
                try:
                    tab.ele('t:button@text():Authorize').click()
                    chrome.wait(20, 25)
                    chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
                    logger.info(f"{env.name}   推特授权成功")
                except Exception as e:
                    logger.info(f"{env.name}   推特授权失败")
                    return

    logger.info(f"{env.name}   开始做入职任务")
    tab.ele('t:div@text():ONBOARDING MISSIONS').click()
    chrome.wait(1, 2)
    tab.ele('t:button@text():Start').click()
    chrome.wait(25, 30)
    try:
        tw_tab = chrome.get_tab(url="x.com")
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
                            chrome.wait(25, 30)
                        else:
                            raise Exception(f"{env.name}: 没有导入TW的账号信息")

        if chrome.get_tab(url='https://x.com/').ele("t:span@text():Log in"):
                chrome.get_tab(url='https://x.com/').ele("t:span@text():Log in").click()
                logger.info(f"{env.name}: 推特未登录,尝试重新登录")
                with app.app_context():
                    tw: Account = Account.query.filter_by(id=env.tw_id).first()
                    if tw:
                        tw_tab.ele("@autocomplete=username").input(tw.name)
                        tw_tab.ele("@@type=button@@text()=Next").click()
                        tab.ele("@type=password").click().input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
                        tw_tab.ele("@@type=button@@text()=Log in").click()
                        fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                        if "login" in tab.url and len(fa2) > 10:
                            tw2faV(tab, fa2)
                        chrome.wait(25, 30)
                    else:
                        raise Exception(f"{env.name}: 没有导入TW的账号信息")
    except Exception as e:
        logger.info(f"{env.name}: 推特登录失败")
        return

    chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(20, 25)

    try:
        tw_tab = chrome.get_tab(url="x.com")
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
                        chrome.wait(25, 30)
                    else:
                        raise Exception(f"{env.name}: 没有导入TW的账号信息")

        if chrome.get_tab(url='https://x.com/').ele("t:span@text():Log in"):
            chrome.get_tab(url='https://x.com/').ele("t:span@text():Log in").click()
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
                    chrome.wait(25, 30)
                else:
                    raise Exception(f"{env.name}: 没有导入TW的账号信息")

    except Exception as e:
        logger.info(f"{env.name}: 推特登陆失败")
        return

    chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(15, 20)
    chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(15, 20)
    chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(15, 20)
    chrome.get_tab(url='https://x.com/').ele("t:span@text():Post").click(by_js=True)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(15, 20)
    chrome.get_tab(url='https://x.com/').ele("@data-testid=reply").click(by_js=True)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').ele("t:div@text():Post your reply").input(random_word)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').ele("t:span@text()Reply").click(by_js=True)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(15, 20)
    chrome.get_tab(url='https://x.com/').ele("@data-testid=retweet").click(by_js=True)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').ele("t:span@text():Repost").click(by_js=True)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    tab.ele('t:button@text():Start').click()
    chrome.wait(15, 20)
    chrome.get_tab(url='https://x.com/').ele("t:span@text():Post").click(by_js=True)
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()

    while True:
        element = tab.ele('t:button@text():Verify')
        if not element:
            break
        else:
            element.click()

    return



def arch(env):
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







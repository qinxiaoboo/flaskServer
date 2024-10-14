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
name = "Claim_diamante"

def getTab(chrome, env):
    tab = chrome.new_tab(url="https://claim.diamante.io/")
    taskData = getTaskObject(env, name)
    env_name = env.name
    chrome.wait(4, 8)
    tab.ele('@class=connect_wallet').click()
    logger.info(f"{env.name}    连接钱包")
    chrome.wait(4, 8)
    # Connect Wallet to Claim
    tab.ele('@class=d-flex gap-4 align-items-center justify-content-between  p-1 cursor-pointer chainItems w-100 false', index=2).click()
    logger.info(f"{env.name}    选择Solana")
    # Solana
    chrome.wait(15, 20)

    if chrome.get_tab(title="Phantom Wallet"):
        chrome.get_tab(title="Phantom Wallet").ele("@type=submit").click()
        chrome.wait(13, 16)

    if tab.ele('I got it'):
        tab.ele('I got it').click()
        logger.info(f"{env.name}   点击明白介绍")
        chrome.wait(3, 4)

    logger.info(f"{env.name}   开始数据统计")
    try:
        points = tab.ele('@class=diam-amount').text
        taskData.Points = points
        updateTaskRecord(env.name, name, taskData, 1)
    except Exception as e:
        logger.info(f"{env.name}   数据统计失败")


    if tab.ele('@class=claim-button'):
        tab.ele('@class=claim-button').click()
        logger.info(f"{env.name}    开始领取DIAM")
        chrome.wait(3, 5)

    if tab.ele('t:button@text():Authorize'):
        tab.ele('t:button@text():Authorize').click()
        logger.info(f"{env.name}    点击推特授权")
        chrome.wait(25, 30)
    # Something went wrong

    try:
        if chrome.get_tab(url='https://twitter.com/').ele("@value=Send email"):
            logger.info(f"{env.name}    退出，推特需要邮箱验证！！")
            return
    except Exception as e:
        pass

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
                        tw_tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
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

    try:
        chrome.wait(10, 15)
        chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
        logger.info(f"{env.name}    授权 X 完成")
        chrome.wait(20, 25)

    except Exception as e:
                max_attempts = 5
                attempt = 0
                while attempt < max_attempts:
                        tab.close()
                        tab = chrome.new_tab(url="https://claim.diamante.io/twitter")
                        tab.refresh()
                        chrome.wait(10, 15)

                        if tab.ele('t:button@text():Authorize'):
                            tab.ele('t:button@text():Authorize').click()
                            logger.info(f"{env.name}    点击推特授权2")
                            chrome.wait(25, 30)
                        try:
                            chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
                            logger.info(f"{env.name}    授权 X 完成")
                            chrome.wait(20, 25)
                            break
                        except Exception as e:
                            pass
                        attempt += 1

    try:
        logger.info(f"{env.name}    关注推特")
        tab.ele('@class=claim-button').click()
        chrome.wait(6, 9)
    except Exception as e:
        logger.info(f"{env.name}    该环境已完成")
        return

    logger.info(f"{env.name}    点赞转发推特")
    tab.ele('@class=claim-button').click()
    chrome.wait(4, 6)

    logger.info(f"{env.name}    领取积分")
    tab.wait.ele_displayed('@class=claim-button', timeout=20)
    tab.ele('@class=claim-button').click()
    logger.info(f"{env.name}    领取积分成功！")
    chrome.wait(10, 15)

def claim_diamante(env):
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


















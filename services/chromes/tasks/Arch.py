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
                            tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
                            tw_tab.ele("@@type=button@@text()=Log in").click()
                            fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                            if "login" in tab.url and len(fa2) > 10:
                                tw2faV(tab, fa2)
                            chrome.wait(25, 30)
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
            if chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button"):
                    chrome.get_tab(url='https://twitter.com/').ele("@data-testid=OAuth_Consent_Button").click()
                    logger.info(f"{env.name}   推特授权成功")
                    chrome.wait(15, 20)
        except Exception as e:
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
                        quitChrome(env, chrome)
    return

def missions(chrome, env):
    tab = chrome.new_tab(url="https://x.com/ArchNtwrk")
    rw = RandomWords()
    random_word = rw.random_word()
    taskData = getTaskObject(env, name)
    env_name = env.name
    logger.info(f"{env.name}   开始做入职任务")
    chrome.wait(15, 25)
    chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
    chrome.wait(3, 6)
    chrome.get_tab(url='https://x.com/').close()
    chrome.wait(15, 20)
    tab = chrome.new_tab(url="https://dashboard.arch.network/missions")
    chrome.wait(3, 6)
    tab.ele('t:div@text():ONBOARDING MISSIONS').click()
    chrome.wait(3, 6)
    tab.ele('t:button@text():Start').click()
    chrome.wait(3, 6)

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
    try:
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
        pass

    tab = chrome.new_tab(url="https://x.com/compose/post")
    chrome.wait(3, 6)
    tab.ele("@class=css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-1h8ys4a r-1bylmt5 r-13tjlyg r-7qyjyx r-1ftll1t").input('I just claimed my Archstronaut spacesuit to complete incentivized missions and explore the Bitcoin galaxy 🚀 Join me and other Archstronauts to rise in the ranks, earn rewards and shape the future of BTCFi through the @ArchNtwrk march to testnet:')
    chrome.wait(3, 6)
    tab.ele("t:span@text():Post").click(by_js=True)
    chrome.wait(3, 6)
    tab.close()

    tab = chrome.new_tab(url="https://x.com/compose/post")
    chrome.wait(3, 6)
    tab.ele("@class=css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-1h8ys4a r-1bylmt5 r-13tjlyg r-7qyjyx r-1ftll1t").input('Want to earn points and help build bridgeless Bitcoin DeFi?\n\nJoin me: https://dashboard.arch.network?referralCode=254c68f9-1b28-4e66-bdf1-4e42c48085f9 #JoinArch ')
    chrome.wait(3, 6)
    tab.ele("t:span@text():Post").click(by_js=True)
    chrome.wait(3, 6)
    tab.close()

    tab = chrome.new_tab(url="https://x.com/ArchNtwrk")
    try:
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/proofofmud")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/0xfinetuned")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/Nick4Iezos")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/ArchNtwrk/status/1848774876322042228")
        chrome.get_tab(url='https://x.com/').ele("@data-testid=reply").click(by_js=True)
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').ele("t:div@text():Post your reply").input(random_word)
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').ele("@data-testid=tweetButton").click(by_js=True)
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').ele("@data-testid=retweet").click(by_js=True)
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Repost").click(by_js=True)
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass


    tab = chrome.new_tab(url="https://dashboard.arch.network/missions")
    if tab.ele('t:span@text():CONTINUE'):
        tab.ele('t:span@text():CONTINUE').click()
    tab.ele('t:div@text():ONBOARDING MISSIONS').click()
    chrome.wait(2, 3)

    logger.info(f"{env.name}    开始验证")
    count = 0
    while count < 10:
        element = tab.ele('t:button@text():Start')
        if not element:
            break
        else:
            element.click()
        count += 1
    chrome.wait(5, 10)
    if tab.ele('t:span@text():CONTINUE'):
        tab.ele('t:span@text():CONTINUE').click()

    return

def weekly(chrome, env):
    logger.info(f"{env.name}    开始做每周任务")

    try:
        tab = chrome.new_tab(url="https://x.com/Saturn_btc")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/bimabtc")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/BoundUSD")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/funkybit_fun")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Follow").click()
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass

    try:
        tab = chrome.new_tab(url="https://x.com/intent/post?text=I+just+claimed+my+Archstronaut+spacesuit+to+complete+incentivized+missions+and+explore+the+Bitcoin+galaxy+%F0%9F%9A%80%0A%0AJoin+me+and+other+Archstronauts+to+rise+in+the+ranks%2C+earn+rewards+and+shape+the+future+of+BTCFi+through+the+%40ArchNtwrk+march+to+testnet%3A+https%3A%2F%2Fdashboard.arch.network%3FreferralCode%3D25fffa06-f376-44cb-b87d-f93616e3b551")
        chrome.get_tab(url='https://x.com/').ele("t:span@text():Post").click(by_js=True)
        chrome.wait(3, 6)
        chrome.get_tab(url='https://x.com/').close()
    except Exception as e:
        pass
    chrome.wait(3, 6)

    tab = chrome.new_tab(url="https://dashboard.arch.network/missions")
    if tab.ele('t:span@text():CONTINUE'):
        tab.ele('t:span@text():CONTINUE').click()

    tab.ele('t:div@text():WEEKLY MISSIONS').click()
    chrome.wait(2, 3)
    count = 0
    while count < 10:
        element = tab.ele('t:button@text():Start')
        if not element:
            break
        else:
            element.click()
        count += 1
    chrome.wait(5, 10)
    if tab.ele('t:span@text():CONTINUE'):
        tab.ele('t:span@text():CONTINUE').click()
    return

def daily(chrome, env):
    logger.info(f"{env.name}   开始做每日任务")
    tab = chrome.new_tab(url="https://dashboard.arch.network/missions")
    if tab.ele('t:span@text():CONTINUE'):
        tab.ele('t:span@text():CONTINUE').click()
    tab.ele('t:div@text():DAILY MISSIONS').click()
    chrome.wait(2, 3)
    count = 0
    while count < 10:
        element = tab.ele('t:button@text():Start')
        if not element:
            break
        else:
            element.click()
        count += 1
    chrome.wait(5, 10)
    if tab.ele('t:span@text():CONTINUE'):
        tab.ele('t:span@text():CONTINUE').click()
    return


def count(chrome, env):
    tab = chrome.new_tab(url="https://dashboard.arch.network/missions")
    taskData = getTaskObject(env, name)
    env_name = env.name

    logger.info(f"{env.name}   开始数据统计")
    try:
        xp = tab.ele('@class=absolute inset-0 flex items-center justify-center text-[18px] font-bold leading-normal text-lighter-yellow', index=1).text
        level = tab.ele('@class=text-lightest-yellow text-[15px] leading-6 uppercase').text
        print(xp)
        print(level)
        taskData.Xp = xp
        taskData.Level = level
        updateTaskRecord(env.name, name, taskData, 1)
    except Exception as e:
        logger.info(f"{env.name}   数据统计失败")

    return


def arch(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getTab(chrome, env)
            missions(chrome, env)
            weekly(chrome, env)
            daily(chrome, env)
            count(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)







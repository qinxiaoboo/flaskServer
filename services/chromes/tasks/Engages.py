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
import time
from flaskServer.utils.chrome import quitChrome, get_Custome_Tab
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
import requests
import openpyxl
from flaskServer.mode.account import Account
from flaskServer.services.chromes.login import OKXChrome, tw2faV
from DrissionPage import ChromiumPage
from loguru import logger
# 连接数据库
import random
from flaskServer.config.connect import app
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.dto.account import updateAccountStatus
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject

def logintw(chrome, env):
    tab = chrome.new_tab(url="https://x.com/home")
    try:
        tw_tab = chrome.get_tab(url="twitter")
        if tw_tab:
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
                        raise Exception(f"{env.name}: 没有导入TW的账号信息")

        if chrome.get_tab(url='https://x.com/').ele("t:span@text():Log in"):
            chrome.get_tab(url='https://x.com/').ele("t:span@text():Log in").click()
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
                    raise Exception(f"{env.name}: 没有导入TW的账号信息")
    except Exception as e:
        pass

    try:
        if chrome.get_tab(url='https://x.com/').s_ele("@@type=submit@@value=Send email"):
            logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
            quitChrome(env, chrome)
    except Exception as e:
        pass

    try:
        if chrome.get_tab(url='https://x.com/').s_ele("@@type=submit@@value=Start"):
            chrome.get_tab(url='https://x.com/').ele("@@type=submit@@value=Start").click()
            chrome.wait(10, 15)
            if chrome.get_tab(url='https://x.com/').s_ele("@@type=submit@@value=Send email"):
                logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
                quitChrome(env, chrome)
            chrome.wait(25, 30)
    except Exception as e:
        pass

    try:
        if chrome.get_tab(url='https://x.com/').ele("@@type=submit@@value=Continue to X"):
            chrome.get_tab(url='https://x.com/').ele("@@type=submit@@value=Continue to X").click()
            chrome.wait(20, 25)
        if chrome.get_tab(url='https://x.com/').s_ele("@@type=submit@@value=Start"):
            chrome.get_tab(url='https://x.com/').ele("@@type=submit@@value=Start").click()
            chrome.wait(10, 15)
        if chrome.get_tab(url='https://x.com/').s_ele("@@type=submit@@value=Send email"):
            logger.info(f"{env.name}   该环境推特需要邮箱验证，请前往验证")
            quitChrome(env, chrome)
    except Exception as e:
        pass

    return

def getTab(chrome, env):
    tab = chrome.new_tab(url="https://engages.io/")
    chrome.wait(2, 3)

    if tab.ele('t:button@text():Connect Discord'):
        tab.ele('t:button@text():Connect Discord').click()
        chrome.wait(1)
    if tab.ele('t:button@text():Continue Discord'):
        tab.ele('t:button@text():Continue Discord').click()

    chrome.wait(3, 6)

    try:
        if chrome.get_tab(url='discord.com').s_ele("t:div@text():Authorize") or chrome.get_tab(url='discord.com').s_ele("t:div@text():授权"):
            chrome.get_tab(url='discord.com').ele("@type=button", index=2).click()
            chrome.wait(10, 16)

    except Exception as e:
        pass

    try:
        if chrome.get_tab(url='discord.com').s_ele("Please log in again") or chrome.get_tab(url='discord.com').s_ele("请再次登录"):
            chrome.get_tab(url='discord.com').ele("@type=button", index=1).click()
            logger.info(f"{env.name} 开始登录 Discord 账号")
            with app.app_context():
                discord: Account = Account.query.filter_by(id=env.discord_id).first()
                if discord:
                    chrome.get_tab(url='discord.com').ele("@name=email").input(discord.name)
                    chrome.get_tab(url='discord.com').ele("@name=password").input(aesCbcPbkdf2DecryptFromBase64(discord.pwd))
                    chrome.get_tab(url='discord.com').ele("@type=submit").click()
                    fa2 = aesCbcPbkdf2DecryptFromBase64(discord.fa2)
                    if "login" in chrome.get_tab(url='discord.com').url and len(fa2) > 10:
                        res = requests.get(fa2)
                        if res.ok:
                            code = res.json().get("data").get("otp")
                            chrome.get_tab(url='discord.com').ele("@autocomplete=one-time-code").input(code)
                            chrome.get_tab(url='discord.com').ele("@type=submit").click()
                else:
                    updateAccountStatus(env.discord_id, 1, "没有导入DISCORD 的账号信息")
                    raise Exception(f"{env.name}: 没有导入DISCORD 账号信息")

                if chrome.get_tab(url='discord.com').s_ele("t:div@text():Authorize") or chrome.get_tab(url='discord.com').s_ele("t:div@text():授权"):
                    chrome.get_tab(url='discord.com').ele("@type=button", index=2).click()
                    chrome.wait(10, 16)

    except Exception as e:
        pass

    if tab.ele("@class= flexItem text-white h-[44px] bg-[#0A121F] rounded-[7px] flex flex-row justify-center items-center px-[24px] py-0 gap-[10px]"):
        try:
                logger.info(f'{env.name}:  discord授权成功, 开始推特授权')
                tab.ele('@class=itemWrapper', index=4).click()
                if tab.ele('t:button@text():Connect Twitter'):
                    tab.ele('t:button@text():Connect Twitter').click()
                    chrome.wait(10, 16)
                    chrome.get_tab(url='api.x.com').ele("@class=submit button selected").click()
                    chrome.wait(10, 16)
        except Exception as e:
                logintw(chrome, env)
                tab.refresh()
                tab.ele('@class=transition-all ease-in-out menuItem rounded-[12px] bg-[#0a121f] transparentBorder w-full').click()
                if tab.ele('t:button@text():Connect Twitter'):
                    tab.ele('t:button@text():Connect Twitter').click()
                    chrome.wait(10, 16)
                    chrome.get_tab(url='api.x.com').ele("@class=submit button selected").click()
                    chrome.wait(10, 16)
    else:
        logger.info(f'{env.name}:  discord授权失败，人工授权')

    if tab.s_ele("Discord ID: ") and tab.s_ele("Twitter: @"):
        logger.info(f'{env.name}:  discord与推特授权成功')
    else:
        logger.info(f'{env.name}:  discord或推特授权失败，人工授权')


def liketw(chrome, env):
    list = [
        'great',
        'LFG',
        'LFG🚀',
        'nice',
        'so nice',
        'lfg',
        'Lfg',
        'Great',
        'amazing',
        'awesome',
        'excellent',
        'outstanding',
        'impressive',
        'incredible',
        'fantastic',
        'wonderful',
        'remarkable',
        'phenomenal',
        'brilliant',
        'exceptional',
        'stunning',
        'terrific',
        'fabulous',
        'splendid',
        'breathtaking',
        'genius',
        'masterpiece',
        'champion',
        'hero',
        'pro',
        'star',
        'virtuoso',
        'expert',
        'trailblazer',
        'maven',
        'You nailed it!',
        'You did an outstanding job!',
        'You\'re amazing!',
        'That\'s impressive!',
        'You\'re a genius!',
        'I\'m so proud of you!',
        'You\'re on fire!',
        'You\'re a rock star!',
        'That was top-notch!',
        'You’ve outdone yourself!',
        'You look stunning!',
        'You look fantastic!',
        'You\'re looking sharp!',
        'You\'re glowing!'
    ]

    random_choice = random.choice(list)
    tab = chrome.new_tab(url="https://x.com/SaharaLabsAI/status/1871088052602319187")
    # 点赞
    tab.ele('@data-testid=like').click()
    chrome.wait(1)
    # 评论
    tab.ele('@data-testid=reply').click()
    chrome.wait(1, 2)
    tab.ele("@class=css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-1h8ys4a r-1bylmt5 r-13tjlyg r-7qyjyx r-1ftll1t").input(random_choice)
    chrome.wait(1, 2)
    tab.ele('@data-testid=tweetButton').click()
    chrome.wait(3, 6)
    tab.close()

    # tab = chrome.new_tab(url="https://x.com/SaharaLabsAI/status/1869411896069333380")
    # # 点赞
    # tab.ele('@data-testid=like').click()
    # chrome.wait(1)
    # # 评论
    # tab.ele('@data-testid=reply').click()
    # chrome.wait(1, 2)
    # tab.ele("@class=css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-1h8ys4a r-1bylmt5 r-13tjlyg r-7qyjyx r-1ftll1t").input(random_choice)
    # chrome.wait(1, 2)
    # tab.ele('@data-testid=tweetButton').click()
    # chrome.wait(3, 6)
    # tab.close()
    #
    # tab = chrome.new_tab(url="https://x.com/SaharaLabsAI/status/1869428301435204003")
    # # 点赞
    # tab.ele('@data-testid=like').click()
    # chrome.wait(1)
    # # 评论
    # tab.ele('@data-testid=reply').click()
    # chrome.wait(1, 2)
    # tab.ele("@class=css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-1h8ys4a r-1bylmt5 r-13tjlyg r-7qyjyx r-1ftll1t").input(random_choice)
    # chrome.wait(1, 2)
    # tab.ele('@data-testid=tweetButton').click()
    # chrome.wait(3, 6)
    # tab.close()

    return





def engages(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            # getTab(chrome, env)
            liketw(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)

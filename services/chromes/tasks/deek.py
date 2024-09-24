import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
import random
from flaskServer.utils.chrome import quitChrome

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
from flaskServer.services.chromes.login import tw2faV
from faker import Faker
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
click_wallet_js = """
            const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet:nth-child(1)").shadowRoot.querySelector("button > wui-text").shadowRoot.querySelector("slot");
            return button
            """

deek_network_js = """
            const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-unsupported-chain-view").shadowRoot.querySelector("wui-flex > wui-flex:nth-child(2) > wui-list-network").shadowRoot.querySelector("button");            
            return button
            """
deek_network_js2 = """
            const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-header").shadowRoot.querySelector("wui-flex > wui-icon-link:nth-child(3)").shadowRoot.querySelector("button");
            return button
            """


def getTab(chrome, env):
    tab = chrome.new_tab(url="https://s.deek.network/invite/detail?inviteCode=13VRQ3&handle=chaojiaichihon1")
    chrome.wait(2, 3)

    try:
        if tab.ele('Join now'):
            tab.ele('Join now').click()
            chrome.wait(3, 6)

    except Exception as e:
            tab.refresh()
            chrome.wait(2, 3)
            if tab.ele('Join now'):
                tab.ele('Join now').click()
                chrome.wait(3, 6)
            else:
                logger.info(f"{env.name}网络异常，Join失败")

    try:
        if tab.ele('t:span@text():Login with X'):
            logger.info(f"{env.name}开始登录X")
            tab.ele('t:span@text():Login with X').click()
            chrome.wait(2, 3)
            for _ in range(2):
                if tab.ele('t:div@text():Authorization failed, please try again'):
                    tab.refresh()
                    chrome.wait(2)
                    tab.ele('t:span@text():Login with X').click()
                    chrome.wait(2, 3)

            logger.info(f"{env.name}授权X")
            tab.wait.ele_displayed(chrome.get_tab(url='https://api.x.com/').ele("@class=submit button selected"), timeout=60)
            try:
                chrome.get_tab(url='https://api.x.com/').ele("@class=submit button selected").click()
                logger.info(f"{env.name}授权X完成")
            except Exception as e:
                tab.wait.load_start()
                chrome.get_tab(url='https://api.x.com/').ele("@class=submit button selected").click()
                logger.info(f"{env.name}授权X完成")


        try:
            tab.wait.ele_displayed('t:button@text():Create', timeout=60)
            if tab.ele('t:button@text():Create'):
                logger.info(f"{env.name}创建账户")
                chrome.wait(2, 3)
                tab.ele('t:button@text():Create').click()
                chrome.wait(2, 3)
                for _ in range(3):
                    if tab.ele('t:button@text():Create'):
                        tab.refresh()
                        chrome.wait(2, 3)
                        tab.ele('t:button@text():Create').click()
                        chrome.wait(1, 2)

                tab.wait.load_start()
                tab.ele('@placeholder=Enter invite code').click().input('13VRQ3', clear=True)
                logger.info(f"{env.name}输入邀请码")
                chrome.wait(1, 2)
                tab.ele('t:button@text():Confirm').click()
                logger.info(f"{env.name}提交邀请码")
                chrome.wait(3, 6)

        except Exception as e:

            if tab.ele('t:button@text():Create'):
                chrome.wait(2, 3)
                tab.ele('t:button@text():Create').click()
                logger.info(f"{env.name}创建账户")
                chrome.wait(2, 3)
                for _ in range(3):
                    if tab.ele('t:button@text():Create'):
                        tab.refresh()
                        chrome.wait(2, 3)
                        tab.ele('t:button@text():Create').click()
                        chrome.wait(1, 2)

                tab.wait.load_start()
                tab.ele('@placeholder=Enter invite code').click().input('13VRQ3', clear=True)
                logger.info(f"{env.name}输入邀请码")
                chrome.wait(1, 2)
                tab.ele('t:button@text():Confirm').click()
                logger.info(f"{env.name}提交邀请码")
                chrome.wait(3, 6)

        try:
            if tab.ele('@placeholder=Enter invite code'):
                tab.ele('@placeholder=Enter invite code').click().input('13VRQ3', clear=True)
                logger.info(f"{env.name}输入邀请码")
                chrome.wait(1, 2)
                tab.ele('t:button@text():Confirm').click()
                logger.info(f"{env.name}提交邀请码")
        except Exception as e:
            logger.info(f"{env.name}邀请码已经输入了")


        if tab.ele('t:button@text():Connect Wallet'):
            logger.info(f"{env.name}主页登录成功")

    except Exception as e:
        try:
            tab.refresh()
            chrome.wait(2, 3)
            if tab.ele('t:span@text():Login with X'):
                tab.ele('t:span@text():Login with X').click()
                chrome.wait(2, 3)
                for _ in range(2):
                    if tab.ele('t:div@text():Authorization failed, please try again'):
                        tab.refresh()
                        chrome.wait(2)
                        tab.ele('t:span@text():Login with X').click()
                        chrome.wait(2, 3)

                logger.info(f"{env.name}授权X")
                tab.wait.ele_displayed(chrome.get_tab(url='https://api.x.com/').ele("@class=submit button selected"), timeout=60)
                try:
                    chrome.get_tab(url='https://api.x.com/').ele("@class=submit button selected").click()
                    logger.info(f"{env.name}授权X完成")
                except Exception as e:
                    tab.wait.load_start()
                    chrome.get_tab(url='https://api.x.com/').ele("@class=submit button selected").click()
                    logger.info(f"{env.name}授权X完成")

            try:
                tab.wait.ele_displayed('t:button@text():Create', timeout=60)
                if tab.ele('t:button@text():Create'):
                    logger.info(f"{env.name}创建账户")
                    chrome.wait(2, 3)
                    tab.ele('t:button@text():Create').click()
                    chrome.wait(2, 3)
                    for _ in range(3):
                        if tab.ele('t:button@text():Create'):
                            tab.refresh()
                            chrome.wait(2, 3)
                            tab.ele('t:button@text():Create').click()
                            chrome.wait(1, 2)

                    tab.wait.load_start()
                    tab.ele('@placeholder=Enter invite code').click().input('13VRQ3', clear=True)
                    logger.info(f"{env.name}输入邀请码")
                    chrome.wait(1, 2)
                    tab.ele('t:button@text():Confirm').click()
                    logger.info(f"{env.name}提交邀请码")
                    chrome.wait(3, 6)

            except Exception as e:
                try:
                    tab.ele('@placeholder=Enter invite code').click().input('13VRQ3', clear=True)
                    logger.info(f"{env.name}输入邀请码")
                    chrome.wait(1, 2)
                    tab.ele('t:button@text():Confirm').click()
                    logger.info(f"{env.name}提交邀请码")
                    chrome.wait(3, 6)
                except Exception as e:
                    logger.info(f"{env.name}邀请码已经输入了")

            if tab.ele('t:button@text():Create'):
                chrome.wait(2, 3)
                tab.ele('t:button@text():Create').click()
                logger.info(f"{env.name}创建账户")
                chrome.wait(2, 3)
                for _ in range(3):
                    if tab.ele('t:button@text():Create'):
                        tab.refresh()
                        chrome.wait(2, 3)
                        tab.ele('t:button@text():Create').click()
                        chrome.wait(1, 2)

            if tab.ele('@placeholder=Enter invite code'):
                tab.ele('@placeholder=Enter invite code').click().input('13VRQ3', clear=True)
                logger.info(f"{env.name}输入邀请码")
                chrome.wait(1, 2)
                tab.ele('t:button@text():Confirm').click()
                logger.info(f"{env.name}提交邀请码")


        except Exception as e:
            logger.info(f"{env.name}主页登录失败")
            return

    if tab.ele('t:button@text():Connect Wallet'):
        logger.info(f"{env.name}主页登录成功")
    return

def getDeek(chrome, env):
    tab = chrome.new_tab(url='https://www.deek.network/')
    chrome.wait(2, 4)
    logger.info(f"{env.name}登陆钱包")



    logger.info(f"{env.name}关注deek_network")
    tab.ele('Go').click()
    chrome.wait(10, 15)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()

    chrome.wait(2, 4)
    if tab.ele('t:span@text():Follow'):
        tab.ele('t:span@text():Follow').click()

    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务1")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()


    logger.info(f"{env.name}关注OpenSocialLabs")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=2).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 4)
    if tab.ele('t:span@text():Follow'):
        tab.ele('t:span@text():Follow').click()

    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务2")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()

    logger.info(f"{env.name}关注chiefbigdeek")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=3).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 4)
    if tab.ele('t:span@text():Follow'):
        tab.ele('t:span@text():Follow').click()
    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务3")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()


    logger.info(f"{env.name}关注EVGHQ")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=4).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 4)
    if tab.ele('t:span@text():Follow'):
        tab.ele('t:span@text():Follow').click()
    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务4")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()


    logger.info(f"{env.name}关注SoMon_OwO")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=5).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 4)
    if tab.ele('t:span@text():Follow'):
        tab.ele('t:span@text():Follow').click()
    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务5")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()


    logger.info(f"{env.name}关注breadnbutterxyz")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=6).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 4)
    if tab.ele('t:span@text():Follow'):
        tab.ele('t:span@text():Follow').click()
    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务6")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()


    logger.info(f"{env.name}加入discord")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]',index=7).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://discord.com/').ele("@type=button").click()
    chrome.wait(2, 4)
    chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务7")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()

    logger.info(f"{env.name}日常任务1")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=6).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').wait(3).ele('@data-testid=tweetButton').click()
    chrome.wait(2, 4)
    # chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务8")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()

    logger.info(f"{env.name}日常任务2")
    tab.ele('@class=btn-primary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]', index=6).click()
    tab.wait.ele_displayed(chrome.get_tab(url='https://x.com/').ele("@type=button"), timeout=90)
    chrome.get_tab(3, 6)
    chrome.get_tab(url='https://x.com/').wait(3).ele('@data-testid=tweetButton').click()
    chrome.wait(2, 4)
    # chrome.wait(3, 6)
    logger.info(f"{env.name}开始验证任务9")
    if tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]'):
        tab.ele('@class=btn-secondary-medium self-stretch max-w-[156px] xs:min-w-[216px] md:min-w-[134px] xl:min-w-[118px] 2xl:max-w-[113px]').click()

    chrome.wait(3, 6)
    return



def deek(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getTab(chrome, env)
            # getDeek(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        # finally:
        #     quitChrome(env, chrome)



import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
from flaskServer.utils.chrome import quitChrome

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
from flaskServer.services.chromes.login import tw2faV
from faker import Faker
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
click_wallet_js2 = """
            const button = document.querySelector("body > div.auto-dialog > div > div.auto-dialog__card__container > div.connect-dialog > div:nth-child(2) > div.grid.grid-more > div:nth-child(5)")
            return button
            """

def getTaskon(chrome, env):
    tab = chrome.new_tab(url="chrome-extension://dijnjcfdpimkanlomlbepfcecgebbhcm/popup/index.html")
    chrome.wait(1, 2)
    logger.info(f"关闭机器人验证器")
    tab.ele('@class=MuiSwitch-root MuiSwitch-sizeMedium css-qplqsr').click()
    chrome.wait(1, 2)

    tab = chrome.new_tab(url="https://taskon.xyz/campaign/detail/805263300")

    if tab.ele('t:button@text():Skip'):
        tab.ele('t:button@text():Skip').click()

    if tab.ele('t:div@text():Login'):
        try:
            tab.ele('t:div@text():Login').click()
            chrome.wait(1, 2)
            logger.info(f"选择OKX钱包并登录")
            tab.run_js(click_wallet_js2).click()
            chrome.wait(3, 5)
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            chrome.wait(3, 5)
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            logger.info(f"钱包登录成功")
            chrome.wait(2, 4)
        except Exception as e:
            logger.info(f"钱包已登录")
    else:
        logger.info(f"钱包已登录")

    logger.info(f"浏览网站任务")
    tab.ele('@class=g-fix-outline g-pointer out-link g-clickable link-text').click()
    chrome.wait(4, 7)
    tab.close()
    tab = chrome.new_tab(url="https://taskon.xyz/campaign/detail/805263300")

    logger.info(f"答题")
    tab.ele('Stablecoins').click()
    chrome.wait(1)
    tab.ele('@type=button', index=2).click()

    tab.ele('There are no tradfi people onchain').click()
    chrome.wait(1)
    tab.ele('@type=button', index=3).click()

    tab.ele('Making them open, permissionless, and composable').click()
    chrome.wait(1)
    tab.ele('@type=button', index=4).click()

    tab.ele('RWAfi', index=3).click()
    chrome.wait(1)
    tab.ele('@type=button', index=5).click()

    tab.ele('Parking stables in a solar farm for 20% APY, trading sports or Pokémon cards, speculating on indexes').click()
    chrome.wait(1)
    tab.ele('@type=button', index=6).click()

    tab.ele('Tradfi products onchain don’t serve the needs of crypto natives').click()
    chrome.wait(1)
    tab.ele('@type=button', index=7).click()

    tab.ele('Offering immediate and engaging activities like trading and speculation').click()
    chrome.wait(1)
    tab.ele('@type=button', index=8).click()
    chrome.wait(2, 4)


    logger.info(f"关注plume推特")
    tab.ele('@class=g-fix-outline g-pointer out-link g-clickable inline').click()
    chrome.wait(6, 9)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 3)

    logger.info(f"推特分享朋友")
    chrome.get_tab(title="TaskOn").ele("@text():this tweet").click()
    chrome.wait(6, 9)
    chrome.get_tab(title="Compose new post / X").ele("@data-contents=true").input(' @POTUS @KingSalman @AmiriDiwan ')
    chrome.wait(2, 4)
    chrome.get_tab(url='https://x.com/').wait(3).ele('@data-testid=tweetButton').click()
    chrome.wait(2, 3)

    logger.info(f"关注Taskonxyz推特")
    chrome.get_tab(title="TaskOn").ele("@text():@taskonxyz").click()
    chrome.wait(6, 9)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click()
    chrome.wait(2, 3)

    logger.info(f"关注TaskonCommunity推特")
    chrome.get_tab(url='https://taskon.xyz/').ele("t:div@text():@TaskOnCommunity").click()
    chrome.wait(6, 9)
    chrome.get_tab(url='https://x.com/').ele("@type=button").click().wait(2).tab.close()
    chrome.wait(2, 3)

    if chrome.get_tab(title="TaskOn").ele('t:button@text():Link & Verify All'):
        logger.info(f"验证")
        chrome.get_tab(title="TaskOn").ele('t:button@text():Link & Verify All').click()
        chrome.wait(5, 10)

    if tab.ele('@data-testid=OAuth_Consent_Button'):
        logger.info(f"推特授权")
        tab.ele('@data-testid=OAuth_Consent_Button').click()
        chrome.wait(5, 10)

    logger.info(f"打开机器人验证器")
    chrome.get_tab(url='chrome-extension://dijnjcfdpimkanlomlbepfcecgebbhcm/').ele('@class=MuiSwitch-root MuiSwitch-sizeMedium css-qplqsr').click()
    tab.refresh()
    chrome.wait(60)

    chrome.get_tab(url='https://taskon.xyz/')

    try:
        tab.ele('@type=button', index=9).click()
    except Exception as e:
        tab.ele('@id=detail-operate-footer').click()

    chrome.wait(10, 15)
    if tab.ele('@type=button', index=9):
        tab.ele('@type=button', index=9).click()
        chrome.wait(2, 4)

    if tab.ele('More Rewards Await!'):
        logger.info(f"任务完成")

    if tab.ele('You have not checked recaptcha. Please check recaptcha first'):
        logger.info(f"任务有未完成的，或人机验证失败")

    return


# def toDo(chrome,env):
#     logger.info(f"======开始执行{env.name}环境")
#     getTaskon(chrome, env)
#     time.sleep(5)

# def toDoPlumeTaskAll(env):
#     with app.app_context():
#         try:
#             chrome: ChromiumPage = OKXChrome(env)
#             toDo(chrome, env)
#             logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
#             chrome.quit()
#         except Exception as e:
#             logger.error(f"{env.name}: {e}")
#             if chrome:
#                 chrome.quit()
def taskon(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getTaskon(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)

# if __name__ == '__main__':
#     with app.app_context():
#         # env = Env.query.filter_by(name="SYL-18").first()
#         # toDoPlumeTaskAll(env)
#         submit(toDoPlumeTaskAll, getAllEnvs())



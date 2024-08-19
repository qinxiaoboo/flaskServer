import random
from random_words import RandomWords
# pip install RandomWords
from DrissionPage import ChromiumPage
from loguru import logger
import random
# 连接数据库
from flaskServer.config.connect import app
# 数据库信息
from flaskServer.mode.env import Env
import time
# 配置代理
from flaskServer.mode.proxy import Proxy
# 创建浏览器
from flaskServer.services.chromes.worker import submit
# 变量
from flaskServer.services.content import Content
# 登录环境账号
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.dto.account import getAccountById
from pprint import pprint

silver_click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connector-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """
# 选择okx钱包并确定
click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """

swap_click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-announced-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """

# 点击选择环境
click_plume_js = """
            const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-unsupported-chain-view").shadowRoot.querySelector("wui-flex > wui-flex:nth-child(2) > wui-list-network").shadowRoot.querySelector("button");
            return button;
            """


def GetTab(chrome,env):
    tab = chrome.new_tab(url="https://miles.plumenetwork.xyz/?invite=PLUME-YJHMI")
    tab.ele("@type=button").click()
    tab.ele("@data-testid=connect-wallet-button").click()
    chrome.wait(1, 2)
    try:
        okxbutton = tab.run_js(click_wallet_js)
        logger.info(f"{env.name}: 链接钱包")
        okxbutton.click.for_new_tab().ele("@type=button").next().click()
        logger.info(f"{env.name}: 确认钱包")
        tab.ele("@data-testid=sign-message-button").click.for_new_tab().ele("@type=button").next().click()
        chrome.wait(1,2)
        tab.run_js(click_plume_js).click()
    except Exception as e:
        logger.warning(f"{env.name}: {e}")
        logger.info(f"{env.name}: 确认钱包")
        tab.ele("@data-testid=sign-message-button").click.for_new_tab().ele("@type=button").next().click()
        try:
            chrome.wait(1, 2)
            tab.run_js(click_plume_js).click()
        except Exception as e:
            logger.warning(f"{env.name}: {e}")
            logger.info(f"{env.name}: 处理弹窗")
            chrome.wait(1)
            try:
                tab.run_js(click_wallet_js).click()
            except Exception as e:
                logger.info(f"{env.name}: 进入plume页面")

    chrome.wait(2)
    logger.info(f"{env.name}: 统计公里数")
    tab.ele('@class=chakra-button css-1mlwjgz').click(by_js=None)
    miles = tab.s_ele('@class=chakra-text css-1c1e297')

    logger.info(f"{env.name}: 统计护照数量（已完成任务数量）")
    tab.ele('@data-testid=passport-nav-link').click(by_js=None)
    passport_list = tab.eles('@class=StyledIconBase-sc-ea9ulj-0 sRDPe chakra-icon css-k8603g')

    logger.info(f"{env.name}: 当前环境check_in积分倍数")
    tab.set.load_mode.normal()
    tab.get(url='https://miles.plumenetwork.xyz/daily-checkin')
    chrome.wait(4)
    multiplier = tab.ele('@class=chakra-text css-1l3wnnl', index=2).text

    env_name = env.name
    miles_raw_text = miles.raw_text
    passport_list = len(passport_list)
    miles_multiplier = multiplier

    with open('miles.txt', 'a') as file:
        file.write(f"{env_name}    {miles_raw_text}    {passport_list}      {miles_multiplier}\n")

    return



def toDo(chrome,env):
    logger.info(f"======开始执行{env.name}环境")
    chrome: ChromiumPage = OKXChrome(env)
    GetTab(chrome,env)
    time.sleep(5)


def toDoCount(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            toDo(chrome,env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
            chrome.quit()
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            if chrome:
                chrome.quit()




if __name__ == '__main__':
    # toDoFaucet("ETH")
    with app.app_context():
        for i in range(1, 11):
            env_name = f"SYL-{i}"
            env = Env.query.filter_by(name=env_name).first()
            toDo(env)









import random

from DrissionPage import ChromiumPage
from flaskServer.config.connect import db,app
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.task_record import TaskRecord
from flaskServer.services.chromes.login import InitChromeOptionByConf,LoginTW,AuthTW, ConfirmOKXWallet
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.task_record import updateTaskRecord
from flaskServer.services.content import Content
from sqlalchemy import and_
from loguru import logger

# 任务名称
name = "plume_network"
swap_url = "https://plume.ambient.finance/swap/chain=0x99c0a0f&tokenA=0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3&tokenB=0xba22114ec75f0d55c34a5e5a3cf384484ad9e733"
fauct_url = "https://faucet.plumenetwork.xyz/"
# 点击钱包shawdown页面
click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """
# 点击选择环境
click_plume_js = """
            const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-unsupported-chain-view").shadowRoot.querySelector("wui-flex > wui-flex:nth-child(2) > wui-list-network").shadowRoot.querySelector("button");
            return button;
            """
def getTab(chrome,env):
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
    return tab
def getFaucetTab(chrome,env):
    tab = chrome.new_tab(url=fauct_url)
    s_ele = tab.s_ele("@@type=button@@data-testid=rk-connect-button")
    if s_ele:
        tab.ele("@@type=button@@data-testid=rk-connect-button").click()
        tab.ele("@@data-testid=rk-wallet-option-com.okex.wallet").click.for_new_tab().ele("@type=button").next().click()
    return tab


def getFaucet(chrome,env,type):
    tab = getFaucetTab(chrome,env)
    chrome.wait(1,2)
    if type=="GOON":
        tab.ele("@data-testid=goon-radio-card").click()
    chrome.wait(2,3)
    try:
        tab.ele("@data-testid=get-tokens-button").click()
        chrome.wait(5,6)
        text = tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2").text
        if "Whoosh! Slow down!" in text:
            logger.info(env.name + f": {text}")
            return
        ele = chrome.get_tab(title=Content.OKX_TITLE).ele("@type=button").next()
        if (ele.text == "Claim via faucet"):
            logger.info(f"{env.name}:{type}不足无法领取测试币")
        else:
            text = tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2").text
            if "Working on it" in text:
                logger.info(f" {env.name}: 正在领取{type}测试币, {text}")
                chrome.wait(3)
                ele.click()
                chrome.wait(3)
                text = tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2").text
                if "Mission accomplished" in text:
                    logger.info(env.name + f": 领取{type}测试币成功")
            elif "Whoosh! Slow down!" in text:
                logger.info( env.name + f": {text}")
    except Exception as e:
        logger.error(f"{env.name}: 该IP已经领取过测试币,{e}")


def worker(env,type):
    logger.info(f"======开始执行{env.name}环境")
    chrome: ChromiumPage = InitChromeOptionByConf(env)
    try:
        getFaucet(chrome, env, type)
    except Exception as e:
        logger.error(f"{env.name} 执行异常：{e}")
    finally:
        chrome.quit()

def toDoFaucet(type):
    num = random.choice([i for i in range(5)])
    with app.app_context():
        proxys = Proxy.query.all()
        envs = []
        envs.append(Env.query.filter_by(name="Q-0").first())
        for proxy in proxys:
            env = Env.query.filter_by(t_proxy_id=proxy.id).all()[num]
            envs.append(env)
        submit(worker, envs, type)


def toDo(env):
    with app.app_context():
        logger.info(f"======开始执行{env.name}环境")
        chrome: ChromiumPage = InitChromeOptionByConf(env)
        try:
            tab = getFaucet(chrome,env,"ETH")
            # tab.get("https://faucet.plumenetwork.xyz/")

        except Exception as e:
            logger.error(f"{env.name} 执行异常：{e}")

if __name__ == '__main__':
    toDoFaucet("ETH")
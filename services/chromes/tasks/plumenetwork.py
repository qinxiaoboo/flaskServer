from DrissionPage import ChromiumPage
from loguru import logger

from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.content import Content
from flaskServer.services.dto.env import getChoiceEnvs

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
    tab.ele("@class=hidden rounded-lg bg-gray-100 px-3 py-2 font-lufga sm:block").click()
    s_ele = tab.s_ele("@@type=button@@data-testid=rk-connect-button")
    if s_ele:
        tab.ele("@@type=button@@data-testid=rk-connect-button").click()
        tab.ele("OKX Wallet").click.for_new_tab().ele("@type=button").next().click()
    return tab

######   消息积压替换   ######
def Replace(chrome):
    okx_wallet = chrome.get_tab(title=Content.OKX_TITLE)
    if okx_wallet:
        if okx_wallet.s_ele("@type=button"):
            okx_wallet.ele("@type=button").next().click()
            chrome.wait(1,2)
            if okx_wallet.s_ele("@class=okui-dialog-container"):
                okx_wallet.ele('@data-testid=okd-dialog-confirm-btn').click()
                okx_wallet.wait(1,2)
                okx_wallet.ele('@data-testid=okd-dialog-confirm-btn').click()
                chrome.wait(1,2)
            Replace(chrome)

def getFaucet(chrome,env,type):
    tab = getFaucetTab(chrome,env)
    chrome.wait(1,2)
    if type=="GOON":
        tab.ele("@data-testid=goon-radio-card").click()
    chrome.wait(2,3)
    tab.ele("@data-testid=get-tokens-button").click()
    chrome.wait(7,8)


    if tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2"):
        text = tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2").text
        if "Whoosh! Slow down!" in text:
            logger.info(env.name + f": {text}")
            return

    var = 1
    while var == 1:
        print("进入循环")
        if chrome.get_tab(title="OKX Wallet").ele("t:div@tx():confirmations"):
            print('识别到消息积压')
            if chrome.get_tab(title="OKX Wallet").ele("@text=Third-party"):
                chrome.get_tab(title="OKX Wallet").ele("@type=button", index=1).click()
                print('签名')
                chrome.wait(2)
            else:
                chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
                print('确认签名')
                chrome.wait(2)
        else:
            var = 0
            print('积压消息处理完毕，推出循环')
    if chrome.get_tab(title="OKX Wallet").ele("@text=Third-party"):
        chrome.get_tab(title="OKX Wallet").ele("@data-testid=okd-button", index=1).click()
        chrome.wait(2)
    else:
        chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()

    try:
        ele = chrome.get_tab(title=Content.OKX_TITLE).ele("@type=button").next()
        if (ele.text == "Fill up PlumeTest_ETH"):
            logger.info(f"{env.name}:{type}不足无法领取测试币")
        else:
            # Replace(chrome)
            text = tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2").text
            if "Working on it" in text:
                logger.info(f" {env.name}: 正在领取{type}测试币, {text}")
                chrome.wait(3)
                ele.click()
                Replace(chrome)
                chrome.wait(3)
                text = tab.s_ele("@class=flex w-[300px] flex-col justify-center py-2").text
                if "Mission accomplished" in text:
                    logger.info(env.name + f": 领取{type}测试币成功")
            elif "Whoosh! Slow down!" in text:
                logger.info( env.name + f": {text}")
    except AttributeError as e:
        logger.info(f" {env.name}: 由于消息积压严重，本次领水动作处理历史消息")

def worker(env,type):
    logger.info(f"======开始执行{env.name}环境")
    chrome=None
    try:
        chrome = OKXChrome(env)
        getFaucet(chrome, env, type)
    except Exception as e:
        logger.error(f"{env.name} 执行异常：{e}")
    finally:
        if chrome:
            chrome.quit()

def toDoFaucet(type):
    submit(worker, getChoiceEnvs(), type)


def toDo(env):
    with app.app_context():
        logger.info(f"======开始执行{env.name}环境")
        try:
            chrome: ChromiumPage = OKXChrome(env)
            tab = getFaucet(chrome,env,"ETH")
            # tab = getTab(chrome,env)
            # if tab:
            #     tab.get("https://miles.plumenetwork.xyz/daily-checkin")

        except Exception as e:
            logger.error(f"{env.name} 执行异常：{e}")
            raise e

if __name__ == '__main__':
    # toDoFaucet("GOON")
    with app.app_context():
        env = Env.query.filter_by(name="zll-1").first()
        toDo(env)
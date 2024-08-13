import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage
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

from pprint import pprint

# 任务名称
name = "Plume Swap"
swap_url = "https://plume.ambient.finance/swap/chain=0x99c0a0f&tokenA=0xba22114ec75f0d55c34a5e5a3cf384484ad9e733&tokenB=0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3"
stake_url = "https://miles.plumenetwork.xyz/nest-staking"
arc_url = "https://miles.plumenetwork.xyz/plume-arc"
cultured_url = "https://miles.plumenetwork.xyz/cultured?tab=crypto"
landshare_url = "https://landshare-plume-sandbox.web.app/"
solidviolet_url = "https://app.solidviolet.com/tokens"


#选择okx钱包并确定
click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """
# 点击选择环境
click_plume_js = """
            const button = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-unsupported-chain-view").shadowRoot.querySelector("wui-flex > wui-flex:nth-child(2) > wui-list-network").shadowRoot.querySelector("button");
            return button;
            """

######   登录主页   ######
def getTab(chrome,env):
    tab = chrome.new_tab(url="https://miles.plumenetwork.xyz/?invite=PLUME-YJHMI")
    tab.ele("@type=button").click()
    for i in range(3):
        if tab.ele("@data-testid=sign-message-button"):
            tab.ele("@data-testid=sign-message-button").click.for_new_tab().ele("@type=button").next().click()
            if tab.ele("@text-sm font-semibold leading-5 text-red-500"):
                tab.refresh()
            else:
                chrome.wait(1, 2)
                break
    else:
        tab.ele("@data-testid=connect-wallet-button").click()
        chrome.wait(1, 2)
        try:
            okxbutton = tab.run_js(click_wallet_js)
            logger.info(f"{env.name}: 链接钱包")
            okxbutton.click.for_new_tab().ele("@type=button").next().click()
            logger.info(f"{env.name}: 确认钱包")
            for i in range(3):
                if tab.ele("@data-testid=sign-message-button"):
                    tab.ele("@data-testid=sign-message-button").click.for_new_tab().ele("@type=button").next().click()
                    if tab.ele("@text-sm font-semibold leading-5 text-red-500"):
                        tab.refresh()
                    else:
                        chrome.wait(1, 2)
                        break
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


def Num(num):
    InputNum = 0
    try:
        if 0.2 < float(num) < 1000:
            InputNum = num - 0.1

        elif float(num) > 1000:
            InputNum = random.randint(600, 900)

        elif float(num) < 0.2:
            InputNum = 0
            print("Goon数量不足请先领取测试币！")
        else:
            InputNum = 0
    except ValueError as e:
        print("Goon不足开始执行下一个任务")
        time.sleep(5)
        InputNum = 0

    return InputNum

######   Swap   ######
def getSwapTab(chrome,env):
    # 访问Swap页面
    tab = chrome.new_tab(url=swap_url)
    if tab.ele('.Header__TitleGradientButton-sc-r62nyn-21 iKuScZ'):
        print("已登录，无需重复登录")
    else:
        #连接钱包
        tab.ele('#connect_wallet_button_page_header').click()
        chrome.wait(1,2)
        if tab.ele('#agree_button_ToS'):
            tab.ele('#agree_button_ToS').click()
            chrome.wait(1, 2)
        okxbutton = tab.run_js(click_wallet_js)
        okxbutton.click.for_new_tab().ele("@type=button").next().click()
    GoonNum = tab.ele('.Container__FlexContainer-sc-1b686b3-0 eveHGW').text
    print(GoonNum)
    InputNum = Num(GoonNum)
    if InputNum == 0:
        print("Goon不足开始执行下一个任务")
        chrome.wait(5,10)
        exit()
    tab.ele('.TradeModules__TokenQuantityInput-sc-7vr3o3-14 iZdQxV').input(InputNum).ele('#confirm_swap_button').click()

######   Stake   ######
def getStake(chrome,env):
    tab = getTab(chrome,env)
    chrome.wait(2,4)
    tab.get(stake_url)
    chrome.wait(3, 5)
    #stake
    balance = tab.ele("t:p@tx():Current balance").text.split( )[2].replace(',','')
    tab.ele('@inputmode=decimal').input(Num(balance))
    if tab.ele('@class=chakra-text css-v50kqq'):
        logger.info(f"{env.name}: 以达到质押上限")
    else:
        try:
            tab.ele('@class=chakra-button css-4pz8ga').click.for_new_tab().ele("@type=button").next().click.for_new_tab().ele("@type=button").next().click()
        except RuntimeError as e:
            logger.info(f"{env.name}: 已授权")

    #claim
    tab.ele('@class=chakra-tabs__tab css-356ze8').next().click()
    nest_num = tab.ele('@class=chakra-text css-1a36ura').text.split( )[0].split('+')[1].replace(',','')

    if nest_num == "0":
        logger.info(f"{env.name}: 今日已领取，请明天再来~")
    else:
        tab.ele('@class=chakra-button css-1v2g7ym').click.for_new_tab().ele("@type=button").next()
        logger.info(f"{env.name}: 质押奖励领取成功！")

######   Arc   ######
def getArc(chrome,env):
    tab = getTab(chrome,env)
    chrome.wait(2,4)
    tab.get(arc_url)
    chrome.wait(3, 5)
    words = RandomWords()
    tab.ele('@class=chakra-input css-dyqcnv').input(words.random_words(count=2))
    for i in words.random_words(count=5):
        tab.ele('@class=chakra-textarea css-1oltc4j').input(i+' ')
    tab.ele('@class=chakra-button css-1mfhrp3').click.for_new_tab().ele("@type=button").next().click()

######   cultured   ######
def getCultured(chrome,env):
    tab = getTab(chrome,env)
    chrome.wait(2,4)
    tab.get(cultured_url)
    chrome.wait(3, 5)
    if tab.ele('@class=chakra-text css-jneyc'):
        print("你已经押注过啦~ 请明天再来")
    else:
        tab.ele('@class=chakra-button css-1pj5uk4').click.for_new_tab().wait(3,5).ele("@type=button").next().click()

######   Landshare   ######
def getLandshare(chrome,env):
    ####   网站卡顿，手动交互不成功。
    tab = getTab(chrome,env)
    chrome.wait(2,4)
    tab.get(landshare_url)
    chrome.wait(3, 5)
    tab.ele('@class=button-container w-full md:w-auto   ').click()
    tab.ele('@data-testid=rk-wallet-option-okx').click.for_new_tab().ele("@type=button").next().click()
    tab.ele('@class=bg-[#61cd81] text-white py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full sm:w-auto ').click.for_new_tab().wait(3,5).ele("@type=button").next().click()

######   Solidviolet   ######
def getSolidviolet(chrome,env):
    tab = getTab(chrome,env)
    chrome.wait(2,4)
    tab.get(solidviolet_url)
    chrome.wait(3, 5)
    #if tab.ele('@class=chakra-modal__header css-1cr2mq4'):

    tab.ele('@class=chakra-button css-vo669l').click()
    chrome.wait(3, 5)
    if tab.ele('@class=chakra-modal__header css-1cr2mq4'):
        chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
    else:
        tab.ele('@data-testid=rk-wallet-option-com.okex.wallet').click.for_new_tab().ele("@type=button").next().click()
        chrome.wait(3, 5)
        chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()

    if tab.ele('@placeholder=Email'):
        tab.ele('@placeholder=Email').input(env.outlook_id)
        tab.ele('@type=submit').click()
    tab.ele('@class=chakra-stack css-w0oinc').click()
    chrome.wait(3, 5)
    tab.ele('@class=chakra-input css-qybfmf').input(1)
    tab.ele('@class=chakra-button css-4i7hvg').click()
    chrome.wait(3, 5)
    chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()









def toDo(env):
    with app.app_context():
        logger.info(f"======开始执行{env.name}环境")
        try:
            chrome: ChromiumPage = OKXChrome(env)
            tab = getSolidviolet(chrome,env)
        except Exception as e:
            logger.error(f"{env.name} 执行异常：{e}")
            raise e

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="SYL-15").first()
        toDo(env)



























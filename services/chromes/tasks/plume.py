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
from flaskServer.services.chromes.login import tw2faV
from faker import Faker
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup


# 任务名称
name = "Plume"

# 任务链接
swap_url = "https://plume.ambient.finance/swap/chain=0x99c0a0f&tokenA=0xba22114ec75f0d55c34a5e5a3cf384484ad9e733&tokenB=0x5c1409a46cd113b3a667db6df0a8d7be37ed3bb3"
stake_url = "https://miles.plumenetwork.xyz/nest-staking"
arc_url = "https://miles.plumenetwork.xyz/plume-arc"
cultured_url = "https://miles.plumenetwork.xyz/cultured?tab=crypto"
landshare_url = "https://landshare-plume-sandbox.web.app/"
solidviolet_url = "https://app.solidviolet.com/tokens"
kuma_url = "https://plume.kuma.bond/"
silverkoi_url = "https://app-alpha.silverkoi.io/trade/ETHUSD"
okxwallet_url = "chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html"


silver_click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connector-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """

#选择okx钱包并确定
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


######   调整数量   ######
def Num(num):
    InputNum = 0
    try:
        num = float(num)
        num = int(num)
        if 1 < num < 10:
            InputNum = num - 1
        elif 100 < num:
            InputNum = random.randint(60, 90)
        elif 2 > num:
            InputNum = num - 0
        else:
            InputNum = 0
    except ValueError as e:
        time.sleep(5)
        InputNum = 0
    return InputNum

######   修改gas   ######
def GasChange(chrome):
    okx_wallet = chrome.get_tab(title="OKX Wallet")
    #调整Gas
    try:
        chrome.wait(3, 4)
        chrome.get_tab(title="OKX Wallet").ele('@class=_module-wrap-hover_m5ibg_13').click()
        chrome.wait(1, 2)
        chrome.get_tab(title="OKX Wallet").ele('@class=network-fee-custom').click()
        chrome.wait(1, 2)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-input', index=1).input("2.42",clear=True)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-input', index=2).input("2.76",clear=True)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-input', index=3).input("8000000",clear=True)
        chrome.wait(1, 2)
        chrome.get_tab(title="OKX Wallet").ele("@class=okui-btn btn-lg btn-fill-highlight block mobile network-fee-custom__confirm").click()
        chrome.wait(3, 5)
        return 1
    except AttributeError as e:
        return 0

######   消息积压替换   ######
def Replace(chrome):
    okx_wallet = chrome.get_tab(title="OKX Wallet")
    chrome.wait(3, 4)
    try:
        if chrome.get_tab(title="OKX Wallet").ele("@class=okui-dialog-container"):
            # 点击Replace
            chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-dialog-confirm-btn').click()
            chrome.wait(1, 2)
            # 点击Confirm
            chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-dialog-confirm-btn').click()
    except AttributeError as e:
        pass
    return

######   处理钱包签名   ######
def exe_okx(chrome):
    try:
        GasChange(chrome)
        if chrome.get_tab(title="OKX Wallet").ele("@type=button", index=3):
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=3).click()
            Replace(chrome)
            chrome.wait(20, 25)
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            chrome.wait(2,3)
            return
        else:
            chrome.wait(2, 3)
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            chrome.wait(4, 5)
            Replace(chrome)
            return
    except AttributeError as e:
        pass
    return

######   登录主页   ######
def getTab(chrome,env):
    logger.info(f"{env.name}: 开始登陆主页")
    tab = chrome.new_tab(url="https://miles.plumenetwork.xyz/?invite=PLUME-YJHMI")
    try:
        if tab.ele("@type=button"):
            tab.ele("@type=button").click(by_js=None)
    except Exception as e:
        logger.info(f"{env.name}: 代理网络不佳，页面访问失败，关闭浏览器")
        chrome.quit()
    chrome.wait(3, 5)
    for i in range(3):
        if tab.s_ele("@data-testid=sign-message-button"):
            tab.ele("@data-testid=sign-message-button").click()
            chrome.wait(5, 10)
            chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
            chrome.wait(3, 5)

        if tab.ele("@text-sm font-semibold leading-5 text-red-500"):
            tab.refresh()

        chrome.wait(3, 6)
        if tab.ele('@class=chakra-button css-17q6q3f'):
            tab.ele('@class=chakra-button css-17q6q3f').click()
            chrome.wait(2, 3)
            tab.back(1)

        else:
            chrome.wait(1, 2)
            break

    if tab.ele('t:button@tx():Enter App'):
        logger.info(f"{env.name}: 主页登录完成")
    else:
        tab.ele("@data-testid=connect-wallet-button").click(by_js=None)
        chrome.wait(1, 2)
        try:
            okxbutton = tab.run_js(click_wallet_js)
            logger.info(f"{env.name}: 链接钱包")
            chrome.wait(3, 5)
            okxbutton.click.for_new_tab().ele("@type=button").next().click()
            logger.info(f"{env.name}: 确认钱包")
            for i in range(3):
                if tab.ele("@data-testid=sign-message-button"):
                    chrome.wait(3,5)
                    tab.ele("@data-testid=sign-message-button").click.for_new_tab(4, 6).ele("@type=button").next().click()
                    if tab.ele("@text-sm font-semibold leading-5 text-red-500"):
                        tab.refresh()
                    else:
                        chrome.wait(1, 2)
                        break
            chrome.wait(1, 2)
            tab.run_js(click_plume_js).click()
            chrome.wait(1, 2)
        except Exception as e:
            logger.warning(f"{env.name}: {e}")
            logger.info(f"{env.name}: 确认钱包")
            chrome.wait(3, 4)
            tab.ele("@data-testid=sign-message-button").click.for_new_tab().wait(4, 6).ele("@type=button").next().click()
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

######   数据统计   ######
def getCount(chrome, env):
    try:
        tab = chrome.new_tab(url="https://miles.plumenetwork.xyz/")
        chrome.wait(4)
        tab.ele('@class=chakra-button css-1mlwjgz').click(by_js=None)
        miles = tab.s_ele('@class=chakra-text css-1c1e297')
        tab.ele('@data-testid=passport-nav-link').click(by_js=None)
        passport_list = tab.eles('@class=StyledIconBase-sc-ea9ulj-0 sRDPe chakra-icon css-k8603g')
        tab.set.load_mode.normal()
        tab.get(url='https://miles.plumenetwork.xyz/daily-checkin')
        chrome.wait(2)
        if tab.ele('text=Switch Network'):
            chrome.wait(4)
            tab.ele('text=Switch Network', index=1).click(by_js=True)
        chrome.wait(4)
        multiplier = tab.ele('@class=chakra-text css-1l3wnnl', index=2).text
        env_name = env.name
        miles_raw_text = miles.raw_text
        passport_list = len(passport_list)
        miles_multiplier = multiplier
        with open('miles.txt', 'a') as file:
            file.write(f"{env_name}          {miles_raw_text}        {passport_list}         {miles_multiplier}\n")
    except Exception as e:
        logger.info(f"{env.name}: 网络异常，统计失败")
    return

######   Swap   ######
def getSwapTab(chrome,env):
    # 访问Swap页面
    logger.info(f"{env.name}: 开始执行Swap")
    tab = chrome.new_tab(url=swap_url)
    try:
        if tab.ele('.Header__TitleGradientButton-sc-r62nyn-21 iKuScZ'):
            logger.info(f"{env.name}: Swap页面登录完成")
        else:
            #连接钱包
            try:
                tab.ele('#connect_wallet_button_page_header').click()
                chrome.wait(3, 4)
            except Exception as e:
                logger.info(f"{env.name}: 代理网络不佳，页面访问失败，关闭当前Tab执行下一项任务")
                tab.close_tabs()
                return
            if tab.ele('#agree_button_ToS'):
                tab.ele('#agree_button_ToS').click()
                chrome.wait(3, 4)
            okxbutton = tab.run_js(swap_click_wallet_js)
            okxbutton.click.for_new_tab().ele("@type=button").next().click()


        chrome.wait(3, 6)
        GoonNum = tab.ele('.Container__FlexContainer-sc-1b686b3-0 eveHGW', index=1).text
        InputNum = Num(GoonNum)

        if InputNum == 0:
            logger.info(f"{env.name}: Goon不足开始执行下一个任务")
            chrome.wait(5, 10)
            tab.close()
            return

        tab.ele('.TradeModules__TokenQuantityInput-sc-7vr3o3-14 iZdQxV', index=1).input(InputNum, clear=True)
        chrome.wait(3, 5)
        tab.ele('#confirm_swap_button').click()
        chrome.wait(3, 5)
        tab.ele('@id=set_skip_confirmation_button').click()
        chrome.wait(6, 8)
        # chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        var = 1
        while var == 1:

            if chrome.get_tab(title="OKX Wallet").ele("t:div@tx():confirmations"):
                logger.info(f"{env.name}: 开始处理钱包消息累积")
                if chrome.get_tab(title="OKX Wallet").ele("t:div@tx():Third-party"):
                    chrome.get_tab(title="OKX Wallet").ele("@type=button", index=1).click()
                    chrome.wait(2)
                else:
                    chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
                    chrome.wait(2)
            else:
                var = 0

        if chrome.get_tab(title="OKX Wallet").ele("t:div@tx():Third-party"):
            chrome.get_tab(title="OKX Wallet").ele("@data-testid=okd-button", index=1).click()
            chrome.wait(2)
        else:
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()

        chrome.wait(10)
        logger.info(f"{env.name}: Swap成功")

    except (RuntimeError,AttributeError) as e:
        pass
    # tab.close()
    return

######   Stake   ######
def getStake(chrome,env):
    logger.info(f"{env.name}: 开始执行Stake")
    tab = chrome.new_tab(url=stake_url)
    chrome.wait(3, 5)
    try:
        #stake
        balance = tab.ele("t:p@tx():Current balance").text.split()[2].replace(',', '')
        tab.ele('@inputmode=decimal').input(Num(int(float(balance))), clear=True)

        if tab.ele('@class=chakra-text css-v50kqq'):
            logger.info(f"{env.name}: 以达到质押上限")
        else:
            try:
                tab.ele('@class=chakra-button css-4pz8ga').click()
                try:
                    exe_okx(chrome)
                except AttributeError as e:
                    logger.info(f"{env.name}: 网络卡顿，钱包签名失败")
            except RuntimeError as e:
                logger.info(f"{env.name}: 已授权")
        #claim
        tab.ele('@class=chakra-tabs__tab css-356ze8').next().click()
        nest_num = tab.ele('@class=chakra-text css-1a36ura',index=3).text.split( )[0].split('+')[1].replace(',','')
        chrome.wait(3, 5)

        if nest_num == "0":
            logger.info(f"{env.name}: 今日已领取，请明天再来~")
        elif int(nest_num) < 101:
            logger.info(f"{env.name}: 奖励公里数大于100才能领取")
        else:
            #tab.ele('@class=chakra-button css-1v2g7ym').click.for_new_tab().ele("@type=button").next().click()
            tab.ele('@class=chakra-button css-1v2g7ym').click()
            exe_okx(chrome)
            chrome.wait(5, 7)
            logger.info(f"{env.name}: 质押奖励领取成功！")
        chrome.wait(3, 5)
    except (RuntimeError,AttributeError) as e:
        pass
    tab.close()

######   Arc   ######
def getArc(chrome,env):
    logger.info(f"{env.name}: 开始执行Arc")
    tab = chrome.new_tab(url=arc_url)
    chrome.wait(3, 5)
    words = RandomWords()
    try:
        tab.ele('@class=chakra-input css-dyqcnv').input(words.random_words(count=2))
        for i in words.random_words(count=5):
            tab.ele('@class=chakra-textarea css-1oltc4j').input(i+' ')
        chrome.wait(3, 5)
        tab.ele('@class=chakra-button css-1mfhrp3').click()
        chrome.wait(3, 5)
        #chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
        exe_okx(chrome)
        chrome.wait(5, 7)
        logger.info(f"{env.name}: Arc执行完成")
        tab.close()
    except (RuntimeError, AttributeError) as e:
        tab.close()

######   Cultured   ######
def getCultured(chrome,env):
    logger.info(f"{env.name}: 开始执行Cultured")
    tab = chrome.new_tab(url=cultured_url)
    chrome.wait(3, 5)
    try:
        if tab.ele('@class=chakra-text css-102t632'):
            logger.info(f"{env.name}: 你已经押注过啦~ 请明天再来")
        else:
            tab.ele('@class=chakra-button css-1pj5uk4').click()
            chrome.wait(5, 7)
            try:
                # chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
                exe_okx(chrome)
            except AttributeError as e:
                pass
            chrome.wait(3, 5)
        tab.close()
    except (RuntimeError,AttributeError) as e:
        tab.close()

######   Landshare   ######
# def getLandshare(chrome,env):
#     logger.info(f"{env.name}: 开始执行Landshare")
#     ####   网站卡顿，手动交互不成功。
#     tab = chrome.new_tab(url=landshare_url)
#     chrome.wait(3, 5)
#     tab.ele('@class=button-container w-full md:w-auto').click()
#     # tab.ele('@data-testid=rk-wallet-option-okx').click.for_new_tab().ele("@type=button").next().click()
#     tab.ele('@data-testid=rk-wallet-option-okx').click()
#     exe_okx(chrome)
#     # tab.ele('@class=bg-[#61cd81] text-white py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full sm:w-auto ').click.for_new_tab().wait(3,5).ele("@type=button").next().click()
#     tab.ele('@class=bg-[#61cd81] text-white py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full sm:w-auto').click()
#     exe_okx(chrome)

######   Solidviolet   ######

def getSolidviolet(chrome,env):
    logger.info(f"{env.name}: 开始执行Solidviolet")
    tab = chrome.new_tab(url=solidviolet_url)
    chrome.wait(3, 5)
    try:
        tab.ele('@class=chakra-button css-vo669l').click()
        chrome.wait(3, 5)
        if tab.ele('@class=chakra-modal__header css-1cr2mq4'):
            chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
        else:
            tab.ele('@data-testid=rk-wallet-option-com.okex.wallet').click()
            chrome.wait(3, 5)
            chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
            chrome.wait(3, 5)
            chrome.get_tab(title="OKX Wallet").ele("@type=button").next().click()
        if tab.ele('@placeholder=Email'):
            tab.ele('@placeholder=Email').input(getAccountById(env.outlook_id).name)
            tab.ele('@type=submit').click()
            chrome.wait(1, 2)
        tab.ele('@class=chakra-stack css-w0oinc').click()
        chrome.wait(2, 3)
        tab.ele('@class=chakra-input css-qybfmf').input(1)
        tab.ele('@class=chakra-button css-4i7hvg').click()
        chrome.wait(5, 8)
        #chrome.get_tab(title="OKX Wallet").ele('@class=okui-btn btn-lg btn-fill-highlight mobile _action-button_j3bvq_1').click()
        exe_okx(chrome)
        chrome.wait(45, 50)
        try:
            #chrome.get_tab(url='chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html').ele('@class=okui-btn btn-lg btn-fill-highlight mobile _action-button_j3bvq_1').click()
            exe_okx(chrome)
            chrome.wait(3, 5)

            exe_result = tab.ele('@class=chakra-heading css-1nagzmw').text
            if exe_result == "Order Successfully Completed":
                logger.info(f"{env.name}: Solidviolet 任务执行完成")
            else:
                logger.info(f"{env.name}: Solidviolet 任务执行失败")
        except Exception as e:
            logger.info(f"{env.name}: Solidviolet 网络延迟太大，执行失败")
        tab.close()
    except (RuntimeError,AttributeError) as e:
        tab.close()

######   kuma   ######
def getKuma(chrome,env):
    logger.info(f"{env.name}: 开始执行Kuma")
    tab = chrome.new_tab(url=kuma_url)
    chrome.wait(5, 7)
    try:
        if tab.ele('t:p@tx():Connect'):
            tab.ele('t:p@tx():Connect').click()
            chrome.wait(3,5)
            if tab.ele('@class=mb-4 text-white'):
                tab.ele('@role=switch').click()
                tab.ele('t:button@tx():Next').click()
            else:
                # 点击连接钱包
                tab.ele('@class=flex items-center rounded-lg p-2 text-xs font-bold hover:bg-[#787880]/20').click()
            # 点击选择okx钱包
            chrome.wait(5, 7)
            tab.ele('@data-testid=rk-wallet-option-metaMask').click.for_new_tab().ele("@type=button").next().click()
            chrome.wait(2, 3)
        logger.info(f"{env.name}: 网页登录成功")
        tab.ele('t:button@tx():MINT AICK').click.for_new_tab().wait(5,8).ele("@type=button").next().click()
        chrome.wait(12, 16)
        tab.ele('t:button@tx():Sell NFTs').click()
        chrome.wait(7, 9)
        nft = tab.ele('@class=flex h-[22rem] w-full transform flex-col overflow-hidden rounded-[12px] bg-[#23252c] duration-200  border border-2px border-transparent bg-clip-padding')

        if nft:
            nft.click()
            chrome.wait(2)
            tab.ele('t:button@tx():APPROVE KUMA NFT').click()
            chrome.wait(7, 10)
            chrome.get_tab(url='chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/notification.html').ele("@type=button",index=3).click()
            chrome.wait(50, 60)
        else:
            logger.info(f"{env.name}: 当前没有NFT可供出售")

        if tab.ele('t:button@tx():SELL KUMA NFT'):
                tab.ele('t:button@tx():SELL KUMA NFT').click()
                chrome.wait(2, 4)
                chrome.get_tab(title="OKX Wallet").ele("@type=button",index=2).click()
                chrome.wait(15, 20)
                exe_result = tab.ele('t:div@tx():Confirmed').text
                if exe_result == "Confirmed":
                    logger.info(f"{env.name}: Kuma 任务执行完成")
        else:
            logger.info(f"{env.name}: ERROR Kuma钱包签名出现网络连接失败")

    except (RuntimeError,AttributeError) as e:
        logger.info(f"{env.name}: Kuma 网络延迟太大，执行失败")
    tab.close()

######   silverkoi   ######
def getSilverkoi(chrome,env):
    logger.info(f"{env.name}: 开始执行Silverkoi")
    tab = chrome.new_tab(url=silverkoi_url)
    chrome.wait(7, 10)
    try:
        # 登录钱包
        if tab.ele('@@class=tracking-[-0.01em] leading-[1.25em] text-[0.75rem] font-bold@@tx():Connect Wallet'):
            tab.ele('t:button',index=2).click()
            okxbutton = tab.run_js(silver_click_wallet_js)
            okxbutton.click.for_new_tab().ele("@type=button",index=2).click()
        try:
            tab.ele('t:button@tx():50x').click()
            chrome.wait(3, 5)
        except Exception as e:
            tab.close()
            return

        # 输入开单数量
        tab.ele('@class=inline-block items-center justify-center rounded-md border border-blue bg-black px-3 text-white tracking-[-0.01em] leading-[1.25em] text-[0.75rem] font-medium box-border w-full h-[1.75rem] focus:outline-none').input(random.randint(1005,1200))
        chrome.wait(7, 10)
        button = tab.ele('@class=shrink-0 w-full h-[2rem] items-center justify-center background-gradient-bright rounded-xl border-none tracking-[-0.01em] leading-[1.25em] text-[0.75rem] font-bold text-neutral-01 flex shrink-0 items-center justify-center align-middle hover:cursor-pointer hover:disabled:cursor-not-allowed  focus:outline-none disabled:bg-none disabled:bg-neutral-03 disabled:bg-opacity-50 disabled:cursor-not-allowed disabled:text-neutral-03 disabled:text-opacity-50')
        if tab.ele('t:p@tx():Register'):
            #注册
            #button.click.for_new_tab().wait(2,3).ele("@type=button", index=2).click()
            button.click()
            chrome.wait(2, 3)
            exe_okx(chrome)
            chrome.wait(7, 10)
        if tab.ele('t:p@tx():Approve'):
            #授权
            # button.click.for_new_tab().wait(2,3).ele("@type=button", index=2).click()
            button.click()
            chrome.wait(2, 3)
            exe_okx(chrome)
            chrome.wait(15, 20)
        if tab.ele('t:p@tx():Open Long Position'):
            #开单
            # button.click.for_new_tab().wait(2,3).ele("@type=button", index=2).click()
            button.click()
            chrome.wait(2, 3)
            exe_okx(chrome)
            chrome.wait(7, 10)
        chrome.wait(2, 3)
        logger.info(f"{env.name}: Silverkoi任务执行完成")
    except (RuntimeError,AttributeError) as e:
        logger.info(f"{env.name}: Silverkoi 网络延迟太大，执行失败")
    tab.close()



# def toDo(env):
#     with app.app_context():
#         logger.info(f"======开始执行{env.name}环境")
#         try:
#             chrome: ChromiumPage = OKXChrome(env)
#             tab = getTab(chrome, env)
#             tab = getCount(chrome, env)
#             tab = getSwapTab(chrome, env)
#             tab = getStake(chrome, env)
#             tab = getArc(chrome, env)
#             tab = getCultured(chrome, env)
#             tab = getSolidviolet(chrome, env)
#             tab = getKuma(chrome, env)
#             tab = getSilverkoi(chrome, env)
#         except Exception as e:
#             logger.error(f"{env.name} 执行异常：{e}")
#             raise e
#
# if __name__ == '__main__':
#     # toDoFaucet("GOON")
#     with app.app_context():
#         # env = Env.query.filter_by(name="SYL-8").first()
#         # toDo(env)
#         submit(toDo, getAllEnvs())

def toDo(chrome,env):
    logger.info(f"======开始执行{env.name}环境")
    getTab(chrome, env)
    getCount(chrome, env)
    # getSwapTab(chrome, env)
    # getStake(chrome, env)
    # getArc(chrome, env)
    # getCultured(chrome, env)
    # getSolidviolet(chrome, env)
    getKuma(chrome, env)
    # getSilverkoi(chrome, env)
    time.sleep(5)

def toDoPlumeTaskAll(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            toDo(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
            chrome.quit()
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            if chrome:
                chrome.quit()

if __name__ == '__main__':
    with app.app_context():
        # env = Env.query.filter_by(name="SYL-12").first()
        # toDoPlumeTaskAll(env)
        submit(toDoPlumeTaskAll, getAllEnvs())

    # for i in range(37,76):
    #     env = Env.query.filter_by(name="SYL-{}".format(i)).first()
    #     toDo(env)






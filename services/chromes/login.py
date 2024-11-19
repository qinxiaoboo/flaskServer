import time

import requests
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger
from flaskServer.services.chromes.mail.factory import Email
from flaskServer.config.config import WALLET_PASSWORD
from flaskServer.config.connect import app
from flaskServer.mode.account import Account
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.utils.chrome import getChrome,get_Custome_Tab, quitChrome
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.content import Content
from flaskServer.services.dto.account import updateAccountStatus

def LoginINITWallet(chrome,env):
    tab = chrome.get_tab(title="Initia Wallet")
    if "#" not in tab.url:
        tab.ele("@type=password").input(WALLET_PASSWORD)
        tab.ele("@type=submit").click()
        tab.ele("@type=button")
        logger.info(f"{env.name}: INIT 解锁成功")
    else:
        with app.app_context():
            init_wallet = Wallet.query.filter_by(id=env.init_id).first()
            if init_wallet:
                tab.ele("@href=#/account/import/mnemonic").click()
                tab.ele("@@name=password@@type=password").input(WALLET_PASSWORD)
                tab.ele("@@name=confirm@@type=password").input(WALLET_PASSWORD)
                tab.ele("@type=checkbox").click()
                tab.ele("@type=submit").click()
                for index, word in enumerate(aesCbcPbkdf2DecryptFromBase64(init_wallet.word_pass).split(" ")):
                    tab.ele("@name=words." + str(index) + ".value").input(word)
                tab.ele("@type=submit").click()
                tab.ele("@type=button")
                logger.info(f"{env.name}: INIT 登录成功")
            else:
                logger.info(f"{env.name}: INIT 账号为空，跳过登录")
    tab.close()
# def LoginPhantomWallet(chrome,env):
#     tab = chrome.get_tab(title="Phantom Wallet")
#     if tab:
#         pass
#     else:
#         chrome.new_tab("chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html")
#         chrome.wait(3,5)
#         tab = chrome.get_tab(title="Phantom Wallet")
#
#     if tab.s_ele("Unlock"):
#         passwords = tab.eles("@type=password")
#         for pwd in passwords:
#             pwd.input(WALLET_PASSWORD)
#         tab.ele("Unlock").click()
#
#     else:
#         with app.app_context():
#             wallet = Wallet.query.filter_by(id=env.okx_id).first()
#             if wallet:
#                 tab.ele("Import an existing wallet").click()
#                 tab.ele("@@class=sc-bdvvtL iZUbiK@@text()=Import Secret Recovery Phrase").click()
#                 eles = tab.eles("@class=sc-bttaWv gSFlAR")
#                 for index, word in enumerate(aesCbcPbkdf2DecryptFromBase64(wallet.word_pass).split(" ")):
#                     eles[index].input(word)
#                 tab.ele("Import Wallet").click()
#                 tab.wait(20)
#                 tab.ele("Continue").click()
#                 passwords = tab.eles("@type=password")
#                 for pwd in passwords:
#                     pwd.input(WALLET_PASSWORD)
#                 tab.ele("@type=checkbox").click()
#                 tab.ele("Continue").click()
#                 chrome.wait(5)
#                 tab.ele("Get Started").click()
#
#                 logger.info(f"{env.name}: Phantom 登录成功")
#             else:
#                 logger.info(f"{env.name}: Phantom 账号为空，跳过登录")
#     tab.close()

def ConfirmOKXWallet(chrome,tab,env):
    ele = tab.ele("@type=button").next()
    if ele.text == "Connect":
        ele.click()
        chrome.wait(1,2)
        new = chrome.get_tab(title=Content.OKX_TITLE)
        logger.info(f"{env.name}: 连接OKX钱包成功")
        try:
            new.ele("@type=button",timeout=8).next().click()
            chrome.wait(2,3)
        except Exception as e:
            new = chrome.get_tab(title=Content.OKX_TITLE)
            new.ele("@type=button").next().click()
            chrome.wait(2,3)
        logger.info(f"{env.name}: 确认OKX钱包成功")
    else:
        ele.click()
        logger.info(f"OKX 钱包 确认成功")
def LoginOKXWallet(chrome,env):
    tab = chrome.get_tab(title="OKX Wallet")
    if "unlock" in tab.url:
        tab.ele("@type=password").input(WALLET_PASSWORD)
        tab.ele("@type=submit").click()
        tab.ele("@type=button")
        logger.info(f"{env.name}: OKX 解锁成功")
    else:
        with app.app_context():
            wallet = Wallet.query.filter_by(id=env.okx_id).first()
            if wallet:
                tab.ele("Import wallet").click()
                tab.ele("@@text()=Seed phrase or private key@@style=font-weight: 500; flex: 1 0 0%;").click()
                eles = tab.eles("@type=text")
                for index, word in enumerate(aesCbcPbkdf2DecryptFromBase64(wallet.word_pass).split(" ")):
                    eles[index].input(word)
                tab.ele("@@type=submit@!btn-disabled").click()
                passwords = tab.eles("@type=password")
                for pwd in passwords:
                    pwd.input(WALLET_PASSWORD)
                tab.ele("@type=submit").click()
                tab.ele("@type=button").click()
                tab.ele("MATIC")
                logger.info(f"{env.name}: OKX 登录成功")
            else:
                logger.info(f"{env.name}: OKX 账号为空，跳过登录")
    tab.close()

def LoginBitlight(chrome:ChromiumPage,env):
    tab = chrome.new_tab(url="chrome-extension://fdojfgffiecmmppcjnahfgiignlnehap/popup/popup.html")
    chrome.wait(0.1)
    if "unlock" not in tab.url:
        tab.ele("@@type=button@@text()=I already have a wallet").click()
        passwords = tab.eles("@type=password")
        eyes = tab.eles("@data-icon=eye-invisible")
        for i,pwd in enumerate(passwords):
            eyes[i].click()
            pwd.input(WALLET_PASSWORD)
        with app.app_context():
            wallet = Wallet.query.filter_by(id=env.bitlight_id).first()
            if wallet:
                tab.ele("@@type=button@@text()=Continue").click()
                eles = tab.eles("@type=password")
                for index, word in enumerate(aesCbcPbkdf2DecryptFromBase64(wallet.word_pass).split(" ")):
                    eles[index].input(word)
                tab.ele("@@type=button@@text()=Continue").click()
                tab.ele("@type=button")
                logger.info(f"{env.name}: 登录Bitlight钱包成功！")
            else:
                logger.info(f"{env.name}: Bitlight 账号为空，跳过登录")
    else:
        tab.ele("@type=password").input(WALLET_PASSWORD)
        tab.ele("@type=button").click()
        logger.info(f"{env.name}: 解锁Bitlight钱包成功！")
    tab.close()
def AuthTW(chrome:ChromiumPage,env):
    tab = chrome.get_tab(url=r"oauth2/authorize")
    if tab :
        tab.ele("@@role=button@@data-testid=OAuth_Consent_Button").click()
        logger.info(f"{env.name}: 推特认证成功")
    else:
        tab = chrome.get_tab(url="twitter.com")
        with app.app_context():
            tw: Account = Account.query.filter_by(id=env.tw_id).first()
            if tw:
                tab.ele("@autocomplete=username").input(tw.name)
                tab.ele("@@type=button@@text()=Next").click()
                tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
                tab.ele("@@type=button@@text()=Log in").click()
                fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                if "login" in tab.url and len(fa2) > 10:
                    tw2faV(tab,fa2)
                tab.ele("@@role=button@@data-testid=OAuth_Consent_Button").click()
                logger.info(f"{env.name}: 推特登录并认证成功")
            else:
                logger.warning(f"{env.name}: TW 账号为空，跳过无法完成")
    return get_Custome_Tab(tab)

def tw2faV(tab,fa2):
    res = requests.get(fa2)
    if res.ok:
        code = res.json().get("data").get("otp")
        print(tab.url)
        tab.ele("@data-testid=ocfEnterTextTextInput").input(code,clear=True)
        tab.ele("@@type=button@@text()=Next").click()

def checkTw(chrome, tab, env):
    tab.wait(2, 3)
    print(f"{env.name}: {tab.url}")
    if ".com/home" in tab.url:
        logger.info(f"{env.name}: 登录推特成功")
        endCheckTW(tab,env)
    elif "account/access" in tab.url:
        tab.wait(1, 2)
        start = tab.s_ele("@@type=submit@@value=Start")
        if start:
            tab.ele("@@type=submit@@value=Start").click(by_js=True)
            tab.wait(1, 2)
            if tab.s_ele("@@type=submit@@value=Send email"):
                tab.ele("@@type=submit@@value=Send email").click()
                verifyTw(chrome, tab, env)
            else:
                reload = tab.s_ele("Reload Challenge")
                if reload:
                    tab.ele("Reload Challenge").click()
                ele = tab.ele("@@type=submit@@value=Continue to X",timeout=120)
                if ele:
                    tab.wait(3, 4)
                    ele.click(by_js=True)
                    logger.info(f"{env.name}: TW验证码验证成功")
                    tab.wait.doc_loaded()
                    tab.wait(2, 3)
                    endCheckTW(tab, env)
                else:
                    updateAccountStatus(env.tw_id, 1, "TW验证码元素未找到")
                    raise Exception(f"{env.name}: TW验证码元素未找到")
        else:
            if tab.s_ele("@@type=submit@@value=Send email"):
                tab.ele("@@type=submit@@value=Send email").click()
                verifyTw(chrome, tab, env)

            if tab.s_ele("@@type=submit@@value=Verify"):
                verifyTw(chrome, tab, env)

            if tab.s_ele("@@type=submit@@value=Continue to X"):
                tab.ele("@@type=submit@@value=Continue to X").click(by_js=True)
                logger.info(f"{env.name}: TW邮箱验证成功")
                tab.wait.doc_loaded()
                tab.wait(5, 6)
                endCheckTW(tab, env)
            else:
                if ".com/home" in tab.url:
                    logger.info(f"{env.name}: 登录推特成功")
                else:
                    updateAccountStatus(env.tw_id, 1, "TW邮箱验证失败，请人工前往验证")
                    raise Exception(f"{env.name}: TW邮箱验证失败，请人工前往验证")
    else:
        tab.wait(1,2)
        if ".com/home" in tab.url:
            logger.info(f"{env.name}: 登录推特成功")
            endCheckTW(tab, env)
        else:
            updateAccountStatus(env.tw_id, 1, "没有检测到登录页面的url为.com/home")
            raise Exception(f"{env.name}: TW 登录失败")
    return tab

def verifyTw(chrome, tab, env):
    with app.app_context():
        tw: Account = Account.query.filter_by(id=env.tw_id).first()
        if tw:
            client = Email.from_account(env.id, chrome, env.name, tw.email_name, tw.email_pass)
            code = client.getCode("confirm your email address to access all of")
            tab.ele("@@type=text@@name=token").input(code)
            tab.ele("@@type=submit@@value=Verify").click()
            if tab.s_ele("@@type=submit@@value=Continue to X"):
                tab.ele("@@type=submit@@value=Continue to X").click(by_js=True)
                logger.info(f"{env.name}: TW邮箱验证成功")
                tab.wait.doc_loaded()
                tab.wait(5, 6)
                endCheckTW(tab, env)
            else:
                updateAccountStatus(env.tw_id, 1, "TW邮箱验证失败，请人工前往验证")
                raise Exception(f"{env.name}: TW邮箱验证失败，请人工前往验证")

def endCheckTW(tab,env):
    sheetDialog = tab.s_ele("@data-testid=sheetDialog")
    if sheetDialog:
        logger.info(f"{env.name}: 推特出现弹窗需要处理！")
        confram = tab.ele("@data-testid=sheetDialog").ele("@role=button")
        if "Yes" in confram.text or "Got it" in confram.text:
            logger.info(f"{env.name}: 弹窗中包含yes含义的按钮：{confram.text} 点击")
            confram.click()
        else:
            logger.warning(f"{env.name}: 弹窗不包含Yes，没有点击")
            return
    updateAccountStatus(env.tw_id, 2)

def preCheckTW(chrome,env):
    tab = chrome.get_tab(url=".com/i/flow/login")
    if tab is None:
        tab = chrome.get_tab(url=".com/login")
        if tab is None:
            tab = chrome.new_tab(url="https://x.com/home")
    chrome.wait(1, 2)
    return tab

def LoginTW(chrome:ChromiumPage,env):
    updateAccountStatus(env.tw_id, 0, "重置了TW登录状态")
    tab = preCheckTW(chrome,env)
    if "logout" in tab.url or "login" in tab.url:
        logger.info(f"{env.name}: 开始登录 TW 账号")
        tab.get(url="https://x.com/i/flow/login")
        with app.app_context():
            tw:Account = Account.query.filter_by(id=env.tw_id).first()
            if tw:
                tab.wait.eles_loaded('@autocomplete=username', timeout=8, raise_err=False)
                tab.ele("@autocomplete=username").input(tw.name, clear=True)
                tab.ele("@@type=button@@text()=Next").click()
                tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd), clear=True)
                tab.ele("@@type=button@@text()=Log in").click()
                fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                if "login" in tab.url and len(fa2) > 10:
                    tw2faV(tab, fa2)
            else:
                updateAccountStatus(env.tw_id, 1, "没有导入TW的账号信息")
                raise Exception(f"{env.name}: 没有导入TW的账号信息")
    return checkTw(chrome, get_Custome_Tab(tab), env)


def LoginDiscord(chrome:ChromiumPage,env):
    updateAccountStatus(env.discord_id, 0, "重置了Discord登录状态")
    tab = chrome.new_tab(url="https://discord.com/app")
    if tab.s_ele("Please log in again"):
        tab.ele("@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85").click()


    if "login" in tab.url:
        logger.info(f"{env.name} 开始登录 Discord 账号")
        with app.app_context():
            discord:Account = Account.query.filter_by(id=env.discord_id).first()
            if discord:
                tab.ele("@name=email").input(discord.name)
                tab.ele("@name=password").input(aesCbcPbkdf2DecryptFromBase64(discord.pwd))
                tab.ele("@type=submit").click()
                fa2 = aesCbcPbkdf2DecryptFromBase64(discord.fa2)
                if "login" in tab.url and len(fa2) > 10:
                    res = requests.get(fa2)
                    if res.ok:
                        code = res.json().get("data").get("otp")
                        tab.ele("@autocomplete=one-time-code").input(code)
                        tab.ele("@type=submit").click()
            else:
                updateAccountStatus(env.discord_id, 1, "没有导入DISCORD 的账号信息")
                raise Exception(f"{env.name}: 没有导入DISCORD 账号信息")
    if "channels" in tab.url or ".com/app" in tab.url:
        updateAccountStatus(env.discord_id, 2)
        logger.info(f"{env.name}登录Discord成功！")
    return get_Custome_Tab(tab)

def preCheckOutlook(chrome):
    tab = chrome.get_tab(url=".com/mail/0/")
    if tab is None:
        tab = chrome.new_tab(url="https://outlook.live.com/mail/0/")
    return tab

def LoginOutlook(chrome:ChromiumPage,env):
    updateAccountStatus(env.outlook_id, 0, "重置了OutLook登录状态")
    tab = preCheckOutlook(chrome)
    tab.wait.url_change("https://outlook.live.com/mail/0/", timeout=8, raise_err=False)
    if "microsoft" in tab.url or "login.srf" in tab.url:
        with app.app_context():
            outlook:Account = Account.query.filter_by(id=env.outlook_id).first()
            if outlook:
                if "outlook" in outlook.name or "hotmail" in outlook.name:
                    logger.info(f"{env.name}: 开始登陆 outlook邮箱")
                    if "login.srf" not in tab.url:
                        tab = tab.eles("@aria-label=Sign in to Outlook")[4].click.for_new_tab()
                    if tab.s_ele("@data-testid=i0116"):
                        tab.ele("@data-testid=i0116").input(outlook.name)
                    if tab.s_ele("@type=submit"):
                        tab.ele("@type=submit").click()
                    if tab.s_ele("@name=passwd"):
                        if tab.s_ele("@id=userDisplayName"):
                            text = tab.ele("@id=userDisplayName").text
                            if text == outlook.name:
                                tab.ele("@name=passwd").input(aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
                            else:
                                if tab.s_ele("@data-testid=secondaryContent"):
                                    othertab_button = tab.ele("@data-testid=secondaryContent").children()[2]
                                    othertab_button.click()
                                    tab.wait(3, 3.1)
                                    if tab.s_ele("@data-testid=i0116"):
                                        tab.ele("@data-testid=i0116").input(outlook.name, clear=True)
                                    if tab.s_ele("@type=submit"):
                                        tab.ele("@type=submit").click()
                                    tab.ele("@name=passwd").input(aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
                    chrome.wait(2, 2.1)
                    if tab.s_ele("t:button@tx():Sign in"):
                        tab.ele("t:button@tx():Sign in").click()
                    if tab.s_ele("t:button@tx():Next"):
                        tab.ele("t:button@tx():Next").click()
                    if tab.s_ele("@type=checkbox"):
                        tab.ele("@type=checkbox").click()
                    if tab.s_ele('t:button@tx():Yes'):
                        tab.ele('t:button@tx():Yes').click()
                    if "https://outlook.live.com/mail/0" in tab.url:
                        logger.info(f"{env.name}: 登录OUTLOOK成功")
                else:
                    tab.close()
                    logger.info(f"{env.name}: 邮箱格式不匹配，关闭邮箱标签,不登录邮箱")
                    return
            else:
                logger.info(f"{env.name}: 邮箱 账号为空，跳过登录")
    if tab.s_ele("@@type=submit@@id=iNext"):
        tab.ele("@@type=submit@@id=iNext").click()
    if tab.s_ele("@id=userDisplayName"):
        text = tab.ele("@id=userDisplayName").text
        with app.app_context():
            outlook:Account = Account.query.filter_by(id=env.outlook_id).first()
            if outlook:
                if text == outlook.name:
                    tab.ele("@name=passwd").input(aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
                    tab.ele("@type=submit").click()
                    if tab.s_ele("@@type=submit@@id=iNext"):
                        tab.ele("@@type=submit@@id=iNext").click()
                    logger.info(f"{env.name}: 登录OUTLOOK成功")

    updateAccountStatus(env.outlook_id, 2)


def OKXChrome(env):
    with app.app_context():
        chrome =None
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            LoginOKXWallet(chrome,env)
            # LoginPhantomWallet(chrome,env)
            chrome.get_tab(title="Initia Wallet").close()
            return chrome
        except Exception as e:
            quitChrome(env, chrome)
            raise e


def NoAccountChrome(env):
    with app.app_context():
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            chrome.get_tab(title="Initia Wallet").close()
            chrome.get_tab(title="OKX Wallet").close()
            return chrome
        except Exception as e:
            quitChrome(env, chrome)
            raise e

def GalxeChrome(env):
    with app.app_context():
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            LoginINITWallet(chrome,env)
            LoginOKXWallet(chrome, env)
            LoginOutlook(chrome, env)
            LoginTW(chrome, env)
            LoginDiscord(chrome, env)
            logger.info(f"{env.name}: {chrome.address}")
            return chrome
        except Exception as e:
            quitChrome(env, chrome)
            raise e

def LoginChrome(env):
    with app.app_context():
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            LoginINITWallet(chrome, env)
            LoginOKXWallet(chrome, env)
            # LoginPhantomWallet(chrome, env)
            LoginOutlook(chrome, env)
            LoginTW(chrome, env)
            LoginDiscord(chrome, env)
            LoginBitlight(chrome, env)
            logger.info(ChromiumOptions().address)
            updateEnvStatus(env.name, 2)
            return chrome
        except Exception as e:
            quitChrome(env, chrome)
            raise e

def DebugChrome(env):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        chrome = getChrome(proxy,env)
        LoginINITWallet(chrome, env)
        LoginOKXWallet(chrome, env)
        # LoginPhantomWallet(chrome, env)
        LoginOutlook(chrome, env)
        LoginTW(chrome, env)
        LoginDiscord(chrome, env)
        LoginBitlight(chrome, env)
        logger.info(ChromiumOptions().address)
        updateEnvStatus(env.name, 2)
        return chrome

def toLoginAll(env):
    if env.status != 2:
        chrome = None
        try:
            logger.info(f"{env.name}: 打开环境")
            chrome = LoginChrome(env)
            logger.info(f"{env.name}环境：初始化成功，关闭环境")
            quitChrome(env, chrome)
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            quitChrome(env, chrome)
            return ("失败",f"{e}")
    else:
        logger.info(f"{env.name}: 已初始化")


if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-2-1").first()
        chrome = DebugChrome(env)
        logger.info("环境初始化成功")
        from flaskServer.services.chromes.mail.factory import Email
        outlook: Account = Account.query.filter_by(id=env.outlook_id).first()
        client = Email.from_account("0", chrome, "Q-2-1", outlook.name, aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
        code = client.getCode("Lauren Brown, confirm your email address to access all", 3, 3)
        print(code)

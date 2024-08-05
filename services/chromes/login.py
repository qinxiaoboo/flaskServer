import requests
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger

from flaskServer.config.config import WALLET_PASSWORD
from flaskServer.config.connect import app
from flaskServer.mode.account import Account
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.utils.chrome import getChrome,get_Custome_Tab
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.content import Content

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

def ConfirmOKXWallet(chrome,tab,env):
    ele = tab.ele("@type=button").next()
    if ele.text == "Connect":
        new = ele.click.for_new_tab()
        logger.info(f"{env.name}: 连接OKX钱包成功")
        new.wait.load_start()
        try:
            new.ele("@type=button",timeout=8).next().click()
        except Exception as e:
            new = chrome.get_tab(title=Content.OKX_TITLE)
            new.ele("@type=button").next().click()
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
                tab.ele("@@text()=Import wallet@@style=font-weight: 500; flex: 1 0 0%;").click()
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
        tab.ele("@data-testid=ocfEnterTextTextInput").input(code)
        tab.ele("@@type=button@@text()=Next").click()

def LoginTW(chrome:ChromiumPage,env):
    tab = chrome.get_tab(url=".com/i/flow/login")
    if tab is None:
        tab = chrome.get_tab(url="x.com/login")
        if tab is None:
            tab = chrome.new_tab(url="https://x.com/home")
    chrome.wait(1,2)
    if "logout" in tab.url or "login" in tab.url:
        logger.info(f"{env.name}: 开始登录 TW 账号")
        tab.get(url="https://x.com/i/flow/login")
    else:
        logger.info(f"{env.name}: 登录TW成功")
        return get_Custome_Tab(tab)
    with app.app_context():
        tw:Account = Account.query.filter_by(id=env.tw_id).first()
        if tw:
            tab.ele("@autocomplete=username").input(tw.name)
            tab.ele("@@type=button@@text()=Next").click()
            tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
            tab.ele("@@type=button@@text()=Log in").click()
            fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
            if "login" in tab.url and len(fa2) > 10:
                tw2faV(tab,fa2)
            if "home" in tab.url:
                logger.info(f"{env.name}: 登录TW成功")
        else:
            logger.info(f"{env.name}: TW 账号为空，跳过登录")
        return get_Custome_Tab(tab)


def LoginDiscord(chrome:ChromiumPage,env):
    tab = chrome.new_tab(url="https://discord.com/app")
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
                logger.info(f"{env.name}: DISCORD 账号为空，跳过登录")
    if "channels" in tab.url:
        logger.info(f"{env.name}登录Discord成功！")
    return get_Custome_Tab(tab)

def LoginOutlook(chrome:ChromiumPage,env):
    tab = chrome.new_tab(url="https://outlook.live.com/mail/0/")
    chrome.wait(2,3)
    if "microsoft" in tab.url:
        with app.app_context():
            outlook:Account = Account.query.filter_by(id=env.outlook_id).first()
            if outlook:
                if "outlook" in outlook.name or "hotmail" in outlook.name:
                    logger.info(f"{env.name}: 开始登陆 outlook邮箱")
                    tab = tab.eles("@aria-label=Sign in to Outlook")[4].click.for_new_tab()
                    tab.ele("@data-testid=i0116").input(outlook.name)
                    tab.ele("@type=submit").click()
                    tab.ele("@name=passwd").input(aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
                    tab.ele("@type=submit").click()
                    tab.ele("@type=checkbox").click()
                    tab.ele("@@type=submit@@text()=Yes").click()
                    if "https://outlook.live.com/mail/0" in tab.url:
                        logger.info(f"{env.name}: 登录OUTLOOK成功")
                else:
                    tab.close()
                    logger.info(f"{env.name}: 邮箱格式不正确，关闭邮箱标签")
                    return
            else:
                logger.info(f"{env.name}: 邮箱 账号为空，跳过登录")
    return get_Custome_Tab(tab)


def OKXChrome(env):
    with app.app_context():
        chrome =None
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            LoginOKXWallet(chrome,env)
            chrome.get_tab(title="Initia Wallet").close()
            return chrome
        except Exception as e:
            if chrome:
                chrome.quit()
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
            if chrome:
                chrome.quit()
            raise e

def GalxeChrome(env):
    with app.app_context():
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            LoginINITWallet(chrome,env)
            LoginOKXWallet(chrome, env)
            LoginTW(chrome, env)
            LoginDiscord(chrome, env)
            LoginOutlook(chrome, env)
            logger.info(f"{env.name}: {chrome.address}")
            return chrome
        except Exception as e:
            if chrome:
                chrome.quit()
            raise e

def LoginChrome(env):
    with app.app_context():
        try:
            proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
            chrome = getChrome(proxy,env)
            LoginINITWallet(chrome, env)
            LoginOKXWallet(chrome, env)
            LoginTW(chrome, env)
            LoginDiscord(chrome, env)
            LoginOutlook(chrome, env)
            LoginBitlight(chrome, env)
            logger.info(ChromiumOptions().address)
            updateEnvStatus(env.name, 2)
            return chrome
        except Exception as e:
            if chrome:
                chrome.quit()
            raise e

def DebugChrome(env):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        chrome = getChrome(proxy,env)
        LoginINITWallet(chrome, env)
        LoginOKXWallet(chrome, env)
        LoginTW(chrome, env)
        LoginDiscord(chrome, env)
        LoginOutlook(chrome, env)
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
            chrome.quit()
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            if chrome:
                chrome.quit()
    else:
        logger.info(f"{env.name}: 已初始化")


if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-2").first()
        try:
            chrome = OKXChrome(env)
            logger.info("环境初始化成功")
            chrome.quit()
        except Exception as e:
            logger.error(env.to_json(),e)

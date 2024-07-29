import requests
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger
from flaskServer.config.chromiumOptions import initChromiumOptions
from flaskServer.config.config import WALLET_PASSWORD
from flaskServer.config.connect import app
from flaskServer.mode.account import Account
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.utils.chrome import initChrom, wait_pages
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.config.config import get_ini_path

def LoginINITWallet(chrome,env):
    tab = chrome.get_tab(title="Initia Wallet")
    if "#" not in tab.url:
        tab.ele("@type=password").input(WALLET_PASSWORD)
        tab.ele("@type=submit").click()
        tab.ele("@type=button")
        logger.info(f"{env.name}: INIT 解锁成功")
    else:
        init_wallet = Wallet.query.filter_by(id=env.init_id).first()
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
    tab.close()

def ConfirmOKXWallet(chrome,tab,env):
    ele = tab.ele("@type=button").next()
    if ele.text == "Connect":
        ele.click()
        logger.info(f"{env.name}: 连接OKX钱包成功")
        chrome.wait.load_start()
        chrome.wait(8,9)
        tab = chrome.get_tab(title="OKX Wallet")
        tab.ele("@type=button").next().click()
        logger.info(f"{env.name}: 确认OKX钱包成功")
    else:
        ele.click()
    logger.info(f"OKX 钱包 确认成功")


def LoginOKXWallet(chrome,env):
    tab = chrome.get_tab(title="OKX Wallet")
    logger.info(tab.url)
    if "unlock" in tab.url:
        tab.ele("@type=password").input(WALLET_PASSWORD)
        tab.ele("@type=submit").click()
        tab.ele("@type=button")
        logger.info(f"{env.name}: OKX 解锁成功")
    else:
        wallet = Wallet.query.filter_by(id=env.okx_id).first()
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
    tab.close()

def LoginBitlight(chrome:ChromiumPage,env):
    tab = chrome.new_tab(url="chrome-extension://fdojfgffiecmmppcjnahfgiignlnehap/popup/popup.html")
    if "unlock" not in tab.url:
        tab.ele("@@type=button@@text()=I already have a wallet").click()
        passwords = tab.eles("@type=password")
        eyes = tab.eles("@data-icon=eye-invisible")
        for i,pwd in enumerate(passwords):
            eyes[i].click()
            pwd.input(WALLET_PASSWORD)
        wallet = Wallet.query.filter_by(id=env.bitlight_id).first()
        tab.ele("@@type=button@@text()=Continue").click()
        eles = tab.eles("@type=password")
        for index, word in enumerate(aesCbcPbkdf2DecryptFromBase64(wallet.word_pass).split(" ")):
            eles[index].input(word)
        tab.ele("@@type=button@@text()=Continue").click()
        tab.ele("@type=button")
        logger.info(f"{env.name}: 登录Bitlight钱包成功！")
    else:
        tab.ele("@type=password").input(WALLET_PASSWORD)
        tab.ele("@type=button").click()
        logger.info(f"{env.name}: 解锁Bitlight钱包成功！")
    tab.close()

def AuthTW(chrome:ChromiumPage,env):
    tab = chrome.get_tab(url=r"oauth2/authorize")
    print(tab)
    if tab :
        tab.ele("@@role=button@@data-testid=OAuth_Consent_Button").click()
        logger.info(f"{env.name}: 推特认证成功")
    else:
        tab = chrome.get_tab(url="twitter.com")
        tw: Account = Account.query.filter_by(id=env.tw_id).first()
        tab.ele("@autocomplete=username").input(tw.name)
        tab.ele("@@type=button@@text()=Next").click()
        tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
        tab.ele("@@type=button@@text()=Log in").click()
        fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
        if "login" in tab.url and len(fa2) > 10:
            res = requests.get(fa2)
            if res.ok:
                code = res.json().get("data").get("otp")
                tab.ele("@data-testid=ocfEnterTextTextInput").input(code)
                tab.ele("@@type=button@@text()=Next").click()
        tab.ele("@@role=button@@data-testid=OAuth_Consent_Button").click()
        logger.info(f"{env.name}: 推特登录并认证成功")


def LoginTW(chrome:ChromiumPage,env):
    tab = chrome.get_tab(url="twitter.com/i/flow/login")
    if tab is None:
        tab = chrome.get_tab(url="x.com/login")
        if tab is None:
            tab = chrome.new_tab(url="https://x.com/home")
    chrome.wait(1,2)
    print(tab.url)
    if "logout" in tab.url or "login" in tab.url:
        logger.info(f"{env.name}: 开始登录 TW 账号")
        tab.get(url="https://x.com/i/flow/login")
    else:
        logger.info(f"{env.name}: 登录TW成功")
        return tab
    tw:Account = Account.query.filter_by(id=env.tw_id).first()
    tab.ele("@autocomplete=username").input(tw.name)
    tab.ele("@@type=button@@text()=Next").click()
    tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd))
    tab.ele("@@type=button@@text()=Log in").click()
    fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
    if "login" in tab.url and len(fa2) > 10:
        res = requests.get(fa2)
        if res.ok:
            code = res.json().get("data").get("otp")
            tab.ele("@data-testid=ocfEnterTextTextInput").input(code)
            tab.ele("@@type=button@@text()=Next").click()
    if "home" in tab.url:
        logger.info(f"{env.name}: 登录TW成功")
    return tab


def LoginDiscord(chrome:ChromiumPage,env):
    tab = chrome.new_tab(url="https://discord.com/app")
    logger.info(tab.url)
    if "login" in tab.url:
        logger.info(f"{env.name} 开始登录 Discord 账号")
        discord:Account = Account.query.filter_by(id=env.discord_id).first()
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
    if "channels" in tab.url:
        logger.info(f"{env.name}登录Discord成功！")
    return tab

def LoginOutlook(chrome:ChromiumPage,env):
    tab = chrome.new_tab(url="https://outlook.live.com/mail/0/")
    chrome.wait(2,3)
    print(tab.url)
    if "microsoft" in tab.url:
        outlook:Account = Account.query.filter_by(id=env.outlook_id).first()
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

    return tab

def InitChromeOptionByConf(env):
    with app.app_context():
        if env.status != 0:
            chrome = ChromiumPage(addr_or_opts=ChromiumOptions(ini_path=get_ini_path(env.name)))
            chrome.get("https://www.browserscan.net/zh?env=" + env.name)
            wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
            wait_pages(chrome, wait_page_list)
            LoginOKXWallet(chrome,env)
            chrome.get_tab(title="Initia Wallet").close()
            chrome.get_tab(title="Welcome to OKX").close()
            return chrome
        else:
            return InitChromeOption(env)

def InitChromeOption(env):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        if proxy:
            chrome = ChromiumPage(addr_or_opts=
                                  initChromiumOptions(env.name, env.port, env.user_agent,
                                                      "http://" + proxy.ip + ":" + proxy.port))
            initChrom(chrome, env.name, proxy.ip, proxy.port, proxy.user, proxy.pwd)
        else:
            chrome = ChromiumPage(addr_or_opts=initChromiumOptions(env.name, env.port, env.user_agent, None))
        chrome.get("https://www.browserscan.net/zh?env=" + env.name)
        wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
        wait_pages(chrome, wait_page_list)
        chrome.get_tab(title="Initia Wallet").close()
        chrome.get_tab(title="Welcome to OKX").close()
        chrome.get_tab(title="OKX Wallet").close()
        return chrome

def GalxeChrome(env):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        if proxy:
            chrome = ChromiumPage(addr_or_opts=
            initChromiumOptions(env.name, env.port, env.user_agent,
                            "http://" + proxy.ip + ":" + proxy.port))
            initChrom(chrome, env.name, proxy.ip, proxy.port, proxy.user, proxy.pwd)
        else:
            chrome = ChromiumPage(addr_or_opts=initChromiumOptions(env.name, env.port, env.user_agent,None))
        chrome.get("https://www.browserscan.net/zh?env="+env.name)
        wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
        wait_pages(chrome, wait_page_list)
        LoginINITWallet(chrome,env)
        LoginOKXWallet(chrome, env)
        LoginTW(chrome, env)
        LoginDiscord(chrome, env)
        LoginOutlook(chrome, env)
        tab = chrome.get_tab(title="Welcome to OKX")
        tab.close()
        logger.info(f"{env.name}: {ChromiumOptions().address}")
        return chrome


def LoginChrome(env):
    with app.app_context():
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        if proxy:
            chrome = ChromiumPage(addr_or_opts=
            initChromiumOptions(env.name, env.port, env.user_agent,
                            "http://" + proxy.ip + ":" + proxy.port))
            initChrom(chrome, env.name, proxy.ip, proxy.port, proxy.user, proxy.pwd)
        else:
            chrome = ChromiumPage(addr_or_opts=initChromiumOptions(env.name, env.port, env.user_agent,None))
        chrome.get("https://www.browserscan.net/zh?env="+env.name)
        wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
        wait_pages(chrome, wait_page_list)
        LoginINITWallet(chrome, env)
        LoginOKXWallet(chrome, env)
        LoginTW(chrome, env)
        LoginDiscord(chrome, env)
        LoginOutlook(chrome, env)
        LoginBitlight(chrome, env)
        tab = chrome.get_tab(title="Welcome to OKX")
        tab.close()
        logger.info(ChromiumOptions().address)
        return chrome

def toLoginAll(env):
    if env.status == 0 or env.status == 1:
        try:
            chrome = LoginChrome(env)
            updateEnvStatus(env.name, 2)
            logger.info(f"{env.name}环境初始化成功")
            chrome.quit()
        except Exception as e:
            logger.error(env.to_json(), e)
    if env.status == 2:
        logger.info(f"{env.name}环境初始化成功")




if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-8-3").first()
        if env.status == 0 or env.status == 2:
            try:
                chrome = InitChromeOptionByConf(env)
                logger.info("环境初始化成功")
                # chrome.quit()
            except Exception as e:
                logger.error(env.to_json(),e)


        # proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        # chrome = ChromiumPage(addr_or_opts=initChromiumOptions(env.name,env.port, env.user_agent, "http://" + proxy.ip + ":" + proxy.port))
        # initChrom(chrome, env.name, proxy.ip, proxy.port,proxy.user,proxy.pwd)
        # chrome.get("https://www.browserscan.net/zh")
        # wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
        # wait_pages(chrome, wait_page_list)
        # LoginINITWallet(chrome,env)
        # LoginOKXWallet(chrome,env)
        # LoginTW(chrome,env)
        # LoginDiscord(chrome,env)
        # LoginOutlook(chrome,env)
        # LoginBitlight(chrome,env)
        #
        #
        # logger.info(ChromiumOptions().address)
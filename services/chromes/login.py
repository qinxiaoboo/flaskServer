import time

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
from flaskServer.services.chromes.mail.factory import Email
from flaskServer.services.chromes.worker import createThread
from flaskServer.services.content import Content
from flaskServer.services.dto.account import getAccountById
from flaskServer.services.dto.account import updateAccountStatus, updateAccountToken
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.utils.chrome import getChrome, get_Custome_Tab, quitChrome
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.utils.decorator import chrome_retry


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
                if tab.s_ele("@data-testid=okd-checkbox-circle"):
                    tab.ele("@data-testid=okd-checkbox-circle").click()
                if tab.s_ele("@data-testid=okd-button"):
                    tab.ele("@data-testid=okd-button").click()
                tab.wait.eles_loaded("@type=password", timeout=8, raise_err=False)
                passwords = tab.eles("@type=password") # 密码
                for pwd in passwords:
                    pwd.input(WALLET_PASSWORD)
                if tab.s_ele("@data-testid=okd-button"):
                    tab.ele("@data-testid=okd-button").click()
                flag = tab.wait.eles_loaded("USDT", timeout=8, raise_err=False)
                if flag:
                    logger.info(f"{env.name}: OKX 登录成功")
                else:
                    logger.warning(f"{env.name}: OKX 登录失败 ")
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

def tw2faV(tab,fa2):
    res = requests.get(fa2)
    if res.ok:
        code = res.json().get("data").get("otp")
        if tab.s_ele("@data-testid=ocfEnterTextTextInput"):
            tab.ele("@data-testid=ocfEnterTextTextInput").input(code,clear=True)
            tab.ele("@@type=button@@text()=Next").click()

def checkTw(chrome, tab, env, count):
    tab.wait(2, 3)
    logger.info(f"{env.name}: 检查tw是否登录成功，当前URL：{tab.url}")
    if ".com/home" in tab.url:
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
                    endCheckTW(tab, env)
                else:
                    updateAccountStatus(env.tw_id, 1, "TW邮箱验证失败，请人工前往验证")
                    raise Exception(f"{env.name}: TW邮箱验证失败，请人工前往验证")
    else:
        tab.wait(1,2)
        if ".com/home" in tab.url:
            logger.info(f"{env.name}: 登录推特成功")
            endCheckTW(tab, env)
        else:
            tab.refresh(ignore_cache=True)
            count +=1
            logger.warning(f"{env.name}: 刷新tw页面，重新登录tw, 第{count}次重试")
            LoginTW(chrome, env, count)
    return tab

def verifyTw(chrome, tab, env):
    with app.app_context():
        tw: Account = Account.query.filter_by(id=env.tw_id).first()
        if tw:
            client = Email.from_account(env.id, chrome, env.name, tw.email_name, tw.email_pass)
            code = client.getCode("confirm your email address to access all of")
            logger.info(f"{env.name}: TW登录获取验证码：{code}")
            tab.ele("@@type=text@@name=token").input(code)
            tab.ele("@@type=submit@@value=Verify").click()
            if tab.s_ele(".Form-message is-errored"):
                logger.info(f"{env.name}: TW登录邮箱验证失败，重新获取验证码")
                code = client.getCode("confirm your email address to access all of", type="other")
                logger.info(f"{env.name}: TW登录获取验证码：{code}")
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

def endCheckTW(tab,env, count=1):
    if tab.s_ele("@@role=button@@text()=Retry"):
        tab.ele("@@role=button@@text()=Retry").click()
        logger.debug(f"{env.name} TW Retry按钮出现, 第{count}次 点击Retry~")
        tab.wait(0,2)
        if count < 5:
            count +=1
            endCheckTW(tab, env, count)
            return
        logger.warning(f"{env.name} TW Retry按钮出现, 账号缓存异常，关闭页面重新登录~")
        tab.set.cookies.remove(name="auth_token", domain=".x.com")
        tab.refresh()
        with app.app_context():
            tw: Account = Account.query.filter_by(id=env.tw_id).first()
            if tw:
                LoginTwByUserPwd(tw, tab, env)
    sheetDialog = tab.s_ele("@data-testid=sheetDialog")
    if sheetDialog:
        logger.info(f"{env.name}: 推特出现弹窗需要处理！")
        confram = tab.ele("@data-testid=sheetDialog").ele("@role=button")
        if "Yes" in confram.text or "Got it" in confram.text:
            logger.info(f"{env.name}: 弹窗中包含yes含义的按钮：{confram.text} 点击")
            confram.click()
        else:
            logger.warning(f"{env.name}: 弹窗不包含Yes，没有点击")
            updateAccountStatus(env.tw_id, 1, "TW账号有弹窗没有处理~")
            return
    if tab.s_ele("@data-testid=SideNav_AccountSwitcher_Button"):
        account = tab.ele("@data-testid=SideNav_AccountSwitcher_Button")
        try:
            username = account.ele("@class=css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3", index=2, timeout=5).text
        except Exception as e:
            account.click()
            if tab.s_ele("@data-testid=AccountSwitcher_Logout_Button"):
                username = tab.ele("@data-testid=AccountSwitcher_Logout_Button").text
            else: username=""
            account.click()
        tw = getAccountById(env.tw_id)
        logger.debug(f"{env.name} tw page name: {username}, db name: @{tw.name}")
        if username and f"@{tw.name}" not in username:
            logger.debug(f"{env.name} TW账号发生改变，点击退出账号")
            account.click()
            if tab.s_ele("@data-testid=AccountSwitcher_Logout_Button"):
                tab.ele("@data-testid=AccountSwitcher_Logout_Button").click()
                tab.ele("@data-testid=confirmationSheetConfirm").click()
                logger.warning(f"{env.name} TW账号已经被替换，老账号退出登录")
                tab.close()
                raise ConnectionError("老账号退出登录")
        elif not username:
            if count < 3:
                count += 1
                endCheckTW(tab, env, count)
                return
            raise Exception(f"{env.name} 没有获取到 TW 名称")
    token = ""
    for cookie in tab.cookies():
        if cookie["name"]=="auth_token":
            token = cookie["value"] + token
        if cookie["name"] == "ct0":
            token+= ","
            token+=cookie["value"]
    updateAccountToken(env.tw_id, token)
    if tab.s_ele("@data-testid=inlinePrompt"):
        ele = tab.ele("@data-testid=inlinePrompt")
        if "Your account is suspended" in ele.text:
            updateAccountStatus(env.tw_id, 1, "TW账号疑似被封，请确认账号状态~")
            logger.warning(f"{env.name}: TW账号疑似被封，请确认账号状态~")
            return
    logger.info(f"{env.name}: 登录推特成功")
    updateAccountStatus(env.tw_id, 2)


def LoginTwByToken(tw, chrome,env):
    tab = chrome.get_tab(url=".com/i/flow/login")
    if tab is None:
        tab = chrome.get_tab(url=".com/login")
        if tab is None:
            tab = chrome.get_tab(url="x.com")
            if tab is None:
                tab = chrome.new_tab(url="https://x.com/home")
    chrome.activate_tab(id_ind_tab=tab)
    if "x.com/home" in tab.url:
        pass
    else:
        if tw and tw.token:
            tab.set.cookies(f'name=auth_token; value={tw.token.split(",")[0]};domain=.x.com;')
            tab.get("https://x.com/home")
    return tab

def LoginTwByUserPwd(tw, tab, env):
    tab.refresh(ignore_cache=True)
    tab.get(url="https://x.com/i/flow/login")
    logger.info(f"{env.name} 刷新页面并清空缓存 -> 开始登录 TW 账号")
    flag = tab.wait.eles_loaded('@autocomplete=username', timeout=5, raise_err=False)
    if not flag:
        tab.refresh()
    if "login" in tab.url:
        tab.ele("@autocomplete=username").input(tw.name, clear=True)
        tab.ele("@@type=button@@text()=Next").click()
        tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd), clear=True)
        tab.ele("@@type=button@@text()=Log in").click()
        fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
        if "login" in tab.url and len(fa2) > 10:
            tw2faV(tab, fa2)

@chrome_retry(exceptions=(ConnectionError,), max_tries=2, initial_delay=2)
def LoginTW(chrome:ChromiumPage,env, count=0):
    if count > 3:
        logger.error(f"{env.name} TW登录重试次数超过三次，停止重试！")
        updateAccountStatus(env.tw_id, 1, "TW登录重试次数超过三次，停止重试！")
        return
    updateAccountStatus(env.tw_id, 0, "重置了TW登录状态")
    with app.app_context():
        tw: Account = Account.query.filter_by(id=env.tw_id).first()
        if tw:
            tab = LoginTwByToken(tw, chrome, env)
            if "logout" in tab.url or "login" in tab.url:
                LoginTwByUserPwd(tw, tab, env)
        else:
            return
    return checkTw(chrome, get_Custome_Tab(tab), env, count)

def LoginDiscordByToken(discord, chrome:ChromiumPage, env):
    tab = chrome.new_tab("https://discord.com/channels/@me")
    if "channels" in tab.url or ".com/app" in tab.url:
        pass
    else:
        if discord and discord.token:
            tab.set.local_storage("token", f'"{discord.token}"')
            tab.get("https://discord.com/channels/@me")
    return tab


def LoginDiscord(chrome:ChromiumPage,env):
    updateAccountStatus(env.discord_id, 0, "重置了Discord登录状态")
    with app.app_context():
        discord: Account = Account.query.filter_by(id=env.discord_id).first()
        if discord:
            tab = LoginDiscordByToken(discord, chrome, env)
            if tab.s_ele("Please log in again"):
                tab.ele("@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85").click()
            if "login" in tab.url:
                tab.refresh(ignore_cache=True)
                tab.get("https://discord.com/login")
                logger.info(f"{env.name} 刷新页面并清空缓存 -> 开始登录 Discord 账号")
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
                tab.listen.start("https://discord.com/api/v9/science")
                tab.wait.url_change("channels", timeout=15, raise_err=False)
                if "channels" in tab.url or ".com/app" in tab.url:
                    tab.refresh()
                    res = tab.listen.wait(timeout=30, raise_err=False)
                    if res:
                        try:
                            updateAccountToken(env.discord_id, res.request.headers["Authorization"])
                            updateAccountStatus(env.discord_id, 2, "登录成功，并获取到Authorization")
                            logger.info(f"{env.name} Discord -> 获取token并登录成功！")
                        except KeyError as e:
                            logger.warning(f"{env.name} Discord -> 获取token失败，但是登录可能成功！")
                    else:
                        updateAccountStatus(env.discord_id, 2, "登录成功，但是没有获取到Authorization")
                        logger.warning(f"{env.name} Discord -> 获取token失败，但是登录可能成功！")
                else:
                    logger.warning(f"{env.name} Discord登录异常，可能登录失败！")
                    chrome.activate_tab(id_ind_tab=tab)
                    updateAccountStatus(env.discord_id, 1, "等待登录超时，可能登录失败！")
                tab.listen.stop()
            else:
                updateAccountStatus(env.discord_id, 2, "登录成功，并获取到Authorization")
                logger.info(f"{env.name} 通过token -> 登录Discord成功")
            return get_Custome_Tab(tab)


def LoginOutlookByCookies(chrome, outlook, env):
    tab = chrome.get_tab(url=".com/mail/0/")
    if tab is None:
        tab = chrome.new_tab(url="https://outlook.live.com/mail/0/")
    # if "outlook" in outlook.name or "hotmail" in outlook.name:
    #     tab.wait.url_change("microsoft", timeout=3, raise_err=False)
    #     tab.wait.url_change("https://outlook.live.com/mail/0/", timeout=5, raise_err=False)
    #     if "microsoft" in tab.url or "login.srf" in tab.url:
    #         if outlook and outlook.token:
    #             tab.set.cookies(json.loads(outlook.token))
    #             chrome.get(url="https://outlook.live.com/mail/0/")
    return tab

def LoginOutlook(chrome:ChromiumPage,env):
    updateAccountStatus(env.outlook_id, 0, "重置了OutLook登录状态")
    with app.app_context():
        outlook: Account = Account.query.filter_by(id=env.outlook_id).first()
        if outlook:
            tab = LoginOutlookByCookies(chrome, outlook, env)
            if "outlook" in outlook.name or "hotmail" in outlook.name:
                tab.wait.url_change("microsoft", timeout=3, raise_err=False)
                tab.wait.url_change("https://outlook.live.com/mail/0/", timeout=5, raise_err=False)
                if "microsoft" in tab.url or "login.srf" in tab.url:
                    logger.info(f"{env.name}: 开始登陆 outlook邮箱")
                    if "login.srf" not in tab.url:
                        tab = tab.eles("@aria-label=Sign in to Outlook")[4].click.for_new_tab()
                    tab.wait.eles_loaded('@data-testid=i0116', timeout=3, raise_err=False)
                    if tab.s_ele("@data-testid=i0116"):
                        tab.ele("@data-testid=i0116").input(outlook.name, clear=True)
                    if tab.s_ele("@type=submit"):
                        tab.ele("@type=submit").click()
                    if tab.s_ele("@name=passwd"):
                        if tab.s_ele("@id=userDisplayName"):
                            text = tab.ele("@id=userDisplayName").text
                            logger.debug(f"{env.name}: 当前准备登录的邮箱 {outlook.name}, 正在登录的邮箱：{text}")
                            if text == outlook.name:
                                if tab.s_ele("@id=idA_PWD_SwitchToPassword"):
                                    ele = tab.ele("@id=idA_PWD_SwitchToPassword")
                                    if "password" in ele.text:
                                        ele.click()
                                tab.ele("@name=passwd").input(aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
                            else:
                                if tab.s_ele("@data-testid=secondaryContent"):
                                    othertab_buttons = tab.ele("@data-testid=secondaryContent").children()
                                    if len(othertab_buttons) >=3:
                                        othertab_buttons[2].click()
                                        tab.wait.url_change("https://login.live.com/ppsecure/secure.srf?", timeout=8, raise_err=False)
                                    else:
                                        tab.ele("@aria-label=Back").click()
                                    tab.wait.eles_loaded('@data-testid=i0116', timeout=6, raise_err=False)
                                    if tab.s_ele("@data-testid=i0116"):
                                        tab.ele("@data-testid=i0116").input(outlook.name, clear=True)
                                    if tab.s_ele("@type=submit"):
                                        tab.ele("@type=submit").click()
                                    tab.ele("@name=passwd").input(aesCbcPbkdf2DecryptFromBase64(outlook.pwd))
                    tab.wait.eles_loaded('t:button@tx():Sign in', timeout=2.1, raise_err=False)
                    if tab.s_ele("t:button@tx():Sign in"):
                        tab.ele("t:button@tx():Sign in").click()
                    if tab.s_ele("@aria-label=Skip for now"):
                        logger.debug(f"{env.name}: 邮箱 Skip for now")
                        tab.ele("@aria-label=Skip for now").click()
                    if tab.s_ele("t:button@tx():Next"):
                        tab.ele("t:button@tx():Next").click()
                    if tab.s_ele("@type=checkbox"):
                        tab.ele("@type=checkbox").click()
                    if tab.s_ele('t:button@tx():Yes'):
                        tab.ele('t:button@tx():Yes').click()
            else:
                logger.info(f"{env.name}: 邮箱格式不匹配,不登录邮箱")
                return
        else:
            logger.info(f"{env.name}: 邮箱 账号为空，跳过登录")
            return
    tab.wait.url_change("https://outlook.live.com/mail/0", timeout=8, raise_err=False)
    if "https://outlook.live.com/mail/0" in tab.url:
        logger.info(f"{env.name}: 登录OUTLOOK成功")
        updateAccountStatus(env.outlook_id, 2)
    else:
        chrome.activate_tab(id_ind_tab=tab)
        logger.warning(f"{env.name}: 登录OUTLOOK失败~")
        updateAccountStatus(env.outlook_id, 1, "邮箱登录失败~")



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
            okxLoginThread = createThread(LoginOKXWallet, (chrome, env,))
            discordLoginThread = createThread(LoginDiscord, (chrome, env,))
            twLoginThread = createThread(LoginTW, (chrome, env,))
            outlookLoginThread = createThread(LoginOutlook, (chrome, env,))
            okxLoginThread.join()
            discordLoginThread.join()
            twLoginThread.join()
            outlookLoginThread.join()
            logger.info(ChromiumOptions().address)
            updateEnvStatus(env.name, 2)
            return chrome
        except Exception as e:
            quitChrome(env, chrome)
            raise e

def DebugChrome(env):
    with app.app_context():
        # 记录开始时间
        start_time = time.perf_counter()
        proxy = Proxy.query.filter_by(id=env.t_proxy_id).first()
        chrome = getChrome(proxy,env)
        chrome.get_tab(title="Initia Wallet").close()
        # LoginINITWallet(chrome, env)
        okxLoginThread = createThread(LoginOKXWallet, (chrome,env,))
        # LoginPhantomWallet(chrome, env)
        discordLoginThread = createThread(LoginDiscord, (chrome,env,))
        twLoginThread = createThread(LoginTW, (chrome,env,))
        outlookLoginThread = createThread(LoginOutlook, (chrome,env,))
        okxLoginThread.join()
        discordLoginThread.join()
        twLoginThread.join()
        outlookLoginThread.join()
        # chrome.new_tab("https://discord.com/invite/wwY5KvYFPC")
        # LoginBitlight(chrome, env)
        logger.info(ChromiumOptions().address)
        updateEnvStatus(env.name, 2)
        # 记录结束时间
        end_time = time.perf_counter()
        # 计算执行时间
        elapsed_time = end_time - start_time
        logger.debug(f"{env.name} 登录用时：{elapsed_time}秒")

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
        envs = Env.query.filter_by(group="qinxiaobo").all()
        for env in envs:
            tw = Account.query.filter_by(id=env.tw_id).first()
            discord = Account.query.filter_by(id=env.discord_id).first()
            if tw:
                print(tw.name)
            if discord:
                print(discord.token)

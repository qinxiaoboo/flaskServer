from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
# 连接数据库
from flaskServer.config.connect import app
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
import time
import random

from flaskServer.utils.chrome import quitChrome

#项目名称
name = 'passport'

#项目链接
Passport_url = 'https://passport.gitcoin.co/#/'
okx_js = '''let button  = 
document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connector-list").shadowRoot.querySelector("wui-flex > w3m-connect-announced-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button > wui-text");
button.click();
'''
civic_url = 'https://getpass.civic.com/?scope=uniqueness,captcha,liveness&chain=polygon,arbitrum%20one,xdc,ethereum,fantom,optimism,base,avalanche&referrer=gitcoin-passport'
civic_okx_js = '''let button  = 
document.querySelector("body > div:nth-child(7) > div > div > div._9pm4ki5.ju367va.ju367v15.ju367v8r > div > div > div > div > div.iekbcc0.ju367va.ju367v15.ju367v4y._1vwt0cg3 > div.iekbcc0.ju367v6p._1vwt0cg2.ju367v7a.ju367v7v > div:nth-child(2) > div:nth-child(1) > button > div > div");
button.click();
'''
civic_wallet = '''
let button  = 
document.querySelector("#root > div > div.main-container.flex.flex-col.p-5.wide\\:p-0.wide\\:pt-5.z-1.relative.bg-gray-50 > div.mb-5 > div > div > button");
button.click();
'''
def exe_okx(chrome,env):
    try:
        chrome.wait(3, 4)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
        chrome.wait(3, 4)
        try:
            chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
        except Exception as e:
            print('不需要二次确认')
    except Exception as e:
        print(f'{env.name}取的ele不对')
    return
def getCivicPass(chrome,env):
    tab = chrome.new_tab(url=civic_url)
    tab.set.window.max()
    time.sleep(2)
    try:
        try:
            print('连接钱包')
            if tab.s_ele('Connect Wallet', index=1):
                print('通过第一个按钮点击')
                tab.ele('Connect Wallet', index=1).click()
            elif tab.s_ele('Connect Wallet', index=2):
                print('通过第二个按钮点击')
                tab.ele('Connect Wallet', index=2).click()
            else:
                print('通过js点击')
                tab.run_js(civic_wallet)
        except Exception as e:
            print('已经登录了无需登录')
            logger.error(e)

        try:
            if tab.s_ele('Polygon'):
                time.sleep(2)
                print('选择链')
                tab.ele('Polygon').click()
                time.sleep(2)
                print('选择钱包')
                tab.run_js(civic_okx_js)
                time.sleep(2)
                print('钱包确认')
                exe_okx(chrome, env)
                time.sleep(2)
        except Exception as e:
                logger.error(e)

        try:
            print('点击选择方式')
            tab.ele('Uniqueness - Proof of Personhood').click()
            time.sleep(2)
            try:
                tab.ele('CAPTCHA Verification').click()
                print('等待人机验证')
                if tab.s_ele('Your Civic Pass request has been rejected.'):
                    print('有问题需要换vpn节点')
                time.sleep(30)


            except Exception as e:
                print('没有该元素或者选择失败')
                logger.error(e)

        except Exception as e:
            logger.error(e)

    except Exception as e:
        logger.error(e)


def getCount(chrome, env,score):
    try:
        taskData = getTaskObject(env, name)
        #tab = chrome.new_tab(url=Passport_url)
        time.sleep(2)
        print('上传gitcoin分数')
        gitcoin_score = float(score)
        print('gitcoin_score:', gitcoin_score)
        taskData.Score = gitcoin_score
        updateTaskRecord(env.name, name, taskData, 1)
    except Exception as e:
        logger.error(e)

def getHumanityScore(chrome,env):
    tab = chrome.new_tab(url=Passport_url)
    time.sleep(2)
    try:
        print('点击Sign in with Ethereum ')
        tab.ele('@class=inline group-disabled:hidden').click()
        time.sleep(2)
        print('选择okx钱包并点击')
        try:
            tab.run_js(okx_js)
            time.sleep(2)
            print('钱包确认')
            exe_okx(chrome, env)
            time.sleep(2)
            print('点击Get Started')
            tab.ele('Get Started').click()
            time.sleep(2)
        except Exception as e:
            logger.error(e)
        num = tab.ele('@class=text-background-5 text-5xl').text
        num2 = float(num)
        getCount(chrome, env, num2)
        # if num2 < 1.5:
        #     print('需要验证积分')
        #     #getCivicPass(chrome, env)
    except Exception as e:
        logger.error(e)

def PassPort(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getHumanityScore(chrome, env)

            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)
import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
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
from flaskServer.config.connect import db
from flaskServer.mode.account import Account
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.chromes.login import tw2faV
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
from threading import Thread
from flaskServer.services.chromes.login import LoginDiscord
from flaskServer.utils.chrome import quitChrome
from flaskServer.utils.decorator import chrome_retry
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.services.chromes.login import LoginTW
import time
import string



#项目名称
name = 'now chain'
#项目邀请链接
now_chain_url = 'https://testnet.nowchain.co/testnet/point-system?referral=0xECB41b49D74D7d13bB51f9603Fd2360557647504/'
faucet_url= 'https://faucet.nowchain.co/'
switch_Network = '''let button  =
document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-unsupported-chain-view").shadowRoot.querySelector("wui-flex > wui-flex:nth-child(2) > wui-list-network:nth-child(2)");
button.click();
'''
okx_url = '''let button  =
document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-announced-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet:nth-child(1)");
button.click();'''




def exe_okx(chrome):
    try:
        chrome.wait(3, 4)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
    except Exception as e:
        print("取的ele不对")
        logger.error(e)
    return

def getCount(chrome, env):
    try:
        taskData = getTaskObject(env, name)
        tab = chrome.new_tab(url=now_chain_url)
        taskData.check_in = 1
        taskData.Liquidity = 1
        taskData.Faucet = 1
        taskData.Swap = 1
        taskData.Leaderboard = 1
        taskData.Bridge = 1
        updateTaskRecord(env.name,name,taskData,1)
        tab.close()

    except Exception as e:
        logger.error(e)

def getTab(chrome,env):
    tab = chrome.new_tab(url=now_chain_url)
    time.sleep(5)
    # 设置全屏
    tab.set.window.max()
    #登录钱包
    try:
        if tab.s_ele('Connect Wallet'):
            print('开始链接钱包')
            tab.ele('Connect Wallet').click()
            time.sleep(5)
            try:
                tab.run_js(okx_url)
                time.sleep(5)
                exe_okx(chrome)
                time.sleep(5)
            except Exception as e:
                logger.error(e)
            try:
                print('开始选择测试网')
                tab.run_js(switch_Network)
                time.sleep(5)
                exe_okx(chrome)
                time.sleep(5)
            except Exception as e:
                logger.error(e)
        try:
            print('开始选择测试网')
            tab.run_js(switch_Network)
            time.sleep(5)
            exe_okx(chrome)
            time.sleep(5)
        except Exception as e:
            logger.error(e)
    except Exception as e:
        logger.error(e)

def getFaucet(chrome, env):
    getTab(chrome, env)
    time.sleep(5)
    print('开始领水')
    tab = chrome.new_tab(url='https://testnet.nowchain.co/testnet/faucet/')
    try:
        if tab.s_ele('Time remaining: '):
            print('领水时间还没到：',tab.ele('Time remaining: ').text)
            return
        elif tab.s_ele('t:button@tx():Request Assets'):
            logger.info('开始等待人机验证')
            time.sleep(60)
            tab.wait.ele_displayed('t:button@tx():Request Assets', timeout=60)
            tab.ele('t:button@tx():Request Assets').click()
            time.sleep(15)
    except Exception as e:
        logger.error(e)


def getChck_in(chrome,env):
    # getTab(chrome, env)
    tab = chrome.new_tab(url=now_chain_url)
    time.sleep(5)
    chrome.refresh(ignore_cache= True)
    time.sleep(5)
    #登录钱包
    try:
        if tab.s_ele('t:button@tx():Checked'):
            logger.info('已经签到完成,或者还没有到签到时间')
            return
        elif tab.s_ele('t:button@tx():Check-in'):
            print('开始签到')
            tab.wait.ele_displayed('t:button@tx():Check-in', timeout=20)
            tab.ele('t:button@tx():Check-in').click()
            time.sleep(5)
            exe_okx(chrome)
            time.sleep(20)

    except Exception as e:
        logger.error(e)


def NowChain(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getCount(chrome, env)
            # getFaucet(chrome, env)
            # getChck_in(chrome,env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)
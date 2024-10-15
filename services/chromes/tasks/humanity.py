import string

from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
# 连接数据库
from flaskServer.config.connect import app
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.dto.account import updateAccountStatus
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
import time
import random
from flaskServer.utils.chrome import quitChrome


#humanity protocol
name = 'humanity'
humanity_url = 'https://testnet.humanity.org/login?ref=sunyunlei'

wallet_js = '''
let button  = 
document.querySelector("body > div:nth-child(31) > div > div > div._9pm4ki5.ju367va.ju367v15.ju367v8r > div > div > div > div > div > div.iekbcc0.ju367v6p._1vwt0cg2.ju367v7a.ju367v7v > div.iekbcc0.ju367va.ju367v15.ju367v1n > div:nth-child(1) > button > div > div");
button.click();
'''
dis_js = '''
let button  = 
document.querySelector("body > div.MuiBox-root.mui-186aokm > div > div > div > div.MuiBox-root.mui-1i3hx1p > div > div > div.MuiBox-root.mui-17age7i > a:nth-child(2)");
button.click();
'''

def exe_okx(chrome,env):
    try:
        if chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2):
            chrome.wait(3, 4)
            chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
            chrome.wait(3, 4)
            try:
                chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
            except Exception as e:
                print('不需要二次确认')
    except Exception as e:
        print(f'{env.name}取的ele不对或者不需要连接')

def LoginDiscord(chrome:ChromiumPage,env):
    updateAccountStatus(env.discord_id, 0, "重置了Discord登录状态")
    tab = chrome.new_tab(url="https://discord.com/app")
    if tab.s_ele("Please log in again"):
        tab.ele("@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85").click()

def generate_random_word(length=7):
    # 生成一个随机的字母单词
    letters = string.ascii_lowercase + string.digits  # 包含小写字母、大写字母和数字
    return ''.join(random.choice(letters) for _ in range(length))

def gethumanity(chrome,env):
    tab = chrome.new_tab(url=humanity_url)
    tab.set.window.max()
    time.sleep(2)
    try:
        if tab.s_ele('Get Started'):
            try:
                tab.run_js(dis_js)
            except Exception as e:
                logger.info("之前登录过不需要再登录")
            time.sleep(2)
            #disocrd 授权过程
            try:
                logger.info(f'{env.name}:开始判断登录discord情况')
                print(tab.title)
                num = 0
                while num < 4:
                    if tab.title != '502 Server Error':
                        print('一切通畅')
                        break
                    elif tab.title == '502 Server Error':
                        print('跳转失败')
                        num += 1
                        time.sleep(30)
                        print('开始刷新')
                        chrome.refresh(ignore_cache=True)
                        if num == 3:
                            if tab.title == '502 Server Error':
                                print('还是无法登录需要关闭网页')
                                quitChrome(env, chrome)

                if chrome.get_tab(title='Discord | Authorize access to your account'):
                    print('Discord | Authorize access to your account进入')
                    chrome.get_tab(title='Discord | Authorize access to your account').ele("@type=button",index=2).click()
                    logger.info(f"{env.name}: 登录discord完成----------------------------------")
                    time.sleep(10)
                elif chrome.get_tab(title='Discord | 授权访问您的账号'):
                    print('Discord | 授权访问您的账号进入')
                    chrome.get_tab(title='Discord | 授权访问您的账号').ele("@type=button", index=2).click()
                    logger.info(f"{env.name}: 登录discord完成----------------------------------")
                    time.sleep(10)
                elif chrome.get_tab(title='Discord'):
                    print('Discord 进入')
                    if tab.s_ele('@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85'):
                        logger.info(f'{env.name}的discord需要重新登录')
                        tab.ele('@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85').click()
                        time.sleep(6)
                        LoginDiscord(chrome, env)
                        time.sleep(6)
                        chrome.close_tabs()
                    elif tab.ele('Welcome back!'):
                        logger.info(f"{env.name}的Discord未登录，尝试重新登录")
                        time.sleep(6)
                        LoginDiscord(chrome, env)
                        time.sleep(6)
                        chrome.close_tabs()
                    elif chrome.get_tab(title='Discord').ele("@type=button",index=2):
                        chrome.get_tab(title='Discord').ele("@type=button", index=2).click()
                        logger.info(f"{env.name}: 登录discord完成----------------------------------")
                        time.sleep(10)
                elif chrome.get_tab('https://discord.com'):
                    print('这是通过网址进去的')
                    chrome.get_tab(title='Discord | Authorize access to your account').ele("@type=button",index=2).click()
                    logger.info(f"{env.name}: 登录discord完成----------------------------------")

                else:
                    logger.info(f'{env.name}:还有其他的语言需要加判断')
            except Exception as e:
                logger.error(e)
            try:
                if tab.s_ele('@class=MuiInputBase-input mui-1qvwndf'):
                    # 首次登录需要的注册，如果不是第一次可能就不需要
                    print('hp_username:',generate_random_word())
                    tab.ele('@class=MuiInputBase-input mui-1qvwndf').input(generate_random_word())
                    time.sleep(2)
                    tab.ele('@class=MuiBox-root mui-171onha', index=2).click()
                    time.sleep(2)
                    print('First Name is:',generate_random_word())
                    tab.ele('@class=MuiInputBase-input mui-1qvwndf', index=1).input(generate_random_word())
                    time.sleep(2)
                    print('Last Name is:',generate_random_word())
                    tab.ele('@class=MuiInputBase-input mui-1qvwndf', index=2).input(generate_random_word())
                    time.sleep(2)
                    tab.ele('@class=MuiBox-root mui-171onha', index=2).click()
                    time.sleep(10)

                try:
                    if tab.s_ele('@class=skip'):
                        tab.ele('@class=skip').click()
                except Exception as e:
                    print('没有出现skip')
                time.sleep(2)
                if tab.s_ele('@class=bottom'):
                    tab.ele('@class=bottom').click()
                    time.sleep(5)
                    try:
                        exe_okx(chrome, env)
                    except Exception as e:
                        print('不需要连接钱包')

            except Exception as e:
                logger.error(e)
    except Exception as e:
        logger.error(e)

def NowChain(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            gethumanity(chrome, env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)
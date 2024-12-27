from flaskServer.utils.chrome import quitChrome
import pandas as pd
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
import random
# 连接数据库
from flaskServer.config.connect import app
#数据库信息
from flaskServer.mode.env import Env
import time
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome


humanity_url = 'https://testnet.humanity.org/login?ref=sunyunlei'
humanity_wallet = 'D:\桌面\humanity_wallet.xlsx'

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
def getDiscord(chrome,env):
    try:
        print('开始discord认证')
        if chrome.get_tab(title='Discord | Authorize access to your account'):
            print('Discord | Authorize access to your account进入')
            chrome.get_tab(title='Discord | Authorize access to your account').ele("@type=button", index=2).click()
            logger.info(f"{env.name}: 登录discord完成----------------------------------")
            time.sleep(10)
        elif chrome.get_tab(title='Discord | 授权访问您的账号'):
            print('Discord | 授权访问您的账号进入')
            chrome.get_tab(title='Discord | 授权访问您的账号').ele("@type=button", index=2).click()
            logger.info(f"{env.name}: 登录discord完成----------------------------------")
            time.sleep(10)
        elif chrome.get_tab(title='Discord'):
            print('Discord 进入')
            # if tab.s_ele('@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85'):
            #     logger.info(f'{env.name}的discord需要重新登录')
            #     tab.ele('@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85').click()
            #     time.sleep(6)
            #     LoginDiscord(chrome, env)
            #     time.sleep(6)
            #     chrome.close_tabs()
            # elif tab.ele('Welcome back!'):
            #     logger.info(f"{env.name}的Discord未登录，尝试重新登录")
            #     time.sleep(6)
            #     LoginDiscord(chrome, env)
            #     time.sleep(6)
            #     chrome.close_tabs()
            if chrome.get_tab(title='Discord').ele("@type=button", index=2):
                chrome.get_tab(title='Discord').ele("@type=button", index=2).click()
                logger.info(f"{env.name}: 登录discord完成----------------------------------")
                time.sleep(10)
        elif chrome.get_tab('Onboarding | Humanity Protocol'):
            print('Onboarding | Humanity Protocol进去的')
            chrome.get_tab(title='Onboarding | Humanity Protocol').ele("@type=button", index=2).click()
            logger.info(f"{env.name}: 登录discord完成----------------------------------")
        else:
            logger.info(f'{env.name}:还有其他的语言需要加判断')
    except Exception as e:
        logger.error(e)

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
            time.sleep(10)
            #disocrd 授权过程
            try:
                logger.info(f'{env.name}:开始判断登录discord情况')
                print('title', chrome.get_tab(url='https://discord.com/').title)
                getDiscord(chrome, env)
            except Exception as e:
                logger.error(e)
            time.sleep(10)
        chrome.wait(10)
        try:
            if tab.s_ele('@class=skip'):
                print('点击skip弹幕')
                tab.ele('@class=skip').click()
            else:
                time.sleep(10)
                tab.ele('@class=skip').click()
        except Exception as e:
            print('没有出现skip')
        time.sleep(2)
        try:


            data = []
            wallet = tab.ele('@class=chain', index=2).text
            print('wallet:', wallet)
            # 新数据
            new_data = pd.DataFrame([{
                '环境编号': env.name,
                '钱包地址': wallet
            }])
            # 尝试读取已有数据
            try:
                # 打开已存在的 Excel 文件
                existing_data = pd.read_excel(humanity_wallet, sheet_name='Sheet1')
                df = pd.DataFrame(existing_data)
            except FileNotFoundError:
                # 如果文件不存在，创建空的 DataFrame
                existing_data = pd.DataFrame()
            # 将新数据追加到 DataFrame
            df = pd.concat([existing_data, new_data], ignore_index=True)
            # 使用 openpyxl 的 engine 保存数据
            with pd.ExcelWriter(humanity_wallet, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')




        except Exception as e:
            logger.info(e)
    except Exception as e:
        logger.error(e)


def humanityWallet(env):
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



# def toDo(env):
#     with app.app_context():
#         logger.info(f"======开始执行{env.name}环境")
#         try:
#             chrome: ChromiumPage = OKXChrome(env)
#             gethumanity(chrome, env)
#             # ------------循环打开网页的重要步骤----------------
#             logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
#             chrome.quit()
#
#         except Exception as e:
#             logger.error(f"{env.name}: {e}")
#
#             #------------循环打开网页的重要步骤----------------
#             if chrome:
#                 chrome.quit()
#
# if __name__ == '__main__':
#
#     # with app.app_context():
#     #     env = Env.query.filter_by(name="ZLL-6").first()
#     #     toDo(env)
# # # ------------循环打开网页的重要步骤----------------
#     submit(toDo, getAllEnvs())
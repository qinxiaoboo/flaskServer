
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
# 连接数据库
from flaskServer.config.connect import app
import time
from flaskServer.services.chromes.login import OKXChrome
#数据库信息
from flaskServer.mode.env import Env


#项目名称
name = 'NowChain'
#项目邀请链接
now_chain_url = 'https://testnet.nowchain.co/testnet/point-system?referral=0xECB41b49D74D7d13bB51f9603Fd2360557647504/'
switch_Network = '''let button  =
document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-unsupported-chain-view").shadowRoot.querySelector("wui-flex > wui-flex:nth-child(2) > wui-list-network:nth-child(2)");
button.click();
'''

okx_url = '''let button  =
document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-announced-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet:nth-child(1)");
button.click();'''



def exe_okx(chrome,env):
    try:
        chrome.wait(3, 4)
        if chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2):
            chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
    except Exception as e:
        print(f'{env.name}取的ele不对')
    return

def getTab(chrome,env):
    tab = chrome.new_tab(now_chain_url)
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
                exe_okx(chrome,env)
                time.sleep(5)
            except Exception as e:
                print('不需要钱包验证')
            try:
                print('开始选择测试网')
                tab.run_js(switch_Network)
                time.sleep(5)
                exe_okx(chrome,env)
                time.sleep(5)
            except Exception as e:
                print('不需要选择测试网了')
        try:
            print('开始选择测试网')
            tab.run_js(switch_Network)
            time.sleep(5)
            exe_okx(chrome,env)
            time.sleep(5)
        except Exception as e:
            print('不需要选择测试网了')
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
        elif tab.s_ele('t:button@tx():Request Assets'):
            logger.info('开始等待人机验证')
            #------------------------------待测试是否需要去掉
            time.sleep(60)
            #--------------------------
            tab.wait.ele_displayed('t:button@tx():Request Assets', timeout=60)
            tab.ele('t:button@tx():Request Assets').click()
            time.sleep(15)
    except Exception as e:
        logger.error(e)


# def toDo(env):
#     with app.app_context():
#         logger.info(f"======开始执行{env.name}环境")
#         try:
#             chrome: ChromiumPage = OKXChrome(env)
#             getFaucet(chrome, env)
#
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
#
#     submit(toDo, getAllEnvs())


#_________________________________需要单个跑的——————————————————————————————————————————


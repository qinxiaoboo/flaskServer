
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
# 连接数据库
from flaskServer.config.connect import app
#数据库信息
from flaskServer.mode.env import Env
import time
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome


Faucet_url = 'https://faucet.testnet.humanity.org/'

def getFaucet(chrome,env):
    tab = chrome.new_tab(url=Faucet_url)
    try:
        with open('D:/桌面/humanity测币领取地址.txt', mode='r', encoding='utf-8') as f:
            for i in f.readlines():
                chrome.wait(3, 4)
                print('addr:', i)
                tab.ele('@placeholder=Enter your address or ENS name').input(i, clear=True)
                time.sleep(2)
                tab.ele('@class=button is-primary is-rounded').click()
                time.sleep(60)
    except Exception as e:
        logger.error(e)
def toDo(env):
    with app.app_context():
        logger.info(f"======开始执行{env.name}环境")
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getFaucet(chrome,env)

        except Exception as e:
            logger.error(f"{env.name} 执行异常：{e}")
            raise e


if __name__ == '__main__':
    # toDoFaucet("ETH")
    with app.app_context():
        env = Env.query.filter_by(name="ZLL-11").first()
        toDo(env)


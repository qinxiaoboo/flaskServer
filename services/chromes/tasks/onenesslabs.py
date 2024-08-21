import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
import random
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


name = "Onenesslabs"
home_page = 'https://task.onenesslabs.io/'


def getOnenesslabs(chrome,env):
    tab = chrome.new_tab(home_page)
    chrome.wait(5,7)
    #处理欢迎页面
    if tab.ele('.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 bg-[#D6B635] mx-[40px] mt-[12px] h-[48px] rounded-full text-black font-[Bangers] text-[20px] hover:scale-[1.1] cursor-pointer'):
        tab.ele('.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 bg-[#D6B635] mx-[40px] mt-[12px] h-[48px] rounded-full text-black font-[Bangers] text-[20px] hover:scale-[1.1] cursor-pointer').click()
    chrome.wait(1, 2)

    #登录discord
    if tab.ele('@type=button',index=1):
        tab.ele('@type=button',index=1).click.for_new_tab().wait(5,6).ele('type=button').click()
        # chrome.wait(5, 6)
        # authorize = chrome.get_tab(url='discord.com')
        # chrome.wait(2,3)
        # authorize.ele('type=button').click()

        # chrome.wait(7,8)

        # 链接钱包待执行













def toDo(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getOnenesslabs(chrome,env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
            #chrome.quit()
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            if chrome:
                #chrome.quit()
                pass

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="ZLL-1").first()
        toDo(env)
















import random

from DrissionPage import ChromiumPage
from loguru import logger

# 连接数据库
from flaskServer.config.connect import app

#数据库信息
from flaskServer.mode.env import Env

#配置代理
from flaskServer.mode.proxy import Proxy

#创建浏览器
from flaskServer.services.chromes.worker import submit

#变量
from flaskServer.services.content import Content

#登录环境账号
from flaskServer.services.chromes.login import OKXChrome


name = "Seeker Alliance"
seekerUrl = "https://seekersalliance-movement.vercel.app/createprofile"



def getTab(chrome, env):
    tab = chrome.new_tab(seekerUrl)
    #登录钱包
    tab.ele('t:a').click.for_new_tab().ele("@w-[100%] focus:outline-none text-body placeholder:text-body placeholder-brand-grey-300 bg-brand-grey-900 text-brand-grey-300 focus:none").input("GalxeStream!").ele(type="button").click.ele('@text-center text-base flex justify-center items-center transition-all duration-300 overflow-hidden cursor-pointer bg-brand-purple-300 text-brand-grey-100 border-transparent hover:bg-brand-purple-400 rounded-8 text-body px-[12px] py-[9px] h-10').click()
















def toDo(env):
    logger.info(f"======开始执行{env.name}环境")
    try:
        chrome: ChromiumPage = OKXChrome(env)
        tab = getTab(chrome, env)
        # tab = getTab(chrome,env)
        # if tab:
        #     tab.get("https://miles.plumenetwork.xyz/daily-checkin")

    except Exception as e:
        logger.error(f"{env.name} 执行异常：{e}")
        raise e

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="SYL-21").first()
        toDo(env)


















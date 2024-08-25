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
from flaskServer.config.connect import db
from flaskServer.mode.account import Account
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.chromes.login import tw2faV
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
from threading import Thread
from flaskServer.services.chromes.login import LoginDiscord



name = "Onenesslabs"
home_page = 'https://task.onenesslabs.io/?code=Z73s9'

click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connector-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """

#登录账号
def getOnenesslabs(chrome,env):

    tab = chrome.new_tab(home_page)

    #处理欢迎页面
    if tab.s_ele("I'm Ready to Fight!"):
        tab.ele("I'm Ready to Fight!").click()
    #登录discord
    if tab.s_ele('SIGN IN WITH DISCORD',index=1):
        discord = tab.ele('SIGN IN WITH DISCORD',index=1).click.for_new_tab()
        time.sleep(10)
        try:
            if discord.s_ele('@class=text-md/medium_dc00ef label_ac2a99'):
                discord.ele("@type=button", index=2).click()
                chrome.wait(7,10)
                logger.info(f"{env.name}: Discord已登录，授权中")
                if tab.s_ele("SIGN IN WITH DISCORD"):
                    logger.info(f"{env.name}: Discord 授权或者登录失败~")
                    chrome.quit()
                else:
                    logger.info(f"{env.name}: Discord 授权成功~")
            else:
                logger.info(f"{env.name}: Discord未登录，尝试重新登录")
                discord.close()
                LoginDiscord(chrome,env)
                getOnenesslabs(chrome, env)

            chrome.wait(7,9)
        except Exception as e:
            logger.info(f"{env.name}: Discord未登录，账号登录失败")
            chrome.quit()

    # 获取表头
    headers = tab.ele("@class=flex justify-center items-center").eles("c:button")
    # 鼠标指针移动到头像
    tab.actions.move_to(headers[2])

    # 连接钱包
    if tab.s_ele("LINK YOUR WALLET"):
        tab.ele("LINK YOUR WALLET").click()
        chrome.wait(1, 2)
        okxbutton = tab.run_js(click_wallet_js)
        logger.info(f"{env.name}: 链接钱包")
        okxbutton.click.for_new_tab().wait(2,3).ele("@type=button").next().click()
        chrome.wait(2,3)
        chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        chrome.wait(2, 3)
        logger.info(f"{env.name}: 钱包链接完成")


#完成任务
def Task(chrome,env):
    tab = chrome.new_tab(home_page)
    chrome.wait(4, 5)
    #点击task
    tab.ele("@@class=ant-badge flex justify-center items-center css-loyarq@@tx()=Reward").click()
    # 关注推特
    if tab.s_ele("@tx()=FOLLOW"):
        twitter = tab.ele("@tx()=FOLLOW").click.for_new_tab()
        chrome.wait(8, 10)
        # 登录推特
        if twitter.s_ele("Sign in to X"):
            logger.info(f"{env.name}: 推特未登录，触发登录推特")
            with app.app_context():
                tw: Account = Account.query.filter_by(id=env.tw_id).first()
                if tw:
                    twitter.ele("@autocomplete=username").input(tw.name,clear=True)
                    twitter.ele("@@type=button@@text()=Next").click()
                    twitter.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd),clear=True)
                    twitter.ele("@@type=button@@text()=Log in").click()
                    fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                    if "login" in twitter.url and len(fa2) > 10:
                        tw2faV(twitter, fa2)
                    twitter.ele('@type=button').click()
                    chrome.wait(2)
                else:
                    raise Exception(f"{env.name}: 没有导入TW的账号信息")
        else:
            twitter.ele('@type=button').click()
    else:
        logger.info(f"{env.name}: 关注推特已完成")

    #修改推特名称
    if tab.s_ele("@tx()=ADD", index=-1):
        tab.ele("@tx()=ADD", index=-1).click.for_new_tab().wait(5,7).close()
        if tab.s_ele("Verify"):
            tab.ele("Verify").click()
        logger.info(f"{env.name}: 修改推特名称执行已完成")

    #转发推特
    if tab.s_ele("RETWEET", index=2):
        tab.ele("RETWEET", index=2).click.for_new_tab().wait(5,7).close()
        if tab.s_ele("Verify"):
            tab.ele("Verify").click()
        logger.info(f"{env.name}: 转发推特已完成")

    #发布推文
    if tab.s_ele("SHARE", index=2):
        tab.ele("SHARE", index=2).click.for_new_tab().wait(5,7).close()
        if tab.s_ele("Verify"):
            tab.ele("Verify").click()
        logger.info(f"{env.name}: 发布推文已完成")

    #关闭task弹窗
    tab.ele("@class=relative").child(index=2).click()
    chrome.wait(4,5)

    if tab.s_ele("BET NOW"):
        # 定位第一名
        tab.ele('@alt=crown.png').click()
        chrome.wait(1, 2)
        tab.ele("@@class=ant-badge flex justify-center items-center css-loyarq@@tx():confirm").click()
        chrome.wait(2, 3)
        tab.ele('@alt=close-icon.png',index=1).click(by_js=None)
        logger.info(f"{env.name}: 下注第一名已完成")
    else:
        logger.info(f"{env.name}: 今日下注已完成")
    chrome.wait(4, 5)
    if tab.s_ele("ATTACK NOW"):
        # 定位其它
        tab.eles("@@class=ant-badge flex justify-center items-center css-loyarq@@tx()=ATTACK")[random.randint(1,5)].click()
        chrome.wait(1, 2)
        tab.ele("@@class=ant-badge flex justify-center items-center css-loyarq@@tx():confirm").click()
        chrome.wait(2, 3)
        tab.ele('@alt=close-icon.png', index=1).click(by_js=None)
        logger.info(f"{env.name}: 攻击第五名已完成")
    else:
        logger.info(f"{env.name}: 今日攻击已完成")


# 宝石升级
def Gem(chrome,env):

    tab = chrome.new_tab("https://task.onenesslabs.io/inventory")
    chrome.wait(3,5)
    tab.ele(".flex justify-center items-center").click()
    chrome.wait(2,3)
    tab.ele('@type=number').input(10,clear=True)
    if tab.s_ele("@tx():Not enough fragments"):
        logger.info(f"{env.name}: 宝石不足无法合成")
    else:
        tab.ele(".relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 w-[320px] h-[52px] text-[24px] mt-[16px] bg-home-betButton hover:scale-[1.1] cursor-pointer").click()
        chrome.wait(8, 10)
        if tab.s_ele(".text-[32px] text-white mt-[24px]"):
            num = tab.ele(".inline-block text-white").text
            logger.info(f"{env.name}: 宝石合成失败..... 合成详情：{num}")

        if tab.s_ele(".text-[#D6B635]"):
            num = tab.ele(".inline-block text-[#D6B635]").text
            logger.info(f"{env.name}: 宝石合成成功！合成详情：{num}")


def Oneness(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            a = 0
            try:
                getOnenesslabs(chrome, env)
            except Exception as e:
                logger.info(f"{env.name}: {e} 开始重新执行~")
                a += 1
                if a < 3:
                    chrome.refresh()
                    chrome.wait(3, 5)
                    chrome.close()
                    getOnenesslabs(chrome, env)
                else:
                    logger.info(f"{env.name}: {e} 超出重试次数")

            a = 0
            try:
                Gem(chrome, env)
            except Exception as e:
                logger.info(f"{env.name}: {e} 开始重新执行~")
                a += 1
                if a < 3:
                    chrome.refresh()
                    chrome.wait(3, 5)
                    chrome.close()
                    Gem(chrome, env)
                else:
                    logger.info(f"{env.name}: {e} 超出重试次数")

            a = 0
            try:
                Task(chrome, env)
            except Exception as e:
                logger.info(f"{env.name}: {e} 开始重新执行~")
                a += 1
                if a < 3:
                    chrome.refresh()
                    chrome.wait(3, 5)
                    chrome.close()
                    Task(chrome, env)
                else:
                    logger.info(f"{env.name}: {e} 超出重试次数")

            a = 0
            try:
                Gem(chrome, env)
            except Exception as e:
                logger.info(f"{env.name}: {e} 开始重新执行~")
                a += 1
                if a < 3:
                    chrome.refresh()
                    chrome.wait(3, 5)
                    chrome.close()
                    Gem(chrome, env)
                else:
                    logger.info(f"{env.name}: {e} 超出重试次数")


            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
            chrome.quit()
        except Exception as e:
            logger.error(f"{env.name}: {e}")
            if chrome:
                chrome.quit()

if __name__ == '__main__':
    # with app.app_context():
    #     env = Env.query.filter_by(name="ZLL-112").first()
    #     Oneness(env)
    submit(Oneness,getAllEnvs())
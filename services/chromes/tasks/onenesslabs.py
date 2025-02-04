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
from flaskServer.utils.chrome import quitChrome
from flaskServer.utils.decorator import chrome_retry
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject

name = "Onenesslabs"
home_page = 'https://task.onenesslabs.io/?code=Z73s9'

click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connector-list").shadowRoot.querySelector("wui-flex > w3m-connect-injected-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """

#登录账号
@chrome_retry(exceptions=(Exception, ),max_tries=3, initial_delay=2)
def getOnenesslabs(chrome, env):
    tab = chrome.new_tab(home_page)
    # 设置全屏
    tab.set.window.max()
    tab.refresh()
    chrome.wait(2, 3)

    #处理欢迎页面
    if tab.s_ele("I'm Ready to Fight!"):
        tab.ele("I'm Ready to Fight!").click()
    #处理弹窗
    if tab.s_ele(
            '.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 font-[Bangers] text-[20px] flex-1 bg-[#D6B635] text-black h-[48px] rounded-full mt-[30px] hover:scale-[1.1] cursor-pointer'):
        tab.ele(
            '.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 font-[Bangers] text-[20px] flex-1 bg-[#D6B635] text-black h-[48px] rounded-full mt-[30px] hover:scale-[1.1] cursor-pointer').click()

    #处理弹窗
    if tab.s_ele('@alt=close-icon.png',index=2):
        tab.ele('@alt=close-icon.png',index=2).click()

    #登录discord
    if tab.s_ele('SIGN IN WITH DISCORD',index=1):
        discord = tab.ele('SIGN IN WITH DISCORD',index=1).click.for_new_tab()
        discord.set.window.max()
        time.sleep(5)
        try:
            if discord.s_ele('@class=text-md/normal_dc00ef label_ac2a99'):
                discord.ele("@type=button", index=2).click()
                chrome.wait(4, 6)
                logger.info(f"{env.name}: Discord已登录，授权中")
                chrome.wait(7, 8)

                if tab.s_ele("SIGN IN WITH DISCORD"):

                    try:
                        raise AttributeError("Discord 授权或者登录失败~")
                    except AttributeError as e:
                        return ("失败", e)
                    finally:
                        quitChrome(env, chrome)

                if tab.s_ele("Please log in again"):
                    tab.ele("@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85")

                else:
                    logger.info(f"{env.name}: Discord 授权成功~")

            else:
                logger.info(f"{env.name}: Discord未登录，尝试重新登录")
                discord.close()
                LoginDiscord(chrome,env)

            chrome.wait(7, 9)
        except Exception as e:
            logger.info(f"{env.name}: Discord未登录，账号登录失败")
            quitChrome(env, chrome)
            return ("Discord未登录，账号登录失败", e)



    # 处理授权成功后的弹窗

    tab.refresh()
    chrome.wait(3, 6)
    # 获取表头
    try:
        headers = tab.ele("@class=flex justify-center items-center").eles("c:button")
        # 鼠标指针移动到头像
        tab.actions.move_to(headers[2])
    except Exception as e:
        chrome.wait(3, 6)
        headers = tab.ele("@class=flex justify-center items-center").eles("c:button")
        # 鼠标指针移动到头像
        tab.actions.move_to(headers[2])

    # 连接钱包
    if tab.s_ele("LINK YOUR WALLET"):
        tab.ele("LINK YOUR WALLET").click()
        chrome.wait(1, 2)
        okxbutton = tab.run_js(click_wallet_js)
        logger.info(f"{env.name}: 链接钱包")
        okxbutton.click.for_new_tab().wait(2, 3).ele("@type=button").next().click()
        chrome.wait(2, 3)
        chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        chrome.wait(2, 3)
        logger.info(f"{env.name}: 钱包链接完成")

    tab.close()

######   oneness 数据统计   ######
def getCount(chrome, env):
    try:
        taskData = getTaskObject(env, name)
        env_name = env.name
        tab = chrome.new_tab(home_page)
        chrome.wait(2, 4)
        logger.info(f"{env.name}: 统计oneness碎片")
        onss = tab.ele('@class=font-bold text-[16px] text-[#EAAE75]', index=2).text

        chrome.wait(2, 4)
        tab.ele('@class=ant-badge flex justify-center items-center css-loyarq', index=11).click()
        chrome.wait(2, 4)

        logger.info(f"{env.name}: 统计L1~L5宝石个数")
        lv_1 = tab.s_ele('@class=leading-none', index=1).text
        lv_2 = tab.s_ele('@class=leading-none', index=2).text
        lv_3 = tab.ele('@class=leading-none', index=3).text
        lv_4 = tab.ele('@class=leading-none', index=4).text
        lv_5 = tab.ele('@class=leading-none', index=5).text

        chrome.wait(2, 4)
        logger.info(f"{env.name}: 统计Task签到天数")
        tab.back(1)
        chrome.wait(2, 4)
        tab.ele('@class=ant-badge flex justify-center items-center css-loyarq', index=13).click()
        chrome.wait(2, 4)

        try:
            day = tab.ele('@class=text-[#F56E52] mr-[2px]').text
        except Exception as e:
            day = '7'

        # 积攒的代币个数
        taskData.OnssCoin_Num = onss
        # 签到天数
        taskData.CheckIn_DaysCount = day
        taskData.level_1 = lv_1
        taskData.level_2 = lv_2
        taskData.level_3 = lv_3
        taskData.level_4 = lv_4
        taskData.level_5 = lv_5
        updateTaskRecord(env.name, name, taskData, 1)
        tab.close()

    except Exception as e:
        logger.info(f"{env.name}: 网络异常，统计失败", e)
        tab.close()

    return

#完成任务
@chrome_retry(exceptions=(Exception, ),max_tries=3, initial_delay=2)
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
            tw: Account = getAccountById(env.tw_id)
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
        tab.ele('t:p@tx():Lords Mobile').click()
        chrome.wait(1)
        tab.ele('t:span@tx():confirm').click()
        chrome.wait(2, 3)
        tab.ele('@alt=close-icon.png', index=1).click(by_js=None)

        logger.info(f"{env.name}: 下注 Lords Mobile")
    else:
        logger.info(f"{env.name}: 今日下注已完成")

    chrome.wait(4, 5)
    if tab.s_ele("ATTACK NOW"):
        tab.ele('t:p@tx():Subway Surfers').click()
        chrome.wait(1)
        tab.ele('t:span@tx():confirm').click()
        chrome.wait(2, 3)
        tab.ele('@alt=close-icon.png', index=1).click(by_js=None)

        logger.info(f"{env.name}: 攻击Subway Surfers已完成")
    else:
        logger.info(f"{env.name}: 今日攻击已完成")

    tab.close()

# 宝石升级
@chrome_retry(exceptions=(Exception, ),max_tries=3, initial_delay=2)
def Gem(chrome,env):

    tab = chrome.new_tab("https://task.onenesslabs.io/inventory")
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
    tab.close()

# 参与抽奖
@chrome_retry(exceptions=(Exception, ),max_tries=3, initial_delay=2)
def Lottery(chrome,env):
    tab = chrome.new_tab(home_page)
    if tab.s_ele(
            '.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 font-[Bangers] text-[20px] flex-1 bg-[#D6B635] text-black h-[48px] rounded-full mt-[30px] hover:scale-[1.1] cursor-pointer'):
        tab.ele(
            '.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 font-[Bangers] text-[20px] flex-1 bg-[#D6B635] text-black h-[48px] rounded-full mt-[30px] hover:scale-[1.1] cursor-pointer').click()

    # 获取表头
    headers = tab.ele("@class=flex justify-center items-center").eles("c:button")
    # 鼠标指针移动到头像
    tab.actions.move_to(headers[2])

    if tab.s_ele('PARTICIPATE IN THE RAFFLE'):
        tab.ele('PARTICIPATE IN THE RAFFLE').click()
        chrome.wait(4, 5)
        num = tab.s_ele('.text-[32px] ml-[12px]').text
        logger.info(f"{env.name}: 抽奖成功！您的Tickets数量为：{num}")
        tab.close()
        return

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

    if tab.s_ele('.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 font-[Bangers] text-[20px] flex-1 bg-[#D6B635] text-black h-[48px] rounded-full mt-[30px] hover:scale-[1.1] cursor-pointer'):
        tab.ele('.relative ease-in-out duration-200 flex justify-center items-center select-none bg-100 font-[Bangers] text-[20px] flex-1 bg-[#D6B635] text-black h-[48px] rounded-full mt-[30px] hover:scale-[1.1] cursor-pointer').click()
    if tab.s_ele('You have no raffle tickets allocated based on earthquake attack gameplay'):
        logger.info(f"{env.name}: 很遗憾，没有抽奖卷")

    if tab.s_ele("YOU'VE PARTICIPATED IN THE RAFFLE"):
        logger.info(f"{env.name}: 已经抽奖完成")
        return

    if tab.s_ele('PARTICIPATE IN THE RAFFLE'):
        tab.ele('PARTICIPATE IN THE RAFFLE').click()
        chrome.wait(4, 5)
        num = tab.s_ele('.text-[32px] ml-[12px]').text
        logger.info(f"{env.name}: 抽奖成功！您的Tickets数量为：{num}")
    tab.close()


def Oneness(env):
    try:
        chrome: ChromiumPage = OKXChrome(env)
        getOnenesslabs(chrome, env)
        getCount(chrome, env)
        Gem(chrome, env)
        Task(chrome, env)
        Gem(chrome, env)
        # Lottery(chrome, env)

        logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
    except Exception as e:
        logger.error(f"{env.name} 执行：{e}")
        return ("失败", e)
    finally:
        quitChrome(env, chrome)

if __name__ == '__main__':
    with app.app_context():
        # env = Env.query.filter_by(name="SYL-1").first()
        # Oneness(env)
        submit(Oneness, getAllEnvs())
import re

from loguru import logger

from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import ConfirmOKXWallet
from flaskServer.services.chromes.login import GalxeChrome
from flaskServer.services.dto.account import getAccountById
from flaskServer.services.content import Content
from flaskServer.services.chromes.login import LoginTW
from flaskServer.config.config import FAKE_TWITTER,FLLOW_FAKE_TWITTER,GALXE_CAMPAIGN_URLS
from flaskServer.services.dto.task_record import updateTaskRecord

def loginGalxe(chrome,env,task):
    tab = chrome.new_tab("https://app.galxe.com/quest/" + task)
    for i in range(10):
        # 判断页面是否刷新出现
        back = tab.s_ele("@@type=button@@text()=Back to Homepage")
        if back:
            logger.info(f"{env.name}: {tab.url}页面正在刷新")
            tab.refresh()
    # 判断钱包是否需要重新登录
    login = tab.s_ele("@@type=button@@text()=Log in")
    if login:
        tab.ele("@@type=button@@text()=Log in").click()
        ele = tab.ele("@@class=col-span-2 text-sm font-bold@@text():OKX")
        try:
            new_tab = ele.click.for_new_tab()
        except Exception as e:
            tab.ele("@@type=button@@text()=Log in").click()
            new_tab = tab.ele("@@class=col-span-2 text-sm font-bold@@text():OKX").click.for_new_tab()
        ConfirmOKXWallet(chrome, new_tab, env)
        logger.info(f"{env.name}: 登录Galxe成功！当前任务：{task}")
    return tab

def checkTW(chrome,tab,env):
    login = tab.s_ele("Log in")
    if login:
        tab.close()
        tw = chrome.get_tab(url="https://x.com/home")
        if tw:
            tw.refresh()
        if tw:
            tw.refresh()
        LoginTW(chrome,env)
        return True

def get_new_tab(wapp):
    try:
        new_tab = wapp.click.for_new_tab()
    except Exception as e:
        new_tab = wapp.click.for_new_tab()
        print(new_tab)
        if not new_tab:
            new_tab = wapp.click.for_new_tab()
    return new_tab

def twConfirm(chrome,wapp,env):
    tab = get_new_tab(wapp)
    if FAKE_TWITTER:
        tab.close()
        return
    chrome.wait(5, 8)
    if not checkTW(chrome,tab,env):
        followTw(tab)
        tab.close()
    else:
        twConfirm(chrome,wapp,env)

def followTw(tab,type=""):
    try:
        tab.ele("@data-testid=confirmationSheetConfirm").click()
        tab.close()
    except Exception as e:
        if type == "FOLLOW":
            followButton = tab.ele("@data-testid=placementTracking")
            if "Following" in followButton.text:
                tab.close()
            else:
                followButton.click()
                tab.close()

def followTWButton(chrome,wapp,env):
    tab = get_new_tab(wapp)
    if FLLOW_FAKE_TWITTER:
        tab.close()
        return
    chrome.wait(5, 8)
    followButton = tab.s_ele("@data-testid=placementTracking")
    if "Following" in followButton.text:
        tab.close()
        return
    if not checkTW(chrome,tab,env):
        followTw(tab,"FOLLOW")
    else:
        followTWButton(chrome,wapp,env)

def twButton(chrome,wapp,env):
    tab = get_new_tab(wapp)
    if FAKE_TWITTER:
        tab.close()
        return
    chrome.wait(5, 8)
    if not checkTW(chrome,tab,env):
        tab.ele("@data-testid=tweetButton").click()
        tab.close()
    else:
        twButton(chrome,wapp,env)

def refreshRole(chrome,role,name):
    if "Twitter" in name or "Tweet" in name:
        role.ele("c:button").click()
        chrome.wait(3, 5)

def claimPoints(chrome,env,tab,task):
    end = tab.ele("@class=flex items-center justify-end z-[2] w-full")
    end = end.ele("c:button")
    print(end.text)
    if "Points" in end.text:
        chrome.wait(1,2)
        print(end.click)
        tab.actions.move_to(end)
        end.click()
        try:
            result = tab.ele("@class=text-size-18 font-extrabold sm:text-size-32 font-mona",timeout=10)
            if "Points" in result.text:
                logger.info(f"{env.name}: 领取成功：{result.text}")
                tab.ele("@@type=button@@text()=Close").click()
                updateTaskRecord(env.name,f"{task}",1)
        except Exception as e:
            end.click()
            result = tab.ele("@class=text-size-18 font-extrabold sm:text-size-32 font-mona",timeout=20)
            if "Points" in result.text:
                logger.info(f"{env.name}: e领取成功：{result.text}")
                tab.ele("@@type=button@@text()=Close").click()
                updateTaskRecord(env.name,f"{task}",1)


def execTask(chrome,env,tab):
    follow = tab.s_ele("@class=text-size-12 font-semibold")
    if "Following" not in follow.text:
        print(f"follow元素: {follow}")
        follow = tab.ele("@class=text-size-12 font-semibold", timeout=3)
        follow.click()
        logger.info(f"{env.name}: 关注space")
    # 获取任务区域
    roleWapper = tab.ele("@class=flex flex-col gap-5 mb-8")
    # 获取任务列表
    roles = roleWapper.eles("x:/div")
    for role in roles[1:]:
        # 判断任务是否成功
        try:
            success = role.s_ele("@class=text-success")
        except Exception:
            success = None
        # 鼠标点击区域
        wapp = role.ele("@class=flex gap-2 items-center w-full")
        # 获取任务名称
        name = wapp.ele("c:p").text
        if name:
            if success: continue
            logger.info(f"{env.name}: {name}任务开始执行")
            if name.startswith("Follow"):
                followTWButton(chrome,wapp,env)
            if name.startswith("Like") or name.startswith("Retweet"):
                twConfirm(chrome,wapp,env)
            if name.startswith("Quote"):
                twButton(chrome,wapp,env)
            if name.startswith("Survey"):
                button = role.ele("c:button")
                button.click()
                chrome.wait(2, 3)
                role.ele("c:input").input("https://x.com/" + tw.name)
                role.ele("@type=button").click()
            logger.info(f"{env.name}: {name} 任务刷新")
            refreshRole(chrome,role,name)

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-4-2").first()
        tw = getAccountById(env.tw_id)
        chrome = GalxeChrome(env)
        for parentTask in GALXE_CAMPAIGN_URLS:
            tab = loginGalxe(chrome, env, parentTask)
            slide = tab.ele("@class=SiblingSlide_slide-bar__i6lXo")
            if slide:
                slide = tab.ele("@class=SiblingSlide_slide-bar__i6lXo")
                eles = slide.eles("css:div[id]")
                for ele in eles:
                    print(ele)
                    id = ele.attr("id")
                    if id in parentTask:
                        task = parentTask
                    else:
                        task = re.sub(r'/\w+',f'/{id}',parentTask)
                        try:
                            tab.actions.move_to(ele)
                            ele.click()
                        except Exception as  e:
                            tab.get("https://app.galxe.com/quest/"+task)
                        chrome.wait(2,3)
                    execTask(chrome,env,tab)
                    claimPoints(chrome,env,tab,task)




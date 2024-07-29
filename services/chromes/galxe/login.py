from DrissionPage._elements.chromium_element import ChromiumElement

from flaskServer.services.chromes.login import GalxeChrome
from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.dto.account import getAccountById
from flaskServer.services.chromes.login import ConfirmOKXWallet
from flaskServer.services.content import Content
from flaskServer.config.config import FAKE_TWITTER
from DrissionPage import ChromiumPage
from loguru import logger

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-3").first()
        tw = getAccountById(env.tw_id)
        chrome = GalxeChrome(env)
        tab  = chrome.new_tab("https://app.galxe.com/quest/PlumeNetwork/GCzqctkqub")
        for i in range(10):
            back = tab.s_ele("@@type=button@@text()=Back to Homepage")
            if back:
                tab.refresh()
                logger.info(f"{env.name}: {tab.url}页面正在刷新")
        login = tab.s_ele("@@type=button@@text()=Log in")
        if login:
            tab.ele("@@type=button@@text()=Log in").click()
            new_tab = tab.ele("@@class=flex items-center@@text()=OKX").next().click.for_new_tab()
            ConfirmOKXWallet(chrome,new_tab,env)
        else:
            pass
        roleWapper = tab.ele("@class=flex flex-col gap-5 mb-8")
        roles = roleWapper.eles("x:/div")
        for role in roles[1:]:

            # 判断任务是否成功
            try:
                success = role.s_ele("@class=text-success")
            except Exception:
                success =None
            wapp: ChromiumElement = role.ele("@class=flex gap-2 items-center w-full")
            name = wapp.ele("c:p").text
            refresh = role.s_ele("@xmlns=http://www.w3.org/2000/svg")
            if name :
                if success: continue
                logger.info(f"{env.name}: {name}任务开始执行")
                if name.startswith("Follow") or name.startswith("Like"):
                    tw_tab = wapp.click.for_new_tab()
                    print(tw_tab)
                if name.startswith("Quote"):
                    tw_tab = wapp.click.for_new_tab()
                    print(tw_tab)
                if name.startswith("Survey"):
                    button = role.ele("c:button")
                    button.click()
                    chrome.wait(2,3)
                    input = role.ele("c:input").input("https://x.com/"+ tw.name)
                    role.ele("@type=button").click()
        for role in roles[1:]:
            button = role.ele("c:button")
            if button.text != "Start":
                success = button.s_ele("x:/div")
                if success: continue
                else: button.click()



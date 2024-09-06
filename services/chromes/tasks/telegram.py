from loguru import logger
from flaskServer.utils.chrome import quitChrome
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import NoAccountChrome
from flaskServer.config.connect import app

name = "telegram"

def checkTG(env):
    with app.app_context():
        chrome = None
        logger.info(f"======开始执行{env.name}环境")
        try:
            tg = getTaskObject(env, name)
            chrome = NoAccountChrome(env)
            tab = chrome.new_tab(url="https://web.telegram.org/k/")
            flag = True
            if tab.s_ele("Log in to Telegram by QR Code"):
                flag = False
            if tab.s_ele(".text-center i18n"):
                if tab.ele(".text-center i18n").text == "Sign in to Telegram":
                    flag = False
            if flag:
                header = tab.ele(".sidebar-header can-have-forum")
                header.ele(".btn-icon rp btn-menu-toggle sidebar-tools-button is-visible").click()
                header.ele(".btn-menu bottom-right has-footer active was-open").ele(".btn-menu-item rp-overflow",index=4).click()
                username = tab.ele(".profile-avatars-info").ele(".peer-title").text
                phone = tab.ele(".sidebar-left-section-container",index=2).ele(".row-title").text
                userName = tab.ele(".sidebar-left-section-container",index=2).ele(".row-title",index=2).text
                tg.name = username
                tg.phone = phone
                tg.userName = userName
                updateTaskRecord(env.name, name, tg, 1)
            else:
                updateTaskRecord(env.name, name, tg, 2)
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)

if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-1-1").first()
        checkTG(env)
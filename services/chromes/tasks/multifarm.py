from loguru import logger

from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import OKXChrome, LoginTW, AuthTW, ConfirmOKXWallet
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.utils.chrome import quitChrome

# 任务名称
name = "multifarm"

def toDo(env):
    with app.app_context():
        chrome = None
        logger.info(f"======开始执行{env.name}环境")
        try:
            taskData = getTaskObject(env, name)
            chrome = OKXChrome(env)
            LoginTW(chrome, env)
            tab = chrome.new_tab(url="http://www.multifarm.io/?r=37JUJ4")
            tab.ele("GET STARTED").click()
            s = tab.s_ele("sign in to x")
            if s:
                tab.ele("sign in to x").click()
                chrome.wait.load_start()
                chrome.wait(14,15)
                AuthTW(chrome,env)
                if (tab.s_ele("Metamask")):
                    wallet_tab = tab.ele("Metamask").click.for_new_tab()
                    ConfirmOKXWallet(chrome,wallet_tab,env)
            buttons = tab.eles("@class=icon uppercase")
            for button in buttons:
                taskData.count += 1
                button.click()
                tw = tab.ele("@class= flex gap-2 items-center ").click.for_new_tab()
                tw.close()
            while tab.eles("@class: max-lg:mr-3 h-[29.43px] uppercase w-[110px] tablet:h-[1.667vw] tablet:w-[7.2vw] flex justify-center items-center font-akiraExpanded font-extrabold tracking-widest text-center text-[9.207px] tablet:text-[0.521vw] rounded-[3.06px] transition-all   text-yellow hover:bg-[#FFCC3E] hover:text-[#0B0B0B] border-[0.04vw] outline-none border-[#FFCC3E] cursor-not-allowed"):
                chrome.wait(2,3)
            updateTaskRecord(env.name, name, taskData, 1)
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)


if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-5-3").first()
        toDo(env)
        # envs = getAllEnvs()
        # submit(toDo,envs)
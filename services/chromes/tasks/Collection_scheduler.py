from flaskServer.services.chromes.worker import createThread
from flaskServer.services.chromes.tasks.humanity import Humanity
from flaskServer.services.chromes.tasks.Theoriq import theoriq
from flaskServer.config.connect import app
from DrissionPage import ChromiumPage,ChromiumOptions
from flaskServer.services.chromes.login import OKXChrome
from loguru import logger
from flaskServer.utils.chrome import quitChrome, get_Custome_Tab

def TaskList(chrome,env):
    HumanityTaskThread = createThread(Humanity, (chrome, env,))
    TheoriqTaskThread = createThread(theoriq, (chrome, env,))
    HumanityTaskThread.join()
    TheoriqTaskThread.join()

def StartTask(env):
    try:
        chrome: ChromiumPage = OKXChrome(env)
        TaskList(chrome, env)
        logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
    except Exception as e:
        logger.error(f"{env.name} 执行：{e}")
        return ("失败", e)
    finally:
        quitChrome(env, chrome)





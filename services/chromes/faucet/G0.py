import random

from loguru import logger

from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.mode.wallet import Wallet
from flaskServer.services.chromes.login import NoAccountChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.utils.decorator import closeChrome

def worker(env):
    chrome = None
    try:
        chrome = NoAccountChrome(env)
        tab = chrome.new_tab(url="https://faucet.0g.ai")
        with app.app_context():
            okx = Wallet.query.filter_by(id=env.okx_id).first()
            tab.ele("#address").input(okx.address)
            tab.ele("@type=submit").wait.enabled(timeout=200)
            tab.ele("@type=submit").click()
            h3 = tab.ele("@id=modal-title").text
            m2 = tab.ele("@class=mt-2").text
            if "Successful" in h3 or "Please" in m2:
                logger.info(f"{env.name}环境领取成功")
    except Exception as e:
        logger.error(f"{env.name}: {e}")
    finally:
        if chrome:
            chrome.quit()

def toDo():
    num = random.choice([ i for i in range(5)])
    with app.app_context():
        proxys = Proxy.query.all()
        envs = []
        envs.append(Env.query.filter_by(name="Q-0").first())
        for proxy in proxys:
            env = Env.query.filter_by(t_proxy_id=proxy.id).all()[num]
            envs.append(env)
        submit(worker,envs)


if __name__ == '__main__':
    # 初始化环境
    # toDo2()
    # 0G任务领取
    toDo()



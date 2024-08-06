import random

from loguru import logger
from flaskServer.config.config import CHROME_VERSION,RANDOM_ORDER
from flaskServer.config.connect import db, app
from flaskServer.mode.env import Env
from flaskServer.mode.proxy import Proxy
from flaskServer.utils.envutil import getUserAgent

def getAllEnvs():
    with app.app_context():
        envs = Env.query.all()
        if RANDOM_ORDER:
            random.shuffle(envs)
        return envs

def getChoiceEnvs():
    num = random.choice([i for i in range(5)])
    with app.app_context():
        proxys = Proxy.query.all()
        envs = []
        # envs.append(Env.query.filter_by(name="Q-0").first())
        for proxy in proxys:
            env = Env.query.filter_by(t_proxy_id=proxy.id).all()[num]
            envs.append(env)
        if RANDOM_ORDER:
            random.shuffle(envs)
        return envs

def getEnvByName(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        return env

def updateEnvStatus(name,status):
    ENV = getEnvByName(name)
    with app.app_context():
        if ENV:
            if ENV.status != status:
                ENV.status = status
        else:
            logger.error(f"{name}环境不存在")
        db.session.add(ENV)
        db.session.commit()

def updateAllStatus(status):
    with app.app_context():
        db.session.query(Env).update({Env.status: status})
        db.session.commit()

def updateEnv(env,port,cookies,proxy,tw,discord,outlook,okx,init,bitlight,userAgent):
    ENV = getEnvByName(env)
    with app.app_context():
        if ENV:
            if ENV.cookies != cookies and cookies:
                ENV.cookies = ENV.cookies
            if proxy and ENV.t_proxy_id != proxy.id:
                ENV.t_proxy_id = proxy.id
            if tw and ENV.tw_id != tw.id:
                ENV.tw_id = tw.id
            if discord and ENV.discord_id != discord.id:
                ENV.discord_id = discord.id
            if outlook and ENV.outlook_id != outlook.id:
                ENV.outlook_id = outlook.id
            if okx and  ENV.okx_id != okx.id:
                ENV.okx = okx.id
            if init and ENV.init_id != init.id:
                ENV.init_id = init.id
            if bitlight and ENV.bitlight_id != bitlight.id:
                ENV.bitlight_id = bitlight.id
            if port and ENV.port != port:
                ENV.port = port
            if CHROME_VERSION not in ENV.user_agent:
                ENV.user_agent = getUserAgent(userAgent)
            print("更新一条环境信息，id：", ENV.id)
        else:
            ENV = Env(name=env,port=port,user_agent=getUserAgent(userAgent),cookies=cookies,t_proxy_id=getId(proxy)
                      ,tw_id=getId(tw),discord_id=getId(discord),outlook_id=getId(outlook),okx_id=getId(okx),
                      init_id=getId(init),bitlight_id=getId(bitlight))
            print("新增一条环境信息，id：", ENV.id)
        db.session.add(ENV)
        db.session.commit()
        return env

def getId(object):
    if object:
        return object.id
    else:
        return 0
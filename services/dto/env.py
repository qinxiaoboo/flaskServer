from flaskServer.mode.env import Env
from flaskServer.config.connect import db,app
from flaskServer.utils.chrome import getUserAgent
from sqlalchemy import and_


def getEnvByName(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        return env

def updateEnv(env,port,cookies,proxy,tw,discord,outlook,okx,init,bitlight):
    env = getEnvByName(env)
    with app.app_context():
        if env:
            if env.cookies != cookies and cookies:
                env.cookies = env.cookies
            if proxy and env.t_proxy_id != proxy.id:
                env.t_proxy_id = proxy.id
            if tw and env.tw_id != tw.id:
                env.tw_id = tw.id
            if discord and env.discord_id != discord.id:
                env.discord_id = discord.id
            if outlook and env.outlook_id != outlook.id:
                env.outlook_id = outlook.id
            if okx and  env.okx_id != okx.id:
                env.okx = okx.id
            if init and env.init_id != init.id:
                env.init_id = init.id
            if bitlight and env.bitlight_id != bitlight.id:
                env.bitlight_id = bitlight.id
        else:
            env = Env(name=env,port=port,user_agent=getUserAgent(),cookies=cookies,t_proxy_id=getId(proxy)
                      ,tw_id=getId(tw),discord_id=getId(discord),outlook_id=getId(outlook),okx_id=getId(okx),
                      init_id=getId(init),bitlight_id=getId(bitlight))
        db.session.add(env)
        db.session.commit()
        return env

def getId(object):
    print(object)
    if object:
        return object.id
    else:
        return None
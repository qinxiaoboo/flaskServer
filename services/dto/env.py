from flaskServer.mode.env import Env
from flaskServer.config.connect import db,app
from flaskServer.utils.chrome import getUserAgent
from sqlalchemy import and_


def getEnvByName(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        return env

def updateEnv(env,port,cookies,proxy,tw,discord,outlook,okx,init,bitlight):
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
        else:
            ENV = Env(name=env,port=port,user_agent=getUserAgent(),cookies=cookies,t_proxy_id=getId(proxy)
                      ,tw_id=getId(tw),discord_id=getId(discord),outlook_id=getId(outlook),okx_id=getId(okx),
                      init_id=getId(init),bitlight_id=getId(bitlight))
        db.session.add(ENV)
        db.session.commit()
        print("新增一条环境信息，id：", ENV.id)
        return env

def getId(object):
    if object:
        return object.id
    else:
        return 0
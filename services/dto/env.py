from flaskServer.mode.env import Env
from flaskServer.config.connect import db,app
from flaskServer.utils.chrome import getUserAgent
from sqlalchemy import and_


def getEnvByName(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        return env

def update(group,name,port,user_agent,cookies,t_proxy_id,tw_id,discord_id,outlook_id):
    env = getEnvByName(name)
    if env:
        return env
    else:
        with app.app_context():
            env = Env(group=group,name=name,port=port,user_agent=getUserAgent())
            db.session.add(env)
            db.session.commit()
            return env

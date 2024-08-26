import json
import random

from loguru import logger
from flaskServer.config.config import CHROME_VERSION,RANDOM_ORDER
from flaskServer.config.connect import db, app
from flaskServer.mode.env import Env,status_descriptions
from flaskServer.mode.proxy import Proxy
from flaskServer.utils.envutil import getUserAgent,to_be_list,can_convert_to_number,can_be_list
from flaskServer.dao.envAccount import EnvAccountInfo
from flaskServer.services.dto.account import Account
from flaskServer.services.dto.proxy import Proxy

def getAllEnvs():
    with app.app_context():
        envs = Env.query.all()
        if RANDOM_ORDER:
            random.shuffle(envs)
        return envs

def getEnvsInfo(page,page_size,search, label, sortBy="env", sortOrder="asc"):
    envs_json = []
    with app.app_context():
        # 构建基本查询
        envs_query = Env.query
        if search:
            search_term = f"%{search}%"
            envs_query = envs_query.filter(
                (Env.group.like(search_term))|
                (Env.name.like(search_term))|
                (Env.label.like(search_term))
            )
            # 动态设置排序
        if sortBy not in ['group']:
            sortBy = 'name'  # 默认排序字段
        if sortOrder == 'desc':
            sort_order = db.desc
        else:
            sort_order = db.asc
        if label:
            page_size = 100000

        envs_query = envs_query.order_by(sort_order(getattr(Env, sortBy)))

        # 分页
        paginated_envs = envs_query.paginate(page=page, per_page=page_size, error_out=False)
        count = 0
        for env in paginated_envs.items:
            if label:
                if can_convert_to_number(label):
                    label = int(label)
                if label not in to_be_list(env.label):
                    count += 1
                    continue
            tw = Account.query.filter_by(id=env.tw_id).first()
            discord = Account.query.filter_by(id=env.discord_id).first()
            outlook = Account.query.filter_by(id=env.outlook_id).first()
            ip = Proxy.query.filter_by(id=env.t_proxy_id).first()
            env_json = EnvAccountInfo(id=env.id,group=env.group,env=env.name,tw=tw.name,tw_status=tw.status,tw_error=tw.error,discord=discord.name,
                                      discord_status=discord.status,discord_error=discord.error,outlook_status=outlook.status,outlook_error=outlook.error,
                                      outlook=outlook.name, ip=ip.ip if ip else "", ip_status=ip.status if ip else 0, status=status_descriptions.get(env.status, "未知状态"),
                                      label=env.label).to_dict()
            envs_json.append(env_json)
    return envs_json,paginated_envs.total - count


def getEnvsByGroup(group):
    with app.app_context():
        envs = Env.query.filter_by(group=group).all()
        if RANDOM_ORDER:
            random.shuffle(envs)
        return envs

def getEnvsByIds(ids):
    with app.app_context():
        envs = Env.query.filter(Env.id.in_(ids)).all()
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

def updateAllStatus(ids,status):
    with app.app_context():
        db.session.query(Env).filter(Env.id.in_(ids)).update({Env.status: status})
        db.session.commit()

def addLabel(ids,label):
    envs = getEnvsByIds(ids)
    if can_convert_to_number(label):
        label = int(label)
    else:
        label = str(label)
    with app.app_context():
        for env in envs:
            if can_be_list(env.label):
                label_l = to_be_list(env.label)
                if label in label_l:
                    continue
                label_l.append(label)
                env.label = json.dumps(label_l)
            db.session.add(env)
        db.session.commit()

def updateLabel(ids,label):
    with app.app_context():
        db.session.query(Env).filter(Env.id.in_(ids)).update({Env.label: label})
        db.session.commit()

def updateEnv(env,group,port,cookies,proxy,tw,discord,outlook,okx,init,bitlight,userAgent, label):
    ENV = getEnvByName(env)
    with app.app_context():
        if ENV:
            if ENV.cookies != cookies and cookies:
                ENV.cookies = ENV.cookies
            if ENV.group != group and group:
                ENV.group = group
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
            if userAgent and CHROME_VERSION not in ENV.user_agent:
                ENV.user_agent = getUserAgent(userAgent)
            if label and ENV.label != label:
                ENV.label = label
            print("更新一条环境信息，id：", ENV.id)
        else:
            ENV = Env(name=env,group=group,port=port,user_agent=getUserAgent(userAgent),cookies=cookies,t_proxy_id=getId(proxy)
                      ,tw_id=getId(tw),discord_id=getId(discord),outlook_id=getId(outlook),okx_id=getId(okx),
                      init_id=getId(init),bitlight_id=getId(bitlight),label=label)
            print("新增一条环境信息，id：", ENV.id)
        db.session.add(ENV)
        db.session.commit()
        return env

def getId(object):
    if object:
        return object.id
    else:
        return 0

if __name__ == '__main__':
    print(int("1"))

import random
import sys

from loguru import logger
from flaskServer.config.connect import app
from gevent import pywsgi
from flask import request
from flaskServer.services.system.dict import getInfo
from flaskServer.services.system.dict import updateInfo
from flaskServer.config.scheduler import scheduler
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import toLoginAll
from flaskServer.services.chromes.login import LoginChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.chromes.tasks.multifarm import toDo as toDoMultifarm
from flaskServer.services.dto.env import updateAllStatus
from threading import Thread

logger.remove()
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: <7}</level> | '
                              '<level>{message}</level>')

result = {"code": 0, 'msg': "success"}
chrome = None



@app.route("/chromes/reset")
def reset ():
    updateAllStatus(0)
    return "success"

@app.route('/system/setting/get')
def systemSettingGet():
    result["data"] = getInfo(request.args)
    return result
@app.route("/system/setting/update")
def systemSettingSet():
    updateInfo(request.get_json())
    return "success"

@app.route("/init/all")
def loginAll ():
    with app.app_context():
        envs = Env.query.all()
        random.shuffle(envs)
        submit(toLoginAll,envs)
    return "success"

@app.route("/init/<name>")
def login(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
    Thread(target=LoginChrome,args=(env,)).start()
    return "success"

@app.route("/todo/multifarm")
def multifarm ():
    with app.app_context():
        envs = Env.query.all()
        random.shuffle(envs)
        submit(toDoMultifarm,envs)
    return "success"


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    server = pywsgi.WSGIServer(("0.0.0.0",9000),app)
    server.serve_forever()

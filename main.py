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
from flaskServer.services.chromes.login import DebugChrome
from flaskServer.services.chromes.worker import submit, executor
from flaskServer.services.chromes.tasks.multifarm import toDo as toDoMultifarm
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs
from flaskServer.services.internal.tasks.spaces_stats import todo as countPoints
from flaskServer.services.chromes.galxe.login import debugGalxeTask,toDoGalxeTaskAll
from threading import Thread

logger.remove()
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: <7}</level> | '
                              '<level>{message}</level>')

result = {"code": 0, 'msg': "success"}

# 初始化 浏览器配置
@app.route("/chromes/reset")
def reset ():
    updateAllStatus(0)
    return "success"

# @app.route('/system/setting/get')
# def systemSettingGet():
#     result["data"] = getInfo(request.args)
#     return result
# #
# @app.route("/system/setting/update")
# def systemSettingSet():
#     updateInfo(request.get_json())
#     return "success"
# 初始化所有环境
@app.route("/init/all")
def loginAll ():
    with app.app_context():
        envs = getAllEnvs()
        Thread(target=submit, args=(toLoginAll, envs,)).start()
    return "success"
# 初始化单个环境
@app.route("/init/<name>")
def login(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        Thread(target=DebugChrome,args=(env,)).start()
    return "success"
# 0g官网任务
@app.route("/todo/multifarm")
def multifarm ():
    with app.app_context():
        envs = getAllEnvs()
        Thread(target=submit, args=(toDoMultifarm, envs,)).start()
    return "success"
# 银河任务统计
@app.route("/galxe/countpoints")
def countpoints():
    Thread(target=countPoints, args=()).start()
    return "success"
# 执行全量银河任务
@app.route("/galxe/task/all")
def galxeAll ():
    with app.app_context():
        envs = getAllEnvs()
        Thread(target=submit, args=(toDoGalxeTaskAll,envs,)).start()
    return "success"
# 单个执行银河任务
@app.route("/galxe/task/<name>")
def taskSign(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        Thread(target=debugGalxeTask, args=(env,)).start()
    return "success"

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    server = pywsgi.WSGIServer(("0.0.0.0",9000),app)
    server.serve_forever()

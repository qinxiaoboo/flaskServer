import random
import sys

from loguru import logger
from flaskServer.config.connect import app,db
from gevent import pywsgi
from flaskServer.config.scheduler import scheduler
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import toLoginAll
from flaskServer.services.chromes.login import DebugChrome
from flaskServer.services.chromes.worker import submit, executor
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
from flaskServer.services.internal.tasks.spaces_stats import todo as countPoints
from flaskServer.services.chromes.galxe.login import debugGalxeTask,toDoGalxeTaskAll
from flaskServer.services.dto.job import addJobByDB
from threading import Thread
from flaskServer.routes import env,task,galxe,user
from flask_cors import CORS
from flaskServer.services.chromes.tasks.plume import toDoPlumeTaskAll
from flaskServer.services.system.auto.updateEtd import updateExten
app.register_blueprint(env.bp)
app.register_blueprint(task.bp)
app.register_blueprint(galxe.bp)
app.register_blueprint(user.bp)
logger.remove()
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
                              '<level>{level: <7}</level> | '
                              '<level>{message}</level>')

result = {"code": 0, 'msg': "success"}
# 初始化所有环境
@app.route("/init/all")
def loginAll ():
    with app.app_context():
        envs = getAllEnvs()
        Thread(target=submit, args=(toLoginAll, envs,)).start()
    return "success"

@app.route("/init/group/<name>")
def loginEnvsByGroup (name):
    with app.app_context():
        envs = getEnvsByGroup(name)
        Thread(target=submit, args=(toLoginAll, envs,)).start()
    return "success"

# 初始化单个环境
@app.route("/init/<name>")
def login(name):
    with app.app_context():
        env = Env.query.filter_by(name=name).first()
        Thread(target=DebugChrome,args=(env,)).start()
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

@app.route("/task/plume/all")
def taskPlume ():
    with app.app_context():
        envs = getAllEnvs()
        Thread(target=submit, args=(toDoPlumeTaskAll, envs,)).start()
    return "success"


# 这是一个测试lele

if __name__ == '__main__':
    # # Create the database and table
    # with app.app_context():
    #     db.create_all()
    # 更新插件
    updateExten()
    addJobByDB()
    scheduler.init_app(app)
    scheduler.start()
    CORS(app)
    server = pywsgi.WSGIServer(("0.0.0.0",9000), app)
    server.serve_forever()

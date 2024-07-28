import random

from flaskServer.config.connect import app
from gevent import pywsgi
from flask import request
from flaskServer.services.system.dict import getInfo
from flaskServer.services.system.dict import updateInfo
from flaskServer.config.scheduler import scheduler
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import toLoginAll
from flaskServer.services.chromes.chrome import Chrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.chromes.tasks.multifarm import toDo as toDoMultifarm

result = {"code": 0, 'msg': "success"}
chrome = None

@app.route('/')
def hello_world():
    return {"username":"ALQLgu","password":"BWkSWw","ipaddress":"45.93.213.234","port":8000}
@app.route('/system/setting/get')
def systemSettingGet():
    result["data"] = getInfo(request.args)
    return result
@app.route("/system/setting/update")
def systemSettingSet():
    updateInfo(request.get_json())
@app.route("/init/all")
def loginAll ():
    with app.app_context():
        envs = Env.query.all()
        random.shuffle(envs)
        submit(toLoginAll,envs)
    return "success"

@app.route("/init/<name>")
def login(name):
    chrome = Chrome(name)
    chrome.toLogin()
    return "success"

@app.route("/off/<name>")
def off(name):
    chrome = Chrome(name)
    chrome.quit()
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

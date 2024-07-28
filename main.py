from flaskServer.config.connect import app
from gevent import pywsgi
from flask import request
from flaskServer.services.system.dict import getInfo
from flaskServer.services.system.dict import updateInfo
from flaskServer.config.scheduler import scheduler

result = {"code": 0, 'msg': "success"}


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

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    server = pywsgi.WSGIServer(("0.0.0.0",9000),app)
    server.serve_forever()

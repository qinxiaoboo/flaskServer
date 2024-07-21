from flaskServer.config.connect import app
from flask import request, jsonify
from flaskServer.services.system.dict import getInfo

result = {"code": 0, 'msg': "success"}


@app.route('/')
def hello_world():
    return {"username":"ALQLgu","password":"BWkSWw","ipaddress":"45.93.213.234","port":8000}

@app.route('/system/setting/get')
def systemSettingGet():
    result["data"] = getInfo(request.args)
    # with app.app_context():
    #     sysdict = SysDict(name="KEYS",key="yesCaptcha",value="47b3e9fb8832222e67a900ff6f32c9beef0383e838919")
    #     db.session.add(sysdict)
    #     db.session.commit()
    return result

if __name__ == '__main__':
    app.run(port=9000)
from threading import Thread

from flask import Blueprint, request
from loguru import logger

from flaskServer.config.connect import app
from flaskServer.services.dto.user import getAllUser,updateUser,getUserByToken,loginUser,deleteUserById
from flaskServer.utils.crypt import decrypt_data
from flaskServer.utils.decorator import ApiCheck
bp = Blueprint('user', __name__)


@app.route("/user/info")
def userInfo():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    data = getAllUser()
    result["data"] = data
    return result

@app.route("/user/add",methods=["POST"])
def userAdd():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    data = request.get_json()
    name = decrypt_data(data.get("username"))
    password = decrypt_data(data.get("password"))
    groups = decrypt_data(data.get("groups"))
    token = request.headers.get("token")
    user = getUserByToken(token)
    if user:
        if user.username == "admin":
            updateUser(name, password, groups)
        else:
            if user.username == name:
                updateUser(name, password, None)
            else:
                return {"code":-1,'error': "只能修改自己的账号密码"}
    else:
        return {"code":-1,'error': "noLogin"}
    return result

@app.route("/user/login", methods=["POST"])
def userLogin():
    data = request.get_json()
    name = data.get("username")
    password = data.get("password")
    user = loginUser(decrypt_data(name),decrypt_data(password))
    if user:
        return {"code":0, "msg": user.token, "groups": user.groups}
    return {"code":-1, "error": "用户或密码不正确"}

@ApiCheck
@app.route("/user/del", methods=["DELETE"])
def userDel():
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    user_id = data.get("id")
    if deleteUserById(user_id):
        return result
    return {"code": -1, "error": "执行失败"}
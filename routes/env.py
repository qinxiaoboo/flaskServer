from threading import Thread

from flask import Blueprint, request
from loguru import logger

from flaskServer.config.connect import app
from flaskServer.services.chromes.login import toLoginAll, DebugChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsByIds
from flaskServer.services.dto.env import getEnvsInfo
from flaskServer.services.dto.env import updateAllStatus, updateLabel, addLabel
from flaskServer.utils.envutil import can_be_list

bp = Blueprint('envs', __name__)

@app.route("/envs/info")
def envsInfo():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 100000))
    sortBy = request.args.get("sortBy","env")
    sortOrder = request.args.get("sortOrder","asc")
    search = request.args.get("search","").strip()
    label = request.args.get("label", "").strip()
    data, total = getEnvsInfo(page, page_size, search, label, sortBy, sortOrder)
    result["data"] = data
    result["total"] = total
    return result

# 初始化 浏览器配置
@app.route("/chromes/reset", methods=["POST"])
def reset ():
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    updateAllStatus(ids, 0)
    logger.info(f"所选环境配置初始化成功，下次登录环境重新加载配置文件")
    return result

@app.route("/envs/debug", methods=["POST"])
def debug ():
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    envs = getEnvsByIds(ids)
    Thread(target=submit, args=(DebugChrome, envs,)).start()

    return result

@app.route("/envs/init", methods=["POST"])
def init ():
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    envs = getEnvsByIds(ids)
    Thread(target=submit, args=(toLoginAll, envs,)).start()
    return result

# 重置标签
@app.route("/envs/set/label", methods=["POST"])
def setslabel ():
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    label = data.get("label","[]").strip()
    logger.info(f"重置标签 Received body: {data}")
    if can_be_list(label):
        updateLabel(ids, label)
        logger.info(f"所选环境配置初始化成功，下次登录环境重新加载配置文件")
    else:
        result = {"code": -1, 'error': "执行失败，传入的标签格式有误"}
    return result

# 追加标签
@app.route("/envs/add/label", methods=["POST"])
def addlabel ():
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    label = data.get("label","[]").strip()
    logger.info(f"追加标签 Received body: {data}")
    addLabel(ids, label)
    return result
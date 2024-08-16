from threading import Thread

from flask import Blueprint, request,jsonify

from flaskServer.config.connect import app
from flaskServer.services.chromes.login import toLoginAll, DebugChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsInfo
from flaskServer.services.dto.env import getEnvsByIds
from flaskServer.services.dto.env import updateAllStatus
from loguru import logger

bp = Blueprint('envs', __name__)

@app.route("/envs/info")
def envsInfo():
    result = {"code": 0, 'msg': "success"}
    page = int(request.args.get('page',1))
    page_size = int(request.args.get('pageSize', 10))
    sortBy = request.args.get("sortBy","env")
    sortOrder = request.args.get("sortOrder","asc")
    search = request.args.get("search","")
    data, total = getEnvsInfo(page, page_size, search, sortBy, sortOrder)
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
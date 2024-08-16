from threading import Thread

from flask import Blueprint, request,jsonify

from flaskServer.config.connect import app
from flaskServer.services.chromes.login import toLoginAll, DebugChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsInfo
from flaskServer.services.dto.env import getEnvsByIds
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
    result["data"] = getEnvsInfo(page, page_size, search, sortBy, sortOrder)
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
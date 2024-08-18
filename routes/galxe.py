from threading import Thread

from flask import Blueprint, request
from loguru import logger

from flaskServer.config.connect import app
from flaskServer.services.chromes.galxe.login import toDoGalxeTaskAll
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsByIds
from flaskServer.services.dto.galxeAccount import getGaxlesInfo
from flaskServer.services.internal.tasks.spaces_stats import todo as countPoints

bp = Blueprint('galxes', __name__)

@app.route("/galxes/info")
def galxesInfo():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    data = getGaxlesInfo()
    result["data"] = data
    return result

# 银河任务统计
@app.route("/galxe/countpoints", methods=["POST"])
def countpoints():
    result = {"code": 0, 'msg': "success"}
    Thread(target=countPoints, args=()).start()
    return result
# 执行全量银河任务
@app.route("/galxe/task/all")
def galxeAll ():
    with app.app_context():
        result = {"code": 0, 'msg': "success"}
        data = request.get_json()
        ids = data.get('ids', [])
        logger.info(f"Received ids: {ids}")
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(toDoGalxeTaskAll,envs,)).start()
    return result
from threading import Thread

from flask import Blueprint, request
from loguru import logger

from flaskServer.config.connect import app
from flaskServer.services.chromes.tasks.multifarm import toDo as toDoMultifarm
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsByIds
from flaskServer.services.dto.task_record import getTaskRecordInfo
from flaskServer.config.task import objects

bp = Blueprint('tasks', __name__)

@app.route("/tasks/info")
def tasksInfo():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    name = request.args.get("name")
    data = getTaskRecordInfo(name)
    result["data"] = data
    return result

@app.route("/tasks")
def tasks():
    return {"code": 0, 'msg': "success","data": list(objects.keys())}


@app.route("/<groups>/todo/multifarm", methods=["POST"])
def p_multifarm (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(toDoMultifarm, envs,)).start()
    return result
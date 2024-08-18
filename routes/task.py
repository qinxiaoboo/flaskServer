from threading import Thread

from flask import Blueprint, request,jsonify

from flaskServer.config.connect import app
from flaskServer.services.dto.task_record import getTaskRecordInfo
from flaskServer.utils.envutil import can_be_list
from loguru import logger

bp = Blueprint('tasks', __name__)

@app.route("/tasks/info")
def tasksInfo():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    data = getTaskRecordInfo()
    result["data"] = data
    return result
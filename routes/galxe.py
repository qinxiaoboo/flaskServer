from threading import Thread

from flask import Blueprint, request,jsonify

from flaskServer.config.connect import app
from flaskServer.services.dto.galxeAccount import getGaxlesInfo
from flaskServer.utils.envutil import can_be_list
from loguru import logger

bp = Blueprint('galxes', __name__)

@app.route("/galxes/info")
def galxesInfo():
    result = {"code": 0, 'msg': "success"}
    logger.info(f"Received args: {request.args}")
    data = getGaxlesInfo()
    result["data"] = data
    return result
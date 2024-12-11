from threading import Thread

from flask import Blueprint, request
from loguru import logger

from flaskServer.config.connect import app
from flaskServer.services.chromes.tasks.multifarm import toDo as toDoMultifarm
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsByIds
from flaskServer.services.dto.task_record import getTaskRecordInfo
from flaskServer.config.task import objects
from flaskServer.services.chromes.tasks.onenesslabs import Oneness
from flaskServer.services.chromes.tasks.plume import toDoPlumeTaskAll
from flaskServer.services.chromes.tasks.telegram import checkTG as toDoCheckTG
from flaskServer.services.chromes.tasks.Hemi import Hemi
from flaskServer.services.chromes.tasks.Portal_zearly import portal
from flaskServer.services.chromes.tasks.Plume_taskon import taskon
from flaskServer.services.chromes.tasks.nowchain import NowChain
from flaskServer.services.chromes.tasks.deek import deek
from flaskServer.services.chromes.tasks.Claim_diamante import claim_diamante
from flaskServer.services.chromes.tasks.Passport import PassPort
from flaskServer.services.chromes.tasks.Highlayer import highlayer
from flaskServer.services.chromes.tasks.humanity import Humanity
from flaskServer.services.chromes.tasks.humanityWallet import humanityWallet
from flaskServer.services.chromes.tasks.Arch import arch
from flaskServer.services.chromes.tasks.Theoriq import theoriq
from flaskServer.services.chromes.tasks.X_active import x_active

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

@app.route("/<groups>/todo/onenesslabs", methods=["POST"])
def onenesslabs (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(Oneness, envs,)).start()
    return result


@app.route("/<groups>/todo/Plume", methods=["POST"])
def Plume (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(toDoPlumeTaskAll, envs,)).start()
    return result

@app.route("/<groups>/todo/checkTG", methods=["POST"])
def checkTG (groups):
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(toDoCheckTG, envs,)).start()
    return {"code": 0, 'msg': "success"}

@app.route("/<groups>/todo/hemi", methods=["POST"])
def hemi (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(Hemi, envs,)).start()
    return result


@app.route("/<groups>/todo/Portal", methods=["POST"])
def Portal (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(portal, envs,)).start()
    return result

@app.route("/<groups>/todo/taskon", methods=["POST"])
def Taskon (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(taskon, envs,)).start()
    return result

@app.route("/<groups>/todo/NowChain", methods=["POST"])
def now_chain (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(NowChain, envs,)).start()
    return result

@app.route("/<groups>/todo/deek", methods=["POST"])
def Deek (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(deek, envs,)).start()
    return result

@app.route("/<groups>/todo/claim_diamante", methods=["POST"])
def Claim_diamante (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(claim_diamante, envs,)).start()
    return result

@app.route("/<groups>/todo/PassPort", methods=["POST"])
def Pass_Port (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(PassPort, envs,)).start()
    return result

@app.route("/<groups>/todo/highlayer", methods=["POST"])
def Highlayer (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(highlayer, envs,)).start()
    return result

@app.route("/<groups>/todo/Humanity", methods=["POST"])
def HumanityProtocol (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(Humanity, envs,)).start()
    return result

@app.route("/<groups>/todo/humanityWallet", methods=["POST"])
def HumanityWallet (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(humanityWallet, envs,)).start()
    return result

@app.route("/<groups>/todo/arch", methods=["POST"])
def Arch (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(arch, envs,)).start()
    return result


@app.route("/<groups>/todo/theoriq", methods=["POST"])
def Theoriq (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(theoriq, envs,)).start()
    return result

@app.route("/<groups>/todo/x_active", methods=["POST"])
def X_active (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    with app.app_context():
        envs = getEnvsByIds(ids)
        Thread(target=submit, args=(x_active, envs,)).start()
    return result
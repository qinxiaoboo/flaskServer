from threading import Thread

from flask import Blueprint, request, jsonify
from loguru import logger
from flaskServer.utils.decorator import ApiCheck
from flaskServer.utils.chrome import quitChromeByEnvIds
from flaskServer.config.connect import app
from flaskServer.services.chromes.login import toLoginAll, DebugChrome
from flaskServer.services.chromes.worker import submit
from flaskServer.services.dto.env import getEnvsByIds
from flaskServer.services.dto.env import getEnvsInfo
from flaskServer.services.dto.env import updateAllStatus, updateLabel, addLabel
from flaskServer.services.dto.user import getUserByToken
from flaskServer.services.dto.account import updateAccountStatus
from flaskServer.utils.envutil import can_be_list
from flaskServer.services.dto.job import updateJob, deleteJob, getJobs, getJob
from flaskServer.config.config import CHROME_USER_DATA_PATH
from pathlib import Path
from flaskServer.utils.fileUtils import removePath
from flaskServer.initData.env import uploadEnvs

bp = Blueprint('envs', __name__)

@app.route("/envs/info")
@ApiCheck
def envsInfo(groups):
    result = {"code": 0, 'msg': "success","data":[],"total":0}
    logger.info(f"Received args: {request.args}")
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 100000))
    sortBy = request.args.get("sortBy","env")
    sortOrder = request.args.get("sortOrder","asc")
    search = request.args.get("search","").strip()
    label = request.args.get("label", "").strip()
    token = request.headers.get("token")
    user = getUserByToken(token)
    if user and user.username!="admin":
        data, total = getEnvsInfo(page, page_size, search, label, sortBy, sortOrder,user.groups)
        result["data"] = data
        result["total"] = total
    else:
        return {"code": 0, "error": "noLogin"}
    return result

# 初始化 浏览器配置
@app.route("/<groups>/chromes/reset", methods=["POST"])
def reset (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    resetType = data.get("type","")
    logger.info(f"Received ids: {ids}, reset type: {resetType}")
    if resetType == "hard":
        envs = getEnvsByIds(ids)
        for env in envs:
            removePath(CHROME_USER_DATA_PATH / Path("config/") / Path(env.name))
            removePath(CHROME_USER_DATA_PATH / Path("dowloads/") / Path(env.name))
            removePath(CHROME_USER_DATA_PATH / Path("data/") / Path(env.name))
            removePath(CHROME_USER_DATA_PATH / Path("cache/") / Path(env.name))
            updateAccountStatus(env.tw_id, 0, "硬重置了tw状态~")
            updateAccountStatus(env.discord_id, 0, "硬重置了discord状态~")
            updateAccountStatus(env.outlook_id, 0, "硬重置了outlook状态~")
    updateAllStatus(ids, 0)
    logger.info(f"所选环境配置初始化成功，下次登录环境重新加载配置文件")
    return result

# 关闭浏览器
@app.route("/<groups>/chromes/close", methods=["POST"])
def close (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    quitChromeByEnvIds(ids)
    return result

@app.route("/<groups>/envs/debug", methods=["POST"])
def debug (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    envs = getEnvsByIds(ids)
    Thread(target=submit, args=(DebugChrome, envs,)).start()

    return result

@app.route("/<groups>/envs/init", methods=["POST"])
def init (groups):
    result = {"code": 0, 'msg': "success"}
    data = request.get_json()
    ids = data.get('ids', [])
    logger.info(f"Received ids: {ids}")
    envs = getEnvsByIds(ids)
    Thread(target=submit, args=(toLoginAll, envs,)).start()
    return result

@app.route("/<groups>/envs/upload", methods=["POST"])
def upload (groups):
    file = request.files['file']  # 获取上传的文件
    uploadEnvs(file)
    return 'File uploaded successfully'

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


@app.route('/<groups>/jobs', methods=['POST','PUT'])
def add_job(groups):
    data = request.json
    user = getUserByToken(request.headers.get("token"))
    if user:
        if groups and groups != user.groups:
            return {"code": -1, "error": "noLogin"}
        data["groups"] = request.headers.get("groups")
        updateJob(data)
        return {"code":0,"msg":"成功"}
    else:
        return {"code":-1,"error":"noLogin"}

@app.route('/jobs', methods=['GET'])
@ApiCheck
def get_jobs(groups):
    jobs = getJobs(groups)
    return {"code":0,"data":jobs}

@app.route('/jobs/<job_id>', methods=['GET'])
@ApiCheck
def get_job(groups,job_id):
    job = getJob(groups, job_id)
    return {"code":0,"msg":job}

@app.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    if deleteJob(job_id):
        return {"code":0,"msg":"成功"}
    else:
        return {"code":-1,"error": "执行失败"}

from flaskServer.services.dto.dataDictionary import getAll,getDataDictionaryById,updataDataDictionary,deleteDataDictionary
@app.route('/dictionary', methods=['GET'])
def get_all_entries():
    return {"code":0,"data":getAll()}

@app.route('/dictionary/<int:id>', methods=['GET'])
def get_entry(id):
    entry = getDataDictionaryById(id)
    if entry:
        return {"code":0,"data": entry.to_dict()}
    return {"code":-1,"error":"没有该数据"}

@app.route('/dictionary', methods=['POST'])
def create_entry():
    data = request.json
    group_name = data['group_name'],
    code = data['code'],
    value = data['value'],
    description = data.get('description', '')
    updataDataDictionary(group_name,code,value,description)
    return {"code":0,"msg":"操作成功"}

@app.route('/dictionary/<int:id>', methods=['DELETE'])
def delete_entry(id):
    deleteDataDictionary(id)
    return {"code":0,"msg":"操作成功"}

from flaskServer.services.chromes.worker import cancelTasks
from flaskServer.services.dto.taskLog import getTaskLogs

@app.route('/task_logs', methods=['GET'])
@ApiCheck
def get_task_logs(groups):
    envName = request.args.get("env_name", "").strip()
    taskName = request.args.get("task_name", "").strip()
    taskLogs = getTaskLogs(groups, envName, taskName)
    return {"code": 0, "data": taskLogs}

@app.route('/<groups>/task_logs/cancel', methods=['POST'])
def cancel_task_logs(groups):
    ids = request.json.get('ids', [])
    cancelTasks(ids)
    return {"code":0,"msg":"操作成功"}
import psutil
@app.route('/<group>/systeminfo', methods=['GET'])
@ApiCheck
def system_info(groups, group):
    # 获取 CPU 使用率
    cpu_usage = psutil.cpu_percent(interval=5)

    # 获取内存使用情况
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    # 获取硬盘使用情况
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    return {"code":0,"data":{
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage}}
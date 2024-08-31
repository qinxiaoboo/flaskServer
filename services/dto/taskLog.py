import json
from datetime import datetime, timedelta
from flaskServer.mode.taskLog import TaskLog
from flaskServer.config.connect import db, app
from flaskServer.services.dto.env import getEnvsByGroup
from flaskServer.services.dto.dataDictionary import getDataDictionaryByValue
from sqlalchemy import and_
from sqlalchemy import desc

def addTaskLog(env_name, task_name, task_result, execution_result, status):
    with app.app_context():
        taskLog = TaskLog(env_name=env_name, task_name=task_name, task_result=task_result, execution_result=execution_result, start_time=datetime.now(), end_time=datetime.now(), status=status)
        db.session.add(taskLog)
        db.session.commit()
        return taskLog.id

def getTaskLogById(task_id):
    with app.app_context():
        taskLog = TaskLog.query.filter_by(id=task_id).first()
        return taskLog

def getTaskLogByEnvs(env_names,task_name):
    with app.app_context():
        if task_name:
            query = TaskLog.query.filter_by(task_name=task_name)
        else:
            query = TaskLog.query
        taskLogs = query.filter(TaskLog.env_name.in_(env_names))\
            .order_by(desc(TaskLog.start_time)).all()
        return taskLogs

def getTaskLogs(groups, env_name, task_name):
    taskLogsRe = []
    env_names = []
    if env_name:
        env_names.append(env_name)
    else:
        envs = getEnvsByGroup(groups)
        for env in envs:
            env_names.append(env.name)
    taskLogs = getTaskLogByEnvs(env_names, task_name)
    for taskLog in taskLogs:
        taskLogsRe.append(taskLog.to_dict())
    return taskLogsRe


def updateTaskLogStatus(task_id, status):
    with app.app_context():
        taskLog = getTaskLogById(task_id)
        if taskLog:
            if status and status != taskLog.status:
                taskLog.status = status
            taskLog.end_time = datetime.now()
            db.session.add(taskLog)
            db.session.commit()
            return taskLog

def updateTaskLogResult(task_id, task_result, execution_result):
    with app.app_context():
        taskLog = getTaskLogById(task_id)
        if taskLog:
            if task_result and task_result != taskLog.task_result:
                taskLog.task_result = task_result
            if execution_result and execution_result != taskLog.execution_result:
                taskLog.execution_result = execution_result
            taskLog.end_time = datetime.now()
            db.session.add(taskLog)
            db.session.commit()
            return taskLog

def clearTaskLog():
    seven_days_ago = datetime.now() - timedelta(days=7)
    with app.app_context():
        # 执行删除操作
        db.session.query(TaskLog).filter(TaskLog.start_time<seven_days_ago).delete(synchronize_session=False)
        db.session.commit()
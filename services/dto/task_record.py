import datetime

from sqlalchemy import and_

from flaskServer.config.connect import db, app
from flaskServer.config.task import get_object_by_name
from flaskServer.mode.task_record import TaskRecord
from flaskServer.services.dto.env import getAllEnvs


# 获取任务记录通过环境和任务名称
def getTaskRecord(env, name):
    with app.app_context():
        taskRecord = TaskRecord.query.filter(and_(TaskRecord.env_name==env,TaskRecord.name==name)).first()
        return taskRecord

def getTaskObject(env, name):
    taskRecord = getTaskRecord(env.name, name)
    if (taskRecord):
        return getObjectByName(name, taskRecord.object)
    return getObjectByName(name, "")


# 检查任务状态
def checkTaskStatus(env, name):
    taskRecord = getTaskRecord(env,name)
    if taskRecord:
        return (taskRecord.status == 1)
    return False

def getTaskRecordInfo(name):
    datas = []
    env_names = []
    for env in getAllEnvs():
        env_names.append(env.name)
    with app.app_context():
        ts = db.session.query(TaskRecord).filter(and_(TaskRecord.env_name.in_(env_names)), TaskRecord.name == name).order_by(TaskRecord.env_name.asc()).all()
        for t in ts:
            datas.append({"id": t.id, "env_name": t.env_name, "name": t.name, "status": t.status, "createTime": t.createtime, "updateTime": t.updatetime} | getObjectByName(t.name, t.object))
    return datas

def getObjectByName(name, str):
    cls = get_object_by_name(name)
    if cls:
        try:
            OB = cls.from_json(str)
            return OB
        except Exception as e:
            return cls()
    else:
        raise Exception("任务名称找不到, 没有定义")

# 更新任务记录
def updateTaskRecord(env, name, object, status):
    taskRecord = getTaskRecord(env, name)
    with app.app_context():
        if taskRecord:
            if taskRecord.status != status:
                taskRecord.status = status
            if taskRecord.object != object:
                taskRecord.object = object
            taskRecord.updatetime = datetime.datetime.now()
        else:
            taskRecord = TaskRecord(name=name,env_name=env,status=status,object=object)
        db.session.add(taskRecord)
        db.session.commit()
        print(f"{env}新增一条{name}任务记录,状态：'{'完成' if status == 1 else '未完成'}'，id：{taskRecord.id if taskRecord else ''}")
        return taskRecord

# 更新任务状态
def updateTaskStatus(env, name, status):
    with app.app_context():
        db.session.query(TaskRecord).filter(TaskRecord.name==name).update({TaskRecord.status:status,TaskRecord.updatetime:datetime.datetime.now()})
        db.session.commit()


import datetime

from flaskServer.mode.task_record import TaskRecord
from flaskServer.config.connect import db,app
from flaskServer.utils.envutil import to_be_exclude
from flaskServer.services.dto.env import getAllEnvs
from sqlalchemy import and_
# 获取任务记录通过环境和任务名称
def getTaskRecord(env,name):
    with app.app_context():
        taskRecord = TaskRecord.query.filter(and_(TaskRecord.env_name==env,TaskRecord.name==name)).first()
        return taskRecord

# 检查任务状态
def checkTaskStatus(env,name):
    taskRecord = getTaskRecord(env,name)
    if taskRecord:
        return (taskRecord.status == 1)
    return False

def getTaskRecordInfo():
    datas = []
    env_names = []
    for env in getAllEnvs():
        env_names.append(env.name)
    with app.app_context():
        ts = db.session.query(TaskRecord).filter(TaskRecord.env_name.in_(env_names)).order_by(TaskRecord.env_name.asc()).all()
        tasks = dict()
        for t in ts:
            if t.env_name in tasks:
                tasks[t.env_name].append({f"{t.name}": f"未完成{t.updatetime}" if t.status == 0 else f"完成{t.updatetime}"})
            else:
                tasks[t.env_name] = [{f"{t.name}": f"未完成{t.updatetime}" if t.status == 0 else f"完成{t.updatetime}"}]
        for key, value in tasks.items():
            dicts = dict()
            dicts["环境"] = key
            for data in value:
                for name, vv in data.items():
                    if to_be_exclude(name):
                        continue
                    dicts[f"{name}"] = f"{vv}"
            datas.append(dicts)
    return datas

# 更新任务记录
def updateTaskRecord(env,name,status):
    taskRecord = getTaskRecord(env,name)
    with app.app_context():
        if taskRecord:
            if taskRecord.status != status:
                taskRecord.status = status
            taskRecord.count = taskRecord.count + 1
            taskRecord.updatetime = datetime.datetime.now()
        else:
            taskRecord = TaskRecord(name=name,env_name=env,status=status,count=1)
        db.session.add(taskRecord)
        db.session.commit()
        print(f"{env}新增一条{name}任务记录,状态：'{'完成' if status == 1 else '未完成'}'，id：{taskRecord.id if taskRecord else ''}")
        return taskRecord

# 更新任务状态
def updateTaskStatus(name,status):
    with app.app_context():
        db.session.query(TaskRecord).filter(TaskRecord.name==name).update({TaskRecord.status:status,TaskRecord.updatetime:datetime.datetime.now()})
        db.session.commit()

if __name__ == '__main__':
    # updateTaskStatus("multifarm",0)
    updateTaskRecord("Q-8-7","multifarm",1)
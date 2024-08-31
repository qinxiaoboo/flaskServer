import time
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

from flaskServer.config.config import THREAD_POOL_NUM
from flaskServer.mode.env import Env
from flaskServer.services.dto.taskLog import addTaskLog, updateTaskLogStatus, updateTaskLogResult

tasks = {}
# 创建线程池
executor = ThreadPoolExecutor(max_workers=THREAD_POOL_NUM)
# def worker(data,name,age,key="key",value="value"):
#     print(data)
#     print(name,age,key,value)

# 异步执行
def submit(func,datas,*args, **kwargs):
    for data in datas:
        if type(data) is Env:
            taskid = addTaskLog(data.name, func.__name__, None, None, "pending")
            if taskid:
                tasks[taskid] = executor.submit(func, data, *args, **kwargs)
        else:
            executor.submit(func, data, *args, **kwargs)

def checkTasks():
    completed = []
    cancelled = []
    keys = list(tasks.keys())
    for key in keys:
        if key in tasks:
            value = tasks.get(key)
            if value.running():
                updateTaskLogStatus(key, "running")
            elif value.cancelled():
                updateTaskLogStatus(key, "cancelled")
                cancelled.append(key)
            elif value.done():
                res = value.result()
                result = "成功"
                msg = "执行成功"
                if res!= None and len(res) ==2:
                    result, msg = res
                updateTaskLogResult(key, result, msg)
                updateTaskLogStatus(key, "completed")
                completed.append(key)

    delTask(completed)
    delTask(cancelled)

def delTask(datas):
    for key in datas:
        if key in tasks:
            del tasks[key]

def cancelTasks(ids):
    for key in ids:
        if key != "on":
            key = int(key)
        if key in tasks:
            task = tasks[key]
            if not task.done():
                cancelled = task.cancel()
                if cancelled:
                    updateTaskLogStatus(key, "cancelled")
                else:
                    logger.info(f"{key}任务不能被取消")
            else:
                logger.info(f"{key} 任务已开始或已结束")

# 同步执行
def awaitSubmit(func,datas,*args, **kwargs):
    fs = []
    with ThreadPoolExecutor(THREAD_POOL_NUM) as executor:
        for data in datas:
            f = executor.submit(func,data, *args, **kwargs)
            fs.append(f)
        while True:
            time.sleep(3)
            flag = True
            for f in fs:
                flag = flag and f.done()
                if not flag:
                    break
            if flag:
                break
    return fs


if __name__ == '__main__':
    pass
    print(addTaskLog.__name__)

    # submit(worker,["test","text"],"qinxiaobo","28",key="change",value="old")


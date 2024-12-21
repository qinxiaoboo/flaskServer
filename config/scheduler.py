from flask_apscheduler import APScheduler
from flaskServer.config.connect import app
from flaskServer.services.chromes.faucet.G0 import toDo as toDoFaucet0G
from flaskServer.services.chromes.tasks.plumenetwork import toDoFaucet as toDoFaucetPlumenetwork
from flaskServer.services.chromes.worker import checkTasks
from flaskServer.services.dto.taskLog import clearTaskLog

# 定时任务配置
class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 添加API

scheduler = APScheduler()
app.config.from_object(Config())

def get_function_by_name(name):
    functions = {
        'toDoFaucet0G': toDoFaucet0G,
        'toDoFaucetPlumenetwork': toDoFaucetPlumenetwork
    }
    return functions.get(name)








# 检查正在执行的任务状态
scheduler.add_job(func=checkTasks, args=(), trigger='interval', seconds=5, id='checkTask')
# 每天21点清理7天以前的执行记录
scheduler.add_job(func=clearTaskLog, args=(), trigger='cron', hour=21, minute=0, id='clearTaskLog')
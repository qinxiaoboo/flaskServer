import time

from flask_apscheduler import APScheduler
from flaskServer.config.connect import app
from flaskServer.services.chromes.faucet.G0 import toDo
from flaskServer.services.chromes.tasks.plumenetwork import toDoFaucet

# 定时任务配置
class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 添加API

scheduler = APScheduler()
app.config.from_object(Config())
#
# @scheduler.task('cron', id='do_faucet_0g', day="*", hour="7")
# def faucet_0g_ai():
#     toDo()

#
# def task1(x):
#     print(f'task 1 executed --------: {x}', time.time())
#
#
# def task2(x):
#     print(f'task 2 executed --------: {x}', time.time())
#
# scheduler.add_job(func=toDoFaucet, args=('ETH',), trigger='interval', hours=1.1, id='interval_toDoFaucet_ETH')
# scheduler.add_job(func=toDoFaucet, args=('GOON',), trigger='interval', hours=2.1, id='interval_toDoFaucet_GOON')
# scheduler.add_job(func=toDo, args=(), trigger='interval', hours=24.1, id='interval_toDoFaucet_0G')

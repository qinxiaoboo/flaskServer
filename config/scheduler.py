import time

from flask_apscheduler import APScheduler
from flaskServer.config.connect import app
from flaskServer.services.chromes.faucet.G0 import toDo

# 定时任务配置
class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 添加API

scheduler = APScheduler()
app.config.from_object(Config())

@scheduler.task('cron', id='do_faucet_0g', day="*", hour="7")
def faucet_0g_ai():
    toDo()


def task1(x):
    print(f'task 1 executed --------: {x}', time.time())


def task2(x):
    print(f'task 2 executed --------: {x}', time.time())

scheduler.add_job(func=task1, args=('循环',), trigger='interval', seconds=5, id='interval_task')
scheduler.add_job(func=task2, args=('定时任务',), trigger='cron', second='*/10', id='cron_task')
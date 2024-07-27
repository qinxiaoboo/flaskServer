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

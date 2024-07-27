from flask import Flask
from flask_apscheduler import APScheduler
import time


class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 添加API

scheduler = APScheduler()


# interval example, 间隔执行, 每10秒执行一次
@scheduler.task('interval', id='task_1', seconds=10, misfire_grace_time=900)
def task1():
    print('task 1 executed --------', time.time())


# cron examples, 每5秒执行一次 相当于interval 间隔调度中seconds = 5
@scheduler.task('cron', id='task_2', second='*/20')
def task2():
    print('task 2 executed --------', time.time())


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run()
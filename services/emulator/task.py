from uiautomator import Task
from threading import Thread
# 南非号码
task1 = Task(1, "113", "27")
Thread(target=task1.exec, ).start()

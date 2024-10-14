from uiautomator import Task
from threading import Thread
# 以色列号码  模拟器id，平台id，国码
task1 = Task(3, "98", "972")
Thread(target=task1.exec, ).start()

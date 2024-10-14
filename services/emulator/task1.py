from uiautomator import Task
from threading import Thread
# 香港
task1 = Task(2, "99", "852")
Thread(target=task1.exec, ).start()

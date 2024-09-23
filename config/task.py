from flaskServer.entity.taskData import TaskData
from flaskServer.entity.taskAccount import TG


objects = {
    'multifarm': TaskData,
    "telegram": TG,
    "Onenesslabs": TaskData,

}

def get_object_by_name(name):
    return objects.get(name)
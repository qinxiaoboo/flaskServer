from flaskServer.entity.taskData import TaskData
from flaskServer.entity.taskAccount import TG
from flaskServer.entity.taskData import TaskChain
from flaskServer.entity.taskData import TaskDeek
from flaskServer.entity.taskData import TaskPortal
from flaskServer.entity.taskData import TaskDiamante


objects = {
    'multifarm': TaskData,
    "telegram": TG,
    "Onenesslabs": TaskData,
    "NowChain": TaskChain,
    "Deek": TaskDeek,
    "Portal": TaskPortal,
    "claim_diamante": TaskDiamante,
}

def get_object_by_name(name):
    return objects.get(name)
from flaskServer.entity.taskData import TaskData
from flaskServer.entity.taskAccount import TG
from flaskServer.entity.taskData import TaskChain
from flaskServer.entity.taskData import TaskDeek
from flaskServer.entity.taskData import TaskPortal
from flaskServer.entity.taskData import TaskDiamante
from flaskServer.entity.taskData import TaskPassport
from flaskServer.entity.taskData import TaskHighlayer
from flaskServer.entity.taskData import TaskArch
from flaskServer.entity.taskData import TaskHumanity




objects = {
    'multifarm': TaskData,
    "telegram": TG,
    "Onenesslabs": TaskData,
    "NowChain": TaskChain,
    "Deek": TaskDeek,
    "Portal": TaskPortal,
    "passport": TaskPassport,
    "Claim_diamante": TaskDiamante,
    "Highlayer": TaskHighlayer,
    "Arch": TaskArch,
    "humanity": TaskHumanity
}

def get_object_by_name(name):
    return objects.get(name)
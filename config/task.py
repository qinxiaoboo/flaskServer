from flaskServer.entity.taskData import TaskData


objects = {
    'multifarm': TaskData
}

def get_object_by_name(name):
    return objects.get(name)
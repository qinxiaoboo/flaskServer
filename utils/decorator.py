from functools import wraps
from loguru import logger
from flask import request
from flaskServer.services.dto.user import getUserByToken,updateToken
""" 装饰器 """
def ApiCheck(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        token = request.headers.get("token")
        groups = request.headers.get("groups")
        user = getUserByToken(token)
        if user:
            updateToken(token)
            if groups and groups != user.groups:
                return {"code":-1, "error": "noLogin"}
            ret = fn(user.groups,*args,**kwargs)
        else:
            return {"code":-1, "error": "noLogin"}
        return ret
    return wrapper

import random
import time
from functools import wraps

from DrissionPage.errors import WaitTimeoutError
from loguru import logger
from flask import request
from flaskServer.services.dto.user import getUserByToken,updateToken
from flaskServer.config.config import MAX_TRIES
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


def chrome_retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tries, delay = MAX_TRIES, 1.5
        while tries > 0:
            try:
                return func(*args, **kwargs)
            except WaitTimeoutError as var1:
                tries -= 1
                if tries <= 0:
                    raise var1
                time.sleep(delay)

                delay *= 2
                delay += random.uniform(0, 1)
                delay = min(delay, 10)
            except Exception as e:
                raise e

    return wrapper
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


def chrome_retry(exceptions=(WaitTimeoutError,), max_tries=MAX_TRIES, initial_delay=1.5, max_delay=10):
    """
    A decorator for retrying a function if it raises specified exceptions.

    :param exceptions: A tuple of exception types to catch and retry on.
    :param max_tries: Maximum number of retry attempts.
    :param initial_delay: Initial delay between retries.
    :param max_delay: Maximum delay between retries.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tries, delay = max_tries, initial_delay
            while tries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    tries -= 1
                    if tries <= 0:
                        raise
                    time.sleep(delay)

                    delay *= 2
                    delay += random.uniform(0, 1)
                    delay = min(delay, max_delay)
                except Exception as e:
                    raise

        return wrapper
    return decorator

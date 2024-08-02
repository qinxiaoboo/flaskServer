from functools import wraps
from loguru import logger

def closeChrome(fn):
    @wraps(fn)
    def decorated(env,*args,**kwargs):
        chrome = None
        try:
            chrome = fn(env,*args,**kwargs)
        except Exception as e:
            logger.error(f"{env.name}: {e}")
        finally:
            if chrome:
                chrome.quit()
    return decorated
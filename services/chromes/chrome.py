from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger

from flaskServer.config.config import get_ini_path
from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import LoginChrome
from flaskServer.services.dto.env import updateEnvStatus,getEnvByName


class Chrome:
    def __init__(self,name):
        self.name = name
        self.chrome = None

    def toLogin(self):
        env = getEnvByName(self.name)
        LoginChrome(env)
        updateEnvStatus(env.name,2)

    def quit(self):
        self.chrome = ChromiumPage(addr_or_opts=ChromiumOptions(ini_path=get_ini_path(self.name)))
        if self.chrome:
            self.chrome.quit()
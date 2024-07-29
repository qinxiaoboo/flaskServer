from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage
from loguru import logger

from flaskServer.config.config import get_ini_path
from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import LoginChrome, InitChromeOption
from flaskServer.services.dto.env import updateEnvStatus


class Chrome:
    def __init__(self,name):
        self.name = name
        self.chrome = None

    def toLogin(self):
        with app.app_context():
            env = Env.query.filter_by(name=self.name).first()
            if env:#.status == 0 or env.status == 1:
                self.chrome = LoginChrome(env)
                updateEnvStatus(env.name,2)
            else:
                self.chrome = InitChromeOption(env)
            logger.info("环境初始化成功")

    def quit(self):
        self.chrome = ChromiumPage(addr_or_opts=ChromiumOptions(ini_path=get_ini_path(self.name)))
        if self.chrome:
            self.chrome.quit()
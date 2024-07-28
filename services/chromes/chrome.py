from flaskServer.config.connect import db,app
from flaskServer.mode.env import Env
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage,errors
from flaskServer.config.config import CHROME_USER_DATA_PATH
from flaskServer.services.dto.env import updateEnvStatus
from flaskServer.services.chromes.login import LoginChrome,InitChromeOption
from pathlib import Path
from loguru import logger

class Chrome:
    def __init__(self,name):
        self.name = name
        self.chrome = None
        self.init_path = CHROME_USER_DATA_PATH / Path("config/") / Path(name) / Path("conf.ini")

    def toLogin(self):
        with app.app_context():
            env = Env.query.filter_by(name=self.name).first()
            if env.status == 0 or env.status == 1:
                self.chrome = LoginChrome(env)
                updateEnvStatus(env.name,2)
            else:
                self.chrome = InitChromeOption(env)
            logger.info("环境初始化成功")

    def quit(self):
        self.chrome = ChromiumPage(addr_or_opts=ChromiumOptions(ini_path=self.init_path))
        if self.chrome:
            self.chrome.quit()
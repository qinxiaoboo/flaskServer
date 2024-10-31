import re
import time

from flaskServer.services.chromes.mail.base import BaseClient
from flaskServer.services.dto.account import updateAccountStatus

from loguru import logger

class Outlook(BaseClient):

    def login(self):
        self.tab = self.chrome.get_tab(url=".com/mail/0/")
        if self.tab is None:
            self.tab = self.chrome.new_tab(url="https://outlook.live.com/mail/0/")
        self.chrome.wait(2, 3)
        if "microsoft" in self.tab.url:
            logger.info(f"{self.envName}: 开始登陆 outlook邮箱")
            self.tab = self.tab.eles("@aria-label=Sign in to Outlook")[4].click.for_new_tab()
            self.tab.ele("@data-testid=i0116").input(self.username)
            self.tab.ele("@type=submit").click()
            self.tab.ele("@name=passwd").input(self.password)
            self.tab.ele("@type=submit").click()
            self.tab.ele("@type=checkbox").click()
            self.tab.ele("@@type=submit@@text()=Yes").click()
            if "https://outlook.live.com/mail/0" in self.tab.url:
                logger.info(f"{self.envName}: 登录OUTLOOK成功")
        if self.tab.s_ele("@@type=submit@@id=iNext"):
            self.tab.ele("@@type=submit@@id=iNext").click()
        if self.tab.s_ele("@id=userDisplayName"):
            text = self.tab.ele("@id=userDisplayName").text
            if text == self.username:
                self.tab.ele("@name=passwd").input(self.password)
                self.tab.ele("@type=submit").click()
                if self.tab.s_ele("@@type=submit@@id=iNext"):
                    self.tab.ele("@@type=submit@@id=iNext").click()
                logger.info(f"{self.envName}: 登录OUTLOOK成功")
        self.tab.wait(3)
        self.tab.ele("#meInitialsButton").click()
        user = self.tab.ele("#mectrl_currentAccount_secondary")
        if user == None:
            self.tab.ele("#meInitialsButton").click()
            user = self.tab.ele("#mectrl_currentAccount_secondary")
        if user.text != self.username:
            self.tab.ele(".mectrl_resetStyle primaryAction signIn").click()
            self.tab.ele("#i0116").input(self.username)
            self.tab.ele("@data-report-event=Signin_Submit").click()
            if self.tab.s_ele("@@data-testid=i0118@@type=password"):
                self.tab.ele("@@data-testid=i0118@@type=password").input(self.password)
                self.tab.ele("#idSIButton9").click()
                if self.tab.s_ele("@@class=btn btn-block btn-primary@@value=Send code"):
                    raise Exception(f"{self.envName}请手动验证登录邮箱:{self.username}")
                logger.info(f"{self.envName}: 登录OUTLOOK成功")


    def getCode(self, text, wtime=10, num=2):
        '''
        :param text: 邮件主题
        :param wtime: 循环一次等待时间
        :param num: 循环等待次数
        :return:
        '''
        if self.tab == None:
            self.login()
        header = self.tab.ele(".EeHm8",index=2)
        TtcXM = header.ele(".TtcXM")
        if text in TtcXM.text:
            self.tab.ele(".EeHm8", index=2).click()
            document = self.tab.ele("@role=document").text
            search = re.search("(\d{6})", document)
            if search:
                return search.group(0)
            else:
                raise Exception("未匹配到验证码！")
        elif num == 0:
            raise Exception("没有获取到验证码")
        else:
            self.tab.wait(wtime)
            self.getCode(text, wtime, num-1)



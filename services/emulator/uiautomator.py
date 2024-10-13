import re
import time

import uiautomator2 as u2
import subprocess
from loguru import logger
from sms import getNumber, changeStatus, getSms
from device import Ldmnq
from flaskServer.services.dto.phone import getPhoneByName, updatePhone
from threading import Thread

def get_device_serials():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    serials = [line.split()[0] for line in lines if line and line != 'List of devices attached']
    return serials


# 打印所有设备序列号
serials = get_device_serials()
tg_app_apk = r'D:\data\apk\Telegram.apk'
tg_app = "org.telegram.messenger.web"
ld_path = r'D:\LeiDian\LDPlayer9'
class Task:
    def __init__(self, index, country_id, country_code):
        self.index = index
        self.country_id = country_id
        self.country_code = country_code
        self.application_id = "3" #TG
        self.ld = Ldmnq(ld_path, index)
        self.d = u2.connect(serials[index])

    def setEnv(self):
        self.d.app_clear(tg_app)
        if tg_app not in self.d.app_list():
            self.d.app_install(tg_app_apk)
        if tg_app in self.d.app_list_running():
            self.d.app_stop(tg_app)
        self.d.app_start(tg_app)
        time.sleep(3)

    def wait_click(self, d, timeout=2):
        d.wait(timeout=timeout)
        if d.exists:
            d.click()

    def siginTG(self):

        self.setEnv()

        self.wait_click(self.d(className="android.widget.TextView", text="Start Messaging"))
        self.wait_click(self.d(className="android.widget.TextView", text="Continue"))
        self.wait_click(self.d(className="android.widget.Button",text="允许"))
        self.wait_click(self.d(text="Yes", className="android.widget.TextView"))
        ma = self.d(className="android.widget.EditText", index="1")
        if ma.exists:
            ma.set_text(self.country_code)
        phone = self.d(className="android.widget.EditText", index="3")
        if phone.exists:
            req = getNumber(self.application_id, self.country_id)
            if type(req) is tuple:
                pp = getPhoneByName(req[1])
                if pp:
                    logger.warning(f"{req[1]} 号码已被使用")
                    changeStatus(req[0], "reject")
                    return
                updatePhone(self.country_code,req[1],self.country_id, req[0], 0)
                phone.set_text(self.remove_country_code(req[1]))
                self.checkPhone(req, self.d)
            elif req == "no_numbers":
                print("没有号码了，换一个国家")
                raise
            elif req == "blance":
                print("没有余额了")
                raise

    def remove_country_code(self,phone_number):
        # 去掉前面的国家代码
        phone_number = re.sub(f'^{re.escape(self.country_code)}', '', phone_number)
        return phone_number

    def checkPhone(self, req, d):
        button = self.d(className="android.widget.FrameLayout", index="2")
        content = self.d(className="android.widget.TextView", text="Your phone number")
        button.wait(timeout=5)
        if button.exists:
            d.drag(800, 400, 1200, 666, duration=1)  # duration 为移动时间
            d.click(1200, 666)
            time.sleep(0.2)
            yes = self.d(text="Yes", className="android.widget.TextView")
            if yes.exists:
                yes.click()
            self.wait_click(self.d(className="android.widget.TextView", text="Continue"))
            allow = self.d(className="android.widget.Button", text="允许")
            self.wait_click(allow)
            time.sleep(3)
            if content.exists:
                time.sleep(10)
                d.click(1200, 666)
                print("double click")
                yes = self.d(text="Yes", className="android.widget.TextView")
                self.wait_click(yes)
                if content.exists:
                    time.sleep(10)
                    d.click(1200, 666)
                    print("thread click")
                    yes = self.d(text="Yes", className="android.widget.TextView")
                    self.wait_click(yes)

        prom = self.d(className="android.widget.TextView", index="0", text="Sorry")
        prom.wait(timeout=3)
        if prom.exists:
            text = self.d(className="android.widget.TextView", index="0", clickable="true")
            if text.exists:
                logger.error(f"注册报错原因：{text.get_text()}")
            self.recyclePhone(req)
            return
        checkMessage = self.d(text="Check your Telegram messages",className="android.widget.TextView")
        checkMessage.wait(timeout=3)
        if checkMessage.exists:
            print(f"TG已经被注册，请另选号码，{req[1]}此号码回收")
            self.recyclePhone(req)
        else:
            self.waitSms(req, d)

    def recyclePhone(self, req):
        changeStatus(req[0], "reject")
        updatePhone(self.country_code, req[1], self.country_id, req[0], 1)

    def waitSms(self, req, d):
        enterCodeMessage = self.d(text="Enter code", className="android.widget.TextView")
        enterCodeMessage.wait(timeout=3)
        if enterCodeMessage.exists:
            sms = getSms(req[0])
            if type(sms) == tuple:
                raise
            else:
                updatePhone(self.country_code, req[1], self.country_id, req[0], 1)
        else:
            phoneVerification = self.d(text="Phone Verification", className="android.widget.TextView")
            phoneVerification2 = self.d(text="Phone verification", className="android.widget.TextView")
            phoneVerification.wait(timeout=3)
            if phoneVerification.exists or phoneVerification2.exists:
                time.sleep(130)
                getCode = self.d(text="Get the code via SMS", className="android.widget.TextView")
                if getCode.exists:
                    getCode.click()
                    self.waitSms(req, d)
                else:
                    self.waitSms(req, d)
            else:
                raise

    def exec(self):
        count = 0
        for i in range(100):
            self.siginTG()
            if count == 6:
                logger.info("重置 雷电模拟器 环境")
                self.ld.resetLd()
                count = 0
            count += 1

if __name__ == '__main__':
    country_id = "7"  # 印度尼西亚 7 ， 马来西亚 6
    country_code = '62'
    taskNum = 5
    # 印度尼西亚
    task = Task(0, country_id, country_code)
    # task1 = Task(1, "113", "27")
    # task2 = Task(2, "6", "60")

    Thread(target=task.exec,).start()
    # Thread(target=task1.exec,).start()
    # Thread(target=task2.exec,).start()


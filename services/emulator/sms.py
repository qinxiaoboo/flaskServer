import datetime
import json
import time
from flaskServer.services.dto.phone import updatePhone
import requests
from loguru import logger

token = "4-nGga6q-5NaUClQMAfEKaoDtlU8fKGb"
country_id = "7" #  印度尼西亚 7 ， 马来西亚 6
country_code = '62'
application_id = "3"
app = "Telegram"
# 获取应用id
def getApplicationId(app):
    data = requests.get(f"https://api.sms-man.com/control/applications?token=${token}")
    data = data.json()
    if data.get("error_msg"):
        return data.get("error_code")
    for key, value in data.items():
        if value.get("title") == app:
            return key
# 获取号码
def getNumber(app_id, country_id):
    data = requests.get(f"https://api.sms-man.com/control/get-number?token={token}&country_id={country_id}&application_id={app_id}")
    if data.status_code == 200:
        data = data.json()
        print(f"手机号码信息：{data}")
        if data.get("error_msg"):
            return data.get("error_code")
        return (data.get("request_id"), data.get("number"))
    else:
        logger.error(data.text)
        return "请求失败"
# 改变状态
def changeStatus(request_id, status):
    data = requests.get(f"https://api.sms-man.com/control/set-status?token={token}&request_id={request_id}&status={status}")
    data = data.json()
    print(f"当前 {request_id} 状态改变为：{status}: {data.get('success')}")

# 查询余额
def findBlance():
    data = requests.get(f"https://api.sms-man.com/control/get-balance?token={token}")
    data = data.json()
    return data.get("success")

# 获取短信
def getSms(request_id):
    def get():
        data = requests.get(f"https://api.sms-man.com/control/get-sms?token={token}&request_id={request_id}")
        data = data.json()
        print(f"正在尝试获取手机短信：{data}")
        if data.get("error_msg"):
            return data.get("error_code")
        return (data.get("sms_code"), data.get("request_id"))
    start_time = datetime.datetime.now()
    while not (datetime.datetime.now() - start_time > datetime.timedelta(minutes=3)):
        res = get()
        if type(res) == tuple:
            return res
        time.sleep(5)
    # 超过三分钟没有获取短信，释放号码
    changeStatus(request_id, "reject")

# 调用限制
def limits(country_id, application_id):
    url = f"https://api.sms-man.com/control/limits?token={token}"
    if country_id:
        url += f"&country_id={country_id}"
    if application_id:
        url += f"&application_id={application_id}"
    data = requests.get(url)
    data = data.json()
    print(data)
# 获取国家列表
def countries(name):
    data = requests.get(f"https://api.sms-man.com/control/countries?token={token}")
    data = data.json()
    if data.get("error_msg"):
        return data.get("error_code")
    for key, value in data.items():
        if value.get("title") == name:
            return (key,)
# 请求可用号码数量
def getPrices(country_id):
    url = f"https://api.sms-man.com/control/get-prices?token={token}"
    if country_id:
        url += f"&country_id={country_id}"
    data = requests.get(url)
    data = data.json()
    print(data)

# req = getNumber(application_id, country_id)
# print(req)
# if type(req) is tuple:
#     # print(changeStatus(req[0], "reject"))
#     print(getSms(req[0]))
# elif req == "no_numbers":
#     print("没有号码了，换一个国家")
# elif req == "blance":
#     print("没有余额了")

# print(countries("Malaysia"))

# print(getSms("572295481"))
if __name__ == '__main__':

    changeStatus("572371954", "reject")
    pass

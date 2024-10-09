import asyncio
import time
import threading
from flaskServer.services.internal.tls.client import TLSClient
from flaskServer.entity.galxeAccount import AccountInfo
import pandas as pd

def toKeep(token,proxy,env_name,username):
    custom_headers = {
            "authorization": token,
             "origin": "chrome-extension://fpdkjdnhkakefebpekbdhillbhonfjjp"
        }
    account = AccountInfo(idx=env_name,proxy=proxy,email_username=username)
    client = TLSClient(account, custom_headers)
    threading.Thread(target=toDoKeepAlive,args=(account,client,)).start()
    threading.Thread(target=toDoGetPoints,args=(account,client,)).start()

def toDoKeepAlive(account,client):
    asyncio.run(toDoKeepAliveRest(account,client))

async def toDoKeepAliveRest(account,client):
    while True:
        data = {
            "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
            "numberoftabs": 0,
            "_v": "1.0.5",
            "username": account.email_username
        }
        try:
            request = await client.post("https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive", data)
        except Exception as e:
            print(e)
        finally:
            time.sleep(20)


def toDoGetPoints(account,client):
  asyncio.run(toDoGetPointsRest(account,client))


async def toDoGetPointsRest(account,client):
    while True:
        try:
            request = await client.get("https://www.aeropres.in/api/atom/v1/userreferral/getpoint")
            print(f"======{request}")
            if request.get("status") and request.get('message') == 'success':
                data = request.get('data')
                rewardPoint = data.get('rewardPoint')
                points = rewardPoint.get("twitter_x_id_points") + rewardPoint.get("discordid_points") + rewardPoint.get(
                    "telegramid_points") + rewardPoint.get("points")
                print(f"{account.idx}: 当前总分数为{points}")
            else:
                print(request)
        except Exception as e:
            print(e)
        finally:
            time.sleep(20)

def readEnvs():
    df = pd.read_excel("D:\data\initData\down.xlsx")
    df = df.fillna(0)
    for index, row in df.iterrows():
        env = row["环境"]
        proxy = row["proxy"]
        username = row["邮箱账号"]
        token = row["token"]
        print(proxy)
        if proxy:
            proxy = proxy.split(",")
            proxy = f"{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
        else:
            print(proxy)
        toKeep(token,proxy,env,username)



if __name__ == '__main__':
    readEnvs()
import asyncio
import json
import time
from flaskServer.services.apiTask.clientApi import TLSClient,userAgent
import requests
HEARTBEAT_INTERVAL = 6 * 60 * 60 * 1000   # 6小时
backendUrl = 'https://api.pipecdn.app/api/heartbeat'
# 报告ip 检测结果
async def toKeep(token,proxy,env_name,username):
    count = 0
    while True:
        start_time = time.time()  # 记录开始时间
        custom_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "origin": "chrome-extension://gelgmmdfajpefjbiaedgjkpekijhkgbe"
            }
        client = TLSClient(proxy, userAgent, custom_headers)
        try:
            nodes = await client.get("https://api.pipecdn.app/api/nodes")
            points = await getPoints(client)
            for node in nodes:
                if node:
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),f"环境名称：{env_name} -- 代理IP：{proxy} --节点ip：{node['ip']} --当前分数：{points} -- 存活检测：True")
                    start = time.time() * 1000
                    await client.get(f"http://{node['ip']}?mode=no-cors", with_text=True)
                    end = time.time() * 1000
                    latency = end - start
                    data = {
                        "node_id": node['node_id'],
                        "ip": node['ip'],
                        "latency": int(latency),
                        "status": "online" if latency > 0 else "offline"
                    }
                    response = await client.post("https://api.pipecdn.app/api/test", json=data)

                    if "points" in response and response["points"]:
                        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),f"环境名称：{env_name} -- 代理IP：{proxy}  -- 上报成功：{response} -- 上报结果：{latency} True")
                    else:
                        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),f"环境名称：{env_name} -- 代理IP：{proxy}  -- 上报失败：{response} -- 上报结果：{latency} False")

            elapsed_time = time.time() - start_time
            sleep_time = max(0, 1800 - elapsed_time)
            await asyncio.sleep(sleep_time)
        except Exception as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),f"环境名称：{env_name} -- 代理IP：{proxy} --异常：{e} -- 存活检测：False", flush=True)
            await asyncio.sleep(3600)
        finally:
            count += 1
            if count >= 12:
                await sendHeartBeat(client, env_name, proxy)
                count = 0
# 心跳检测
async def sendHeartBeat(client,env_name, proxy):
    try:
        geoInfo = await getGeoLocation()
        data = {
            "ip": geoInfo["ip"],
            "location": geoInfo["location"],
            "timestamp": int(time.time() * 1000)
        }
        response = await client.post("https://api.pipecdn.app/api/heartbeat", json=data)
        if "message" in response and "successfully" in response["message"]:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                  f"环境名称：{env_name} -- 代理IP：{proxy}  -- 心跳发送成功：{response}  True")
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                  f"环境名称：{env_name} -- 代理IP：{proxy}  -- 心跳发送失败：{response}  False")
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
              f"环境名称：{env_name} -- 代理IP：{proxy}  -- 心跳发送失败：{e}  False")
# 获取分数
async def getPoints(client):
    response = await client.get("https://api.pipecdn.app/api/points" )
    return response["points"]

# 获取本地ip信息
async def getGeoLocation():
    response = requests.get('https://ipapi.co/json/').json()
    return {"ip":response["ip"],"location":f"{response['city']}, {response['region']}, {response['country_name']}"}

async def main():
    with open(r".\output.txt", "r") as f:
        data = f.readlines()
        tasks = []
        for line in data:
            env_name, email, token, proxy = line.strip().split("|")
            await asyncio.sleep(5)
            task = asyncio.create_task(toKeep(token, proxy, env_name, email))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

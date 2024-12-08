
import asyncio
import json
import time
from flaskServer.services.apiTask.clientApi import TLSClient,userAgent
import requests


#注册
async def signup(env_name, email, datas,proxy):
    custom_headers = {
        "Content-Type": "application/json",
    }
    client = TLSClient(proxy, userAgent, custom_headers)
    data = {
        "email": email,
        "password" : "123qweasd",
        "referralCode": "",
    }
    # response = await client.post("https://api.pipecdn.app/api/signup", json=data, with_text=True)
    # print(f"{env_name}:{email} {response}")
    await login(client, env_name, email, datas, proxy)

#登录
async def login(client, env_name, email,datas,proxy):
    data = {
        "email": email,
        "password": "123qweasd",
    }
    response = await client.post("https://api.pipecdn.app/api/login", json=data)
    token = response["token"]
    # await reward(client, email)
    print(f"环境：{env_name} 登录成功 ，token：{token}")
    datas.append(f"{env_name}|{email}|{token}|{proxy}\n")
# 获取邀请连接
async def reward(client, email):
    data = {
        "email": email
    }
    response = await client.get("https://api.pipecdn.app/api/generate-referral", json=data)
    return response["response"]

async def main():
    datas = []
    with open(r".\input.txt", "r") as f:
        data = f.readlines()
        tasks = []
        for line in data:
            env_name, email, token, proxy = line.strip().split("|")
            await asyncio.sleep(5)
            task = asyncio.create_task(signup(env_name, email, datas, proxy))
            tasks.append(task)
        await asyncio.gather(*tasks)
    with open(r".\output.txt", "w") as f:
        f.writelines(datas)

if __name__ == '__main__':
    asyncio.run(main())
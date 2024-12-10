import asyncio
import random
from urllib.parse import urlparse, parse_qs

from flaskServer.config.connect import app
from flaskServer.mode.account import Account
from flaskServer.mode.proxy import Proxy
from flaskServer.services.apiTask.clientApi import TLSClient, userAgent
from flaskServer.config.config import WALLET_PASSWORD
# 代理列表
proxyList = []
# 邮箱列表
accountList=[]
# 邀请列表
#第一次执行会生成这个列表
reffers = ['eXVuMTY2MD', 'Y29jb3NieW', 'a3JvZ2NvdH', 'Y2xhcmtlLm', 'aGVsZW5jbm', 'QW50aG9ueV', 'bWluZGVybW', 'bW9ucm9lZG', 'aGVybmFuZG', 'eXVuMTY2MD']
# 是否是第一次执行,如果不是第一次执行，则使用上面reffers中的邀请码，并随机选中一个使用
FIRST=True


#注册
async def signup(env_name, email, datas,proxy):
    custom_headers = {
        "Content-Type": "application/json",
    }
    client = TLSClient(proxy, userAgent, custom_headers)
    if email =="yun16603860403@outlook.com":
        password = "xxx"
    else:
        password = WALLET_PASSWORD
    data = {
        "email": email,
        "password" : password,
        "referralCode": "MTMzNzU1Nj" if FIRST else random.choice(reffers)
    }
    response = await client.post("https://api.pipecdn.app/api/signup", json=data, with_text=True)
    print(f"{env_name}:{email} {response}")
    await login(client, env_name, email, datas, proxy, password)

#登录
async def login(client, env_name, email,datas,proxy,password):
    data = {
        "email": email,
        "password": password,
    }
    response = await client.post("https://api.pipecdn.app/api/login", json=data)
    token = response["token"]
    reffer = await reward(client, email)
    reffers.append(reffer)
    print(f"环境：{env_name} 登录成功 ，token：{token}")
    datas.append(f"{env_name}|{email}|{token}|{proxy}\n")

# 获取邀请连接
async def reward(client, email):
    data = {
        "email": email
    }
    response = await client.get("https://api.pipecdn.app/api/generate-referral", json=data)
    url = response["referralLink"]
    # 解析 URL
    parsed_url = urlparse(url)
    # 获取查询参数部分并解析
    query_params = parse_qs(parsed_url.query)
    # 获取 ref 参数的值
    ref_value = query_params.get('ref', [None])[0]
    return ref_value

async def main():
    tasks = []
    datas = []
    for i in range(10):
        if i == 0:
            task = asyncio.create_task(signup(i, accountList[i], datas, ''))
            tasks.append(task)
        if i < len(proxyList):
            task = asyncio.create_task(signup(i+1, accountList[i+1], datas, proxyList[i]))
            tasks.append(task)
    await asyncio.gather(*tasks)
    with open(r".\output.txt", "w") as f:
        f.writelines(datas)

def getProxys():
    with app.app_context():
        proxys = Proxy.query.all()
        for proxy in proxys:
            proxyList.append(f"{proxy.user}:{proxy.pwd}@{proxy.ip}:{proxy.port}")
    return proxyList

def getDiscordEmailName():
    with app.app_context():
        accounts = Account.query.filter(Account.type=="DISCORD").all()
        for account in accounts:
            if account.name:
                accountList.append(account.name)

def getFileEmailName():
    with open("input.txt") as f:
        # 按需添加
        pass

def getTWEmailName():
    with app.app_context():
        accounts = Account.query.filter(Account.type=="TW").all()
        for account in accounts:
            if account.email_name:
                accountList.append(account.email_name)

def getOutlookEmailName():
    #按需添加
    pass

if __name__ == '__main__':

    getProxys()
    getDiscordEmailName()
    # getFileEmailName()
    print(proxyList)
    print(accountList)
    asyncio.run(main())
    print(reffers)

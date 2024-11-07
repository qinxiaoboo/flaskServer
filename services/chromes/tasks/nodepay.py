import asyncio
import gc
import time
from flaskServer.services.internal.tls.client import TLSClient
from flaskServer.entity.galxeAccount import AccountInfo
from flaskServer.config.connect import app

async def toKeep(token,proxy,env_name,username):
    a = 10
    while True:
        start_time = time.time()  # 记录开始时间
        custom_headers = {
                "authorization": token,
                 "origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm"
            }
        account = AccountInfo(idx=env_name,proxy=proxy,email_username=username)
        client = TLSClient(account, custom_headers)
        try:
            request = await client.post("https://api.nodepay.org/api/auth/session")
            a += 1
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                "||| 环境ID：{7}||| 节点名: {0} ||| 邮箱：{1} ||| 节点状态：{2} ||| 任务积分：{3} ||| 挖矿积分：{4} ||| 总积分：{5} ||| 代理：{6}".format(
                    request["data"]["name"],
                    request["data"]["email"],
                    request["data"]["state"],
                    request["data"]["balance"]["current_amount"],
                    float(request["data"]["balance"]["total_collected"]) - float(
                        request["data"]["balance"]["current_amount"]),
                    request["data"]["balance"]["total_collected"],
                    proxy,
                    env_name,
                )
            )

            if a == 11:
                if request["code"] == 0:
                    data = {
                        "browser_id": None,
                        "id": request["data"]["uid"],
                        "timestamp": int(time.time()),
                        "version": "2.2.7"
                    }
                    ping = await client.post("https://nw.nodepay.org/api/network/ping",json=data)
                    print(
                        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                        " ||| 环境ID：{3} ||| Ping检测状态：{0} ||| IP检测分数：{1} ||| 代理：{2}".format(ping['success'],ping['data']['ip_score'],proxy,env_name)
                    )

                    a = 0
            elapsed_time = time.time() - start_time
            sleep_time = max(0, 300 - elapsed_time)
            await asyncio.sleep(sleep_time)
            await client.close()
        except Exception as e:
            print(account)
            await asyncio.sleep(5)
            await client.close()
            gc.collect()

async def main():
    with open(r"C:\Users\Joye\Desktop\nodepay.txt", "r") as f:
        data = f.readlines()
        tasks = []
        for line in data:
            env_name, email, browser_id, token, proxy, none = line.strip().split("|")
            await asyncio.sleep(5)
            task = asyncio.create_task(toKeep(token, proxy, env_name, email))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    with app.app_context():
        asyncio.run(main())
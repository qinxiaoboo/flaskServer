import asyncio
import re
import time
import warnings
from curl_cffi.requests import AsyncSession, BrowserType

CHROME_VERSION = "129"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
def getUserAgent(userAgent):
    if userAgent:
        userAgent = re.sub(r"Chrome/\d+", f"Chrome/{CHROME_VERSION}", userAgent)
        return userAgent
    return userAgent

def getSEC_CH_UA_PLATFORM(userAgent):
    if "Win64" in userAgent:
        return "Windows"
    if "Mac OS" in userAgent:
        return "macOS"
    if "WOW64" in userAgent:
        return "Windows"
    else:
        return "Windows"

def getSEC_CH_UA():
    return f'"Not)A;Brand";v="99", "Google Chrome";v="{CHROME_VERSION}", "Chromium";v="{CHROME_VERSION}"'

warnings.filterwarnings('ignore', module='curl_cffi')

def get_default_headers(useragent):
    return {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': getSEC_CH_UA(),
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': getSEC_CH_UA_PLATFORM(useragent),
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': getUserAgent(useragent),
        'content-type': 'application/json'
    }


class TLSClient:

    def __init__(self, proxy, useragent, custom_headers: dict = None, custom_cookies: dict = None):
        self._headers = {}
        self.proxy = proxy
        self.proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else {}
        headers = get_default_headers(useragent)
        if custom_headers is not None:
            headers.update(custom_headers)
        self.sess = AsyncSession(
            proxies=self.proxies,
            headers=headers,
            cookies=custom_cookies,
            impersonate=BrowserType.chrome120
        )

    async def close(self):
        self.sess.close()

    @classmethod
    def _handle_response(cls, resp_raw, acceptable_statuses=None, resp_handler=None, with_text=False):
        if acceptable_statuses and len(acceptable_statuses) > 0:
            if resp_raw.status_code not in acceptable_statuses:
                raise Exception(f'Bad status code [{resp_raw.status_code}]: Response = {resp_raw.text}')
        try:
            if with_text:
                return resp_raw.text if resp_handler is None else resp_handler(resp_raw.text)
            else:
                return resp_raw.json() if resp_handler is None else resp_handler(resp_raw.json())
        except Exception as e:
            raise Exception(f'{str(e)}: Status = {resp_raw.status_code}. '
                            f'Response saved in logs/errors.txt\n{resp_raw.text}')

    def update_headers(self, new_headers: dict):
        self._headers.update(new_headers)

    async def _raw_request(self, method, url, headers, **kwargs):
        match method:
            case 'GET':
                resp = await self.sess.get(url, headers=headers, **kwargs)
            case 'POST':
                resp = await self.sess.post(url, headers=headers, **kwargs)
            case unexpected:
                raise Exception(f'Wrong request method: {unexpected}')
        return resp

    async def request(self, method, url, acceptable_statuses=None, resp_handler=None, with_text=False, **kwargs):
        headers = self._headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': 60})
        kwargs.update({'verify': False})
        resp = await self._raw_request(method, url, headers, **kwargs)
        return self._handle_response(resp, acceptable_statuses, resp_handler, with_text)

    async def get(self, url, acceptable_statuses=None, resp_handler=None, with_text=False, **kwargs):
        return await self.request('GET', url, acceptable_statuses, resp_handler, with_text, **kwargs)

    async def post(self, url, acceptable_statuses=None, resp_handler=None, with_text=False, **kwargs):
        return await self.request('POST', url, acceptable_statuses, resp_handler, with_text, **kwargs)

async def toKeep(token,proxy,env_name,username):
    a = 10
    while True:
        start_time = time.time()  # 记录开始时间
        custom_headers = {
                "authorization": token,
                 "origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm"
            }
        client = TLSClient(proxy, userAgent, custom_headers)
        try:
            request = await client.post("https://api.nodepay.org/api/auth/session")

            a += 1

            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                "||| 环境ID：{7}||| 节点名: {0} ||| 邮箱：{1} ||| 节点状态：{2} ||| 返回状态码：{8} ||| 任务积分：{3} ||| 挖矿积分：{4} ||| 总积分：{5} ||| 代理：{6}".format(
                    request["data"]["name"],
                    request["data"]["email"],
                    request["data"]["state"],
                    request["data"]["balance"]["current_amount"],
                    float(request["data"]["balance"]["total_collected"]) - float(
                        request["data"]["balance"]["current_amount"]),
                    request["data"]["balance"]["total_collected"],
                    proxy,
                    env_name, request["code"],flush=True
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
                    b = 0
                    while b < 10:
                        try:
                            ping = await client.post("https://nw.nodepay.org/api/network/ping",json=data)
                            print(
                                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                " ||| 环境ID：{3} ||| Ping检测状态：{0} ||| IP检测分数：{1} ||| 代理：{2}".format(ping['success'],ping['data']['ip_score'],proxy,env_name), flush=True
                            )
                            a = 0
                            b = 15
                        except Exception as e:
                            b += 1
                            print(
                                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                " ||| 环境ID：{1} ||| 代理：{0} ||| 执行PING失败,正在重试,第 {2} 次重试~".format(proxy,env_name,b), flush=True
                            )

                            await asyncio.sleep(30)


            elapsed_time = time.time() - start_time
            sleep_time = max(0, 300 - elapsed_time)
            await asyncio.sleep(sleep_time)

        except Exception as e:
            print(env_name,"|||",proxy, flush=True)
            await asyncio.sleep(3600)


async def main():
    with open("/root/nodepay-1.txt", "r") as f:
        data = f.readlines()

        tasks = []
        for line in data:
            env_name, email, browser_id, token, proxy, none = line.strip().split("|")
            await asyncio.sleep(5)
            task = asyncio.create_task(toKeep(token, proxy, env_name, email))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

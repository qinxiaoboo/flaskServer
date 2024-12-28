from DrissionPage import Chromium
from flaskServer.config.chromiumOptions import initChromiumOptions
from flaskServer.utils.chrome import getChromiumOptions
from flaskServer.services.dto.proxy import getProxyByID
from flaskServer.services.dto.env import getChoiceEnvs
import time
import itertools

def initChrom(chrome,env,http_host,http_port,user,pw):
    # 设置代理
    chrome.new_tab(f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    chrome.new_tab("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.new_tab(f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")

chrome = Chromium(addr_or_opts=getChromiumOptions(initChromiumOptions("custom_env", 30000, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", None)))

def get_wallet(chrome):
    tab = chrome.new_tab(url="chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html")
    if tab.s_ele("@type=password"):
        tab.ele("@data-testid=okd-input").input("123qweasd")
        tab.ele("@type=submit").click()
        tab.ele("@type=button")

    chrome.wait(1,2)
    tab.ele("@class=_address_1czhn_28").click()
    next_wallet = tab.ele("@class=okui-checkbox-circle okui-checkbox-circle-checked").after("t:div")
    tab.ele(next_wallet).click()
    tab.close()

Faucet_url = 'https://faucet.testnet.humanity.org/'

proxy = [
    {"ip": "", "user": "", "passwd": ""},

]
wallet_address = [

]

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")


for i, proxy_msg in enumerate(proxy):
    address = list(itertools.islice(itertools.cycle(wallet_address), i, i + 1))[0]
    initChrom(chrome, "custom_env", proxy_msg["ip"], "8000", proxy_msg["user"], proxy_msg["passwd"])
    tab = chrome.new_tab("https://faucet.testnet.humanity.org/")
    chrome.close_tabs(tabs_or_ids=tab, others=True)
    tab.ele('@placeholder=Enter your address or ENS name').input(address, clear=True)
    chrome.wait(2)
    tab.ele('@class=button is-primary is-rounded').click()

    if tab.s_ele("Txhash"):
        print_colored(f"序号：{wallet_address.index(address)} -- 地址：{address} -- 测试币领取成功","32")

    else:
        print_colored(f"序号：{wallet_address.index(address)} -- 地址：{address} -- 测试币领取失败", "31")



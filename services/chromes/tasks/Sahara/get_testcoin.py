from DrissionPage import Chromium
from flaskServer.config.chromiumOptions import initChromiumOptions
from flaskServer.utils.chrome import getChromiumOptions
from flaskServer.services.dto.proxy import getProxyByID
from flaskServer.services.dto.env import getChoiceEnvs
import time



def initChrom(chrome,env,http_host,http_port,user,pw):
    # 设置代理
    chrome.new_tab(f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    chrome.new_tab("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.new_tab(f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")

chrome = Chromium(addr_or_opts=getChromiumOptions(initChromiumOptions("custom_env", 30000, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", None)))

proxy = [
    {"ip": "181.177.100.195", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.203", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.194", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.253", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.153", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.141", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.95", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.153", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.41", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.192", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.40", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.98", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.244", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.35", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.101", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.31", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.164", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.132", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.176", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.140", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.168", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.239", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.253", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.42", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.152", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.219", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.146", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.98", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.137", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.56", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.107", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.133", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.196", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.116", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.119", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.72", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.232", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.194", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.65", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.52", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.18", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.168", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.166", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.217", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.209", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.111", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.57", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.252", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.172", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.103", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.145", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.178", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.25", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.98", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.67", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.136", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.137", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.122", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.66", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.230", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.108", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.215", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.97", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.30", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.176", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.233", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.25", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.55", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.43", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.102", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.141", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.123", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.229", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.73", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.82", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.112", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.203", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.77", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.89", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.209", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.215", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.89", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.24", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.45", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.68", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.86", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.214", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.64", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.102", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.187", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.82", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "132.255.134.166", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.39", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.202", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.3", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.176", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.100.75", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.199", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "161.0.71.56", "user": "h7RtWs", "passwd": "c41FXA"},
    {"ip": "181.177.101.118", "user": "h7RtWs", "passwd": "c41FXA"},
]

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



for proxy_msg in proxy:

    initChrom(chrome, "custom_env", proxy_msg["ip"], "8000", proxy_msg["user"], proxy_msg["passwd"])
    tab = chrome.new_tab("https://faucet.saharaa.info/")
    new_tab = chrome.new_tab("https://faucet.saharaa.info/")
    get_wallet(chrome)
    chrome.close_tabs(tabs_or_ids=new_tab, others=True)
    new_tab.refresh()
    chrome.wait(2, 3)

    if new_tab.s_ele("Logout"):
        new_tab.ele("Logout").click()

    new_tab.ele("@class=text-saPrimaryBg body-1-normal").click()
    new_tab.ele("OKX Wallet").click.for_new_tab(timeout=3).ele("t:button",index=2).click()

    new_tab.refresh()
    chrome.wait(2, 3)

    time.sleep(5)
    new_tab.ele("@class=text-saPrimaryBg body-1-normal").click()
    time.sleep(20)


    if new_tab.s_ele("Txhash"):
        print("领取成功")
    if new_tab.s_ele("You have exceeded the rate limit."):
        print("You have exceeded the rate limit.")

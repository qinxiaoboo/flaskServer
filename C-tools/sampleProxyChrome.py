from DrissionPage import Chromium
from flaskServer.config.chromiumOptions import initChromiumOptions
from flaskServer.utils.chrome import getChromiumOptions
from flaskServer.services.dto.proxy import getProxyByID
from flaskServer.services.dto.env import getChoiceEnvs

def initChrom(chrome,env,http_host,http_port,user,pw):
    # 设置代理
    chrome.new_tab(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    chrome.new_tab("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.new_tab(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")

chrome = Chromium(addr_or_opts=getChromiumOptions(initChromiumOptions("custom_env", 30000, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", None)))


for env in getChoiceEnvs():
    proxy = getProxyByID(env.t_proxy_id)
    initChrom(chrome, "custom_env", proxy.ip, proxy.port, proxy.user, proxy.pwd)
    tab = chrome.new_tab("https://faucet.saharaa.info/")
    chrome.close_tabs(tabs_or_ids=tab, others=True)
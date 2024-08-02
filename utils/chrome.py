
from loguru import logger
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from flaskServer.config.chromiumOptions import initChromiumOptions
from flaskServer.config.config import get_ini_path
from flaskServer.services.dto.env import updateEnvStatus


def wait_pages(chrome,wait_page_list):
    count = 100
    while count:
        for tab_id in chrome.tab_ids:
            tab = chrome.get_tab(id_or_num=tab_id)
            for title in wait_page_list:
                if title in tab.title:
                    wait_page_list.remove(title)
                    continue
        if len(wait_page_list) > 0:
            chrome.wait(1,2)
            count-= 1
        else:
            break

def setTitle(chrome,env):
    tab = chrome.get_tab(url="whoer.com")
    tab.run_js(f"document.title='{env.name}'")

def closeInitTab(chrome):
    tab = chrome.get_tab(title="Welcome to OKX")
    tab.close()

def getChrome(proxy,env):
    chrome = None
    try:
        if env.status == 0 or env.status == None:  # 如果环境是初始化状态
            if proxy:  # 需要代理
                chrome = ChromiumPage(addr_or_opts=
                    initChromiumOptions(env.name, env.port, env.user_agent,"http://" + proxy.ip + ":" + proxy.port))
                initChrom(chrome, env.name, proxy.ip, proxy.port, proxy.user, proxy.pwd)
            else:
                chrome = ChromiumPage(addr_or_opts=initChromiumOptions(env.name, env.port, env.user_agent, None))
        else:
            ini_path = get_ini_path(env.name)
            if ini_path.exists():
                chrome = ChromiumPage(addr_or_opts=ChromiumOptions(ini_path=ini_path))
            else:
                logger.error(f"{env.name}: ini_path配置文件不存在")
        if chrome:
            chrome.get("https://whoer.com/zh?env=" + env.name)
            wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
            wait_pages(chrome, wait_page_list)
            closeInitTab(chrome)
            setTitle(chrome, env)
            updateEnvStatus(env.name, 1)
        return chrome
    except Exception as e:
        if chrome:
            chrome.quit()
        raise e

def initChrom(chrome,env,http_host,http_port,user,pw):
    # 设置代理
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    chrome.get("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")


if __name__ == '__main__':
    pass


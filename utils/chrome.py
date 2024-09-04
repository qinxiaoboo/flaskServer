from loguru import logger
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from DrissionPage.errors import *
from flaskServer.config.chromiumOptions import initChromiumOptions
from flaskServer.config.config import HEADLESS,get_ini_path,MUTE,OFF_VIDEO,OFF_IMG,WORK_PATH
from flaskServer.services.dto.env import updateEnvStatus, updateOpenStatus, getEnvsByIds
from flaskServer.services.dto.proxy import updateProxyStatus
from flaskServer.utils.envutil import getUserAgent
from flaskServer.utils.decorator import chrome_retry

def get_Custome_Tab(tab):
    # if OFF_VIDEO:
    #     tab.set.blocked_urls(('*f=MP4*','*.m4s*','*.mp4*', '*.m3u8*','*ext_tw_video*','*amplify_video*'))
    # if OFF_IMG:
    #     tab.set.blocked_urls(('*f=JPEG*','*f=PNG*','*f=JPG*','*.png*','*.jpg*','*.gif*','*images*'))
    return tab

def get_captcha_response(iframe):
    if "data-hcaptcha-response" in iframe.attrs:
        return iframe.attrs.get("data-hcaptcha-response")
    elif 'id="recaptcha-token"' in iframe.html:
        ele = iframe.ele("@class=rc-anchor-center-item rc-anchor-checkbox-holder").ele("@role=checkbox")
        return ele.attrs.get("aria-checked") == "true"
    else:
        return False

def wait_captcha_page(tab,env):
    count = 0
    tab.ele('@title=reCAPTCHA')
    logger.info(f"{env.name}: 开始人机验证")
    while not get_captcha_response(tab.get_frame(1)):
        if count < 40:
            count += 1
            tab.wait(5, 6)
        else:
            logger.error(f"{env.name}: 人机验证时间过长，验证失败， 请查看失败原因~")
            return False
    logger.info(f"{env.name}：人机验证成功")
    return True


def wait_pages(chrome, wait_page_list):
    count = 66
    while count:
        for tab_id in chrome.tab_ids:
            tab = chrome.get_tab(id_or_num=tab_id)
            for title in wait_page_list:
                if title in tab.title:
                    wait_page_list.remove(title)
                    continue
        if len(wait_page_list) > 0:
            chrome.wait(1,2)
            refreshInitTab(chrome)
            count-= 1
        else:
            break
    return (len(wait_page_list) == 0)


def setTitle(chrome,env):
    tab = chrome.get_tab(title=f"Browser Fingerprint")
    tab.run_js(f"document.title='{env.name}'")

def refreshInitTab(chrome):
    tab = chrome.get_tab(title="www.okx.com")
    if tab:
        tab.refresh()
    okx = chrome.get_tab(title="OKX Wallet")
    if okx:
        okx.refresh()

def closeInitTab(chrome):
    tab = chrome.get_tab(title="Welcome to OKX")
    tab.close()

def getChromiumOptions(co):
    co.headless(on_off=HEADLESS)
    co.mute(on_off=MUTE)
    return co

def getChromiumPage(env, proxy): # 获取一个ChromiumPage对象
    chrome = None
    try:
        if env.status == 0 or env.status == None:  # 如果环境是初始化状态
            if proxy:  # 需要代理
                chrome = ChromiumPage(addr_or_opts=getChromiumOptions(initChromiumOptions(env.name, env.port, getUserAgent(env.user_agent), "http://" + proxy.ip + ":" + proxy.port)))
                initChrom(chrome, env.name, proxy.ip, proxy.port, proxy.user, proxy.pwd)
            else:
                chrome = ChromiumPage(addr_or_opts=getChromiumOptions(initChromiumOptions(env.name, env.port, getUserAgent(env.user_agent), None)))
        else:
            ini_path = get_ini_path(env.name)
            if ini_path.exists():
                chrome = ChromiumPage(addr_or_opts=getChromiumOptions(ChromiumOptions(ini_path=ini_path)))
            else:
                raise Exception(f"{env.name}: ini_path配置文件不存在")
        return chrome
    except Exception as e:
        quitChrome(env, chrome)
        raise e

def checkIP(env,chrome):
    while "正在获取 IP 信息..." in chrome.ele("#result").text:
        chrome.wait(1)
    print(f'{env.name}: {chrome.ele("#result").text}')
    if "TypeError: Failed to fetch" in chrome.ele("#result").text:
        updateProxyStatus(env, 1)
        raise Exception(f"{env.name}: 代理IP连接失败")
    else:
        updateProxyStatus(env, 2)

@chrome_retry(exceptions=(WaitTimeoutError,), max_tries=3, initial_delay=2)
def getChrome(proxy, env):
    chrome = None
    try:
        chrome = getChromiumPage(env, proxy)
        updateOpenStatus(env.name, 1)
        # chrome.set.auto_handle_alert(accept=False,all_tabs=True)
        chrome.get(fr'file:///{WORK_PATH}\flaskServer\utils\pages\index.html?env={env.name}')
        checkIP(env, chrome)
        wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
        flag = wait_pages(chrome, wait_page_list)
        if flag:
            closeInitTab(chrome)
            setTitle(chrome, env)
            updateEnvStatus(env.name, 1)
            logger.info(f"{env.name}: 页面等待成功~ \nUserAgent：{chrome.user_agent}")
        else:
            raise WaitTimeoutError("等待初始页面等待超时！~")
        return chrome
    except Exception as e:
        quitChrome(env, chrome)
        raise e

def initChrom(chrome,env,http_host,http_port,user,pw):
    # 设置代理
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    chrome.get("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")

def quitChrome(env, chrome):
    if chrome:
        chrome.quit()
    updateOpenStatus(env.name, 0)

def quitChromeByEnvIds(ids):
    envs = getEnvsByIds(ids)
    for env in envs:
        if env.isOpen == 1:
            env.status = 1
            quitChrome(env, getChromiumPage(env, None))







if __name__ == '__main__':
    pass


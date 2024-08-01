import random
from flaskServer.config.config import WORK_PATH
s = list()
with open(WORK_PATH + r'\flaskServer\utils\useragent.txt', 'r') as f:
    for line in f:
        s.append(line.strip())

def getUserAgent(userAgent):
    if userAgent:return userAgent
    return random.choice(s)


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

def initChrom(chrome,env,http_host,http_port,user,pw):
    # 设置代理
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    chrome.get("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")


if __name__ == '__main__':
    print(getUserAgent(userAgent=""))


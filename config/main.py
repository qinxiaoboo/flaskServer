import time
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from flaskServer.config.chromiumOptions import initChromiumOptions
env = "q1"
user = "oz2USP"
pw= "Pr382u"
http_host = "168.80.24.58"
http_port = "8000"

def initChrom(chrome,env,user,pw,http_host,http_port):
    # 设置代理
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
    time.sleep(1)
    chrome.get("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/popup.html")
    chrome.get(
        f"chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html?env={env}&user={user}&pass={pw}&http_host={http_host}&http_port={http_port}")
def wait_pages(chrome,wait_page_list):
    while True:
        for tab_id in chrome.tab_ids:
            tab = chrome.get_tab(id_or_num=tab_id)
            for title in wait_page_list:
                if title in tab.title:
                    wait_page_list.remove(title)
                    continue
        if len(wait_page_list) > 0:
            chrome.wait(1,2)
        else:
            break

def print_hi(name):
    useragent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Agency/98.8.8175.80"
    chrome = ChromiumPage(addr_or_opts=initChromiumOptions("Q-1","9223", useragent, "http://168.80.24.58:8000"))

    initChrom(chrome,env,user,pw,http_host,http_port)
    chrome.get("https://www.browserscan.net/zh")
    wait_page_list = ["Initia Wallet", "Welcome to OKX", "OKX Wallet"]
    wait_pages(chrome,wait_page_list)
    tab = chrome.get_tab(title="Initia Wallet")
    print(tab.title)


    # chrome.close_tabs(others=True)
    print(ChromiumOptions().address)
    # tab = chrome.new_tab()
    # tab.get("https://faucet.0g.ai")
    # tab.ele("#address").input("0x670d0e57dc475ec92c9268bbec5db9e5162378e2")
    # tab.ele("@type=submit").wait.enabled(timeout=200)
    # tab.ele("@type=submit").click()
    # ele = tab.ele("@class=mt-2")
    # ele = ele.ele("tag:p")
    #
    # print(ele)

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

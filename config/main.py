import time
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions

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


def print_hi(name):
    chrome = ChromiumPage(9222)

    initChrom(chrome,env,user,pw,http_host,http_port)
    chrome.get("https://www.browserscan.net/zh")

    time.sleep(3)
    chrome.close_tabs(others=True)
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

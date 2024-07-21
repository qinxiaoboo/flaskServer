# DrissionPage 包含三种主要页面类。根据需要在其中选择使用。
import time

from DrissionPage import ChromiumPage
#如果只要收发数据包，导入SessionPage。
from DrissionPage import SessionPage
# WebPage是功能最全面的页面类，既可控制浏览器，也可收发数据包。
from DrissionPage import WebPage
# ChromiumOptions类用于设置浏览器启动参数。
from DrissionPage import ChromiumOptions
# SessionOptions类用于设置Session对象启动参数。
#
# 用于配置SessionPage或WebPages 模式的连接参数。

from DrissionPage import SessionOptions
# Settings
# Settings用于设置全局运行配置，如找不到元素时是否抛出异常等。

from DrissionPage.common import Settings
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
    chrome = ChromiumPage()
    # initChrom(chrome,env,user,pw,http_host,http_port)
    chrome.get("https://whoer.net")
    chrome.close_tabs(others=True)
    print(ChromiumOptions().address)
    tab = chrome.new_tab()
    tab.get("https://faucet.0g.ai")
    tab.ele("#address").input("0x670d0e57dc475ec92c9268bbec5db9e5162378e2")
    tab.ele("@type=submit").wait.enabled(timeout=200)
    tab.ele("@type=submit").click()
    ele = tab.ele("@class=mt-2")
    ele = ele.ele("tag:p")

    print(ele)

    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

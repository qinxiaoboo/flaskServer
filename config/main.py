import time
import requests

def print_hi(name):
    # tab = chrome.new_tab()
    # tab.get("https://faucet.0g.ai")
    # tab.ele("#address").input("0x670d0e57dc475ec92c9268bbec5db9e5162378e2")
    # tab.ele("@type=submit").wait.enabled(timeout=200)
    # tab.ele("@type=submit").click()
    # ele = tab.ele("@class=mt-2")
    # ele = ele.ele("tag:p")
    #
    # print(ele)
    res = requests.get("https://2fa.fb.rip/api/otp/TQNSHKZUJZNZWDMG")
    print(res.ok)
    print(res.json().get("data").get("otp"))
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

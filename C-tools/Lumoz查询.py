from DrissionPage import Chromium
from DrissionPage import ChromiumPage
from DrissionPage import WebPage
from DrissionPage import SessionPage
from DrissionPage.common import Settings
from DrissionPage import SessionOptions
from DrissionPage import ChromiumOptions
from concurrent.futures import ThreadPoolExecutor
import time




name = 'Lumoz'
Lumoz_url = 'https://lumoz.org/airdrop'
WALLET_PASSWORD = '123qweasd'

silver_click_wallet_js = """
            const button  = document.querySelector("body > w3m-modal").shadowRoot.querySelector("wui-flex > wui-card > w3m-router").shadowRoot.querySelector("div > w3m-connect-view").shadowRoot.querySelector("wui-flex > w3m-wallet-login-list").shadowRoot.querySelector("wui-flex > w3m-connect-announced-widget").shadowRoot.querySelector("wui-flex > wui-list-wallet").shadowRoot.querySelector("button");
            return button
            """


path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
ChromiumOptions().set_browser_path(path).save()

co1 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co1 = co1.add_extension(r'D:\data\etd\yescap_v2.0')
co1 = co1.set_local_port(19888).set_user_data_path('data6')

co2 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co2 = co2.add_extension(r'D:\data\etd\yescap_v2.0')
co2 = co2.set_local_port(19777).set_user_data_path('data5')

co3 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co3 = co3.add_extension(r'D:\data\etd\yescap_v2.0')
co3 = co3.set_local_port(19999).set_user_data_path('data7')

co4 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co4 = co4.add_extension(r'D:\data\etd\yescap_v2.0')
co4 = co4.set_local_port(20000).set_user_data_path('data8')



Mnemonics1 = {
# "地址": "私钥"

}


Mnemonics2 = {
# "地址": "私钥"

}


Mnemonics3 = {
# "地址": "私钥"

}


Mnemonics4 = {
# "地址": "私钥"

}


def AddWallet(chrome, row):
    tab = chrome.get_tab(title="OKX Wallet")
    try:
        if tab.s_ele("@type=password"):
            tab.ele("@data-testid=okd-input").input(WALLET_PASSWORD)
            tab.ele("@type=submit").click()
            tab.ele("@type=button")
            change(chrome,row)
        else:
            tab.ele("导入已有钱包").click()
            tab.ele("助记词或私钥").click()
            tab.ele("@class=okui-tabs-pane okui-tabs-pane-sm okui-tabs-pane-grey okui-tabs-pane-segmented").click()
            tab.ele("@type=password").input(row)
            chrome.wait(8,10)
            tab.ele("@class=okui-btn btn-lg btn-fill-highlight block mobile").click()
            tab.ele("@class=okui-btn btn-lg btn-fill-highlight block mobile chains-choose-network-modal__confirm-button").click()
            chrome.wait(2)
            passwords = tab.eles("@type=password")
            for pwd in passwords:
                pwd.input(WALLET_PASSWORD)
            tab.ele("@type=submit").click()
            tab.ele("@type=button").click()
            chrome.wait(2)
        okxtab = chrome.get_tab(url="https://www.okx.com/zh-hans/web3/extension/welcome")
        okxtab.close()
        tab.close()
    except Exception as e:
        print(e)

def change(chrome, row):
    tab = chrome.new_tab(url="chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html")
    tab.ele("@class=_wallet-icon_e7iqh_1 _wallet-icon__radius_e7iqh_22 _wallet-icon__icon_e7iqh_64 okx-wallet-plugin-down-1").click()
    chrome.wait(1)
    tab.ele("@class=_wallet-link_fxfbg_1 _editWalletEntry_12w6i_6").click()
    chrome.wait(1)
    tab.ele("@class=_wallet-icon_e7iqh_1 _wallet-icon__radius_e7iqh_22 _wallet-icon__md_e7iqh_44 _wallet-icon__icon_e7iqh_64 undefined okx-wallet-plugin-delete").click()
    chrome.wait(1)
    tab.ele("@data-testid=okd-dialog-confirm-btn").click()
    chrome.wait(1)
    tab.ele("@data-testid=okd-input").input(WALLET_PASSWORD)
    chrome.wait(1)
    tab.ele("@data-testid=okd-button").click()
    chrome.wait(1)
    tab.ele("导入已有钱包").click()
    tab.ele("助记词或私钥").click()
    tab.ele("@class=okui-tabs-pane okui-tabs-pane-sm okui-tabs-pane-grey okui-tabs-pane-segmented").click()
    tab.ele("@type=password").input(row)
    chrome.wait(8, 10)
    if tab.s_ele("@class=okui-btn btn-lg btn-fill-highlight block mobile"):
        tab.ele("@class=okui-btn btn-lg btn-fill-highlight block mobile").click()
        tab.ele("@class=okui-btn btn-lg btn-fill-highlight block mobile chains-choose-network-modal__confirm-button").click()
    else:
        tab.ele("@class=okui-btn btn-lg btn-fill-highlight block").click()
        tab.ele("@class=okui-btn btn-lg btn-fill-highlight block chains-choose-network-modal__confirm-button").click()
    chrome.wait(2)
    passwords = tab.eles("@type=password")
    for pwd in passwords:
        pwd.input(WALLET_PASSWORD)
    tab.ele("@type=submit").click()
    tab.ele("@type=button").click()
    tab.close()


def getLumoz(chrome,token,txt):
    tab = chrome.latest_tab
    tab.get('https://lumoz.org/airdrop')

    if tab.s_ele("@src=data:image/svg+xml,%3csvg%20width='21'%20height='20'%20viewBox='0%200%2021%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3crect%20x='1'%20y='0.5'%20width='19'%20height='19'%20rx='3.5'%20stroke='%23BEFE00'/%3e%3c/svg%3e"):
        tab.ele("@src=data:image/svg+xml,%3csvg%20width='21'%20height='20'%20viewBox='0%200%2021%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3crect%20x='1'%20y='0.5'%20width='19'%20height='19'%20rx='3.5'%20stroke='%23BEFE00'/%3e%3c/svg%3e").click()
        tab.ele("@class=home-button-corner px-4 py-1.5 hvr-bounce-in home-button-corner text-black w-32").click()

    addresses = list(token.keys())
    for i in range(len(addresses)):
        address = addresses[i]
        AddWallet(chrome, token[address])
        tab.wait(10, 15)
        tab.refresh()
        tab.wait(5,10)

        try:
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        except Exception as e:
            pass
        if tab.s_ele("Connect Wallet"):
            tab.ele("Connect Wallet").click()
            chrome.wait(3, 5)
            try:
                chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
            except AttributeError as e:
                okxbutton = tab.run_js(silver_click_wallet_js)
                okxbutton.click.for_new_tab().ele("@type=button", index=2).click()
                chrome.wait(3, 5)
                try:
                    chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
                except AttributeError as e:
                    pass
            except RuntimeError as e:
                pass
        chrome.wait(1, 2)
        esMOZ_num = tab.ele("@class=font-bold text-primary-900 mr-2 text-xl").text
        MOZ_num = tab.ele("@class=font-bold text-primary-900 text-xl").text

        with open(f'{txt}.txt', 'a') as file:
            # 钱包地址、esMOZ数量、MOZ数量
            file.write("\n"f'{address} {esMOZ_num} {MOZ_num}')

        if txt == "co1":
            print(f"线程 1 : {address} 统计完成：{esMOZ_num} esMoz，{MOZ_num}")

        if txt == "co2":
            print(f"线程 2 : {address} 统计完成：{esMOZ_num} esMoz，{MOZ_num}")

        if txt == "co3":
            print(f"线程 3 : {address} 统计完成：{esMOZ_num} esMoz，{MOZ_num}")

        if txt == "co4":
            print(f"线程 4 : {address} 统计完成：{esMOZ_num} esMoz，{MOZ_num}")

        if i + 1 < len(addresses):
            next_address = addresses[i + 1]
            change(chrome, token[next_address])

def run_lumoz_with_delay(co, mnemonics, label, delay):
    time.sleep(delay)
    getLumoz(Chromium(co), mnemonics, label)

if __name__ == '__main__':
    # getLumoz(Chromium( co1), Mnemonics1, 'co1')
    with ThreadPoolExecutor() as executor:
        executor.submit(run_lumoz_with_delay, co1, Mnemonics1, 'co1', 0)
        executor.submit(run_lumoz_with_delay, co2, Mnemonics2, 'co2', 10)
        executor.submit(run_lumoz_with_delay, co3, Mnemonics3, 'co3', 20)
        executor.submit(run_lumoz_with_delay, co4, Mnemonics4, 'co4', 30)
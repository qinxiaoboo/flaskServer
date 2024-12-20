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

# 设置浏览器
path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

ChromiumOptions().set_browser_path(path).save()
co1 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co1 = co1.add_extension(r'D:\data\etd\yescap_v2.0')
co1 = co1.set_local_port(22222).set_user_data_path('data1')

co2 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co2 = co2.add_extension(r'D:\data\etd\yescap_v2.0')
co2 = co2.set_local_port(19777).set_user_data_path('data2')

co3 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co3 = co3.add_extension(r'D:\data\etd\yescap_v2.0')
co3 = co3.set_local_port(22221).set_user_data_path('data3')

co4 = ChromiumOptions().add_extension(r'D:\data\etd\okx')
co4 = co4.add_extension(r'D:\data\etd\yescap_v2.0')
co4 = co4.set_local_port(22220).set_user_data_path('data4')



# 指纹内地址合集
Mnemonics1 = {
"evm地址": "助记词",

}

Mnemonics2 = {

}

Mnemonics3 = {


}

Mnemonics4 = {

}

def AddWallet(chrome, row):
    # 打开okx钱包标签
    # tab = chrome.get_tab(url="chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html")
    tab = chrome.get_tab(title="OKX Wallet")
    try:
        if tab.s_ele("@type=password"):
            tab.ele("@data-testid=okd-input").input(WALLET_PASSWORD)
            tab.ele("@type=submit").click()
            tab.ele("@type=button")

        else:
            chrome.wait(2)
            # 开始更换钱包
            tab.ele("导入已有钱包").click()
            tab.ele("助记词或私钥").click()
            input_box = tab.eles("@type=text")
            for index, word in enumerate(row.split(" ")):
                input_box[index].input(word)
            chrome.wait(2)
            tab.ele("确认").click()
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
        pass

def change(chrome, row):
    tab = chrome.new_tab(url="chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html")
    tab.ele("@class=_wallet-icon_e7iqh_1 _wallet-icon__radius_e7iqh_22 _wallet-icon__icon_e7iqh_64 okx-wallet-plugin-down-1").click()
    chrome.wait(1)
    tab.ele("@class=_wallet-link_fxfbg_1 _editWalletEntry_12w6i_6").click()
    chrome.wait(1)
    tab.ele("@class=icon iconfont okx-wallet-plugin-delete _wallet-icon__icon__core_e7iqh_64").click()
    chrome.wait(1)
    tab.ele("@data-testid=okd-dialog-confirm-btn").click()
    chrome.wait(1)
    tab.ele("@data-testid=okd-input").input(WALLET_PASSWORD)
    chrome.wait(1)
    tab.ele("@data-testid=okd-button").click()
    chrome.wait(1)
    tab.ele("导入已有钱包").click()
    tab.ele("助记词或私钥").click()

    input_box = tab.eles("@type=text")
    for index, word in enumerate(row.split(" ")):
        input_box[index].input(word)
    chrome.wait(2)
    tab.ele("确认").click()
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
        tab.refresh()
        chrome.wait(3,5)
        try:
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        except Exception as e:
            pass
        if tab.s_ele("Connect Wallet"):
            tab.ele("Connect Wallet").click()
            chrome.wait(3,5)
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

        tab.ele("Lumoz OG NFT").click()
        chrome.wait(1, 2)
        sly_claim_num = tab.ele("@class=text-base font-bold ml-1",index=1).text
        sly_claim = tab.ele("@class=text-base font-bold ml-1", index=2).text

        puff_claim_num = tab.ele("@class=text-base font-bold ml-1",index=3).text
        puff_claim = tab.ele("@class=text-base font-bold ml-1", index=4).text

        claw_claim_num = tab.ele("@class=text-base font-bold ml-1",index=5).text
        claw_claim = tab.ele("@class=text-base font-bold ml-1", index=6).text

        with open(f'{txt}.txt', 'a') as file:
                            #钱包地址、sly已领取数量、sly未领取数量、puff已领取数量、puff未领取数量、claw已领取数量、claw未领取数量
            file.write("\n"f'{address} {sly_claim_num} {sly_claim} {puff_claim_num} {puff_claim} {claw_claim_num} {claw_claim}')

        if txt == "co1":
            print("线程 1 ： ",address,"   统计完成")

        if txt == "co2":
            print("线程 2 ： ",address,"   统计完成")

        if txt == "co3":
            print("线程 3 ： ",address, "   统计完成")

        if txt == "co4":
            print("线程 4 ： ",address, "   统计完成")

        if i + 1 < len(addresses):
            next_address = addresses[i + 1]
            change(chrome, token[next_address])


def claimNFT(chrome,token):
    tab = chrome.latest_tab
    tab.get('https://lumoz.org/airdrop')

    if tab.s_ele("@src=data:image/svg+xml,%3csvg%20width='21'%20height='20'%20viewBox='0%200%2021%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3crect%20x='1'%20y='0.5'%20width='19'%20height='19'%20rx='3.5'%20stroke='%23BEFE00'/%3e%3c/svg%3e"):
        tab.ele("@src=data:image/svg+xml,%3csvg%20width='21'%20height='20'%20viewBox='0%200%2021%2020'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3crect%20x='1'%20y='0.5'%20width='19'%20height='19'%20rx='3.5'%20stroke='%23BEFE00'/%3e%3c/svg%3e").click()
        tab.ele("@class=home-button-corner px-4 py-1.5 hvr-bounce-in home-button-corner text-black w-32").click()


    addresses = list(token.keys())
    for i in range(len(addresses)):
        address = addresses[i]
        AddWallet(chrome, token[address])
        tab.refresh()
        chrome.wait(3,5)
        try:
            chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
        except Exception as e:
            pass
        if tab.s_ele("Connect Wallet"):
            tab.ele("Connect Wallet").click()
            chrome.wait(3,5)
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

        tab.ele("Lumoz OG NFT").click()
        chrome.wait(1, 2)
        if tab.s_ele("@class=mt-4 py-1 text-sm w-24 lg:w-28 lg:text-base rounded-lg font-bold flex items-center justify-center bg-[#BEFE0044] text-primary-900 hvr-grow"):
            claim_button = tab.eles("@class=mt-4 py-1 text-sm w-24 lg:w-28 lg:text-base rounded-lg font-bold flex items-center justify-center bg-[#BEFE0044] text-primary-900 hvr-grow")
            chrome.wait(1, 2)
            for claim in claim_button:
                # 网页点击claim
                claim.click()
                chrome.wait(2, 3)
                # 钱包点击确认
                chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
                chrome.wait(2, 3)
                if tab.s_ele("@class=el-notification__title"):
                    print(f"{address}被女巫标记")
                    break

                if tab.s_ele("Your last claim is being executed"):
                    print(f"{address}正常，领取失败，手工介入")
                    break

                # 网页点击confim
                tab.ele("@class=text-center border border-primary-900 bg-[#BEFE0044] text-primary-900 font-bold py-2 rounded-lg cursor-pointer opacity-90 hover:opacity-100 w-full flex items-center justify-center").click()
                chrome.wait(2, 3)
                # 钱包确认交易

                if chrome.get_tab(title="OKX Wallet").s_ele("补充"):
                    chrome.get_tab(title="OKX Wallet").ele("@type=button", index=1).click()
                    print(f"{address}正常，没有足够的ETH")
                    break

                chrome.get_tab(title="OKX Wallet").ele("@type=button", index=2).click()
                chrome.wait(15, 20)
                print(f"{address}领取成功")
        else:
            print(f"{address}没有NFT可以领取")
        if i + 1 < len(addresses):
            next_address = addresses[i + 1]
            change(chrome, token[next_address])

def run_lumoz_with_delay(co, mnemonics, label, delay):
    time.sleep(delay)  # 延迟启动
    # getLumoz(Chromium(co), mnemonics, label)
    claimNFT(Chromium(co), mnemonics)

if __name__ == '__main__':
    # run_lumoz_with_delay(co1, Mnemonics1, 'co1', 0)

    with ThreadPoolExecutor() as executor:
        # 提交任务，并设置启动延迟
        executor.submit(run_lumoz_with_delay, co1, Mnemonics1, 'co1', 0)   # 立即启动
        executor.submit(run_lumoz_with_delay, co2, Mnemonics2, 'co2', 10)  # 延迟10秒启动
        executor.submit(run_lumoz_with_delay, co3, Mnemonics3, 'co3', 20)  # 延迟20秒启动
        executor.submit(run_lumoz_with_delay, co4, Mnemonics4, 'co4', 30)  # 延迟30秒启动


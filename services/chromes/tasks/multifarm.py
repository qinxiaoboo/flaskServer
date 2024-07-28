from DrissionPage import ChromiumPage
from flaskServer.config.connect import db,app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import InitChromeOptionByConf,LoginTW,AuthTW, ConfirmOKXWallet

def toDo():
    with app.app_context():
        env = Env.query.filter_by(name="Q-8-3").first()
        chrome:ChromiumPage = InitChromeOptionByConf(env)
        LoginTW(chrome,env)
        tab = chrome.new_tab(url="http://www.multifarm.io/?r=37JUJ4")
        tab.ele("get started").click()
        if "dashboard" not in tab.url:
            tab.ele("sign in to x").click()
            chrome.wait(2,3)
            AuthTW(chrome,env)
            wallet_tab = tab.ele("Metamask").click.for_new_tab()
            ConfirmOKXWallet(chrome,wallet_tab,env)
        buttons = tab.eles("@class=icon uppercase")
        for button in buttons:
            button.click()
            tw = tab.ele("@class= flex gap-2 items-center ").click.for_new_tab()
            print(tw)
            tw.close()
        tab.eles("Completed")






if __name__ == '__main__':
    pass
    toDo()
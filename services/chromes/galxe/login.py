from flaskServer.services.chromes.login import GalxeChrome
from flaskServer.config.connect import app
from flaskServer.mode.env import Env
from flaskServer.services.chromes.login import ConfirmOKXWallet


if __name__ == '__main__':
    with app.app_context():
        env = Env.query.filter_by(name="Q-1").first()
        chrome = GalxeChrome(env)
        tab  = chrome.new_tab("https://app.galxe.com/quest/PlumeNetwork/GCzqctkqub")
        login = tab.s_ele("@@type=button@@text()=Log in")
        if login:
            tab.ele("@@type=button@@text()=Log in").click()
            new_tab = tab.ele("@@class=flex items-center@@text()=OKX").next().click.for_new_tab()
            ConfirmOKXWallet(chrome,new_tab,env)
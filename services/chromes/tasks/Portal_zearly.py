import random
from random_words import RandomWords
#pip install RandomWords
from DrissionPage import ChromiumPage,ChromiumOptions
from loguru import logger
# 连接数据库
from flaskServer.config.connect import app
#数据库信息
from flaskServer.mode.env import Env
import time
#配置代理
from flaskServer.mode.proxy import Proxy
#创建浏览器
from flaskServer.services.chromes.worker import submit
#变量
from flaskServer.services.content import Content
#登录环境账号
from flaskServer.services.chromes.login import OKXChrome
from flaskServer.services.dto.account import getAccountById
from pprint import pprint
from flaskServer.config.connect import db
from flaskServer.mode.account import Account
from flaskServer.utils.crypt import aesCbcPbkdf2DecryptFromBase64
from flaskServer.services.chromes.login import tw2faV
from flaskServer.services.dto.env import updateAllStatus,getAllEnvs,getEnvsByGroup
from threading import Thread
from flaskServer.services.chromes.login import LoginDiscord
from flaskServer.utils.chrome import quitChrome
from flaskServer.utils.decorator import chrome_retry
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.services.chromes.login import LoginTW
import time
import string
import random




# Portal_url = 'https://zealy.io/cw/portaltobitcoin/invite/slbLWMwfLoIgPJCfNO-9u'
def getrandom_url():
    items =[
        'https://zealy.io/cw/portaltobitcoin/invite/ckFoGaoYsQI8NaLS5rh90',
        'https://zealy.io/cw/portaltobitcoin/invite/axrEs-G-Gs9E2t43dk06D',
        'https://zealy.io/cw/portaltobitcoin/invite/SuILo3bStLYzYgHHw9SNb',
        'https://zealy.io/cw/portaltobitcoin/invite/Sr-qCTv0XjZEKA7jgtGv-',
        'https://zealy.io/cw/portaltobitcoin/invite/6MtWuarcjE0Q_OGwA-Xv9',
        'https://zealy.io/cw/portaltobitcoin/invite/kXYNqQbuLJtVaR65nLcjU',
        'https://zealy.io/cw/portaltobitcoin/invite/TCh8HSl6XuPqBbLPBYyfb',
        'https://zealy.io/cw/portaltobitcoin/invite/Z9X3Be0s7u9uwOxvLgM-v',
        'https://zealy.io/cw/portaltobitcoin/invite/zqOwOaOYRpTD7yTrRR016',
        'https://zealy.io/cw/portaltobitcoin/invite/lagg9ZO0mEonQ_hRsVIHI',
        'https://zealy.io/cw/portaltobitcoin/invite/A5rxMfMySJV3G0EA7W0oC',
        'https://zealy.io/cw/portaltobitcoin/invite/hmnnvPZ825LQnGsqXg7wf',
        'https://zealy.io/cw/portaltobitcoin/invite/h4QWy7Q0NeBuCcWwSrhWj',
        'https://zealy.io/cw/portaltobitcoin/invite/h0XCiMMMEvWjJTrAcm89A',
        'https://zealy.io/cw/portaltobitcoin/invite/Ad1tFZASJgfZK55Fbogc9',
        'https://zealy.io/cw/portaltobitcoin/invite/vnReLbAZtqHk66ZSpp-x4',
        'https://zealy.io/cw/portaltobitcoin/invite/E5x-4NXNDKavwFvL5XoNl',
        'https://zealy.io/cw/portaltobitcoin/invite/aDN4zuhkodcoi9oMWAPEL',
        'https://zealy.io/cw/portaltobitcoin/invite/juHIa43dGkF1_stISTGpt'
    ]
    random_item = random.choice(items)
    return random_item
#--------Staying----------
Staying_js = """let button  = 
document.querySelector("#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010.r-18u37iz > main > div > div > div > div > div > div:nth-child(3) > div > div > section > div > div > div:nth-child(1) > div > div > article");               
                button.click(); """

url_js = '''let button  =
document.querySelector("#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010.r-18u37iz > header > div > div > div > div:nth-child(1) > div.css-175oi2r.r-15zivkp.r-1bymd8e.r-13qz1uu.r-1awozwy > nav > a:nth-child(11) > div");
button.click(); '''

url_js_2 = '''let button  =
document.querySelector("#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010.r-18u37iz > header > div > div > div > div:nth-child(1) > div.css-175oi2r.r-15zivkp.r-1bymd8e.r-13qz1uu.r-1awozwy > nav > a:nth-child(10) > div");
button.click(); '''
def generate_random_word(length=4):
    # 生成一个随机的字母单词
    letters = string.ascii_letters + string.digits  # 包含小写字母、大写字母和数字
    return ''.join(random.choice(letters) for _ in range(length))

def getSigninTW(chrome,env):
    num = 0
    while num < 3:
        tab = chrome.new_tab(url='https://x.com/')
        chrome.wait(8, 10)
        logger.info('开始判断')
        if tab.s_ele("Sign in") or tab.s_ele("Log in", index=4) or tab.s_ele('Retry') or tab.s_ele('Refish'):
            logger.info(f"{env.name}: 推特未登录，触发登录推特")
            if tab.s_ele('Sign in'):
                tab.ele('Sign in').click()
            elif tab.s_ele('Log in'):
                tab.ele('Log in').click()
            elif tab.s_ele('Retry'):
                print('Retry')
                tab.refresh(ignore_cache= True)
            time.sleep(10)
            with app.app_context():
                tw: Account = Account.query.filter_by(id=env.tw_id).first()
                if tw:
                    tab.ele("@autocomplete=username").input(tw.name, clear=True)
                    tab.ele("@@type=button@@text()=Next").click()
                    tab.ele("@type=password").input(aesCbcPbkdf2DecryptFromBase64(tw.pwd), clear=True)
                    tab.ele("@@type=button@@text()=Log in").click()
                    fa2 = aesCbcPbkdf2DecryptFromBase64(tw.fa2)
                    if "login" in tab.url and len(fa2) > 10:
                        tw2faV(tab, fa2)
                    tab.ele('@type=button').click()
                    chrome.wait(2)
                    logger.info(f'{env.name}:登录完成')
                    chrome.close_tabs()
                    break
                else:
                    raise Exception(f"{env.name}: 没有导入TW的账号信息")
        elif tab.s_ele('@value=Start') or tab.s_ele('@value=Send email') or tab.s_ele('@value=Continue to X'):
            if tab.s_ele('@value=Send email'):
                logger.info(f'{env.name}:需要人工验证twitter')
                time.sleep(1)
                chrome.quit()
            elif tab.s_ele('@value=Start'):
                tab.ele('@value=Start').click()
                time.sleep(15)
                if tab.s_ele('@value=Continue to X'):
                    tab.ele('@value=Continue to X').click()
                elif tab.s_ele('@value=Send email'):
                    logger.info(f'{env.name}:需要人工验证twitter')
                    time.sleep(1)
                    chrome.quit()
                else:
                    time.sleep(10)
                    tab.ele('@value=Continue to X').click()
            elif tab.s_ele('@value=Continue to X'):
                tab.ele('@value=Continue to X').click()
        else:
            logger.info('判断完成')
            try:
                print('发布推文')
                tab.ele('@class=public-DraftStyleDefault-block public-DraftStyleDefault-ltr').input(generate_random_word())
                time.sleep(2)
                tab.ele('Post').click()
                time.sleep(2)
                if tab.s_ele('@class=css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-2yi16 r-1qi8awa r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l'):
                    tab.ele('@class=css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-2yi16 r-1qi8awa r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l').click()
                    time.sleep(2)
                tab.ele('@class=css-175oi2r r-172uzmj r-1pi2tsx r-13qz1uu r-o7ynqc r-6416eg r-1ny4l3l').click()
                time.sleep(2)
                print('点赞')
                tab.ele('@class=css-175oi2r r-xoduu5 r-1p0dtai r-1d2f490 r-u8s1d r-zchlnj r-ipm5af r-1niwhzg r-sdzlij r-xf4iuw r-o7ynqc r-6416eg r-1ny4l3l',index=4).click()
                time.sleep(2)
                print('转发')
                tab.ele('@class=css-175oi2r r-xoduu5 r-1p0dtai r-1d2f490 r-u8s1d r-zchlnj r-ipm5af r-1niwhzg r-sdzlij r-xf4iuw r-o7ynqc r-6416eg r-1ny4l3l',index=3).click()
                time.sleep(2)
                tab.ele('Repost').click()
                time.sleep(2)
                chrome.close_tabs()
                break
            except Exception as e:
                logger.error(e)
                chrome.close_tabs()
                num = num + 1
                if num == 2:
                    logger.info(f'{env.name}:三次尝试有问题')

#登录zearly平台
def getZearly(chrome,env):
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard')
    chrome.wait(2, 3)
    try:
        #logger.info(f'{env.name}:判断弹窗')
        if tab.ele('t:button@tx():Only necessary'):
            #logger.info("点击弹窗")
            tab.ele('t:button@tx():Only necessary').click()
            chrome.wait(1, 2)
            #logger.info(f'{env.name}:弹窗处理完成')
        else:
            pass
            #logger.info(f'{env.name}:没有弹窗')
    except Exception as e:
        logger.info(e)
    try:
        #logger.info('开始加入社区')
        if tab.ele('t:button@tx():Connect to Zealy'):
            #logger.info("点击加入社区")
            tab.ele('t:button@tx():Connect to Zealy').click()
            time.sleep(5)
            #logger.info("点击login登录")
            tab.ele('t:a@tx():Log in').click()
            time.sleep(5)
            #logger.info("点击用discord登录")
            tab.ele('t:button@tx():Log in with Discord').click()
            time.sleep(20)
            #logger.info(f"{env.name}:开始discord登录")
            try:
                logger.info(f'{env.name}:开始判断登录discord情况')
                if chrome.get_tab(title='Discord | Authorize access to your account'):
                    chrome.get_tab(title='Discord | Authorize access to your account').ele("@type=button",index=2).click()
                    logger.info(f"{env.name}: 登录discord完成----------------------------------")
                    time.sleep(10)
                    chrome.close_tabs()
                    chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard')
                    time.sleep(6)

                elif chrome.get_tab(title='Discord | 授权访问您的账号'):
                    chrome.get_tab(title='Discord | 授权访问您的账号').ele("@type=button",index=2).click()
                    logger.info(f"{env.name}: 登录discord完成----------------------------------")
                    time.sleep(10)
                    chrome.close_tabs()
                    chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard')
                    time.sleep(6)

                elif chrome.get_tab(title='Discord'):
                    if tab.s_ele('@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85'):
                        logger.info(f'{env.name}的discord需要重新登录')
                        tab.ele('@class=button_dd4f85 lookFilled_dd4f85 colorPrimary_dd4f85 sizeMedium_dd4f85 grow_dd4f85').click()
                        time.sleep(6)
                        chrome.close_tabs()
                        LoginDiscord(chrome, env)
                        chrome.close_tabs()
                        getZearly(chrome, env)

                    elif tab.ele('Welcome back!'):
                        logger.info(f"{env.name}的Discord未登录，尝试重新登录")
                        LoginDiscord(chrome, env)
                        chrome.close_tabs()
                        getZearly(chrome, env)

                else:
                    logger.info(f'{env.name}:还有其他的语言需要加判断')

            except Exception as e:
                logger.info(e)
                logger.info(f"{env.name}：Discord未登录，账号登录失败????????????????????????????????")
                #chrome.quit()
                logger.info(e)
        else:
            logger.info(f'------------{env.name}已经登录了---------------')
    except Exception as e:
        logger.info(e)

#twitter的like,twitter的retweet,twitter的follow
def getTW_Three_Elements(chrome,elements,retry_function):
    chrome.wait(8, 10)
    tab = chrome.get_tab(url='https://x.com/')

    if elements == 'Follow':
        tab.wait(8).ele('t:span@tx():Follow', index=2).click()
        chrome.close_tabs()

    elif elements == 'Like':
        tab.ele('t:span@tx():Like', index=2).click()
        chrome.close_tabs()

    elif elements == 'Retweet':
        tab.wait(8).ele('t:span@tx():Repost').click()
        chrome.close_tabs()

#连接钱包
def exe_okx(chrome):
    try:
        chrome.wait(3, 4)
        chrome.get_tab(title="OKX Wallet").ele('@data-testid=okd-button', index=2).click()
    except Exception as e:
        print("取的ele不对")
        logger.error(e)
    return

#GET STARTED
def getStarted(chrome,env):
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/d1a85be3-67ab-4eac-a997-aab4db2f5631/02a57e83-c01d-4c07-a859-b344ee0b7a32')
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        logger.info(f'{env.name}:twitter关注任务')
        chrome.wait(2, 3)
        tab.ele('@class=shrink-0 w-button-icon-lg h-button-icon-lg').click()
        time.sleep(5)
        #print('判断是否需要连接钱包')
        if tab.s_ele('t:button@tx():Connect wallet'):
            print('开始连接钱包')
            time.sleep(3)
            tab.ele('t:button@tx():Connect wallet').click()
            time.sleep(5)
            tab.ele('t:div@tx():OKX Wallet').click()
            time.sleep(3)
            exe_okx(chrome)
            time.sleep(2)
            print('判断是否需要钱包签名')
            if tab.s_ele('t:div@tx():Sign message'):
                tab.ele('t:div@tx():Sign message').click()
                time.sleep(2)
                exe_okx(chrome)
            time.sleep(10)
            tab.ele('@class=shrink-0 w-button-icon-lg h-button-icon-lg').click()
        time.sleep(6)
        #print('跳转到twitter关注')
        #logger.info('开始点')
        getTW_Three_Elements(chrome, 'Follow',lambda: getStarted(chrome,env))
        #logger.info('结束')
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()
        logger.info(f'{env.name}:twitter任务完成$$$$$$$$$$$$$$$$')

    #print('Follow our Medium')
    #--------------Follow our Medium------------
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/d1a85be3-67ab-4eac-a997-aab4db2f5631/b5817b0f-4b29-4478-a961-c8f3024ead2e')
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('@class=flex flex-col gap-embed-url-texts flex-1 w-full p-embed-url-container').click()
        time.sleep(1)
        chrome.close_tabs()
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()

    #print('Subscribe to our YouTube Channel and watch a video!')
    #---------------Subscribe to our YouTube Channel and watch a video!---------------------------------
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/d1a85be3-67ab-4eac-a997-aab4db2f5631/55b14c1a-3c8e-4a4e-9239-81d263268360')
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('@class=flex flex-col gap-embed-url-texts flex-1 w-full p-embed-url-container').click()
        time.sleep(1)
        chrome.close_tabs()
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()


#BitScalerLaunch
def getBitScalerLaunch(chrome,env):
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/dd364b5b-667c-4b2e-9b82-28041e938911/8b940e7c-a7a7-425f-8555-18519ebc043e')
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
        return
    else:
        time.sleep(2)
        tab.ele('t:button@tx():Retweet').click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Retweet', lambda: getBitScalerLaunch(chrome,env))
        time.sleep(2)
        tab.ele('t:button@tx():Like').click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getBitScalerLaunch(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Like', index=2).click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getBitScalerLaunch(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Like', index=3).click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getBitScalerLaunch(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Like', index=4).click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getBitScalerLaunch(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Like', index=5).click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getBitScalerLaunch(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Retweet', index=2).click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Retweet',lambda: getBitScalerLaunch(chrome,env))
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()
        logger.info(f'{env.name}:BitScalerLaunch任务完成$$$$$$$$$$$$$$$$')

#BitScalerWhitepaper
def getBitScalerWhitepaper(chrome,env):
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/dd364b5b-667c-4b2e-9b82-28041e938911/5638cc93-6ecd-44a0-b8cb-055a11005491')
    time.sleep(2)
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
        return
    else:
        tab.ele('@class=flex flex-col gap-embed-url-texts flex-1 w-full p-embed-url-container').click()
        time.sleep(1)
        chrome.close_tabs()
        time.sleep(1)
        tab.ele('@value=Bitcoin Scaling Solution').click()
        time.sleep(1)
        tab.ele('@value=Channel factories').click()
        time.sleep(1)
        tab.ele('@value=MuSig2, FROST, DLCs, Eltoo').click()
        time.sleep(1)
        tab.ele('@value=To enable n-of-n multisig addresses and timelock constraints').click()
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()
        logger.info(f'{env.name}:BitScalerWhitepaper任务完成$$$$$$$$$$$$$$$$')

#Partnership
def getPartnership(chrome,env):
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/4bfd79a1-8a54-4aca-9dc7-eca26781721a/926bc3c5-fd62-4fcf-a5d3-89954d0701fc')
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
        return
    else:
        chrome.close_tabs()
        #logger.info(f'{env.name}:twitter关注任务')
        tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/4bfd79a1-8a54-4aca-9dc7-eca26781721a/926bc3c5-fd62-4fcf-a5d3-89954d0701fc')
        chrome.wait(2, 3)
        tab.ele('@class=shrink-0 w-button-icon-lg h-button-icon-lg').click()
        time.sleep(6)
        #print('跳转到twitter关注')
        getTW_Three_Elements(chrome, 'Follow',lambda: getPartnership(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()
        logger.info(f'{env.name}:twitter任务完成$$$$$$$$$$$$$$$$')

#Staying on top of twitter!
def getStayingExplore(chrome,env):
    # -----------Explore Bitcoin's potential with us!----------------------
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/efda5f96-98c8-4fc4-96c2-0c3c7cb13938/8ae6a745-1eb4-4b4a-a543-0f6923f87e37')
    time.sleep(2)
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('t:button@tx():Retweet').click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Retweet',lambda: getStayingExplore(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Like').click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getStayingExplore(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()
        logger.info(f'{env.name}:Explore Bitcoin\'s potential with us!任务完成$$$$$$$$$$$$$$$$')


    #---------------Share the news about the Portal ReBrand!----------------
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/efda5f96-98c8-4fc4-96c2-0c3c7cb13938/c4dadb6e-352f-4867-9c29-c48a8bf5d186')
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('@class=flex flex-col gap-embed-url-texts flex-1 w-full p-embed-url-container').click()
        time.sleep(1)
        chrome.close_tabs()
        time.sleep(2)
        tab.ele('t:button@tx():Tweet').click()
        time.sleep(3)
        chrome.get_tab(url='https://x.com/').wait(5).ele('t:span@tx():Post').click()
        time.sleep(5)
        try:
            print('开始')
            time.sleep(5)
            chrome.get_tab(url='https://x.com/').wait(5).run_js(url_js)
            time.sleep(5)
            print('执行第二个js')
            chrome.get_tab(url='https://x.com/').wait(5).run_js(Staying_js)
        except Exception as e:
            logger.info(e)
            chrome.get_tab(url='https://x.com/').wait(5).run_js(url_js_2)
            time.sleep(5)
            chrome.get_tab(url='https://x.com/').wait(5).run_js(Staying_js)
        time.sleep(2)
        link = chrome.get_tab(url='https://x.com/').url
        tab.ele('@id=2c0ed6c4-f66a-4638-85e3-4038528e8d69.tweetUrl').input(link)
        #关闭复制链接的twitter页面
        chrome.close_tabs()
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        #关闭平台任务的页面
        chrome.close_tabs()
        logger.info(f'{env.name}:Share the news about the Portal ReBrand!任务完成$$$$$$$$$$$$$$$$')

    #-----------------Share a unique element from our Website PortalToBitcoin.com--------------
    tab = chrome.new_tab('https://zealy.io/cw/portaltobitcoin/questboard/efda5f96-98c8-4fc4-96c2-0c3c7cb13938/7420cb49-fed6-44b3-8532-68f22fc64045')
    time.sleep(2)
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('t:button@tx():Tweet').click()
        time.sleep(3)
        chrome.get_tab(url='https://x.com/').wait(5).ele('t:span@tx():Post').click()
        time.sleep(5)
        try:
            print('开始')
            time.sleep(5)
            chrome.get_tab(url='https://x.com/').wait(5).run_js(url_js)
            time.sleep(5)
            print('执行第二个js')
            chrome.get_tab(url='https://x.com/').wait(5).run_js(Staying_js)
        except  Exception as e:
            logger.info(e)
            chrome.get_tab(url='https://x.com/').wait(5).run_js(url_js_2)
            time.sleep(5)
            chrome.get_tab(url='https://x.com/').wait(5).run_js(Staying_js)
        time.sleep(2)
        link = chrome.get_tab(url='https://x.com/').url
        tab.ele('@id=09558b57-410e-405a-ab33-7364f7ffa51d.tweetUrl').input(link)
        # 关闭复制链接的twitter页面
        chrome.close_tabs()
        time.sleep(2)
        tab.ele('@class=flex flex-col gap-embed-url-texts flex-1 w-full p-embed-url-container').click()
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        # 关闭平台任务的页面
        chrome.close_tabs()
        logger.info(f'{env.name}:Share a unique element from our Website PortalToBitcoin.com任务完成$$$$$$$$$$$$$$$$')


    # #Discover the future of Decentralized Finance with Portal to Bitcoin and share it-------------
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/efda5f96-98c8-4fc4-96c2-0c3c7cb13938/96df73c3-1125-4311-b264-a9ec6b6e28ac')
    time.sleep(2)
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('t:button@tx():Retweet').click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Retweet',lambda: getStayingExplore(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Like').click()
        time.sleep(5)
        getTW_Three_Elements(chrome, 'Like',lambda: getStayingExplore(chrome, env))
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()
        logger.info(f'{env.name}:Explore Bitcoin\'s potential with us!任务完成$$$$$$$$$$$$$$$$')

    #------Portal CEO on Forbes-----------------------------------------
    tab = chrome.new_tab(url='https://zealy.io/cw/portaltobitcoin/questboard/efda5f96-98c8-4fc4-96c2-0c3c7cb13938/932d068a-9652-423d-be15-802cf849d88a')
    time.sleep(2)
    if tab.s_ele('@class=whitespace-nowrap min-w-0 truncate badge-xs text-badge-positive-primary'):
        logger.info(f'{env.name}:任务已经完成')
        chrome.close_tabs()
    else:
        tab.ele('@class=flex flex-col gap-embed-url-texts flex-1 w-full p-embed-url-container').click()
        time.sleep(1)
        chrome.close_tabs()
        time.sleep(2)
        tab.ele('t:button@tx():Claim').click()
        time.sleep(6)
        chrome.close_tabs()


def getPortal(chrome,env):
    portal_url = getrandom_url()
    print('邀请码:',portal_url)
    tab = chrome.new_tab(url=portal_url)
    print('开始做任务了')
    time.sleep(2)
    if tab.ele('t:button@tx():Join Portal To Bitcoin'):
        print('加入社团')
        tab.ele('t:button@tx():Join Portal To Bitcoin').click()
    time.sleep(10)

    # #--------------------GET STARTED(完成)----------------
    logger.info(f'{env.name}:GET STARTED开始')
    getStarted(chrome,env)
    time.sleep(2)
    logger.info(f'{env.name}:GET STARTED结束')
    # #-----------------------------------------------
    #
    # #---------------------------BitScaler(完成)--------------------------
    logger.info(f'{env.name}:BitScaler任务结束')
    getBitScalerLaunch(chrome, env)
    time.sleep(2)
    getBitScalerWhitepaper(chrome, env)
    time.sleep(2)
    logger.info(f'{env.name}:BitScaler任务结束')
    # #--------------------------------------------------------------
    #
    # #-------------PARTNERSHIP(完成)-----------------------
    logger.info(f'{env.name}:PARTNERSHIP的任务开始')
    getPartnership(chrome, env)
    time.sleep(2)
    logger.info(f'{env.name}:PARTNERSHIP的任务结束')
    # # -----------------------------------------------
    #
    #-------------Staying on top of twitter!-----------------------
    logger.info(f'{env.name}:Staying on top of 任务开始')
    getStayingExplore(chrome, env)
    logger.info(f'{env.name}:Staying on top of 任务结束')
    # -----------------------------------------------
    logger.info(f'{env.name}:脚本任务全部完成，转人工')


def portal(env):
    with app.app_context():
        try:
            chrome: ChromiumPage = OKXChrome(env)
            getZearly(chrome, env)
            time.sleep(5)
            chrome.close_tabs()
            time.sleep(5)
            getPortal(chrome,env)
            logger.info(f"{env.name}环境：任务执行完毕，关闭环境")
        except Exception as e:
            logger.error(f"{env.name} 执行：{e}")
            return ("失败", e)
        finally:
            quitChrome(env, chrome)

if __name__ == '__main__':

    with app.app_context():
        env = Env.query.filter_by(name="ZLL-13").first()
        portal(env)



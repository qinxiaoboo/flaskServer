from DrissionPage import ChromiumOptions
from flaskServer.config.config import CHROME_EXEC_PATH,CHROME_EXTEND,CHROME_EXTEND_PATH,DEFAULT_OPEN_PAGE,DEFAULT_REMOVE_PAGE
from flaskServer.config.config import CHROME_USER_DATA_PATH, OFF_IMG, HEADLESS
from loguru import logger
from pathlib import Path
CHROME_USER_DATA_PATH = Path(CHROME_USER_DATA_PATH)

def initChromiumOptions(env,port,useragent,proxy_server):
    co = ChromiumOptions()
    co.set_browser_path(Path(CHROME_EXEC_PATH))
    co.set_argument("--no-first-run")
    if useragent:
        co.set_argument("--user-agent", useragent)
    if proxy_server:
        co.set_argument("--proxy-server", proxy_server)
    if port:
        co.set_local_port(port)
    # 用户文件夹路径
    data_path = CHROME_USER_DATA_PATH / Path("data/") / env
    co.set_user_data_path(initDir(data_path))
    # 缓存路径
    cache_path = CHROME_USER_DATA_PATH / Path("cache/") / env
    co.set_cache_path(initDir(cache_path))
    # 下载路径
    dowload_path = CHROME_USER_DATA_PATH / Path("dowloads/") / env
    co.set_download_path(path=initDir(dowload_path))

    # 默认参数
    co.set_argument("--disable-background-timer-throttling")
    co.set_argument("--disable-backgrounding-occluded-windows")
    co.set_argument("--disable-renderer-backgrounding")
    co.set_argument("--force-color-profile","srgb")
    co.set_argument("--metrics-recording-only")
    co.set_argument("--password-store","basic")
    co.set_argument("--use-mock-keychain")
    co.set_argument("--export-tagged-pdf")
    co.set_argument("--no-default-browser-check")
    co.set_argument("--window-position","0,0")
    co.set_argument("--no-sandbox")
    co.set_argument("--disable-setuid-sandbox")
    co.set_argument("--disable-background-mode")
    co.set_argument("--disable-renderer-accessibility")
    co.set_argument("--disable-legacy-window")
    co.set_argument("--component-updater","initial-delay=6e5")
    co.set_argument("--lang","en")
    co.set_argument("--remote-debugging-port","0")
    co.set_argument("--flag-switches-begin ")
    co.set_argument("--flag-switches-end ")
    # 打开的功能列表
    co.set_argument("--enable-features","NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions")
    # 禁用的功能列表
    co.set_argument("--disable-features","FlashDeprecationWarning,EnablePasswordsAccountStorage")
    co.set_argument("--enable-blink-features","IdleDetection,Fledge,Parakeet")
    # if HEADLESS:
    #     co.set_argument("--headless=new")
    # # 是否禁止图片
    # co.no_imgs(on_off=OFF_IMG)

    # 不打开的页面
    for rem in DEFAULT_REMOVE_PAGE:
        co.remove_argument(rem)
    # 打开的页面
    for op in DEFAULT_OPEN_PAGE:
        co.set_argument(op)


    # 禁用webRTC 防止通过摄像头获取真实IP地址
    co.set_argument("--disable-webrtc")
    co.set_pref("webrtc.ip_handling_policy","disable_non_proxied_udp")
    co.set_pref("webrtc.multiple_routes_enabled",False)
    co.set_pref("webrtc.nonproxied_udp_enabled", False)

    # 添加扩展
    co.remove_extensions()
    extends_path = ""
    for extend in CHROME_EXTEND:
        etdpath = Path(CHROME_EXTEND_PATH) / Path(extend)
        if etdpath.exists():
            co.add_extension(etdpath)
            extends_path += CHROME_EXTEND_PATH + extend + ","
        else:
            logger.error(f"配置文件可能有误，{etdpath},路径不存在")
            raise Exception(f"配置文件可能有误，{etdpath},路径不存在")
    co.set_argument("--load-extension",extends_path.rstrip(","))
    init_path = CHROME_USER_DATA_PATH / Path("config/") / Path(env) / Path("conf.ini")
    co.save(path=init_path)
    return co

def initDir(path:Path):
    if path.exists():
        pass
    else:
        path.mkdir(parents=True)
    return path

if __name__ == '__main__':
    print(CHROME_USER_DATA_PATH / Path("data/"))
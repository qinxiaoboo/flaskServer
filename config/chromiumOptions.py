from DrissionPage import ChromiumOptions
from flaskServer.config.config import CHROME_EXEC_PATH,CHROME_CONF_PATH,CHROME_EXTEND,CHROME_EXTEND_PATH,DEFAULT_OPEN_PAGE,DEFAULT_REMOVE_PAGE
def initChromiumOptions(first,useragent):
    co = ChromiumOptions()
    co.set_browser_path(CHROME_EXEC_PATH)
    if first:
        co.set_argument("--no-first-run")
    if useragent:
        co.set_argument("--user-agent", useragent)
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
    # extends_path = ""
    if first:
        for extend in CHROME_EXTEND:
            co.add_extension(CHROME_EXTEND_PATH+extend)
        # extends_path += CHROME_EXTEND_PATH + extend + ","
    # co.set_argument("--load-extension",extends_path.rstrip(","))

    co.save()

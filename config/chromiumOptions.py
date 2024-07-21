from DrissionPage import ChromiumOptions
co = ChromiumOptions()

path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 请改为你电脑内Chrome可执行文件路径
co.set_browser_path(path)

extends = ["wf-proxyIp","ffbceckpkpbcmgiaehlloocglmijnpmp","mcohilncbfahbmgdjkbpemcciiolgcge","yescap_v2.0.beta"]
extend_path = r"D:\data\etd\\"

co.set_argument("--no-first-run")
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
co.set_argument("--user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
# co.remove_argument("--no-sandbox")
# co.remove_argument("--disable-setuid-sandbox")
co.set_argument("--disable-background-mode")
co.set_argument("--disable-renderer-accessibility")
co.set_argument("--disable-legacy-window")
co.set_argument("--component-updater","initial-delay=6e5")
# co.set_argument("--lang","fr")
co.set_argument("--remote-debugging-port","0")
co.set_argument("--flag-switches-begin ")
co.set_argument("--flag-switches-end ")
# co.remove_argument("https://whoer.net/zh")
# co.remove_argument("chrome-extension://mnloefcpaepkpmhaoipjkpikbnkmbnic/options.html")

co.remove_extensions()
extends_path = ""
for extend in extends:
    co.add_extension(extend_path+extend)
    extends_path += extend_path + extend + ","
co.set_argument("--load-extension",extends_path.rstrip(","))

co.save()
print(co.ini_path)
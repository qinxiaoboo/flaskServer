import toml,csv
from pathlib import Path

cfg = toml.load(open(r'D:\python\wf-chrome\flaskServer\config.toml', 'r', encoding='utf-8'))

ENV_PATH = cfg.get('ENV_PATH')
THREAD_POOL_NUM = cfg.get('THREAD_POOL_NUM')
CHROME_EXEC_PATH = cfg.get("CHROME_EXEC_PATH")
CHROME_EXTEND = cfg.get("CHROME_EXTEND")
WORK_PATH = cfg.get("WORK_PATH")
CHROME_EXTEND_PATH = cfg.get("CHROME_EXTEND_PATH")

CHROME_USER_DATA_PATH = cfg.get("CHROME_USER_DATA_PATH")

CHROME_EXTEND_UPDATE = cfg.get("CHROME_EXTEND_UPDATE")

DEFAULT_OPEN_PAGE = cfg.get("DEFAULT_OPEN_PAGE")
DEFAULT_REMOVE_PAGE = cfg.get("DEFAULT_REMOVE_PAGE")
YES_CAPTCHA_API_KEY = cfg.get("YES_CAPTCHA_API_KEY")
WALLET_PASSWORD = cfg.get("WALLET_PASSWORD")
TEXT_PASSWORD = cfg.get("TEXT_PASSWORD")
RANDOM_ORDER = cfg.get("RANDOM_ORDER")
SKIP_FIRST_ACCOUNTS = cfg.get("SKIP_FIRST_ACCOUNTS")
WAIT_BETWEEN_ACCOUNTS = cfg.get("WAIT_BETWEEN_ACCOUNTS")
THREADS_NUM = cfg.get("THREADS_NUM")
def get_ini_path(name):
    return CHROME_USER_DATA_PATH / Path("config/") / Path(name) / Path("conf.ini")

HEADLESS = cfg.get("HEADLESS")
MUTE = cfg.get("MUTE")
OFF_VIDEO = cfg.get("OFF_VIDEO")
OFF_IMG = cfg.get("OFF_IMG")
REFERRAL_LINKS = [line.strip() for line in open(Path(WORK_PATH) / Path('flaskServer/files/referral_links.txt'), 'r', encoding='utf-8').read().splitlines()
                  if line.strip() != '']
with open(Path(WORK_PATH) / Path('flaskServer/files/surveys.csv'), 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    SURVEYS = [row for row in reader]
TWO_CAPTCHA_API_KEY = cfg.get('TWO_CAPTCHA_API_KEY')
CAP_SOLVER_API_KEY = cfg.get('CAP_SOLVER_API_KEY')
PRIVATE_KEY_PEM = cfg.get("PRIVATE_KEY_PEM")
SURVEYS = {row[0].lower(): row[1:] for row in SURVEYS}
CHROME_VERSION = cfg.get("CHROME_VERSION")
MAX_TRIES = cfg.get("MAX_TRIES")
DISABLE_SSL = cfg.get("DISABLE_SSL")
FLLOW_FAKE_TWITTER = cfg.get("FLLOW_FAKE_TWITTER")
FAKE_TWITTER = cfg.get("FAKE_TWITTER")
GALXE_CAMPAIGN_IDS = cfg.get("GALXE_CAMPAIGN_IDS")
GALXE_CAMPAIGN_URLS = cfg.get("GALXE_CAMPAIGN_URLS")
RPCs = cfg.get('RPCs')
CAPTCHA_ON = cfg.get("CAPTCHA_ON")
HIDE_UNSUPPORTED = cfg.get("HIDE_UNSUPPORTED")
EXCLUDE_TASK_LIST = cfg.get("EXCLUDE_TASK_LIST")
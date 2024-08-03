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

DEFAULT_OPEN_PAGE = cfg.get("DEFAULT_OPEN_PAGE")
DEFAULT_REMOVE_PAGE = cfg.get("DEFAULT_REMOVE_PAGE")

WALLET_PASSWORD = cfg.get("WALLET_PASSWORD")
TEXT_PASSWORD = cfg.get("TEXT_PASSWORD")
RANDOM_ORDER = cfg.get("RANDOM_ORDER")
SKIP_FIRST_ACCOUNTS = cfg.get("SKIP_FIRST_ACCOUNTS")
WAIT_BETWEEN_ACCOUNTS = cfg.get("WAIT_BETWEEN_ACCOUNTS")
THREADS_NUM = cfg.get("THREADS_NUM")
def get_ini_path(name):
    return CHROME_USER_DATA_PATH / Path("config/") / Path(name) / Path("conf.ini")

HEADLESS = cfg.get("HEADLESS")
REFERRAL_LINKS = [line.strip() for line in open(Path(WORK_PATH) / Path('flaskServer/files/referral_links.txt'), 'r', encoding='utf-8').read().splitlines()
                  if line.strip() != '']
with open(Path(WORK_PATH) / Path('flaskServer/files/surveys.csv'), 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    SURVEYS = [row for row in reader]
TWO_CAPTCHA_API_KEY = cfg.get('TWO_CAPTCHA_API_KEY')
CAP_SOLVER_API_KEY = cfg.get('CAP_SOLVER_API_KEY')
SURVEYS = {row[0].lower(): row[1:] for row in SURVEYS}
CHROME_VERSION = cfg.get("CHROME_VERSION")
MAX_TRIES = cfg.get("MAX_TRIES")
DISABLE_SSL = cfg.get("DISABLE_SSL")
FAKE_TWITTER = cfg.get("FAKE_TWITTER")
GALXE_CAMPAIGN_IDS = cfg.get("GALXE_CAMPAIGN_IDS")
RPCs = cfg.get('RPCs')
CAPTCHA_ON = cfg.get("CAPTCHA_ON")
HIDE_UNSUPPORTED = cfg.get("HIDE_UNSUPPORTED")
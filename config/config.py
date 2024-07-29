import toml
from pathlib import Path

cfg = toml.load(open(r'D:\python\wf-chrome\flaskServer\config.toml', 'r', encoding='utf-8'))

ENV_PATH = cfg.get('ENV_PATH')
THREAD_POOL_NUM = cfg.get('THREAD_POOL_NUM')
CHROME_EXEC_PATH = cfg.get("CHROME_EXEC_PATH")
CHROME_EXTEND = cfg.get("CHROME_EXTEND")
CHROME_EXTEND_PATH = cfg.get("CHROME_EXTEND_PATH")

CHROME_USER_DATA_PATH = cfg.get("CHROME_USER_DATA_PATH")

DEFAULT_OPEN_PAGE = cfg.get("DEFAULT_OPEN_PAGE")
DEFAULT_REMOVE_PAGE = cfg.get("DEFAULT_REMOVE_PAGE")

WALLET_PASSWORD = cfg.get("WALLET_PASSWORD")

def get_ini_path(name):
    return CHROME_USER_DATA_PATH / Path("config/") / Path(name) / Path("conf.ini")

GALXE_CAMPAIGN_IDS = cfg.get("GALXE_CAMPAIGN_IDS")
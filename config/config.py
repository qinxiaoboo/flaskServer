import toml


cfg = toml.load(open('../config.toml', 'r', encoding='utf-8'))

ENV_PATH = cfg.get('ENV_PATH')
CHROME_CONF_PATH = cfg.get("CHROME_CONF_PATH")
CHROME_EXEC_PATH = cfg.get("CHROME_EXEC_PATH")
CHROME_EXTEND = cfg.get("CHROME_EXTEND")
CHROME_EXTEND_PATH = cfg.get("CHROME_EXTEND_PATH")

DEFAULT_OPEN_PAGE = cfg.get("DEFAULT_OPEN_PAGE")
DEFAULT_REMOVE_PAGE = cfg.get("DEFAULT_REMOVE_PAGE")
import ast
import random
import re

import loguru

from flaskServer.config.config import WORK_PATH
from flaskServer.config.config import CHROME_VERSION
from flaskServer.config.config import EXCLUDE_TASK_LIST

s = list()
# 读取UserAgent文件
with open(WORK_PATH + r'\flaskServer\utils\useragent.txt', 'r') as f:
    for line in f:
        useragent = re.sub(r"Chrome/\d+",f"Chrome/{CHROME_VERSION}",line.strip())
        s.append(useragent)

def getUserAgent(userAgent):
    if userAgent:
        userAgent = re.sub(r"Chrome/\d+", f"Chrome/{CHROME_VERSION}", userAgent)
        return userAgent
    return random.choice(s)

def getSEC_CH_UA_PLATFORM(userAgent):
    if "Win64" in userAgent:
        return "Windows"
    if "Mac OS" in userAgent:
        return "macOS"
    if "WOW64" in userAgent:
        return "Windows"
    else:
        return "Android"

def getSEC_CH_UA():
    return f'""Google Chrome";v="{CHROME_VERSION}", "Chromium";v="{CHROME_VERSION}", "Not_A Brand";v="24"'
# 检查字符串是否能转换为python对象中的列表
def can_be_list(string):
    try:
        # 尝试将字符串转换为 Python 对象
        obj = ast.literal_eval(string)
        # 检查对象是否为列表
        return isinstance(obj, list)
    except (ValueError, SyntaxError):
        # 捕捉解析过程中出现的错误
        return False
# 检查一个字符串是否能转换为数字
def can_convert_to_number(string):
    try:
        int(string)  # 尝试转换为浮点数
        return True
    except ValueError:
        return False
# 字符串转为列表
def to_be_list(string):
    try:
        return ast.literal_eval(string)
    except Exception as e:
        loguru.logger.error(e)
        return []

def to_be_exclude(string):
    for exclude in EXCLUDE_TASK_LIST:
        if exclude in string:
            return True
    return False

if __name__ == '__main__':
    useragent = getUserAgent("UserAgent：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Config/92.2.2788.20")
    print(useragent)

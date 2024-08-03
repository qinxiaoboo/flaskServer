import random
import re

from flaskServer.config.config import WORK_PATH
from flaskServer.config.config import CHROME_VERSION

s = list()

with open(WORK_PATH + r'\flaskServer\utils\useragent.txt', 'r') as f:
    for line in f:
        useragent = re.sub(r"Chrome/\d+",f"Chrome/{CHROME_VERSION}",line.strip())
        s.append(useragent)

def getUserAgent(userAgent):
    if userAgent:return userAgent
    return random.choice(s)

def getSEC_CH_UA_PLATFORM(userAgent):
    if "Win64" in userAgent:
        return "Windows"
    if "Mac OS" in userAgent:
        return "macOS"
    if "WOW64" in userAgent:
        return "Windows"
    else:
        return "Windows"

def getSEC_CH_UA():
    return f'"Not)A;Brand";v="99", "Google Chrome";v="{CHROME_VERSION}", "Chromium";v="{CHROME_VERSION}"'
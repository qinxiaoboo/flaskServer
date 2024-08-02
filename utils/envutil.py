import random

from flaskServer.config.config import WORK_PATH

s = list()

with open(WORK_PATH + r'\flaskServer\utils\useragent.txt', 'r') as f:
    for line in f:
        s.append(line.strip())

def getUserAgent(userAgent):
    if userAgent:return userAgent
    return random.choice(s)
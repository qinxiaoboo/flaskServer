import pandas as pd
from flaskServer.config.config import ENV_PATH
from flaskServer.services.dto.proxy import update

df = pd.read_excel(ENV_PATH)
for index,row in df.iterrows():
    group = row["分组"]
    name = row["环境名称"]
    port = row["启动端口"]
    proxy = row["代理"]
    tw = row["推特账号"]
    discord = row["discord账号"]
    outlook = row["outlook账号"]
    cookies = row["cookies"]
    if group and name and port:
        if proxy:
            ip,port,user,pwd = proxy.split(":")
            proxy = update(ip,port,user,pwd)
        if tw:
            pass

if __name__ == '__main__':
    pass
    

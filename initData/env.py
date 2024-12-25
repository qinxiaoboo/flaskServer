import pandas as pd
from flaskServer.config.config import ENV_PATH
from flaskServer.services.dto.proxy import update
from flaskServer.services.dto.account import updateAccount
from flaskServer.services.dto.wallet import updateWallt
from flaskServer.services.dto.env import updateEnv,getEnvsByIds

def readEnvs(ids):
    envs = getEnvsByIds(ids)
    envSet = set()
    for env in envs:
        envSet.add(env.name)
    return envSet

def uploadEnvs(file, ids):
    envSet = readEnvs(ids)
    df = pd.read_excel(file)
    df = df.fillna(0)
    for index, row in df.iterrows():
        group = row["分组"]
        env = row["环境名称"]
        if ids:
            if env not in envSet:
                continue
        chrom_port = row["启动端口"]
        proxy = row["代理"]
        tw = row["推特账号"]
        discord = row["discord账号"]
        outlook = row["outlook账号"]
        cookies = row["cookies"]
        init = row["init钱包"]
        bitlight = row["bitlight钱包"]
        okx = row["okx钱包"]
        userAgent = row["UserAgent"]
        # label = row["标签"]
        print(row)
        PROXY, TW, DISCORD, OUTLOOK, OKX, BITLIGHT, INIT = [None for i in range(7)]
        if env and chrom_port:
            if proxy:
                ip, port, user, pwd = proxy.split(",")
                PROXY = update(ip, port, user, pwd)
            if tw:
                twList = tw.split(",")
                if len(twList) == 3:
                    name, pwd, fa2 = twList
                    TW = updateAccount(name, pwd, fa2, "TW")
                elif len(twList) == 5:
                    name, pwd, fa2, emailUser, emailPassword = twList
                    TW = updateAccount(name, pwd, fa2, "TW", emailUser, emailPassword)
                elif len(twList) == 6:
                    name, pwd, fa2, emailUser, emailPassword,token = twList
                    TW = updateAccount(name, pwd, fa2, "TW", emailUser, emailPassword,token)
            if discord:
                discordList = discord.split(",")
                if len(discordList) == 3:
                    name, pwd, fa2 = discordList
                    DISCORD = updateAccount(name, pwd, fa2, "DISCORD")
                elif len(discordList) == 4:
                    name, pwd, fa2, token = discordList
                    DISCORD = updateAccount(name, pwd, fa2, "DISCORD", token=token)
            if outlook:
                name, pwd = outlook.split(",")
                OUTLOOK = updateAccount(name, pwd, "", "OUTLOOK")
            if okx:
                word, address = okx.split(",")
                OKX = updateWallt(env, word, address, "OKX")
            if bitlight:
                word, address = bitlight.split(",")
                BITLIGHT = updateWallt(env, word, address, "BITLIGHT")
            if init:
                word, address = init.split(",")
                INIT = updateWallt(env, word, address, "INIT")
            updateEnv(env,group, chrom_port, cookies, PROXY, TW, DISCORD, OUTLOOK, OKX, INIT, BITLIGHT,userAgent, None)

if __name__ == '__main__':
    uploadEnvs(ENV_PATH, [])

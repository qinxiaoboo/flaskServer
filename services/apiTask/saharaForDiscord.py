from flaskServer.services.dto.env import getAllEnvs
from flaskServer.services.dto.account import getAccountById
from flaskServer.services.apiTask.APIForDiscord import Discord
def main():
    for env in getAllEnvs():
        tw = getAccountById(env.tw_id)
        discord = getAccountById(env.discord_id)
        if discord and discord.token:
            discordApi = Discord(discord.token, env)
            # 获取discord用户信息
            userinfo = discordApi.get_userInfo()
            # 获取用户排名
            discordApi.sendLeaderboard()
            # 解析用户排名获取分数
            rank,points = discordApi.get_context(userinfo["username"])
            # 打印一下
            if rank and points:
                print(f"环境：{env.name}, Rank: {rank}, Username: {userinfo['username']}, Points: {points}")
            else:
                # 如果没有排名则绑定tw
                # discordApi.setTw(tw.name)
                # discordApi.signIn()
                print(f"{env.name} 没有查到分数")

if __name__ == '__main__':
    main()
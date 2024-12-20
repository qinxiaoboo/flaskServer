from flaskServer.services.dto.env import getChoiceEnvs,getAllEnvs
from flaskServer.services.dto.account import getAccountById
from flaskServer.services.apiTask.APIForDiscord import Discord
from flaskServer.services.dto.task_record import updateTaskRecord, getTaskObject
from flaskServer.entity.taskAccount import SaHaRa
name = "sahara"
def main():
    for env in getAllEnvs():
        tw = getAccountById(env.tw_id)
        sahara:SaHaRa = getTaskObject(env, name)
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
                sahara.rank = rank
                sahara.points=points
                sahara.setTwitter=True
                # 签到
                discordApi.signIn()
                updateTaskRecord(env.name, name, sahara, 1)
                print(f"环境：{env.name}, Rank: {rank}, Username: {userinfo['username']}, Points: {points}")
            else:
                # 如果没有排名则绑定tw
                discordApi.setTw(tw.name)
                discordApi.signIn()
                print(f"{env.name} 没有查到分数")
                updateTaskRecord(env.name, name, sahara, 2)

if __name__ == '__main__':
    main()
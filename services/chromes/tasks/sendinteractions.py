import json
import random
import concurrent.futures
import time
from flaskServer.services.apiTask.APIForDiscord import Discord
import requests

url = 'https://discord.com/api/v9/interactions'

def print_green(text):
    print("\033[32m" + text + "\033[0m")

def print_red(text):
    print("\033[31m" + text + "\033[0m")


def verityRole(header,task_list,name):

    for custom_id,message_id in task_list.items():

        msg = {"type": 3,
               "nonce": "13178426{}6341028864".format(random.randrange(0, 1000)),
               "guild_id": "1209630079936630824",
               "channel_id": "1280246851739848818",
               "message_flags": 0,
               "message_id": message_id,
               "application_id": "1077740178476630129",
               "session_id": "a5b653ceb6f1e87f{}fbbf2f3424fe3e6".format(random.randrange(0, 1000)),
               "data": {"component_type": 2, "custom_id": custom_id}}
        try:
            res = requests.post(url=url, headers=header, data=json.dumps(msg))
            if res.status_code == 204:
                print_green(f"{name} - 验证任务成功")
            else:
                print_red(f"{name} - 验证任务失败 - {header['Authorization']} - Failed with status code: {res.status_code}")
        except requests.RequestException as e:
            # print(f"Error with Authorization: {header['Authorization']} - {str(e)}")
            print_red(f"{name} - Token失效: {header['Authorization']}")

        time.sleep(2)


def setTw(twName,header,name):
    msg = {"type": 2,
           "application_id": "1077740178476630129", "guild_id": "1209630079936630824",
           "channel_id": "1280446642528456705",
           "session_id": "a5b653ceb6f1e87f{}faaf2f3424fe3e6".format(random.randrange(0, 1000)),
           "data": {"version": "1317142034250862606", "id": "1123730728040009825", "name": "set", "type": 1,
                    "options": [{"type": 1, "name": "twitter",
                                 "options": [{"type": 3, "name": "account", "value": "@{}".format(twName)}]}],
                    "application_command": {"id": "1123730728040009825", "type": 1,
                                            "application_id": "1077740178476630129", "version": "1317142034250862606",
                                            "name": "set", "description": "Set your twitter", "options": [
                            {"type": 1, "name": "twitter", "description": "Set your Twitter Account", "options": [
                                {"type": 3, "name": "account", "description": "Your Twitter account username",
                                 "required": "true", "description_localized": "Your Twitter account username",
                                 "name_localized": "account"}], "description_localized": "Set your Twitter Account",
                             "name_localized": "twitter"},
                            {"type": 1, "name": "wallet", "description": "Set your Wallet", "options": [
                                {"type": 3, "name": "wallet",
                                 "description": "Your Wallet Address, Accepts ETH SOL BTC SEI AVAX BSC ZKS ADA RONIN",
                                 "required": "true", "min_length": 26, "max_length": 200,
                                 "description_localized": "Your Wallet Address, Accepts ETH SOL BTC SEI AVAX BSC ZKS ADA RONIN",
                                 "name_localized": "wallet"}], "description_localized": "Set your Wallet",
                             "name_localized": "wallet"},
                            {"type": 1, "name": "youtube", "description": "Set your Youtube Account", "options": [
                                {"type": 3, "name": "account",
                                 "description": "Your Youtube Account Username Example: EngageIO", "required": "true",
                                 "description_localized": "Your Youtube Account Username Example: EngageIO",
                                 "name_localized": "account"}], "description_localized": "Set your Youtube Account",
                             "name_localized": "youtube"},
                            {"type": 1, "name": "tiktok", "description": "Set your tiktok Account", "options": [
                                {"type": 3, "name": "account",
                                 "description": "Your tiktok Account Username Example: EngageIO", "required": "true",
                                 "description_localized": "Your tiktok Account Username Example: EngageIO",
                                 "name_localized": "account"}], "description_localized": "Set your tiktok Account",
                             "name_localized": "tiktok"},
                            {"type": 1, "name": "telegram", "description": "Set your telegram Account",
                             "description_localized": "Set your telegram Account", "name_localized": "telegram"}],
                                            "dm_permission": "true", "integration_types": [0],
                                            "global_popularity_rank": 3, "description_localized": "Set your twitter",
                                            "name_localized": "set"}, "attachments": []},
           "nonce": "131784151{}659474432".format(random.randrange(0, 1000)), "analytics_location": "slash_ui"}
    res = requests.post(url=url, headers=header, data=json.dumps(msg))
    if res.status_code == 204:
        print_green(f"{name} - {header['Authorization']} - 绑定推特执行成功")

# 每日签到
def signIn(header,name):
    msg = {"type": 2, "application_id": "1077740178476630129", "guild_id": "1209630079936630824",
           "channel_id": "1280446642528456705", "session_id": "a5b653ceb6f1e87f{}faaf2f3424fe3e6".format(random.randrange(0, 1000)),
           "data": {"version": "1227035648716705804", "id": "1227035648716705802", "name": "claim", "type": 1,
                    "options": [{"type": 1, "name": "daily", "options": []}],
                    "application_command": {"id": "1227035648716705802", "type": 1,
                                            "application_id": "1077740178476630129", "version": "1227035648716705804",
                                            "name": "claim", "description": "Claim your rewards!", "options": [
                            {"type": 1, "name": "daily", "description": "Claim your daily rewards!",
                             "description_localized": "Claim your daily rewards!", "name_localized": "daily"},
                            {"type": 1, "name": "role", "description": "Claim your role rewards!",
                             "description_localized": "Claim your role rewards!", "name_localized": "role"}],
                                            "dm_permission": "true", "integration_types": [0],
                                            "global_popularity_rank": 1, "description_localized": "Claim your rewards!",
                                            "name_localized": "claim"}, "attachments": []},
           "nonce": "13178423{}7827920896".format(random.randrange(0, 1000)), "analytics_location": "slash_ui"}
    res = requests.post(url=url, headers=header, data=json.dumps(msg))
    if res.status_code == 204:
        print_green(f"{name} - {header['Authorization']} - 每日签到执行成功")

def main():

    env_name = {
        "token": "环境名",
    }


    authorization = {
        "token": "推特名称",
    }

    task_list = {
        # custom_id : message_id
        "proceed-1868336916887990471-172800000": "1317896324917760171", # 只点赞
        "proceed-1868370217811779615-172800000": "1317929403661160499", # 只点赞
        "proceed-1868382798580687197-172800000": "1317941901739167786", # 只点赞
        "proceed-1868122825091080294-259200000": "1317682125876760588", # 只点赞
        "proceed-1868017402681991447-259200000": "1317576997316329473", # 只点赞
    }


    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for token in authorization:
            header = {
                "Authorization": token,
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0"
            }

            # # setTw
            # futures.append(executor.submit(setTw, authorization[token], header, env_name[token]))

            # 每日签到
            futures.append(executor.submit(signIn, header, env_name[token]))

            # 验证任务
            futures.append(executor.submit(verityRole, header, task_list, env_name[token]))

        # 等待所有线程完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # 获取任务结果，若任务抛出异常，会在此处被捕获
            except Exception as e:
                print_red(f"任务执行失败: {e}")

if __name__ == '__main__':
    main()
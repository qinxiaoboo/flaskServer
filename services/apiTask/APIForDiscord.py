import json
import random
import re
import time

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = 'https://discord.com/api/v9/interactions'


class Discord():
    def __init__(self, authorization, env):
        self.env = env
        self.authorization = authorization
        self.headers = {
            "Authorization": authorization,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0"
        }

    def verityRole(self, custom_id, message_id):
        # 每个任务这两个id可能不一样
        msg = {"type": 3, "nonce": "13178426{}6341028864".format(random.randrange(0, 1000)),
               "guild_id": "1209630079936630824", "channel_id": "1280246851739848818", "message_flags": 0,
               "message_id": message_id,
               "application_id": "1077740178476630129",
               "session_id": "a5b653ceb6f1e87f{}fbbf2f3424fe3e6".format(random.randrange(0, 1000)),
               "data": {"component_type": 2, "custom_id": custom_id}}
        res = requests.post(url=url, headers=self.headers, data=json.dumps(msg), verify=False)
        time.sleep(5)
        if res.status_code == 204:
            print(f"{self.env.name} 任务校验成功success")
            return True
        else:
            return False

    def setTw(self, twName):
        msg = {"type": 2,
               "application_id": "1077740178476630129", "guild_id": "1209630079936630824",
               "channel_id": "1280446642528456705",
               "session_id": "a5b653ceb6f1e87f{}faaf2f3424fe3e6".format(random.randrange(0, 1000)),
               "data": {"version": "1317142034250862606", "id": "1123730728040009825", "name": "set", "type": 1,
                        "options": [{"type": 1, "name": "twitter",
                                     "options": [{"type": 3, "name": "account", "value": "@{}".format(twName)}]}],
                        "application_command": {"id": "1123730728040009825", "type": 1,
                                                "application_id": "1077740178476630129",
                                                "version": "1317142034250862606",
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
                                     "description": "Your Youtube Account Username Example: EngageIO",
                                     "required": "true",
                                     "description_localized": "Your Youtube Account Username Example: EngageIO",
                                     "name_localized": "account"}], "description_localized": "Set your Youtube Account",
                                 "name_localized": "youtube"},
                                {"type": 1, "name": "tiktok", "description": "Set your tiktok Account", "options": [
                                    {"type": 3, "name": "account",
                                     "description": "Your tiktok Account Username Example: EngageIO",
                                     "required": "true",
                                     "description_localized": "Your tiktok Account Username Example: EngageIO",
                                     "name_localized": "account"}], "description_localized": "Set your tiktok Account",
                                 "name_localized": "tiktok"},
                                {"type": 1, "name": "telegram", "description": "Set your telegram Account",
                                 "description_localized": "Set your telegram Account", "name_localized": "telegram"}],
                                                "dm_permission": "true", "integration_types": [0],
                                                "global_popularity_rank": 3,
                                                "description_localized": "Set your twitter",
                                                "name_localized": "set"}, "attachments": []},
               "nonce": "131784151{}659474432".format(random.randrange(0, 1000)), "analytics_location": "slash_ui"}
        res = requests.post(url=url, headers=self.headers, data=json.dumps(msg), verify=False)
        if res.status_code == 204:
            print(f"{self.env.name} 绑定推特：{twName} success")
            return True
        else:
            return False

    # 每日签到
    def signIn(self):
        msg = {"type": 2, "application_id": "1077740178476630129", "guild_id": "1209630079936630824",
               "channel_id": "1280446642528456705",
               "session_id": "a5b653ceb6f1e87f{}faaf2f3424fe3e6".format(random.randrange(0, 1000)),
               "data": {"version": "1227035648716705804", "id": "1227035648716705802", "name": "claim", "type": 1,
                        "options": [{"type": 1, "name": "daily", "options": []}],
                        "application_command": {"id": "1227035648716705802", "type": 1,
                                                "application_id": "1077740178476630129",
                                                "version": "1227035648716705804",
                                                "name": "claim", "description": "Claim your rewards!", "options": [
                                {"type": 1, "name": "daily", "description": "Claim your daily rewards!",
                                 "description_localized": "Claim your daily rewards!", "name_localized": "daily"},
                                {"type": 1, "name": "role", "description": "Claim your role rewards!",
                                 "description_localized": "Claim your role rewards!", "name_localized": "role"}],
                                                "dm_permission": "true", "integration_types": [0],
                                                "global_popularity_rank": 1,
                                                "description_localized": "Claim your rewards!",
                                                "name_localized": "claim"}, "attachments": []},
               "nonce": "13178423{}7827920896".format(random.randrange(0, 1000)), "analytics_location": "slash_ui"}
        res = requests.post(url=url, headers=self.headers, data=json.dumps(msg), verify=False)
        time.sleep(5)
        if res.status_code == 204:
            print(f"{self.env.name} 每日签到 success")
            return True
        else:
            return False

    def sendLeaderboard(self):
        msg = {"type": 2, "application_id": "1077740178476630129", "guild_id": "1209630079936630824",
               "channel_id": "1280446642528456705",
               "session_id": "590ddeed54c07b1a{}d9901c3974e4788".format(random.randrange(0, 1000)),
               "data": {"version": "1123730728224563254", "id": "1123730728040009821", "name": "leaderboard", "type": 1,
                        "options": [], "application_command": {"id": "1123730728040009821", "type": 1,
                                                               "application_id": "1077740178476630129",
                                                               "version": "1123730728224563254", "name": "leaderboard",
                                                               "description": "Show the leaderboard for the activity of The Engage bot.",
                                                               "dm_permission": "true", "integration_types": [0],
                                                               "global_popularity_rank": 2, "options": [],
                                                               "description_localized": "Show the leaderboard for the activity of The Engage bot.",
                                                               "name_localized": "leaderboard"}, "attachments": []},
               "nonce": "1317884564{}65238528".format(random.randrange(0, 1000)), "analytics_location": "slash_ui"}
        res = requests.post(url=url, headers=self.headers, data=json.dumps(msg), verify=False)
        time.sleep(5)
        if res.status_code == 204:
            print(f"{self.env.name} 发送排名 success")
            return True
        else:
            return False

    def get_context(self,username):
        chanel_list = ['1280446642528456705']
        chanel_id = random.choice(chanel_list)
        url = "https://discord.com/api/v9/channels/{}/messages?limit=4".format(
            chanel_id)
        res = requests.get(url=url, headers=self.headers)
        result = json.loads(res.content)
        for item in result:
            if "embeds" in item and item["embeds"]:
                description = item["embeds"][0]["description"]
                # 正则表达式
                pattern = r"(\d+)\s•\s{}\s•\s(\d+)\sPoints".format(username)
                match = re.search(pattern, description)
                if match:
                    rank = match.group(1)
                    points = match.group(2)
                    return rank,points
        return None,None

    def get_userInfo(self):
        url = "https://discord.com/api/v9/users/@me"
        res = requests.get(url=url, headers=self.headers)
        result = json.loads(res.content)
        return result


if __name__ == '__main__':
    custom_id = "proceed-1868122825091080294-259200000"
    message_id = "1317682125876760588"
    # 绑定tw
    # setTw("vjvat73443575")
    # 每日签到
    # signIn()
    # 任务
    # verityRole(custom_id, message_id)
    # get_userInfo()
    # 获取排名
    # sendLeaderboard()
    # get_context()

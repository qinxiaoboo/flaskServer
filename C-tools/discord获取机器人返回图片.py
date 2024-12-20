# -*- coding: utf-8 -*-
import csv

import requests
import json
import random
import time
from loguru import logger
import datetime
from pytesseractDemo import getName,getGrade

def download_image(url, save_path, count=None):
    try:
        # 发送 GET 请求获取图片
        response = requests.get(url)

        # 确保响应成功
        if response.status_code == 200:
            # 将图片内容写入到文件
            with open(save_path, 'wb') as file:
                file.write(response.content)
                count+=1
            print(f"图片已成功下载并保存为 {save_path}")
        else:
            print(f"无法下载图片，HTTP状态码：{response.status_code}")
    except Exception as e:
        print(f"下载图片时发生错误: {e}")

def dowloadJpgs():
    count = 0
    chanel_list = ['1075613094035861524']
    headr = {
        "Authorization": "token",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0"
    }
    chanel_id = random.choice(chanel_list)
    url = "https://discord.com/api/v9/channels/{}/messages?limit=4".format(chanel_id)
    res = requests.get(url=url, headers=headr)
    result = json.loads(res.content)
    for item in result:
        # print(item)
        attachments = item["attachments"]
        if len(attachments) > 0:
            attachment = attachments[0]
            url = attachment["url"]
            download_image(url, f"{count}.jpg", count)
            count+=1


def send_message(authorization, chanel_id):
    header = {
        "Authorization": authorization,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0"
    }
    msg = {
        "content": "!rank",
        "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
        "tts": False
    }
    url = 'https://discord.com/api/v9/channels/{}/messages'.format(chanel_id)
    try:
        res = requests.post(url=url, headers=header, data=json.dumps(msg))
        if res.status_code == 200:
            message_data = res.json()
            message_id = message_data['id']
            logger.info(f"{datetime.datetime.now()} 状态：发送成功。Token：{authorization}")
        else:
            logger.info(f"{datetime.datetime.now()} 状态：发送失败。Token：{authorization}")
            return True
    except Exception as e:
        logger.info(f"{datetime.datetime.now()} 状态：发送失败。Token：{authorization}")
        return True
    # Sleep for 1 second before the next message is sent
    time.sleep(2)

from collections import Counter
def common_char_count(str1, str2):
    c = 0
    common = Counter(str1)&Counter(str2)
    for value in common.values():
        c+=value
    return (c / len(str2))
# 更准确
def main():
    data = []
    authorization_list = {
        "用户名": 'token',

    }

    for key, value in authorization_list.items():
        try:
            flag = send_message(value, "1075613094035861524")
            if flag:
                continue
            dowloadJpgs()
            for i in range(2):
                try:
                    name = getName(f"{i}.jpg")
                    grade = getGrade(f"{i}.jpg")
                    if isinstance(key,str) and common_char_count(key, name) > 0.8:
                        print(f"匹配成功: {name}: {grade}分")
                        data.append([key, value,grade])
                        break
                except FileNotFoundError:
                    pass
        except Exception as e:
            logger.exception(e)
    with open("../output.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print("数据已写入 'output.csv' 文件")

def main2():
    data = []
    authorization_list = [
        'token',

    ]

    for value in authorization_list:
        try:
            flag = send_message(value, "1075613094035861524")
            if flag:
                continue
            dowloadJpgs()
            for i in range(1):
                try:
                    name = getName(f"{i}.jpg")
                    grade = getGrade(f"{i}.jpg")
                    print(f"匹配成功: {name}: {grade}分")
                    data.append([value, grade])
                except FileNotFoundError:
                    pass
        except Exception as e:
            logger.exception(e)

    with open("../output.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print("数据已写入 'output.csv' 文件")


if __name__ == '__main__':
    main2()

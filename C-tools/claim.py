import requests,json,random,time,datetime
from concurrent.futures import ThreadPoolExecutor, as_completed




def send_message(authorization, chanel_id):
    header = {
        "Authorization": authorization,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }
    msg = {
        "content": "/dailycheck address:0xecb41b49d74d7d13bb51f9603fd2360557647504",
        "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
        "tts": False
    }
    url = 'https://discord.com/api/v9/channels/{}/messages'.format(chanel_id)
    try:
        res = requests.post(url=url, headers=header, data=json.dumps(msg))
        if res.status_code == 200:
            message_data = res.json()
            message_id = message_data['id']
            print(datetime.datetime.now(),f"状态：发送成功。频道ID：{chanel_id}。Token：{authorization}")

        else:
            print(datetime.datetime.now(),f"状态：发送失败。频道ID：{chanel_id}。Token：{authorization}")
    except Exception as e:
        print(datetime.datetime.now(),f"状态：发送失败。频道ID：{chanel_id}。Token：{authorization}")
    time.sleep(5)

def chat():
    chanel_list = [
        '1299551565647970314'
    ]
    authorization_list = [

    ]

    with ThreadPoolExecutor(max_workers=5) as executor:  # Limit concurrent threads to 5 or adjust as needed
        futures = []

        for authorization in authorization_list:
            for chanel_id in chanel_list:
                futures.append(executor.submit(send_message, authorization, chanel_id))
                time.sleep(2)

        for future in as_completed(futures):
            future.result()

if __name__ == '__main__':

    while True:
        current_time = datetime.datetime.now()
        if current_time.hour >= 1 and current_time.hour < 24:
            try:
                chat()
                sleeptime = random.randrange(1300, 1600)
                time.sleep(sleeptime)
            except Exception as e:
                print(f"Error in main loop: {e}")
                pass
        else:
            print(f"当前时间：{datetime.datetime.now()},继续等待")
            time.sleep(60)













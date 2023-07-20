import requests
import time
import pytz
from datetime import datetime, timedelta
from random import random

# Get the timezone object for Hong Kong
hk_tz = pytz.timezone('Asia/Hong_Kong')

class DiscordChannelSendMsg:
    def __init__(self, times: int, wait: int, margin: int):
        with open('msg.txt', encoding='utf-8') as f:
            self.msg2 = f.read()
        self.times = times
        self.wait = wait
        self.margin = margin
        self.randomTime = random() * (self.margin)
    def send_msg(self):
        payload = {
            'content': f'{self.msg2}'
        }
        header = {
            'Authorization': "MTEyOTg1NzIxNjA1NzQ1MDUxNw.GAhDgH.gvatZhFe_bjmwYpWlaL24Qfi2OuBrtgNUb9kVI"
        }

        with requests.Session() as session:
            for i in range(self.times):
                files = {
                    "file1": ("./leg1.png", open("leg1.png", 'rb')),
                    "file2": ("./leg2.png", open("leg2.png", 'rb')),
                    "file3": ("./sliv.png", open("sliv.png", 'rb'))
                }
                # Get the current time in Hong Kong
                now = datetime.now(hk_tz)
                # Format the current time as a string
                now_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
                print(f'現在香港的時間是 {now_time_str}')
                print(i, ": ", self.wait + self.randomTime)
                next_arrival = now + timedelta(seconds=self.wait + self.randomTime + 2.8)
                next_arrival_str = next_arrival.strftime('%Y-%m-%d %H:%M:%S')
                print(f"下一條消息將在 {next_arrival_str} 到達")
                try: # handle exceptions that may occur when sending a single message
                    # if the request to the Discord API fails due to a connection error or invalid credentials
                    r = session.post("https://discord.com/api/v9/channels/663787450652688405/messages", data=payload,
                                  headers=header, files=files)
                    r.raise_for_status()  # Response object that raises an exception if the response status code indicates an error
                except requests.exceptions.RequestException as e:
                    print(f'An error occurred while sending the message: {e}')
                    print("It continues...")
                time.sleep(self.wait + self.randomTime)
                self.randomTime = random() * self.margin

if __name__ == '__main__':
    times = int(input("消息數量： "))
    wait = int(input("消息之間的秒數(s)： "))
    margin = int(input("人為誤差範圍(s)： "))
    messageVarObject = DiscordChannelSendMsg(times, wait, margin) # init the auto message class
    messageVarObject.send_msg() # start to send the message
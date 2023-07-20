import requests
import time
import pytz
from datetime import datetime, timedelta
from random import random

# Get the timezone object for Hong Kong
hk_tz = pytz.timezone('Asia/Hong_Kong')

class sendMessage:
    def __init__(self, times, wait, margin):
        with open('msg.txt', encoding='utf-8') as f:
            self.msg2 = f.read()
        self.times = times
        self.wait = wait
        self.margin = margin
        self.randomTime = random() * (self.margin)
    def main(self):
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
                r = session.post("https://discord.com/api/v9/channels/1131512993700655168/messages", data=payload,
                              headers=header, files=files)
                time.sleep(self.wait + self.randomTime)
                self.randomTime = random() * self.margin

if __name__ == '__main__':
    times = int(input("Amount of messages: "))
    wait = int(input("Seconds between messages: "))
    margin = int(input("Human error margin: "))
    messageVarObject = sendMessage(times, wait, margin)
    messageVarObject.main()
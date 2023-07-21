import requests
import time
import pytz
from datetime import datetime, timedelta
from random import random
from random import randint

discord_url = "https://discord.com"
hk_tz = pytz.timezone('Asia/Hong_Kong') # Get the timezone object for Hong Kong
channel_ID = 663787450652688405 # the channel id you want to send msg to
cur_Token = "MTEyOTg1NzIxNjA1NzQ1MDUxNw.GTkB73.qwm9jA5pqMHGJaYl46QYt2m0w4IkA4fChMXmIM" # User Token for authorization to send msg
class DiscordChannelFunctions:
    def __init__(self, times: int, wait: int, human_margin: int):
        with open('text&phot/msg1.txt', encoding='utf-8') as f:
            self.msg2 = f.read()
        self.times = times # how many msg you want to send
        self.wait = wait # the fixed (at least) waiting time between msgs
        self.human_margin = human_margin # random margin time for making each interval time more natural (look like a real human sending)
        self.randomTime = random() * (self.human_margin) # 0 to self.human_margin (random pick)
    def create_nonce(self):
        nonce = ""
        for digit in range(1, 16):
            nonce += str(randint(0, 9))
        return nonce
    def get_ChannelInfo(self, channel_ID):
        full_url = discord_url+"/channels/"+str(channel_ID)
        print(full_url)
        channel_Info = requests.request("GET", full_url)
        return channel_Info.text
    def send_msg(self): # sending files and texts at the same time
        payload = {
            "content": f'{self.msg2}',
            "nonce": str(self.create_nonce()), # a nonce to prevent replay attacks and ensure that each message is sent only once
            "tts" : False
        }
        header = {
            'Authorization': cur_Token, # token-based authentication (as is typically the case with the Discord API)
            #'Content-Type': "application/json" # tells the server the type of data that is being sent in the request
        }

        with requests.Session() as session:
            for i in range(self.times):
                files = {
                    "file1": ("./leg1.png", open("text&phot/leg1.png", 'rb')),
                    "file2": ("./leg2.png", open("text&phot/leg2.png", 'rb')),
                    "file3": ("./sliv.png", open("text&phot/sliv.png", 'rb'))
                }

                now = datetime.now(hk_tz) # Get the current time in Hong Kong
                now_time_str = now.strftime('%Y-%m-%d %H:%M:%S') # Format the current time as a string
                print(f'現在香港的時間是 {now_time_str}')
                print(i, ": ", self.wait + self.randomTime)
                # calculate the message arrival time ( current time + fixed waiting time + random interval time)
                next_arrival = now + timedelta(seconds=self.wait + self.randomTime + 2.8)
                next_arrival_str = next_arrival.strftime('%Y-%m-%d %H:%M:%S')
                print(f"下一條消息將在 {next_arrival_str} 到達")
                # https://discord.com/api/v9/channels/663787450652688405/messages
                try: # handle exceptions that may occur when sending a single message
                    # if the request to the Discord API fails due to a connection error or invalid credentials
                    r = session.post(discord_url+"/api/v9/channels/"+str(channel_ID)+"/messages", data=payload,
                                  headers=header, files=files)
                    r.raise_for_status()  # Response object that raises an exception if the response status code indicates an error
                except requests.exceptions.RequestException as e: # whenever the server side returns an error, catch it here and just leave it -> continue the loop
                    print(f'An error occurred while sending the message: {e}')
                    print("It continues...")
                time.sleep(self.wait + self.randomTime) # the waiting time between msgs
                self.randomTime = random() * self.human_margin # re-calculate a random interval time
                # hihihi
if __name__ == '__main__':
    times = int(input("消息數量： "))
    wait = int(input("消息之間的秒數(s)： "))
    human_margin = int(input("人為誤差範圍(s)： "))
    messageVarObject = DiscordChannelFunctions(times, wait, human_margin) # init the auto message class
    print(messageVarObject.get_ChannelInfo(channel_ID))
    messageVarObject.send_msg() # start to send the message
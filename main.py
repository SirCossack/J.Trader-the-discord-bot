import discord_interactions
import config
from random import randint, uniform
import websocket
from time import sleep
import json
import threading
import requests as rq





if __name__ == '__main__':
    def on_message(socket, message):
        """
        Function reacting to Gateway websocket connection messages

        """

        message = json.loads(message)

        if message['op'] == 10:  #reaction to the hello message
            heartbeat_interval = int(message['d']['heartbeat_interval']) / 1000
            sleep(heartbeat_interval * uniform(0, 0.1))
            socket.send(json.dumps({"op": 1, "d": message['s']}))

            sleep(1)

            identify_message = json.dumps({
                                'op': 2,
                                'd': {
                                    'token': config.TOKEN,
                                    'properties': {
                                        'os': 'windows',
                                        'browser': 'stonks',
                                        'device': 'stonks'},
                                    'intents': 2048
                                }})
            socket.send(identify_message)



        elif message['op'] == 1:  #reaction to the heartbeat, aka ping
            socket.send(json.dumps({'op': 1, 'd': message['s']}))


    def mainthread():
        websocket.enableTrace(True)
        gateway = websocket.WebSocketApp(url='wss://gateway.discord.gg/?v=10&encoding=json',
                                         on_message=on_message)
        gateway.run_forever()


    def secondthread():
        print(rq.post(url='https://discord.com/api//channels//696138228088176782//messages',
                      headers={'Authorization': 'Bot {}'.format(config.TOKEN), 'Content-type': 'application/json'},
                      json={
                            "content": "Hello, World!",
                            "tts": False,
                            "embeds": [{
                              "title": "Hello, Embed!",
                              "description": "This is an embedded message."}]}))



    t1 = threading.Thread(target=mainthread)
    t2 = threading.Thread(target=secondthread)
    t1.start()
    sleep(10)
    t2.start()
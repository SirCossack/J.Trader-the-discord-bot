import discord_interactions
import config
from random import uniform
import websocket
from time import sleep
import json
import threading
import requests as rq





if __name__ == '__main__':
    def on_message(socket, message):
        """
        Function reacting to Gateway websocket connection messages

        :param socket: The WebSocket connection the app is connected to
        :param message: The messages received with the aforementioned connection
        """

        message = json.loads(message)

        if message['t'] == 'INTERACTION_CREATE': #reacts to commands
            interaction_id = message['d']['id']
            interaction_token = message['d']['token']
            command_name = message['d']['data']['name']
            react_to_command(interaction_id=interaction_id, interaction_token=interaction_token, command=command_name)

        elif message['op'] == 10:  #reaction to the hello message
            connect_to_discord(socket, message)

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
        command_start_RSI()

    def command_start_RSI():
        url = "https://discord.com/api/v10/applications/{}/commands".format(config.CLIENT_ID)
        json = {
            "name": "relative_strength_index",
            "type": 1,
            "description": "Start calculating and sending RSI values for chosen pair, timeframe and period.",
            "options": []}
        headers = {"Authorization": "Bot {}".format(config.TOKEN)}
        print(rq.post(url=url, json=json, headers=headers))


    def react_to_command(interaction_id, interaction_token, command):
        """
        Function handling reacting to users' commands.
        :param interaction_id: Interaction ID from the Gateway message
        :param interaction_token: Interaction token from the Gateway message
        :param command: For now doesn't do anything, but in the future can be used to send different data depending on the command used
        :return:
        """
        url = "https://discord.com/api/v10/interactions/{}/{}/callback".format(interaction_id, interaction_token)
        data = {
            "type": 4,
            "data": {
                "content": "Congrats on sending your command!"}}
        rq.post(url, json=data)

    def connect_to_discord(socket, message):
        heartbeat_interval = int(message['d']['heartbeat_interval']) / 1000
        sleep(heartbeat_interval * uniform(0, 0.1))
        socket.send(json.dumps({"op": 1, "d": message['s']}))
        identify_message = json.dumps({
            'op': 2,
            'd': {
                'token': config.TOKEN,
                'properties': {
                    'os': 'windows',
                    'browser': 'stonks',
                    'device': 'stonks'},
                'intents': 8}})
        socket.send(identify_message)

    t1 = threading.Thread(target=mainthread)
    t2 = threading.Thread(target=secondthread)
    t1.start()
    sleep(10)
    t2.start()
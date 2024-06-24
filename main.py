import config
from random import uniform
import websocket
from time import sleep
import json
import requests as rq
import bybit

"""

README.txt will have some instructions on what is necessary to run, as well as comments from the author.
I'm 50% sure this works. Have fun.

"""



def on_message(socket, message):
    """
    Function reacting to Gateway websocket connection messages

    :param socket: The WebSocket connection the app is connected to
    :param message: The messages received with the aforementioned connection
    """

    message = json.loads(message)

    if message['t'] == 'INTERACTION_CREATE':  #reacts to commands
        channel_id = message['d']['channel_id']
        interaction_id = message['d']['id']
        interaction_token = message['d']['token']
        command_name = message['d']['data']['name']
        options = message['d']['data']['options']
        react_to_command(interaction_id=interaction_id, interaction_token=interaction_token,
                         command=command_name, options=options, channel_id=channel_id)

    elif message['op'] == 10:  #reaction to the hello message
        connect_to_discord(socket, message)
        add_command_start_RSI()

    elif message['op'] == 1:  #reaction to the heartbeat, aka ping
        socket.send(json.dumps({'op': 1, 'd': message['s']}))


def run():
    #websocket.enableTrace(True)
    gateway = websocket.WebSocketApp(url='wss://gateway.discord.gg/?v=10&encoding=json',
                                     on_message=on_message)
    gateway.run_forever()


def add_command_start_RSI():
    url = "https://discord.com/api/v10/applications/{}/commands".format(config.CLIENT_ID)
    data = {
        "name": "relative_strength_index",
        "type": 1,
        "description": "Start calculating and sending RSI values for chosen pair, timeframe and period.",
        "options": [
                    {'name': 'timeframe',
                     'description': 'The K-line chart time scale (in minutes)',
                     'type': 4,
                     'required': True},
                    {'name': 'period',
                     'description': 'How many past datapoints to use for RSI calculation',
                     'type': 4,
                     'required': True},
                    {'name': 'symbol',
                     'description': 'The trading pair symbol',
                     'type': 3,
                     'required': True}
        ]}
    headers = {"Authorization": "Bot {}".format(config.TOKEN)}
    rq.post(url=url, json=data, headers=headers)


def react_to_command(interaction_id, interaction_token, command, options, channel_id):
    """
    Function handling reacting to users' commands.
    :param interaction_id: Interaction ID from the Gateway message
    :param interaction_token: Interaction token from the Gateway message
    :param command: For now doesn't do anything, but in the future can be used to send different data depending on the command used
    :param options: Options passed in via command in discord channel
    :param channel_id: Channel_id in which the command was called
    :return:
    """
    url = "https://discord.com/api/v10/interactions/{}/{}/callback".format(interaction_id, interaction_token)
    data = {
        "type": 4,
        "data": {
            "content": "Starting to monitor RSI of {} pair for period = {} and timeframe = {} in this channel! Announcements will be sent for values less than 30 or more than 70. Right now RSI is {:.2f}".format(
                options[2]['value'], options[1]['value'], options[0]['value'],
                bybit.relative_strength_index(options[0]['value'], options[1]['value'], options[2]['value'], channel_id=channel_id)
            )}}

    rq.post(url, json=data)


def connect_to_discord(socket, message):
    heartbeat_interval = int(message['d']['heartbeat_interval']) / 1000
    sleep(heartbeat_interval * uniform(0, 0.4))
    socket.send(json.dumps({"op": 1, "d": message['s']}))
    identify_message = json.dumps({
        'op': 2,
        'd': {
            'token': config.TOKEN,
            'properties': {
                'os': 'windows',
                'browser': 'stonks',
                'device': 'stonks'},
            'intents': 2048}})
    socket.send(identify_message)


if __name__ == '__main__':
    run()

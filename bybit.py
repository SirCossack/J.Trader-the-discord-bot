from pybit.unified_trading import HTTP as pybit_HTTP, WebSocket as pybit_WebSocket
from ta.momentum import rsi
import pandas as pd
from collections import deque
import requests as rq
import config


def relative_strength_index(timeframe, period, symbol, channel_id):
    """
    Function getting the spot K-Line data from Bybit and returning RSI everytime a candle is finished.
    :param timeframe: The K-line chart time scale (in minutes)
    :param period: How many past datapoints to use for RSI calculation
    :param symbol: The trading pair symbol ('BTCUSDT', 'SOLUSDT' etc.)
    :param channel_id: Channel_id in which the command was called
    :return:
    """
    time = int(pybit_HTTP().get_server_time()['result']['timeSecond']) * 1000
    entry_data = pybit_HTTP().get_kline(category='spot',
                                        symbol=symbol,
                                        interval=timeframe,
                                        start=time-(timeframe*1000*60*period*4),
                                        end=time)

    dataset = deque(maxlen=period*4)
    for i in entry_data['result']['list']:
        dataset.appendleft(i[4])  #Appending closing prices to the dataset

    starting_rsi = rsi(close=pd.Series(data=dataset, dtype=float), window=period)[period*4-1]

    def handler(x):
        if x['data'][0]['confirm'] is True:
            dataset.append(x['data'][0]['close'])
            curr_RSI = (rsi(close=pd.Series(data=dataset, dtype=float), window=period)[period*4-1])
            if curr_RSI > 70 or curr_RSI < 30:
                print(rq.post(url='https://discord.com/api//channels//{}//messages'.format(channel_id),
                              headers={'Authorization': 'Bot {}'.format(config.TOKEN), 'Content-type': 'application/json'},
                              json={
                                  "content": "The RSI for {} pair (timeframe - {} | period - {}) is {:.2f}".format(symbol, timeframe, period, curr_RSI),
                                  "tts": False,
                                  }))

    session = pybit_WebSocket(channel_type='spot', testnet=False)
    session.kline_stream(symbol=symbol, interval=timeframe, callback=handler)
    return starting_rsi

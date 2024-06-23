from pybit.unified_trading import HTTP, WebSocket
from ta.momentum import rsi
import pandas as pd
from time import sleep
from collections import deque

PERIOD = 50 # in timeframes - if timeframe is 60 then period is 1 hour
TIMEFRAME = 1 #in minutes
time = int(HTTP().get_server_time()['result']['timeSecond']) * 1000
entry_data = HTTP().get_kline(category='spot', symbol='SOLUSDT', interval=TIMEFRAME, start=time-(TIMEFRAME*1000*60*PERIOD*4), end=time)
dataset = deque(maxlen=PERIOD*4)

for i in entry_data['result']['list']:
    dataset.appendleft(i[4])

print(rsi(close=pd.Series(data=dataset, dtype=float),window=PERIOD)[PERIOD*4-1])


def handler(x):
    if x['data'][0]['confirm'] == True:
        dataset.append(x['data'][0]['close'])
        curr_RSI = (rsi(close=pd.Series(data=dataset, dtype=float),window=PERIOD)[PERIOD*4-1])
        print(curr_RSI)




session = WebSocket(channel_type='spot', testnet=False)
session.kline_stream(
    symbol="SOLUSDT",
    interval=TIMEFRAME,
    callback=handler)


while True:     #for some reason necessary for pybit.unified_trading.WebSocket to work, otherwise program stops after 5-10 callbacks
    sleep(1)




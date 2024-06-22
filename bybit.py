import requests
import websocket as ws
import json
from pybit.unified_trading import HTTP, WebSocket
from ta.momentum import rsi
import config
import pandas


session = HTTP(testnet=False)
print(session.get_kline(
    category="inverse",
    symbol="SOLUSDT",
    interval=60,
    start=1670601600000,
    end=1670608800000,
))
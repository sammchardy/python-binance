from binance.client import Client
from datetime import timezone, datetime
import pandas as pd

keys = pd.read_csv('./tradingkey.csv')
print(keys)
print(keys['key'][0],keys['key'][1])
client = Client(keys['key'][0], keys['key'][1],tld = 'us')
print(client.get_asset_balance(asset = 'ETH', recvWindow=10000))
from binance.websockets import BinanceSocketManager

import zmq
import json
from util import *


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(connEndPoint)
bm = BinanceSocketManager(client)

def process_message(msg):
    try:
        socket.send_string(connTopic + json.dumps(msg))
    except zmq.ZMQError as error:
        print(msg)
        print(error)

bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start_aggtrade_socket('ETHUSDT', process_message)
bm.start_aggtrade_socket('LTCUSDT', process_message)
bm.start_aggtrade_socket('BNBUSDT', process_message)
bm.start_depth_socket('BNBUSDT', process_message, 5)
#print(bm.start_user_socket(process_message))
#print(bm._conns)
bm.start()

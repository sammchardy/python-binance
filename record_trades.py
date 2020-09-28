from binance.client import Client
from datetime import timezone, datetime
import pandas as pd

keys = pd.read_csv('./tradingkey.csv')
print(keys)
print(keys['key'][0],keys['key'][1])
client = Client(keys['key'][0], keys['key'][1],tld = 'us')
print(client.get_asset_balance(asset = 'ETH', recvWindow=10000))
from binance.websockets import BinanceSocketManager

import socket
import pickle
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)

bm = BinanceSocketManager(client)



def process_message(msg):
    print(msg)

    server.sendto(pickle.dumps(msg), ('<broadcast>', 37020))

bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start_aggtrade_socket('ETHUSDT', process_message)
bm.start_aggtrade_socket('LTCUSDT', process_message)
bm.start_aggtrade_socket('BNBUSDT', process_message)
bm.start_depth_socket('BNBUSDT',process_message,5)
#print(bm.start_user_socket(process_message))
#print(bm._conns)
bm.start()

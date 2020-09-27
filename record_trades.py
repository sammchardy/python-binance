from binance.client import Client
from datetime import timezone, datetime


api_key = '7Pq5uub6PBZKShPBLJOJTnRKbR8DpbBsGh7iG0pCu3GyBDCJmALelyzmWiYEE8yA';
api_secret = 'OZMbRNtDzRqX7dthbwFDLWCHZLwW2fH0mNpREXg4iuCbkXStVlVMtH8mN0BgubUo';
client = Client(api_key, api_secret)

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
#    print(msg)

    server.sendto(pickle.dumps(msg), ('<broadcast>', 37020))


bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start_aggtrade_socket('ETHUSDT', process_message)
bm.start_aggtrade_socket('LTCUSDT', process_message)
bm.start_aggtrade_socket('BNBUSDT', process_message)
bm.start_depth_socket('BNBUSDT',process_message,5)

bm.start()

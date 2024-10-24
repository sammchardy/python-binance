import os
# import pytest
import sys
import asyncio

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance import ThreadedWebsocketManager, ThreadedDepthCacheManager


proxies = {}
proxy = os.getenv("PROXY")

if not proxy:
    print("No proxy set")

twm = ThreadedWebsocketManager(https_proxy=proxy)

def handle_socket_message(msg):
    # {'e': 'kline', 'E': 1729784531169, 's': 'BTCUSDT', 'k': {'t': 1729784520000, 'T': 1729784579999, 's': 'BTCUSDT', 'i': '1m', 'f': 3958478889, 'L': 3958479671, 'o': '67836.00000000', 'c': '67842.48000000', 'h': '67848.49000000', 'l': '67836.00000000', 'v': '1.67046000', 'n': 783, 'x': False, 'q': '113325.18336150', 'V': '1.47741000', 'Q': '100227.77923420', 'B': '0'}}
    assert msg['e'] == 'kline'
    assert msg['k']['s'] == 'BTCUSDT'
    assert msg['k']['i'] == '1m'
    twm.stop()

def test_threaded_websocket_manager():
    twm.start()
    twm.start_kline_socket(callback=handle_socket_message, symbol='BTCUSDT')
    twm.join()
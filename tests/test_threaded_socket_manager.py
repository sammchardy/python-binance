
import pytest
import os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)


from binance import ThreadedWebsocketManager
from binance.streams import BinanceSocketManager
from binance.client import AsyncClient

received_ohlcv = False
received_depth = False

twm: ThreadedWebsocketManager

def handle_socket_message(msg):
    global received_ohlcv, received_depth
    print(msg)
    if 'e' in msg:
        if msg['e'] == 'depthUpdate':
            received_depth = True
        if msg['e'] == 'kline':
            received_ohlcv = True
    if received_depth and received_ohlcv:
        twm.stop()

def test_socket_stopped_on_aexit():
    global twm
    twm = ThreadedWebsocketManager(api_key="", api_secret="", testnet=True)

    symbol = "BTCUSDT"

    twm.start()

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    twm.join()
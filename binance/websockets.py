import json
import threading

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS
from twisted.internet import reactor, ssl


BINANCE_STREAM_URL = 'wss://stream.binance.com:9443/ws/'


class BinanceClientProtol(WebSocketClientProtocol):

    def onMessage(self, payload, isBinary):
        if not isBinary:
            payload_obj = json.loads(payload.decode('utf8'))
            self.factory.callback(payload_obj)


class BinanceSocketManager(threading.Thread):

    _conns = {}

    def __init__(self):
        threading.Thread.__init__(self)

    def _start_socket(self, path, callback):
        if path in self._conns:
            return

        factory = WebSocketClientFactory(BINANCE_STREAM_URL + path)
        factory.protocol = BinanceClientProtol
        factory.callback = callback
        context_factory = ssl.ClientContextFactory()

        self._conns[path] = connectWS(factory, context_factory)

    def start_depth_socket(self, symbol, callback):
        self._start_socket(symbol.lower() + '@depth', callback)

    def start_kline_socket(self, symbol, callback):
        self._start_socket(symbol.lower() + '@kline', callback)

    def start_trade_socket(self, symbol, callback):
        self._start_socket(symbol.lower() + '@trade', callback)

    def start_ticker_socket(self, callback):
        self._start_socket('!ticker@arr', callback)

    def start_user_socket(self, listen_key, callback):
        self._start_socket(listen_key, callback)

    def _stop_socket(self, path):
        if path not in self._conns:
            return

        self._conns[path].disconnect()
        del(self._conns[path])

    def stop_depth_socket(self, symbol):
        self._stop_socket(symbol.lower() + '@depth')

    def stop_kline_socket(self, symbol):
        self._stop_socket(symbol.lower() + '@kline')

    def stop_trade_socket(self, symbol):
        self._stop_socket(symbol.lower() + '@trade')

    def stop_ticker_socket(self):
        self._stop_socket('!ticker@arr')

    def stop_user_socket(self, listen_key):
        self._stop_socket(listen_key)

    def run(self):
        reactor.run(installSignalHandlers=False)

    def close(self):
        reactor.stop()

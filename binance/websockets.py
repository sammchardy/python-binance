#!/usr/bin/env python
# coding=utf-8

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
    _user_timer = None
    _client = None
    _user_listen_key = None
    _user_timeout = 50 * 60  # 50 minutes

    def __init__(self, client):
        """
        Intialise the BinanceSocketManager
        :param client: Binance API client
        """
        threading.Thread.__init__(self)
        self._client = client

    def _start_socket(self, path, callback):
        if path in self._conns:
            return False

        factory = WebSocketClientFactory(BINANCE_STREAM_URL + path)
        factory.protocol = BinanceClientProtol
        factory.callback = callback
        context_factory = ssl.ClientContextFactory()

        self._conns[path] = connectWS(factory, context_factory)
        return True

    def start_depth_socket(self, symbol, callback):
        """
        Start a websocket for symbol market depth
        :param symbol:
        :param callback:
        :return:
        """
        return self._start_socket(symbol.lower() + '@depth', callback)

    def start_kline_socket(self, symbol, callback):
        """
        Start a websocket for symbol kline data
        :param symbol:
        :param callback:
        :return:
        """
        return self._start_socket(symbol.lower() + '@kline', callback)

    def start_trade_socket(self, symbol, callback):
        """
        Start a websocket for symbol trade data
        :param symbol:
        :param callback:
        :return:
        """
        return self._start_socket(symbol.lower() + '@trade', callback)

    def start_ticker_socket(self, callback):
        """
        Start a websocket for ticker data
        :param callback:
        :return:
        """
        return self._start_socket('!ticker@arr', callback)

    def start_user_socket(self, callback):
        """
        Start a websocket for user data
        :param callback:
        :return:
        """
        self._user_listen_key = self._client.stream_get_listen_key()
        if self._start_socket(self._user_listen_key, callback):
            # start timer to keep socket alive
            self._start_user_timer()

    def _start_user_timer(self):
        self._user_timer = threading.Timer(self._user_timeout, self._keepalive_user_socket)
        self._user_timer.setDaemon(True)
        self._user_timer.start()

    def _keepalive_user_socket(self):
        self._client.stream_keepalive(listenKey=self._user_listen_key)
        self._start_user_timer()

    def _stop_socket(self, path):
        if path not in self._conns:
            return

        self._conns[path].disconnect()
        del(self._conns[path])

    def stop_depth_socket(self, symbol):
        """
        Stop the symbol depth socket
        :param symbol:
        :return:
        """
        self._stop_socket(symbol.lower() + '@depth')

    def stop_kline_socket(self, symbol):
        """
        Stop the symbol kline socket
        :param symbol:
        :return:
        """
        self._stop_socket(symbol.lower() + '@kline')

    def stop_trade_socket(self, symbol):
        """
        Stop the symbol trade socket
        :param symbol:
        :return:
        """
        self._stop_socket(symbol.lower() + '@trade')

    def stop_ticker_socket(self):
        """
        Stop the ticker data websocket
        :return:
        """
        self._stop_socket('!ticker@arr')

    def stop_user_socket(self):
        """
        Stop the user data websocket
        :return:
        """
        if not self._user_listen_key:
            return
        self._stop_socket(self._user_listen_key)
        # stop the timer
        self._user_timer.cancel()
        self._user_timer = None
        # close the stream
        self._client.stream_close(listenKey=self._user_listen_key)
        self._user_listen_key = None

    def run(self):
        reactor.run(installSignalHandlers=False)

    def close(self):
        """
        Stop the websocket manager and close connections
        :return:
        """
        reactor.stop()

        self.stop_user_socket()
        self._conns = {}

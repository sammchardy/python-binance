#!/usr/bin/env python
# coding=utf-8

import json
import threading

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS
from twisted.internet import reactor, ssl
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.error import ReactorAlreadyRunning

from .enums import KLINE_INTERVAL_1MINUTE, WEBSOCKET_DEPTH_1

BINANCE_STREAM_URL = 'wss://stream.binance.com:9443/ws/'


class BinanceClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        # reset the delay after reconnecting
        self.factory.resetDelay()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            payload_obj = json.loads(payload.decode('utf8'))
            self.factory.callback(payload_obj)


class BinanceReconnectingClientFactory(ReconnectingClientFactory):

    # set initial delay to a short time
    initialDelay = 0.1

    maxDelay = 10

    maxRetries = 5


class BinanceClientFactory(WebSocketClientFactory, BinanceReconnectingClientFactory):

    protocol = BinanceClientProtocol

    def clientConnectionFailed(self, connector, reason):
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        self.retry(connector)


class BinanceSocketManager(threading.Thread):

    _user_timeout = 50 * 60  # 50 minutes

    def __init__(self, client):
        """Initialise the BinanceSocketManager

        :param client: Binance API client
        :type client: binance.Client

        """
        threading.Thread.__init__(self)
        self._conns = {}
        self._user_timer = None
        self._user_listen_key = None
        self._client = client

    def _start_socket(self, path, callback):
        if path in self._conns:
            return False

        factory = BinanceClientFactory(BINANCE_STREAM_URL + path)
        factory.protocol = BinanceClientProtocol
        factory.callback = callback
        context_factory = ssl.ClientContextFactory()

        self._conns[path] = connectWS(factory, context_factory)
        return path

    def start_depth_socket(self, symbol, callback, depth=WEBSOCKET_DEPTH_1):
        """Start a websocket for symbol market depth

        https://www.binance.com/restapipub.html#depth-wss-endpoint

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :param depth: Number of depth entries to return, default WEBSOCKET_DEPTH_1
        :type depth: enum

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "depthUpdate",			# event type
                "E": 1499404630606, 		# event time
                "s": "ETHBTC", 				# symbol
                "u": 7913455, 				# updateId to sync up with updateid in /api/v1/depth
                "b": [						# bid depth delta
                    [
                        "0.10376590", 		# price (need to update the quantity on this price)
                        "59.15767010", 		# quantity
                        []					# can be ignored
                    ],
                ],
                "a": [						# ask depth delta
                    [
                        "0.10376586", 		# price (need to update the quantity on this price)
                        "159.15767010", 	# quantity
                        []					# can be ignored
                    ],
                    [
                        "0.10383109",
                        "345.86845230",
                        []
                    ],
                    [
                        "0.10490700",
                        "0.00000000", 		# quantity=0 means remove this level
                        []
                    ]
                ]
            }
        """
        socket_name = symbol.lower() + '@depth'
        if depth != WEBSOCKET_DEPTH_1:
            socket_name = '{}{}'.format(socket_name, depth)
        return self._start_socket(socket_name, callback)

    def start_kline_socket(self, symbol, callback, interval=KLINE_INTERVAL_1MINUTE):
        """Start a websocket for symbol kline data

        https://www.binance.com/restapipub.html#kline-wss-endpoint

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function
        :param interval: Kline interval, default KLINE_INTERVAL_1MINUTE
        :type interval: enum

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "kline",					# event type
                "E": 1499404907056,				# event time
                "s": "ETHBTC",					# symbol
                "k": {
                    "t": 1499404860000, 		# start time of this bar
                    "T": 1499404919999, 		# end time of this bar
                    "s": "ETHBTC",				# symbol
                    "i": "1m",					# interval
                    "f": 77462,					# first trade id
                    "L": 77465,					# last trade id
                    "o": "0.10278577",			# open
                    "c": "0.10278645",			# close
                    "h": "0.10278712",			# high
                    "l": "0.10278518",			# low
                    "v": "17.47929838",			# volume
                    "n": 4,						# number of trades
                    "x": false,					# whether this bar is final
                    "q": "1.79662878",			# quote volume
                    "V": "2.34879839",			# volume of active buy
                    "Q": "0.24142166",			# quote volume of active buy
                    "B": "13279784.01349473"	# can be ignored
                    }
            }
        """
        socket_name = '{}@kline_{}'.format(symbol.lower(), interval)
        return self._start_socket(socket_name, callback)

    def start_trade_socket(self, symbol, callback):
        """Start a websocket for symbol trade data

        :param symbol: required
        :type symbol: str
        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "aggTrade",		# event type
                "E": 1499405254326,		# event time
                "s": "ETHBTC",			# symbol
                "a": 70232,				# aggregated tradeid
                "p": "0.10281118",		# price
                "q": "8.15632997",		# quantity
                "f": 77489,				# first breakdown trade id
                "l": 77489,				# last breakdown trade id
                "T": 1499405254324,		# trade time
                "m": false,				# whether buyer is a maker
                "M": true				# can be ignored
            }

        """
        return self._start_socket(symbol.lower() + '@trade', callback)

    def start_ticker_socket(self, callback):
        """Start a websocket for ticker data

        By default all markets are included in an array.

        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            [
                {
                    'F': 278610,
                    'o': '0.07393000',
                    's': 'BCCBTC',
                    'C': 1509622420916,
                    'b': '0.07800800',
                    'l': '0.07160300',
                    'h': '0.08199900',
                    'L': 287722,
                    'P': '6.694',
                    'Q': '0.10000000',
                    'q': '1202.67106335',
                    'p': '0.00494900',
                    'O': 1509536020916,
                    'a': '0.07887800',
                    'n': 9113,
                    'B': '1.00000000',
                    'c': '0.07887900',
                    'x': '0.07399600',
                    'w': '0.07639068',
                    'A': '2.41900000',
                    'v': '15743.68900000'
                }
            ]
        """
        return self._start_socket('!ticker@arr', callback)

    def start_user_socket(self, callback):
        """Start a websocket for user data

        https://www.binance.com/restapipub.html#user-wss-endpoint

        :param callback: callback function to handle messages
        :type callback: function

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        if self._user_listen_key:
            # cleanup any sockets with this key
            for conn_key in self._conns:
                if len(conn_key) >= 60 and conn_key[:60] == self._user_listen_key:
                    self.stop_socket(conn_key)
                    break
        self._user_listen_key = self._client.stream_get_listen_key()
        conn_key = self._start_socket(self._user_listen_key, callback)
        if conn_key:
            # start timer to keep socket alive
            self._start_user_timer()

        return conn_key

    def _start_user_timer(self):
        self._user_timer = threading.Timer(self._user_timeout, self._keepalive_user_socket)
        self._user_timer.setDaemon(True)
        self._user_timer.start()

    def _keepalive_user_socket(self):
        self._client.stream_keepalive(listenKey=self._user_listen_key)
        self._start_user_timer()

    def stop_socket(self, conn_key):
        """Stop a websocket given the connection key

        :param conn_key: Socket connection key
        :type conn_key: string

        :returns: connection key string if successful, False otherwise
        """
        if conn_key not in self._conns:
            return

        self._conns[conn_key].disconnect()
        del(self._conns[conn_key])

        # check if we have a user stream socket
        if len(conn_key) >= 60 and conn_key[:60] == self._user_listen_key:
            self._stop_user_socket()

    def _stop_user_socket(self):
        if not self._user_listen_key:
            return
        # stop the timer
        self._user_timer.cancel()
        self._user_timer = None
        # close the stream
        self._client.stream_close(listenKey=self._user_listen_key)
        self._user_listen_key = None

    def run(self):
        try:
            reactor.run(installSignalHandlers=False)
        except ReactorAlreadyRunning:
            # Ignore error about reactor already running
            pass

    def close(self):
        """Stop the websocket manager and close connections

        """
        reactor.stop()

        self._stop_user_socket()
        self._conns = {}

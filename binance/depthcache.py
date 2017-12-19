#!/usr/bin/env python
# coding=utf-8

from operator import itemgetter

from .websockets import BinanceSocketManager


class DepthCache(object):

    def __init__(self, symbol):
        """Intialise the DepthCache

        :param symbol: Symbol to create depth cache for
        :type symbol: string

        """
        self.symbol = symbol
        self._bids = {}
        self._asks = {}

    def add_bid(self, bid):
        """Add a bid to the cache

        :param bid:
        :return:

        """
        self._bids[bid[0]] = float(bid[1])
        if bid[1] == "0.00000000":
            del self._bids[bid[0]]

    def add_ask(self, ask):
        """Add an ask to the cache

        :param ask:
        :return:

        """
        self._asks[ask[0]] = float(ask[1])
        if ask[1] == "0.00000000":
            del self._asks[ask[0]]

    def get_bids(self):
        """Get the current bids

        :return: list of bids with price and quantity as floats

        .. code-block:: python

            [
                [
                    0.0001946,  # Price
                    45.0        # Quantity
                ],
                [
                    0.00019459,
                    2384.0
                ],
                [
                    0.00019158,
                    5219.0
                ],
                [
                    0.00019157,
                    1180.0
                ],
                [
                    0.00019082,
                    287.0
                ]
            ]

        """
        return DepthCache.sort_depth(self._bids, reverse=True)

    def get_asks(self):
        """Get the current asks

        :return: list of asks with price and quantity as floats

        .. code-block:: python

            [
                [
                    0.0001955,  # Price
                    57.0'       # Quantity
                ],
                [
                    0.00019699,
                    778.0
                ],
                [
                    0.000197,
                    64.0
                ],
                [
                    0.00019709,
                    1130.0
                ],
                [
                    0.0001971,
                    385.0
                ]
            ]

        """
        return DepthCache.sort_depth(self._asks, reverse=False)

    @staticmethod
    def sort_depth(vals, reverse=False):
        """Sort bids or asks by price
        """
        lst = [[float(price), quantity] for price, quantity in vals.items()]
        lst = sorted(lst, key=itemgetter(0), reverse=reverse)
        return lst


class DepthCacheManager(object):

    def __init__(self, client, symbol, callback):
        """Intialise the DepthCacheManager

        :param client: Binance API client
        :type client: binance.Client
        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param callback: Function to receive depth cache updates
        :type callback: function

        """
        self._client = client
        self._symbol = symbol
        self._callback = callback
        self._first_update_id = 0
        self._bm = None
        self._depth_cache = DepthCache(self._symbol)

        self._init_cache()
        self._start_socket()

    def _init_cache(self):
        res = self._client.get_order_book(symbol=self._symbol, limit=500)

        self._first_update_id = res['lastUpdateId']

        for bid in res['bids']:
            self._depth_cache.add_bid(bid)
        for ask in res['asks']:
            self._depth_cache.add_ask(ask)

    def _start_socket(self):
        self._bm = BinanceSocketManager(self._client)

        self._bm.start_depth_socket(self._symbol, self._depth_event)

        self._bm.start()

    def _depth_event(self, msg):
        """

        :param msg:
        :return:

        """
        # ignore any updates before the initial update id
        if msg['u'] <= self._first_update_id:
            return

        # add any bid or ask values
        for bid in msg['b']:
            self._depth_cache.add_bid(bid)
        for ask in msg['a']:
            self._depth_cache.add_ask(ask)

        # call the callback with the updated depth cache
        self._callback(self._depth_cache)

    def get_depth_cache(self):
        """Get the current depth cache

        :return: DepthCache object

        """
        return self._depth_cache

    def close(self):
        """Close the open socket for this manager

        :return:
        """
        self._bm.close()

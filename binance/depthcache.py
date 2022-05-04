import logging
from operator import itemgetter
import asyncio
import time
from typing import Optional, Dict, Callable

from .streams import BinanceSocketManager
from .threaded_stream import ThreadedApiManager


class DepthCache(object):

    def __init__(self, symbol, conv_type=float):
        """Initialise the DepthCache

        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param conv_type: Optional type to represent price, and amount, default is float.
        :type conv_type: function.

        """
        self.symbol = symbol
        self._bids = {}
        self._asks = {}
        self.update_time = None
        self.conv_type = conv_type
        self._log = logging.getLogger(__name__)

    def add_bid(self, bid):
        """Add a bid to the cache

        :param bid:
        :return:

        """
        self._bids[bid[0]] = self.conv_type(bid[1])
        if bid[1] == "0.00000000":
            del self._bids[bid[0]]

    def add_ask(self, ask):
        """Add an ask to the cache

        :param ask:
        :return:

        """
        self._asks[ask[0]] = self.conv_type(ask[1])
        if ask[1] == "0.00000000":
            del self._asks[ask[0]]

    def get_bids(self):
        """Get the current bids

        :return: list of bids with price and quantity as conv_type

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
        return DepthCache.sort_depth(self._bids, reverse=True, conv_type=self.conv_type)

    def get_asks(self):
        """Get the current asks

        :return: list of asks with price and quantity as conv_type.

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
        return DepthCache.sort_depth(self._asks, reverse=False, conv_type=self.conv_type)

    @staticmethod
    def sort_depth(vals, reverse=False, conv_type=float):
        """Sort bids or asks by price
        """
        if isinstance(vals, dict):
            lst = [[conv_type(price), conv_type(quantity)] for price, quantity in vals.items()]
        elif isinstance(vals, list):
            lst = [[conv_type(price), conv_type(quantity)] for price, quantity in vals]
        else:
            raise ValueError(f'Unknown order book depth data type: {type(vals)}')
        lst = sorted(lst, key=itemgetter(0), reverse=reverse)
        return lst


class BaseDepthCacheManager:
    DEFAULT_REFRESH = 60 * 30  # 30 minutes
    TIMEOUT = 60

    def __init__(self, client, symbol, loop=None, refresh_interval=None, bm=None, limit=10, conv_type=float):
        """Create a DepthCacheManager instance

        :param client: Binance API client
        :type client: binance.Client
        :param loop:
        :type loop:
        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param refresh_interval: Optional number of seconds between cache refresh, use 0 or None to disable
        :type refresh_interval: int
        :param bm: Optional BinanceSocketManager
        :type bm: BinanceSocketManager
        :param limit: Optional number of orders to get from orderbook
        :type limit: int
        :param conv_type: Optional type to represent price, and amount, default is float.
        :type conv_type: function.

        """

        self._client = client
        self._depth_cache = None
        self._loop = loop or asyncio.get_event_loop()
        self._symbol = symbol
        self._limit = limit
        self._last_update_id = None
        self._bm = bm or BinanceSocketManager(self._client, self._loop)
        self._refresh_interval = refresh_interval or self.DEFAULT_REFRESH
        self._conn_key = None
        self._conv_type = conv_type
        self._log = logging.getLogger(__name__)

    async def __aenter__(self):
        await asyncio.gather(
            self._init_cache(),
            self._start_socket()
        )
        await self._socket.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._socket.__aexit__(*args, **kwargs)

    async def recv(self):
        dc = None
        while not dc:
            try:
                res = await asyncio.wait_for(self._socket.recv(), timeout=self.TIMEOUT)
            except Exception as e:
                self._log.warning(e)
            else:
                dc = await self._depth_event(res)
        return dc

    async def _init_cache(self):
        """Initialise the depth cache calling REST endpoint

        :return:
        """

        # initialise or clear depth cache
        self._depth_cache = DepthCache(self._symbol, conv_type=self._conv_type)

        # set a time to refresh the depth cache
        if self._refresh_interval:
            self._refresh_time = int(time.time()) + self._refresh_interval

    async def _start_socket(self):
        """Start the depth cache socket

        :return:
        """
        self._socket = self._get_socket()

    def _get_socket(self):
        raise NotImplementedError

    async def _depth_event(self, msg):
        """Handle a depth event

        :param msg:
        :return:

        """

        if not msg:
            return None

        if 'e' in msg and msg['e'] == 'error':
            # close the socket
            await self.close()

            # notify the user by returning a None value
            return None

        return await self._process_depth_message(msg)

    async def _process_depth_message(self, msg):
        """Process a depth event message.

        :param msg: Depth event message.
        :return:

        """

        # add any bid or ask values
        self._apply_orders(msg)

        # call the callback with the updated depth cache
        res = self._depth_cache

        # after processing event see if we need to refresh the depth cache
        if self._refresh_interval and int(time.time()) > self._refresh_time:
            await self._init_cache()

        return res

    def _apply_orders(self, msg):
        for bid in msg.get('b', []) + msg.get('bids', []):
            self._depth_cache.add_bid(bid)
        for ask in msg.get('a', []) + msg.get('asks', []):
            self._depth_cache.add_ask(ask)

        # keeping update time
        self._depth_cache.update_time = msg.get('E') or msg.get('lastUpdateId')

    def get_depth_cache(self):
        """Get the current depth cache

        :return: DepthCache object

        """
        return self._depth_cache

    async def close(self):
        """Close the open socket for this manager

        :return:
        """
        self._depth_cache = None

    def get_symbol(self):
        """Get the symbol

        :return: symbol
        """
        return self._symbol


class DepthCacheManager(BaseDepthCacheManager):

    def __init__(
        self, client, symbol, loop=None, refresh_interval=None, bm=None, limit=500, conv_type=float, ws_interval=None
    ):
        """Initialise the DepthCacheManager

        :param client: Binance API client
        :type client: binance.Client
        :param loop: asyncio loop
        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param refresh_interval: Optional number of seconds between cache refresh, use 0 or None to disable
        :type refresh_interval: int
        :param limit: Optional number of orders to get from orderbook
        :type limit: int
        :param conv_type: Optional type to represent price, and amount, default is float.
        :type conv_type: function.
        :param ws_interval: Optional interval for updates on websocket, default None. If not set, updates happen every second. Must be 0, None (1s) or 100 (100ms).
        :type ws_interval: int

        """
        super().__init__(client, symbol, loop, refresh_interval, bm, limit, conv_type)
        self._ws_interval = ws_interval

    async def _init_cache(self):
        """Initialise the depth cache calling REST endpoint

        :return:
        """
        self._last_update_id = None
        self._depth_message_buffer = []

        res = await self._client.get_order_book(symbol=self._symbol, limit=self._limit)

        # initialise or clear depth cache
        await super()._init_cache()

        # process bid and asks from the order book
        self._apply_orders(res)
        for bid in res['bids']:
            self._depth_cache.add_bid(bid)
        for ask in res['asks']:
            self._depth_cache.add_ask(ask)

        # set first update id
        self._last_update_id = res['lastUpdateId']

        # Apply any updates from the websocket
        for msg in self._depth_message_buffer:
            await self._process_depth_message(msg)

        # clear the depth buffer
        self._depth_message_buffer = []

    async def _start_socket(self):
        """Start the depth cache socket

        :return:
        """
        if not getattr(self, '_depth_message_buffer', None):
            self._depth_message_buffer = []

        await super()._start_socket()

    def _get_socket(self):
        return self._bm.depth_socket(self._symbol, interval=self._ws_interval)

    async def _process_depth_message(self, msg):
        """Process a depth event message.

        :param msg: Depth event message.
        :return:

        """

        if self._last_update_id is None:
            # Initial depth snapshot fetch not yet performed, buffer messages
            self._depth_message_buffer.append(msg)
            return

        if msg['u'] <= self._last_update_id:
            # ignore any updates before the initial update id
            return
        elif msg['U'] != self._last_update_id + 1:
            # if not buffered check we get sequential updates
            # otherwise init cache again
            await self._init_cache()

        # add any bid or ask values
        self._apply_orders(msg)

        # call the callback with the updated depth cache
        res = self._depth_cache

        self._last_update_id = msg['u']

        # after processing event see if we need to refresh the depth cache
        if self._refresh_interval and int(time.time()) > self._refresh_time:
            await self._init_cache()

        return res


class FuturesDepthCacheManager(BaseDepthCacheManager):
    async def _process_depth_message(self, msg):
        """Process a depth event message.

        :param msg: Depth event message.
        :return:

        """
        msg = msg.get('data')
        return await super()._process_depth_message(msg)

    def _apply_orders(self, msg):
        self._depth_cache._bids = msg.get('b', [])
        self._depth_cache._asks = msg.get('a', [])

        # keeping update time
        self._depth_cache.update_time = msg.get('E') or msg.get('lastUpdateId')

    def _get_socket(self):
        sock = self._bm.futures_depth_socket(self._symbol)
        return sock


class OptionsDepthCacheManager(BaseDepthCacheManager):

    def _get_socket(self):
        return self._bm.options_depth_socket(self._symbol)


class ThreadedDepthCacheManager(ThreadedApiManager):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Dict[str, str] = None, tld: str = 'com',
        testnet: bool = False
    ):
        super().__init__(api_key, api_secret, requests_params, tld, testnet)

    def _start_depth_cache(
        self, dcm_class, callback: Callable, symbol: str,
        refresh_interval=None, bm=None, limit=10, conv_type=float, **kwargs
    ) -> str:
        dcm = dcm_class(
            client=self._client,
            symbol=symbol,
            loop=self._loop,
            refresh_interval=refresh_interval,
            bm=bm,
            limit=limit,
            conv_type=conv_type,
            **kwargs
        )
        path = symbol.lower() + '@depth' + str(limit)
        self._socket_running[path] = True
        self._loop.call_soon(asyncio.create_task, self.start_listener(dcm, path, callback))
        return path

    def start_depth_cache(
        self, callback: Callable, symbol: str, refresh_interval=None, bm=None, limit=10, conv_type=float, ws_interval=0
    ) -> str:
        return self._start_depth_cache(
            dcm_class=DepthCacheManager,
            callback=callback,
            symbol=symbol,
            refresh_interval=refresh_interval,
            bm=bm,
            limit=limit,
            conv_type=conv_type,
            ws_interval=ws_interval
        )

    def start_futures_depth_socket(
            self, callback: Callable, symbol: str, refresh_interval=None, bm=None, limit=10, conv_type=float
    ) -> str:
        return self._start_depth_cache(
            dcm_class=FuturesDepthCacheManager,
            callback=callback,
            symbol=symbol,
            refresh_interval=refresh_interval,
            bm=bm,
            limit=limit,
            conv_type=conv_type
        )

    def start_options_depth_socket(
        self, callback: Callable, symbol: str, refresh_interval=None, bm=None, limit=10, conv_type=float
    ) -> str:
        return self._start_depth_cache(
            dcm_class=OptionsDepthCacheManager,
            callback=callback,
            symbol=symbol,
            refresh_interval=refresh_interval,
            bm=bm,
            limit=limit,
            conv_type=conv_type
        )

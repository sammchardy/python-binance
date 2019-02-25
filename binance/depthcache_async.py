

from .websockets_async import BinanceSocketManager
from .depthcache import DepthCache


class DepthCacheManager(object):

    _default_refresh = 60 * 30  # 30 minutes

    @classmethod
    async def create(cls, client, loop, symbol, coro=None, refresh_interval=_default_refresh):
        """Create a DepthCacheManager instance

        :param client: Binance API client
        :type client: binance.Client
        :param loop:
        :type loop:
        :param symbol: Symbol to create depth cache for
        :type symbol: string
        :param coro: Optional coroutine to receive depth cache updates
        :type coro: async coroutine
        :param refresh_interval: Optional number of seconds between cache refresh, use 0 or None to disable
        :type refresh_interval: int

        """
        self = DepthCacheManager()
        self._client = client
        self._loop = loop
        self._symbol = symbol
        self._coro = coro
        self._last_update_id = None
        self._depth_message_buffer = []
        self._bm = None
        self._depth_cache = DepthCache(self._symbol)
        self._refresh_interval = refresh_interval

        await self._start_socket()
        await self._init_cache()

        return self

    async def _init_cache(self):
        """Initialise the depth cache calling REST endpoint

        :return:
        """
        self._last_update_id = None
        self._depth_message_buffer = []

        res = await self._client.get_order_book(symbol=self._symbol, limit='500')

        # process bid and asks from the order book
        for bid in res['bids']:
            self._depth_cache.add_bid(bid)
        for ask in res['asks']:
            self._depth_cache.add_ask(ask)

        # set first update id
        self._last_update_id = res['lastUpdateId']

        # set a time to refresh the depth cache
        if self._refresh_interval:
            self._refresh_time = int(time.time()) + self._refresh_interval

        # Apply any updates from the websocket
        for msg in self._depth_message_buffer:
            await self._process_depth_message(msg, buffer=True)

        # clear the depth buffer
        del self._depth_message_buffer

    async def _start_socket(self):
        """Start the depth cache socket

        :return:
        """
        self._bm = BinanceSocketManager(self._client, self._loop)
        await self._bm.start_depth_socket(self._symbol, self._depth_event)

        # wait for some socket responses
        while not len(self._depth_message_buffer):
            await asyncio.sleep(1)

    async def _depth_event(self, msg):
        """Handle a depth event

        :param msg:
        :return:

        """

        if 'e' in msg and msg['e'] == 'error':
            # close the socket
            await self.close()

            # notify the user by returning a None value
            if self._callback:
                self._callback(None)

        if self._last_update_id is None:
            # Initial depth snapshot fetch not yet performed, buffer messages
            self._depth_message_buffer.append(msg)
        else:
            await self._process_depth_message(msg)

    async def _process_depth_message(self, msg, buffer=False):
        """Process a depth event message.

        :param msg: Depth event message.
        :return:

        """

        if buffer and msg['u'] <= self._last_update_id:
            # ignore any updates before the initial update id
            return
        elif msg['U'] != self._last_update_id + 1:
            # if not buffered check we get sequential updates
            # otherwise init cache again
            await self._init_cache()

        # add any bid or ask values
        for bid in msg['b']:
            self._depth_cache.add_bid(bid)
        for ask in msg['a']:
            self._depth_cache.add_ask(ask)

        # keeping update time
        self._depth_cache.update_time = msg['E']

        # call the callback with the updated depth cache
        if self._coro:
            await self._coro(self._depth_cache)

        self._last_update_id = msg['u']

        # after processing event see if we need to refresh the depth cache
        if self._refresh_interval and int(time.time()) > self._refresh_time:
            await self._init_cache()

    def get_depth_cache(self):
        """Get the current depth cache

        :return: DepthCache object

        """
        return self._depth_cache

    async def close(self):
        """Close the open socket for this manager

        :return:
        """
        await self._bm.close()
        self._depth_cache = None

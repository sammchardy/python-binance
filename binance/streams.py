import asyncio
import gzip
import json
import logging
import time
from asyncio import sleep
from enum import Enum
from random import random
from socket import gaierror
from typing import Optional, List, Dict, Callable, Any

import websockets as ws
from websockets.exceptions import ConnectionClosedError

from .client import AsyncClient
from .enums import FuturesType
from .exceptions import BinanceWebsocketUnableToConnect
from .enums import ContractType
from .helpers import get_loop
from .threaded_stream import ThreadedApiManager

KEEPALIVE_TIMEOUT = 5 * 60  # 5 minutes


class WSListenerState(Enum):
    INITIALISING = 'Initialising'
    STREAMING = 'Streaming'
    RECONNECTING = 'Reconnecting'
    EXITING = 'Exiting'


class BinanceSocketType(str, Enum):
    SPOT = 'Spot'
    USD_M_FUTURES = 'USD_M_Futures'
    COIN_M_FUTURES = 'Coin_M_Futures'
    OPTIONS = 'Vanilla_Options'
    ACCOUNT = 'Account'


class ReconnectingWebsocket:
    MAX_RECONNECTS = 5
    MAX_RECONNECT_SECONDS = 60
    MIN_RECONNECT_WAIT = 0.1
    TIMEOUT = 10
    NO_MESSAGE_RECONNECT_TIMEOUT = 60
    MAX_QUEUE_SIZE = 100

    def __init__(
        self, url: str, path: Optional[str] = None, prefix: str = 'ws/', is_binary: bool = False, exit_coro=None
    ):
        self._loop = get_loop()
        self._log = logging.getLogger(__name__)
        self._path = path
        self._url = url
        self._exit_coro = exit_coro
        self._prefix = prefix
        self._reconnects = 0
        self._is_binary = is_binary
        self._conn = None
        self._socket = None
        self.ws: Optional[ws.WebSocketClientProtocol] = None  # type: ignore
        self.ws_state = WSListenerState.INITIALISING
        self._queue = asyncio.Queue()
        self._handle_read_loop = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._exit_coro:
            await self._exit_coro(self._path)
        self.ws_state = WSListenerState.EXITING
        if self.ws:
            self.ws.fail_connection()
        if self._conn and hasattr(self._conn, 'protocol'):
            await self._conn.__aexit__(exc_type, exc_val, exc_tb)
        self.ws = None
        if not self._handle_read_loop:
            self._log.error("CANCEL read_loop")
            await self._kill_read_loop()

    async def connect(self):
        await self._before_connect()
        assert self._path
        ws_url = self._url + self._prefix + self._path
        self._conn = ws.connect(ws_url, close_timeout=0.1)  # type: ignore
        try:
            self.ws = await self._conn.__aenter__()
        except:  # noqa
            await self._reconnect()
            return
        self.ws_state = WSListenerState.STREAMING
        self._reconnects = 0
        await self._after_connect()
        # To manage the "cannot call recv while another coroutine is already waiting for the next message"
        if not self._handle_read_loop:
            self._handle_read_loop = self._loop.call_soon_threadsafe(asyncio.create_task, self._read_loop())

    async def _kill_read_loop(self):
        self.ws_state = WSListenerState.EXITING
        while self._handle_read_loop:
            await sleep(0.1)

    async def _before_connect(self):
        pass

    async def _after_connect(self):
        pass

    def _handle_message(self, evt):
        if self._is_binary:
            try:
                evt = gzip.decompress(evt)
            except (ValueError, OSError):
                return None
        try:
            return json.loads(evt)
        except ValueError:
            self._log.debug(f'error parsing evt json:{evt}')
            return None

    async def _read_loop(self):
        try:
            while True:
                try:
                    while self.ws_state == WSListenerState.RECONNECTING:
                        await self._run_reconnect()

                    if self.ws_state == WSListenerState.EXITING:
                        self._log.debug(f"_read_loop {self._path} break for {self.ws_state}")
                        break
                    elif self.ws.state == ws.protocol.State.CLOSING:  # type: ignore
                        await asyncio.sleep(0.1)
                        continue
                    elif self.ws.state == ws.protocol.State.CLOSED:  # type: ignore
                        await self._reconnect()
                    elif self.ws_state == WSListenerState.STREAMING:
                        assert self.ws
                        res = await asyncio.wait_for(self.ws.recv(), timeout=self.TIMEOUT)
                        res = self._handle_message(res)
                        if res:
                            if self._queue.qsize() < self.MAX_QUEUE_SIZE:
                                await self._queue.put(res)
                            else:
                                self._log.debug(f"Queue overflow {self.MAX_QUEUE_SIZE}. Message not filled")
                                await self._queue.put({
                                    'e': 'error',
                                    'm': 'Queue overflow. Message not filled'
                                })
                                raise BinanceWebsocketUnableToConnect
                except asyncio.TimeoutError:
                    self._log.debug(f"no message in {self.TIMEOUT} seconds")
                    # _no_message_received_reconnect
                except asyncio.CancelledError as e:
                    self._log.debug(f"cancelled error {e}")
                    break
                except asyncio.IncompleteReadError as e:
                    self._log.debug(f"incomplete read error ({e})")
                except ConnectionClosedError as e:
                    self._log.debug(f"connection close error ({e})")
                except gaierror as e:
                    self._log.debug(f"DNS Error ({e})")
                except BinanceWebsocketUnableToConnect as e:
                    self._log.debug(f"BinanceWebsocketUnableToConnect ({e})")
                    break
                except Exception as e:
                    self._log.debug(f"Unknown exception ({e})")
                    continue
        finally:
            self._handle_read_loop = None  # Signal the coro is stopped
            self._reconnects = 0

    async def _run_reconnect(self):
        await self.before_reconnect()
        if self._reconnects < self.MAX_RECONNECTS:
            reconnect_wait = self._get_reconnect_wait(self._reconnects)
            self._log.debug(
                f"websocket reconnecting. {self.MAX_RECONNECTS - self._reconnects} reconnects left - "
                f"waiting {reconnect_wait}"
            )
            await asyncio.sleep(reconnect_wait)
            await self.connect()
        else:
            self._log.error(f'Max reconnections {self.MAX_RECONNECTS} reached:')
            # Signal the error
            await self._queue.put({
                'e': 'error',
                'm': 'Max reconnect retries reached'
            })
            raise BinanceWebsocketUnableToConnect

    async def recv(self):
        res = None
        while not res:
            try:
                res = await asyncio.wait_for(self._queue.get(), timeout=self.TIMEOUT)
            except asyncio.TimeoutError:
                self._log.debug(f"no message in {self.TIMEOUT} seconds")
        return res

    async def _wait_for_reconnect(self):
        while self.ws_state != WSListenerState.STREAMING and self.ws_state != WSListenerState.EXITING:
            await sleep(0.1)

    def _get_reconnect_wait(self, attempts: int) -> int:
        expo = 2 ** attempts
        return round(random() * min(self.MAX_RECONNECT_SECONDS, expo - 1) + 1)

    async def before_reconnect(self):
        if self.ws and self._conn:
            await self._conn.__aexit__(None, None, None)
            self.ws = None
        self._reconnects += 1

    def _no_message_received_reconnect(self):
        self._log.debug('No message received, reconnecting')
        self.ws_state = WSListenerState.RECONNECTING

    async def _reconnect(self):
        self.ws_state = WSListenerState.RECONNECTING


class KeepAliveWebsocket(ReconnectingWebsocket):

    def __init__(
        self, client: AsyncClient, url, keepalive_type, prefix='ws/', is_binary=False, exit_coro=None,
        user_timeout=None
    ):
        super().__init__(path=None, url=url, prefix=prefix, is_binary=is_binary, exit_coro=exit_coro)
        self._keepalive_type = keepalive_type
        self._client = client
        self._user_timeout = user_timeout or KEEPALIVE_TIMEOUT
        self._timer = None

    async def __aexit__(self, *args, **kwargs):
        if not self._path:
            return
        if self._timer:
            self._timer.cancel()
            self._timer = None
        await super().__aexit__(*args, **kwargs)

    async def _before_connect(self):
        if not self._path:
            self._path = await self._get_listen_key()

    async def _after_connect(self):
        self._start_socket_timer()

    def _start_socket_timer(self):
        self._timer = self._loop.call_later(
            self._user_timeout,
            lambda: asyncio.create_task(self._keepalive_socket())
        )

    async def _get_listen_key(self):
        if self._keepalive_type == 'user':
            listen_key = await self._client.stream_get_listen_key()
        elif self._keepalive_type == 'margin':  # cross-margin
            listen_key = await self._client.margin_stream_get_listen_key()
        elif self._keepalive_type == 'futures':
            listen_key = await self._client.futures_stream_get_listen_key()
        elif self._keepalive_type == 'coin_futures':
            listen_key = await self._client.futures_coin_stream_get_listen_key()
        else:  # isolated margin
            # Passing symbol for isolated margin
            listen_key = await self._client.isolated_margin_stream_get_listen_key(self._keepalive_type)
        return listen_key

    async def _keepalive_socket(self):
        try:
            listen_key = await self._get_listen_key()
            if listen_key != self._path:
                self._log.debug("listen key changed: reconnect")
                self._path = listen_key
                await self._reconnect()
            else:
                self._log.debug("listen key same: keepalive")
                if self._keepalive_type == 'user':
                    await self._client.stream_keepalive(self._path)
                elif self._keepalive_type == 'margin':  # cross-margin
                    await self._client.margin_stream_keepalive(self._path)
                elif self._keepalive_type == 'futures':
                    await self._client.futures_stream_keepalive(self._path)
                elif self._keepalive_type == 'coin_futures':
                    await self._client.futures_coin_stream_keepalive(self._path)
                else:  # isolated margin
                    # Passing symbol for isolated margin
                    await self._client.isolated_margin_stream_keepalive(self._keepalive_type, self._path)
        except Exception:
            pass  # Ignore
        finally:
            self._start_socket_timer()


class BinanceSocketManager:
    STREAM_URL = 'wss://stream.binance.{}:9443/'
    STREAM_TESTNET_URL = 'wss://testnet.binance.vision/'
    FSTREAM_URL = 'wss://fstream.binance.{}/'
    FSTREAM_TESTNET_URL = 'wss://stream.binancefuture.com/'
    DSTREAM_URL = 'wss://dstream.binance.{}/'
    DSTREAM_TESTNET_URL = 'wss://dstream.binancefuture.com/'
    VSTREAM_URL = 'wss://vstream.binance.{}/'
    VSTREAM_TESTNET_URL = 'wss://testnetws.binanceops.{}/'

    WEBSOCKET_DEPTH_5 = '5'
    WEBSOCKET_DEPTH_10 = '10'
    WEBSOCKET_DEPTH_20 = '20'

    def __init__(self, client: AsyncClient, user_timeout=KEEPALIVE_TIMEOUT):
        """Initialise the BinanceSocketManager

        :param client: Binance API client
        :type client: binance.AsyncClient

        """
        self.STREAM_URL = self.STREAM_URL.format(client.tld)
        self.FSTREAM_URL = self.FSTREAM_URL.format(client.tld)
        self.DSTREAM_URL = self.DSTREAM_URL.format(client.tld)
        self.VSTREAM_URL = self.VSTREAM_URL.format(client.tld)
        self.VSTREAM_TESTNET_URL = self.VSTREAM_TESTNET_URL.format(client.tld)

        self._conns = {}
        self._loop = get_loop()
        self._client = client
        self._user_timeout = user_timeout

        self.testnet = self._client.testnet

    def _get_stream_url(self, stream_url: Optional[str] = None):
        if stream_url:
            return stream_url
        stream_url = self.STREAM_URL
        if self.testnet:
            stream_url = self.STREAM_TESTNET_URL
        return stream_url

    def _get_socket(
        self, path: str, stream_url: Optional[str] = None, prefix: str = 'ws/', is_binary: bool = False,
        socket_type: BinanceSocketType = BinanceSocketType.SPOT
    ) -> ReconnectingWebsocket:
        conn_id = f'{socket_type}_{path}'
        if conn_id not in self._conns:
            self._conns[conn_id] = ReconnectingWebsocket(
                path=path,
                url=self._get_stream_url(stream_url),
                prefix=prefix,
                exit_coro=lambda p: self._exit_socket(f'{socket_type}_{p}'),
                is_binary=is_binary,
            )

        return self._conns[conn_id]

    def _get_account_socket(
        self, path: str, stream_url: Optional[str] = None, prefix: str = 'ws/', is_binary: bool = False
    ):
        conn_id = f'{BinanceSocketType.ACCOUNT}_{path}'
        if conn_id not in self._conns:
            self._conns[conn_id] = KeepAliveWebsocket(
                client=self._client,
                url=self._get_stream_url(stream_url),
                keepalive_type=path,
                prefix=prefix,
                exit_coro=self._exit_socket,
                is_binary=is_binary,
                user_timeout=self._user_timeout
            )

        return self._conns[conn_id]

    def _get_futures_socket(self, path: str, futures_type: FuturesType, prefix: str = 'stream?streams='):
        socket_type: BinanceSocketType = BinanceSocketType.USD_M_FUTURES
        if futures_type == FuturesType.USD_M:
            stream_url = self.FSTREAM_URL
            if self.testnet:
                stream_url = self.FSTREAM_TESTNET_URL
        else:
            stream_url = self.DSTREAM_URL
            if self.testnet:
                stream_url = self.DSTREAM_TESTNET_URL
        return self._get_socket(path, stream_url, prefix, socket_type=socket_type)

    def _get_options_socket(self, path: str, prefix: str = 'ws/'):
        stream_url = self.VSTREAM_URL
        if self.testnet:
            stream_url = self.VSTREAM_TESTNET_URL
        return self._get_socket(path, stream_url, prefix, is_binary=True, socket_type=BinanceSocketType.OPTIONS)

    async def _exit_socket(self, path: str):
        await self._stop_socket(path)

    def depth_socket(self, symbol: str, depth: Optional[str] = None, interval: Optional[int] = None):
        """Start a websocket for symbol market depth returning either a diff or a partial book

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#partial-book-depth-streams

        :param symbol: required
        :type symbol: str
        :param depth: optional Number of depth entries to return, default None. If passed returns a partial book instead of a diff
        :type depth: str
        :param interval: optional interval for updates, default None. If not set, updates happen every second. Must be 0, None (1s) or 100 (100ms)
        :type interval: int

        :returns: connection key string if successful, False otherwise

        Partial Message Format

        .. code-block:: python

            {
                "lastUpdateId": 160,  # Last update ID
                "bids": [             # Bids to be updated
                    [
                        "0.0024",     # price level to be updated
                        "10",         # quantity
                        []            # ignore
                    ]
                ],
                "asks": [             # Asks to be updated
                    [
                        "0.0026",     # price level to be updated
                        "100",        # quantity
                        []            # ignore
                    ]
                ]
            }


        Diff Message Format

        .. code-block:: python

            {
                "e": "depthUpdate", # Event type
                "E": 123456789,     # Event time
                "s": "BNBBTC",      # Symbol
                "U": 157,           # First update ID in event
                "u": 160,           # Final update ID in event
                "b": [              # Bids to be updated
                    [
                        "0.0024",   # price level to be updated
                        "10",       # quantity
                        []          # ignore
                    ]
                ],
                "a": [              # Asks to be updated
                    [
                        "0.0026",   # price level to be updated
                        "100",      # quantity
                        []          # ignore
                    ]
                ]
            }

        """
        socket_name = symbol.lower() + '@depth'
        if depth and depth != '1':
            socket_name = f'{socket_name}{depth}'
        if interval:
            if interval in [0, 100]:
                socket_name = f'{socket_name}@{interval}ms'
            else:
                raise ValueError("Websocket interval value not allowed. Allowed values are [0, 100]")
        return self._get_socket(socket_name)

    def kline_socket(self, symbol: str, interval=AsyncClient.KLINE_INTERVAL_1MINUTE):
        """Start a websocket for symbol kline data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams

        :param symbol: required
        :type symbol: str
        :param interval: Kline interval, default KLINE_INTERVAL_1MINUTE
        :type interval: str

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
        path = f'{symbol.lower()}@kline_{interval}'
        return self._get_socket(path)

    def kline_futures_socket(self, symbol: str, interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                             futures_type: FuturesType = FuturesType.USD_M,
                             contract_type: ContractType = ContractType.PERPETUAL):
        """Start a websocket for symbol kline data for the perpeual futures stream

        https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-streams

        :param symbol: required
        :type symbol: str
        :param interval: Kline interval, default KLINE_INTERVAL_1MINUTE
        :type interval: str
        :param futures_type: use USD-M or COIN-M futures default USD-M
        :param contract_type: use PERPETUAL or CURRENT_QUARTER or NEXT_QUARTER default PERPETUAL

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

                {
                "e":"continuous_kline",   // Event type
                "E":1607443058651,        // Event time
                "ps":"BTCUSDT",           // Pair
                "ct":"PERPETUAL"          // Contract type
                "k":{
                    "t":1607443020000,      // Kline start time
                    "T":1607443079999,      // Kline close time
                    "i":"1m",               // Interval
                    "f":116467658886,       // First trade ID
                    "L":116468012423,       // Last trade ID
                    "o":"18787.00",         // Open price
                    "c":"18804.04",         // Close price
                    "h":"18804.04",         // High price
                    "l":"18786.54",         // Low price
                    "v":"197.664",          // volume
                    "n": 543,               // Number of trades
                    "x":false,              // Is this kline closed?
                    "q":"3715253.19494",    // Quote asset volume
                    "V":"184.769",          // Taker buy volume
                    "Q":"3472925.84746",    //Taker buy quote asset volume
                    "B":"0"                 // Ignore
                }
            }
            <pair>_<contractType>@continuousKline_<interval>
        """

        path = f'{symbol.lower()}_{contract_type.value}@continuousKline_{interval}'
        return self._get_futures_socket(path, prefix='ws/', futures_type=futures_type)

    def miniticker_socket(self, update_time: int = 1000):
        """Start a miniticker websocket for all trades

        This is not in the official Binance api docs, but this is what
        feeds the right column on a ticker page on Binance.

        :param update_time: time between callbacks in milliseconds, must be 1000 or greater
        :type update_time: int

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            [
                {
                    'e': '24hrMiniTicker',  # Event type
                    'E': 1515906156273,     # Event time
                    's': 'QTUMETH',         # Symbol
                    'c': '0.03836900',      # close
                    'o': '0.03953500',      # open
                    'h': '0.04400000',      # high
                    'l': '0.03756000',      # low
                    'v': '147435.80000000', # volume
                    'q': '5903.84338533'    # quote volume
                }
            ]
        """

        return self._get_socket(f'!miniTicker@arr@{update_time}ms')

    def trade_socket(self, symbol: str):
        """Start a websocket for symbol trade data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#trade-streams

        :param symbol: required
        :type symbol: str

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "trade",     # Event type
                "E": 123456789,   # Event time
                "s": "BNBBTC",    # Symbol
                "t": 12345,       # Trade ID
                "p": "0.001",     # Price
                "q": "100",       # Quantity
                "b": 88,          # Buyer order Id
                "a": 50,          # Seller order Id
                "T": 123456785,   # Trade time
                "m": true,        # Is the buyer the market maker?
                "M": true         # Ignore.
            }

        """

        return self._get_socket(symbol.lower() + '@trade')

    def aggtrade_socket(self, symbol: str):
        """Start a websocket for symbol trade data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#aggregate-trade-streams

        :param symbol: required
        :type symbol: str

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
        return self._get_socket(symbol.lower() + '@aggTrade')

    def aggtrade_futures_socket(self, symbol: str, futures_type: FuturesType = FuturesType.USD_M):
        """Start a websocket for aggregate symbol trade data for the futures stream

        :param symbol: required
        :param futures_type: use USD-M or COIN-M futures default USD-M

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "aggTrade",  // Event type
                "E": 123456789,   // Event time
                "s": "BTCUSDT",    // Symbol
                "a": 5933014,     // Aggregate trade ID
                "p": "0.001",     // Price
                "q": "100",       // Quantity
                "f": 100,         // First trade ID
                "l": 105,         // Last trade ID
                "T": 123456785,   // Trade time
                "m": true,        // Is the buyer the market maker?
            }

        """
        return self._get_futures_socket(symbol.lower() + '@aggTrade', futures_type=futures_type)

    def symbol_miniticker_socket(self, symbol: str):
        """Start a websocket for a symbol's miniTicker data

                https://binance-docs.github.io/apidocs/spot/en/#individual-symbol-mini-ticker-stream

                :param symbol: required
                :type symbol: str

                :returns: connection key string if successful, False otherwise

                Message Format

                .. code-block:: python

                    {
                        "e": "24hrMiniTicker",  // Event type
                        "E": 123456789,         // Event time
                        "s": "BNBBTC",          // Symbol
                        "c": "0.0025",          // Close price
                        "o": "0.0010",          // Open price
                        "h": "0.0025",          // High price
                        "l": "0.0010",          // Low price
                        "v": "10000",           // Total traded base asset volume
                        "q": "18"               // Total traded quote asset volume
                    }

                """
        return self._get_socket(symbol.lower() + '@miniTicker')

    def symbol_ticker_socket(self, symbol: str):
        """Start a websocket for a symbol's ticker data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#individual-symbol-ticker-streams

        :param symbol: required
        :type symbol: str

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "e": "24hrTicker",  # Event type
                "E": 123456789,     # Event time
                "s": "BNBBTC",      # Symbol
                "p": "0.0015",      # Price change
                "P": "250.00",      # Price change percent
                "w": "0.0018",      # Weighted average price
                "x": "0.0009",      # Previous day's close price
                "c": "0.0025",      # Current day's close price
                "Q": "10",          # Close trade's quantity
                "b": "0.0024",      # Best bid price
                "B": "10",          # Bid bid quantity
                "a": "0.0026",      # Best ask price
                "A": "100",         # Best ask quantity
                "o": "0.0010",      # Open price
                "h": "0.0025",      # High price
                "l": "0.0010",      # Low price
                "v": "10000",       # Total traded base asset volume
                "q": "18",          # Total traded quote asset volume
                "O": 0,             # Statistics open time
                "C": 86400000,      # Statistics close time
                "F": 0,             # First trade ID
                "L": 18150,         # Last trade Id
                "n": 18151          # Total number of trades
            }

        """
        return self._get_socket(symbol.lower() + '@ticker')

    def ticker_socket(self):
        """Start a websocket for all ticker data

        By default all markets are included in an array.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#all-market-tickers-stream

        :param coro: callback function to handle messages
        :type coro: function

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
        return self._get_socket('!ticker@arr')

    def index_price_socket(self, symbol: str, fast: bool = True):
        """Start a websocket for a symbol's futures mark price
        https://binance-docs.github.io/apidocs/delivery/en/#index-price-stream
        :param symbol: required
        :param fast: use faster or 1s default
        :returns: connection key string if successful, False otherwise

        Message Format
        .. code-block:: python
            {
                "e": "indexPriceUpdate",  // Event type
                "E": 1591261236000,       // Event time
                "i": "BTCUSD",            // Pair
                "p": "9636.57860000",     // Index Price
              }
        """
        stream_name = '@indexPrice@1s' if fast else '@indexPrice'
        return self._get_futures_socket(symbol.lower() + stream_name, futures_type=FuturesType.COIN_M)

    def futures_depth_socket(self, symbol: str, depth: str = '10', futures_type=FuturesType.USD_M):
        """Subscribe to a futures depth data stream

        https://binance-docs.github.io/apidocs/futures/en/#partial-book-depth-streams

        :param symbol: required
        :type symbol: str
        :param depth: optional Number of depth entries to return, default 10.
        :type depth: str
        :param futures_type: use USD-M or COIN-M futures default USD-M
        """
        return self._get_futures_socket(symbol.lower() + '@depth' + str(depth), futures_type=futures_type)

    def symbol_mark_price_socket(self, symbol: str, fast: bool = True, futures_type: FuturesType = FuturesType.USD_M):
        """Start a websocket for a symbol's futures mark price
        https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream
        :param symbol: required
        :param fast: use faster or 1s default
        :param futures_type: use USD-M or COIN-M futures default USD-M
        :returns: connection key string if successful, False otherwise
        Message Format
        .. code-block:: python
            {
                "e": "markPriceUpdate",  // Event type
                "E": 1562305380000,      // Event time
                "s": "BTCUSDT",          // Symbol
                "p": "11185.87786614",   // Mark price
                "r": "0.00030000",       // Funding rate
                "T": 1562306400000       // Next funding time
            }
        """
        stream_name = '@markPrice@1s' if fast else '@markPrice'
        return self._get_futures_socket(symbol.lower() + stream_name, futures_type=futures_type)

    def all_mark_price_socket(self, fast: bool = True, futures_type: FuturesType = FuturesType.USD_M):
        """Start a websocket for all futures mark price data
        By default all symbols are included in an array.
        https://binance-docs.github.io/apidocs/futures/en/#mark-price-stream-for-all-market
        :param fast: use faster or 1s default
        :param futures_type: use USD-M or COIN-M futures default USD-M
        :returns: connection key string if successful, False otherwise
        Message Format
        .. code-block:: python

            [
                {
                    "e": "markPriceUpdate",  // Event type
                    "E": 1562305380000,      // Event time
                    "s": "BTCUSDT",          // Symbol
                    "p": "11185.87786614",   // Mark price
                    "r": "0.00030000",       // Funding rate
                    "T": 1562306400000       // Next funding time
                }
            ]
        """
        stream_name = '!markPrice@arr@1s' if fast else '!markPrice@arr'
        return self._get_futures_socket(stream_name, futures_type=futures_type)

    def symbol_ticker_futures_socket(self, symbol: str, futures_type: FuturesType = FuturesType.USD_M):
        """Start a websocket for a symbol's ticker data
        By default all markets are included in an array.
        https://binance-docs.github.io/apidocs/futures/en/#individual-symbol-book-ticker-streams
        :param symbol: required
        :param futures_type: use USD-M or COIN-M futures default USD-M
        :returns: connection key string if successful, False otherwise
        .. code-block:: python
            [
                {
                  "u":400900217,     // order book updateId
                  "s":"BNBUSDT",     // symbol
                  "b":"25.35190000", // best bid price
                  "B":"31.21000000", // best bid qty
                  "a":"25.36520000", // best ask price
                  "A":"40.66000000"  // best ask qty
                }
            ]
        """
        return self._get_futures_socket(symbol.lower() + '@bookTicker', futures_type=futures_type)

    def individual_symbol_ticker_futures_socket(self, symbol: str, futures_type: FuturesType = FuturesType.USD_M):
        """Start a futures websocket for a single symbol's ticker data
        https://binance-docs.github.io/apidocs/futures/en/#individual-symbol-ticker-streams
        :param symbol: required
        :type symbol: str
        :param futures_type: use USD-M or COIN-M futures default USD-M
        :returns: connection key string if successful, False otherwise
        .. code-block:: python
            {
                "e": "24hrTicker",  // Event type
                "E": 123456789,     // Event time
                "s": "BTCUSDT",     // Symbol
                "p": "0.0015",      // Price change
            }
        """
        return self._get_futures_socket(symbol.lower() + '@ticker', futures_type=futures_type)

    def all_ticker_futures_socket(self, futures_type: FuturesType = FuturesType.USD_M):
        """Start a websocket for all ticker data
        By default all markets are included in an array.
        https://binance-docs.github.io/apidocs/futures/en/#all-book-tickers-stream
        :param futures_type: use USD-M or COIN-M futures default USD-M
        :returns: connection key string if successful, False otherwise
        Message Format
        .. code-block:: python
            [
                {
                  "u":400900217,     // order book updateId
                  "s":"BNBUSDT",     // symbol
                  "b":"25.35190000", // best bid price
                  "B":"31.21000000", // best bid qty
                  "a":"25.36520000", // best ask price
                  "A":"40.66000000"  // best ask qty
                }
            ]
        """

        return self._get_futures_socket('!bookTicker', futures_type=futures_type)

    def symbol_book_ticker_socket(self, symbol: str):
        """Start a websocket for the best bid or ask's price or quantity for a specified symbol.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#individual-symbol-book-ticker-streams

        :param symbol: required
        :type symbol: str

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                "u":400900217,     // order book updateId
                "s":"BNBUSDT",     // symbol
                "b":"25.35190000", // best bid price
                "B":"31.21000000", // best bid qty
                "a":"25.36520000", // best ask price
                "A":"40.66000000"  // best ask qty
            }

        """
        return self._get_socket(symbol.lower() + '@bookTicker')

    def book_ticker_socket(self):
        """Start a websocket for the best bid or ask's price or quantity for all symbols.

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#all-book-tickers-stream

        :returns: connection key string if successful, False otherwise

        Message Format

        .. code-block:: python

            {
                // Same as <symbol>@bookTicker payload
            }

        """
        return self._get_socket('!bookTicker')

    def multiplex_socket(self, streams: List[str]):
        """Start a multiplexed socket using a list of socket names.
        User stream sockets can not be included.

        Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

        Combined stream events are wrapped as follows: {"stream":"<streamName>","data":<rawPayload>}

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md

        :param streams: list of stream names in lower case
        :type streams: list

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types

        """
        path = f'streams={"/".join(streams)}'
        return self._get_socket(path, prefix='stream?')

    def options_multiplex_socket(self, streams: List[str]):
        """Start a multiplexed socket using a list of socket names.
        User stream sockets can not be included.

        Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

        Combined stream events are wrapped as follows: {"stream":"<streamName>","data":<rawPayload>}

        https://binance-docs.github.io/apidocs/voptions/en/#account-and-trading-interface

        :param streams: list of stream names in lower case
        :type streams: list

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types

        """
        stream_name = '/'.join([s.lower() for s in streams])
        stream_path = f'streams={stream_name}'
        return self._get_options_socket(stream_path, prefix='stream?')

    def futures_multiplex_socket(self, streams: List[str], futures_type: FuturesType = FuturesType.USD_M):
        """Start a multiplexed socket using a list of socket names.
        User stream sockets can not be included.

        Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

        Combined stream events are wrapped as follows: {"stream":"<streamName>","data":<rawPayload>}

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md

        :param streams: list of stream names in lower case
        :param futures_type: use USD-M or COIN-M futures default USD-M

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types

        """
        path = f'streams={"/".join(streams)}'
        return self._get_futures_socket(path, prefix='stream?', futures_type=futures_type)

    def user_socket(self):
        """Start a websocket for user data

        https://github.com/binance-exchange/binance-official-api-docs/blob/master/user-data-stream.md
        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        stream_url = self.STREAM_URL
        if self.testnet:
            stream_url = self.STREAM_TESTNET_URL
        return self._get_account_socket('user', stream_url=stream_url)

    def futures_user_socket(self):
        """Start a websocket for coin futures user data

        https://binance-docs.github.io/apidocs/futures/en/#user-data-streams

        :returns: connection key string if successful, False otherwise

        Message Format - see Binanace API docs for all types
        """

        stream_url = self.FSTREAM_URL
        if self.testnet:
            stream_url = self.FSTREAM_TESTNET_URL
        return self._get_account_socket('futures', stream_url=stream_url)

    def margin_socket(self):
        """Start a websocket for cross-margin data

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        stream_url = self.STREAM_URL
        if self.testnet:
            stream_url = self.STREAM_TESTNET_URL
        return self._get_account_socket('margin', stream_url=stream_url)

    def futures_socket(self):
        """Start a websocket for futures data

            https://binance-docs.github.io/apidocs/futures/en/#websocket-market-streams

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        stream_url = self.FSTREAM_URL
        if self.testnet:
            stream_url = self.FSTREAM_TESTNET_URL
        return self._get_account_socket('futures', stream_url=stream_url)

    def coin_futures_socket(self):
        """Start a websocket for coin futures data

            https://binance-docs.github.io/apidocs/delivery/en/#websocket-market-streams

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        stream_url = self.DSTREAM_URL
        if self.testnet:
            stream_url = self.DSTREAM_TESTNET_URL
        return self._get_account_socket('coin_futures', stream_url=stream_url)

    def isolated_margin_socket(self, symbol: str):
        """Start a websocket for isolated margin data

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str

        :returns: connection key string if successful, False otherwise

        Message Format - see Binance API docs for all types
        """
        stream_url = self.STREAM_URL
        if self.testnet:
            stream_url = self.STREAM_TESTNET_URL
        return self._get_account_socket(symbol, stream_url=stream_url)

    def options_ticker_socket(self, symbol: str):
        """Subscribe to a 24 hour ticker info stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-24-hour-ticker

        :param symbol: required
        :type symbol: str
        """
        return self._get_options_socket(symbol.lower() + '@ticker')

    def options_ticker_by_expiration_socket(self, symbol: str, expiration_date: str):
        """Subscribe to a 24 hour ticker info stream
        https://binance-docs.github.io/apidocs/voptions/en/#24-hour-ticker-by-underlying-asset-and-expiration-data
        :param symbol: required
        :type symbol: str
        :param expiration_date : required
        :type expiration_date: str
        """
        return self._get_options_socket(symbol.lower() + '@ticker@' + expiration_date)

    def options_recent_trades_socket(self, symbol: str):
        """Subscribe to a latest completed trades stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-latest-completed-trades

        :param symbol: required
        :type symbol: str
        """
        return self._get_options_socket(symbol.lower() + '@trade')

    def options_kline_socket(self, symbol: str, interval=AsyncClient.KLINE_INTERVAL_1MINUTE):
        """Subscribe to a candlestick data stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-candle

        :param symbol: required
        :type symbol: str
        :param interval: Kline interval, default KLINE_INTERVAL_1MINUTE
        :type interval: str
        """
        return self._get_options_socket(symbol.lower() + '@kline_' + interval)

    def options_depth_socket(self, symbol: str, depth: str = '10'):
        """Subscribe to a depth data stream

        https://binance-docs.github.io/apidocs/voptions/en/#market-streams-payload-depth

        :param symbol: required
        :type symbol: str
        :param depth: optional Number of depth entries to return, default 10.
        :type depth: str
        """
        return self._get_options_socket(symbol.lower() + '@depth' + str(depth))

    async def _stop_socket(self, conn_key):
        """Stop a websocket given the connection key

        :param conn_key: Socket connection key
        :type conn_key: string

        :returns: None
        """
        if conn_key not in self._conns:
            return

        del (self._conns[conn_key])


class ThreadedWebsocketManager(ThreadedApiManager):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com',
        testnet: bool = False, session_params: Optional[Dict[str, Any]] = None
    ):
        super().__init__(api_key, api_secret, requests_params, tld, testnet, session_params)
        self._bsm: Optional[BinanceSocketManager] = None

    async def _before_socket_listener_start(self):
        assert self._client
        self._bsm = BinanceSocketManager(client=self._client)

    def _start_async_socket(
        self, callback: Callable, socket_name: str, params: Dict[str, Any], path: Optional[str] = None
    ) -> str:
        while not self._bsm:
            time.sleep(0.1)
        socket = getattr(self._bsm, socket_name)(**params)
        socket_path: str = path or socket._path  # noqa
        self._socket_running[socket_path] = True
        self._loop.call_soon_threadsafe(asyncio.create_task, self.start_listener(socket, socket_path, callback))
        return socket_path

    def start_depth_socket(
        self, callback: Callable, symbol: str, depth: Optional[str] = None, interval: Optional[int] = None
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='depth_socket',
            params={
                'symbol': symbol,
                'depth': depth,
                'interval': interval,
            }
        )

    def start_kline_socket(self, callback: Callable, symbol: str, interval=AsyncClient.KLINE_INTERVAL_1MINUTE) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='kline_socket',
            params={
                'symbol': symbol,
                'interval': interval,
            }
        )

    def start_kline_futures_socket(self, callback: Callable, symbol: str,
                                   interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                                   futures_type: FuturesType = FuturesType.USD_M,
                                   contract_type: ContractType = ContractType.PERPETUAL) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='kline_futures_socket',
            params={
                'symbol': symbol,
                'interval': interval,
                'futures_type': futures_type,
                'contract_type': contract_type
            }
        )

    def start_miniticker_socket(self, callback: Callable, update_time: int = 1000) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='miniticker_socket',
            params={
                'update_time': update_time,
            }
        )

    def start_trade_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='trade_socket',
            params={
                'symbol': symbol,
            }
        )

    def start_aggtrade_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='aggtrade_socket',
            params={
                'symbol': symbol,
            }
        )

    def start_aggtrade_futures_socket(
        self, callback: Callable, symbol: str, futures_type: FuturesType = FuturesType.USD_M
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='aggtrade_futures_socket',
            params={
                'symbol': symbol,
                'futures_type': futures_type,
            }
        )

    def start_symbol_miniticker_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='symbol_miniticker_socket',
            params={
                'symbol': symbol,
            }
        )

    def start_symbol_ticker_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='symbol_ticker_socket',
            params={
                'symbol': symbol,
            }
        )

    def start_ticker_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='ticker_socket',
            params={}
        )

    def start_index_price_socket(self, callback: Callable, symbol: str, fast: bool = True) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='index_price_socket',
            params={
                'symbol': symbol,
                'fast': fast
            }
        )

    def start_symbol_mark_price_socket(
        self, callback: Callable, symbol: str, fast: bool = True, futures_type: FuturesType = FuturesType.USD_M
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='symbol_mark_price_socket',
            params={
                'symbol': symbol,
                'fast': fast,
                'futures_type': futures_type
            }
        )

    def start_all_mark_price_socket(
        self, callback: Callable, fast: bool = True, futures_type: FuturesType = FuturesType.USD_M
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='all_mark_price_socket',
            params={
                'fast': fast,
                'futures_type': futures_type
            }
        )

    def start_symbol_ticker_futures_socket(
        self, callback: Callable, symbol: str, futures_type: FuturesType = FuturesType.USD_M
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='symbol_ticker_futures_socket',
            params={
                'symbol': symbol,
                'futures_type': futures_type
            }
        )

    def start_individual_symbol_ticker_futures_socket(
        self, callback: Callable, symbol: str, futures_type: FuturesType = FuturesType.USD_M
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='individual_symbol_ticker_futures_socket',
            params={
                'symbol': symbol,
                'futures_type': futures_type
            }
        )

    def start_all_ticker_futures_socket(self, callback: Callable, futures_type: FuturesType = FuturesType.USD_M) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='all_ticker_futures_socket',
            params={
                'futures_type': futures_type
            }
        )

    def start_symbol_book_ticker_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='symbol_book_ticker_socket',
            params={
                'symbol': symbol
            }
        )

    def start_book_ticker_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='book_ticker_socket',
            params={}
        )

    def start_multiplex_socket(self, callback: Callable, streams: List[str]) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='multiplex_socket',
            params={
                'streams': streams
            }
        )

    def start_options_multiplex_socket(self, callback: Callable, streams: List[str]) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='options_multiplex_socket',
            params={
                'streams': streams
            }
        )

    def start_futures_multiplex_socket(
        self, callback: Callable, streams: List[str], futures_type: FuturesType = FuturesType.USD_M
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='futures_multiplex_socket',
            params={
                'streams': streams,
                'futures_type': futures_type
            }
        )

    def start_user_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='user_socket',
            params={}
        )

    def start_futures_user_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='futures_user_socket',
            params={}
        )

    def start_margin_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='margin_socket',
            params={}
        )

    def start_futures_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='futures_socket',
            params={}
        )

    def start_coin_futures_socket(self, callback: Callable) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='coin_futures_socket',
            params={}
        )

    def start_isolated_margin_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='isolated_margin_socket',
            params={
                'symbol': symbol
            }
        )

    def start_options_ticker_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='options_ticker_socket',
            params={
                'symbol': symbol
            }
        )

    def start_options_ticker_by_expiration_socket(self, callback: Callable, symbol: str, expiration_date: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='options_ticker_by_expiration_socket',
            params={
                'symbol': symbol,
                'expiration_date': expiration_date
            }
        )

    def start_options_recent_trades_socket(self, callback: Callable, symbol: str) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='options_recent_trades_socket',
            params={
                'symbol': symbol
            }
        )

    def start_options_kline_socket(
        self, callback: Callable, symbol: str, interval=AsyncClient.KLINE_INTERVAL_1MINUTE
    ) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='options_kline_socket',
            params={
                'symbol': symbol,
                'interval': interval
            }
        )

    def start_options_depth_socket(self, callback: Callable, symbol: str, depth: str = '10') -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='options_depth_socket',
            params={
                'symbol': symbol,
                'depth': depth
            }
        )

    def start_futures_depth_socket(self, callback: Callable, symbol: str, depth: str = '10', futures_type=FuturesType.USD_M) -> str:
        return self._start_async_socket(
            callback=callback,
            socket_name='futures_depth_socket',
            params={
                'symbol': symbol,
                'depth': depth,
                'futures_type': futures_type
            }
        )

Websockets
==========

There are 2 ways to interact with websockets.

with `ThreadedWebsocketManager <binance.html#binance.websockets.ThreadedWebsocketManager>`_ or `BinanceSocketManager <binance.html#binance.websockets.BinanceSocketManager>`_.

ThreadedWebsocketManager does not require asyncio programming, while BinanceSocketManager does.

ThreadedWebsocketManager function begin with `start_`, e.g `start_ticker_socket` while BinanceSocketManager is simply `ticker_socket`.

Multiple socket connections can be made through either manager.

Only one instance of each socket type will be created, i.e. only one BNBBTC Depth socket can be created
and there can be both a BNBBTC Depth and a BNBBTC Trade socket open at once.

Messages are received as dictionary objects relating to the message formats defined in the `Binance WebSocket API documentation <https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams>`_.

Websockets are setup to reconnect with a maximum of 5 retries with an exponential backoff strategy.

ThreadedWebsocketManager Websocket Usage
----------------------------------------

Starting sockets on the ThreadedWebsocketManager requires a callback parameter, similar to the old implementations of websockets on python-binance.

ThreadedWebsocketManager takes similar parameters to the `Client <binance.html#binance.client.Client>`_ class as it
creates an AsyncClient internally.

For authenticated streams `api_key` and `api_stream` are required.

As these use threads `start()` is required to be called before starting any sockets.

To keep the ThreadedWebsocketManager running, use `join()` to join it to the main thread.

.. code:: python

    import time

    from binance import ThreadedWebsocketManager

    api_key = '<api_key>'
    api_secret = '<api_secret>'

    def main():

        symbol = 'BNBBTC'

        twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        # start is required to initialise its internal loop
        twm.start()

        def handle_socket_message(msg):
            print(f"message type: {msg['e']}")
            print(msg)

        twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

        # multiple sockets can be started
        twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

        # or a multiplex socket can be started like this
        # see Binance docs for stream names
        streams = ['bnbbtc@miniTicker', 'bnbbtc@bookTicker']
        twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

        twm.join()


    if __name__ == "__main__":
       main()

**Stop Individual Stream**

When starting a stream, a name for that stream will be returned. This can be used to stop that individual stream.

.. code:: python

    from binance import ThreadedWebsocketManager

    symbol = 'BNBBTC'

    twm = ThreadedWebsocketManager()
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

        twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
    depth_stream_name = twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    # some time later

    twm.stop_socket(depth_stream_name)

**Stop All Streams**

.. code:: python

    from binance import ThreadedWebsocketManager

    twm = ThreadedWebsocketManager()
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    depth_stream_name = twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)

    twm.stop()

Attempting to start a stream after `stop` is called will not work.


BinanceSocketManager Websocket Usage
------------------------------------

Create the manager like so, passing an AsyncClient.

.. code:: python

    import asyncio
    from binance import AsyncClient, BinanceSocketManager


    async def main():
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        # start any sockets here, i.e a trade socket
        ts = bm.trade_socket('BNBBTC')
        # then start receiving messages
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                print(res)

        await client.close_connection()

    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

Set a custom timeout for the websocket connections

.. code:: python

    # set a timeout of 60 seconds
    bm = BinanceSocketManager(client, user_timeout=60)

Manually enter and exit the Asynchronous context manager

.. code:: python

    ts = bm.trade_socket('BNBBTC')
    # enter the context manager
    await ts.__aenter__()
    # receive a message
    msg = await ts.recv()
    print(msg)
    # exit the context manager
    await ts.__aexit__(None, None, None)


Using a different TLD
---------------------

The ThreadedWebsocketManager can take the tld when created if required.

.. code:: python

    from binance.streams import ThreadedWebsocketManager

    twm = ThreadedWebsocketManager(tld='us')

The BinanceSocketManager uses the same tld value as the AsyncClient that is passed in. To use the 'us' tld we
can do this.

.. code:: python

    from binance import AsyncClient, BinanceSocketManager

    async def x():
        client = await AsyncClient.create(tld='us')
        bm = BinanceSocketManager(client)

        # start a socket...

        await client.close_connection()


Websocket Errors
----------------

If the websocket is disconnected and is unable to reconnect, a message is sent to the callback to indicate this. The format is

.. code:: python

    {
        'e': 'error',
        'm': 'Max reconnect retries reached'
    }

    # check for it like so
    def process_message(msg):
        if msg['e'] == 'error':
            # close and restart the socket
        else:
            # process message normally


`Multiplex Socket <binance.html#binance.websockets.BinanceSocketManager.multiplex_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Create a socket combining multiple streams.

These streams can include the depth, kline, ticker and trade streams but not the user stream which requires extra authentication.

Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

See the `Binance Websocket Streams API documentation <https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams>`_ for details on socket names.

.. code:: python

    # pass a list of stream names
    ms = bm.multiplex_socket(['bnbbtc@aggTrade', 'neobtc@ticker'])

`Depth Socket <binance.html#binance.websockets.BinanceSocketManager.depth_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Depth sockets have an optional depth parameter to receive partial book rather than a diff response.
By default this the diff response is returned.
Valid depth values are 5, 10 and 20 and `defined as enums <enums.html>`_.

.. code:: python

    # depth diff response
    ds = bm.depth_socket('BNBBTC')

    # partial book response
    ds = bm.depth_socket('BNBBTC', depth=BinanceSocketManager.WEBSOCKET_DEPTH_5)


`Kline Socket <binance.html#binance.websockets.BinanceSocketManager.kline_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Kline sockets have an optional interval parameter. By default this is set to 1 minute.
Valid interval values are `defined as enums <enums.html>`_.

.. code:: python

    from binance.enums import *
    ks = bm.kline_socket('BNBBTC', interval=KLINE_INTERVAL_30MINUTE)


`Aggregated Trade Socket <binance.html#binance.websockets.BinanceSocketManager.aggtrade_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    ats = bm.aggtrade_socket('BNBBTC')


`Trade Socket <binance.html#binance.websockets.BinanceSocketManager.trade_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    ts = bm.trade_socket('BNBBTC')

`Symbol Ticker Socket <binance.html#binance.websockets.BinanceSocketManager.symbol_ticker_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    sts = bm.symbol_ticker_socket('BNBBTC')

`Ticker Socket <binance.html#binance.websockets.BinanceSocketManager.ticker_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    ts = bm.ticker_socket(process_message)

`Mini Ticker Socket <binance.html#binance.websockets.BinanceSocketManager.miniticker_socket>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    # by default updates every second
    mts = bm.miniticker_socket()

    # this socket can take an update interval parameter
    # set as 5000 to receive updates every 5 seconds
    mts = bm.miniticker_socket(5000)

User Socket
+++++++++++

This watches for 3 different user events

- Account Update Event
- Order Update Event
- Trade Update Event

The Manager handles keeping the socket alive.

There are separate sockets for Spot, Cross-margin and separate Isolated margin accounts.

`Spot trading <binance.html#binance.websockets.BinanceSocketManager.user_socket>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    bm.user_socket()


`Cross-margin <binance.html#binance.websockets.BinanceSocketManager.margin_socket>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    bm.margin_socket()


`Isolated margin <binance.html#binance.websockets.BinanceSocketManager.isolated_margin_socket>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    bm.isolated_margin_socket(symbol)


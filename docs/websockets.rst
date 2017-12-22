Websockets
==========

Sockets are handled through a Socket Manager `BinanceSocketManager <binance.html#binance.websockets.BinanceSocketManager>`_.

Multiple socket connections can be made through the manager.

Only one instance of each socket type will be created, i.e. only one BNBBTC Depth socket can be created
and there can be both a BNBBTC Depth and a BNBBTC Trade socket open at once.

When creating socket connections a callback function is passed which receives the messages.

Messages are received as dictionary objects relating to the message formats defined in the `Binance WebSocket API documentation <https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md>`_.

Websockets are setup to reconnect with a maximum of 5 retries.

Websocket Usage
---------------

Create the manager like so, passing the API client.

.. code:: python

    from binance.websockets import BinanceSocketManager
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    conn_key = bm.start_trade_socket('BNBBTC', process_message)
    # then start the socket manager
    bm.start()

A callback to process messages would take the format

.. code:: python

    def process_message(msg):
        print("message type: {}".format(msg['e']))
        print(msg)
        # do something


`Multiplex Socket <binance.html#binance.websockets.BinanceSocketManager.start_multiplex_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Create a socket combining multiple streams.

These streams can include the depth, kline, ticker and trade streams but not the user stream which requires extra authentication.

Symbols in socket name must be lowercase i.e bnbbtc@aggTrade, neobtc@ticker

See the `Binance Websocket Streams API documentation <https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md>`_ for details on socket names.

.. code:: python

    def process_m_message(msg):
        print("stream: {} data: {}".format(msg['stream'], msg['data']))

    # pass a list of stream names
    conn_key = bm.start_multiplex_socket(['bnbbtc@aggTrade', 'neobtc@ticker'], process_m_message)

`Depth Socket <binance.html#binance.websockets.BinanceSocketManager.start_depth_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Depth sockets have an optional depth parameter. By default this is set to 1.
Valid depth values are 1, 5, 10 and 20 and `defined as enums <enums.html>`_.

.. code:: python

    conn_key = bm.start_depth_socket('BNBBTC', process_message, depth=BinanceSocketManager.WEBSOCKET_DEPTH_5)


`Kline Socket <binance.html#binance.websockets.BinanceSocketManager.start_kline_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Kline sockets have an optional interval parameter. By default this is set to 1 minute.
Valid interval values are `defined as enums <enums.html>`_.

.. code:: python

    from binance.enums import *
    conn_key = bm.start_kline_socket('BNBBTC', process_message, interval=KLINE_INTERVAL_30MINUTE)


`Aggregated Trade Socket <binance.html#binance.websockets.BinanceSocketManager.start_aggtrade_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    conn_key = bm.start_aggtrade_socket('BNBBTC', process_message)


` Trade Socket <binance.html#binance.websockets.BinanceSocketManager.start_trade_socket>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    conn_key = bm.start_trade_socket('BNBBTC', process_message)

`Symbol Ticker Socket <binance.html#binance.websockets.BinanceSocketManager.start_symbol_ticker_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    conn_key = bm.start_symbol_ticker_socket('BNBBTC', process_message)

`Ticker Socket <binance.html#binance.websockets.BinanceSocketManager.start_ticker_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

    conn_key = bm.start_ticker_socket(process_message)

`User Socket <binance.html#binance.websockets.BinanceSocketManager.start_user_socket>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This watches for 3 different user events

- Account Update Event
- Order Update Event
- Trade Update Event

The Manager handles keeping the socket alive.

.. code:: python

    bm.start_user_socket(process_message)


`Close a Socket <binance.html#binance.websockets.BinanceSocketManager.stop_socket>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

To close an individual socket call the `stop_socket` function.
This takes a conn_key parameter which is returned when starting the socket.

.. code:: python

    bm.stop_socket(conn_key)


To stop all sockets and end the manager call `close` after doing this a `start` call would be required to connect any new sockets.

.. code:: python

    bm.close()

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-binance/docs/websockets?pixel

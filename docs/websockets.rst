Websockets
==========


Sockets are handled through a Socket Manager `BinanceSocketManager`.

Multiple socket connections can be made through the manager.

Only one instance of each socket type will be created, i.e. only one BNBBTC Depth socket can be created
and there can be both a BNBBTC Depth and a BNBBTC Trade socket open at once.

Socket connections pass a callback function to receive messages.

Messages are received as dictionary objects relating to the message formats defined in the `Binance API documentation <https://www.binance.com/restapipub.html#wss-endpoint>`_.

Create the manager like so, passing the api client.

.. code:: python

    from binance.websockets import BinanceSocketManager
    bm = BinanceSocketManager(client)
    # attach any sockets here then start
    bm.start()

A callback to process messages would take the format

.. code:: python

    def process_message(msg):
        print("message type:" + msg[e])
        print(msg)
        # do something

Depth Socket
++++++++++++

.. code:: python

    bm.start_depth_socket('BNBBTC', process_message)

Kline Socket
++++++++++++

.. code:: python

    bm.start_kline_socket('BNBBTC', process_message)

Aggregated Trade Socket
+++++++++++++++++++++++

.. code:: python

    bm.start_trade_socket('BNBBTC', process_message)

Ticker Socket
+++++++++++++

.. code:: python

    bm.start_ticker_socket(process_message)

User Socket
+++++++++++

This watches for 3 different events

- Account Update Event
- Order Update Event
- Trade Update Event

The Manager handles keeping the socket alive.

.. code:: python

    bm.start_user_socket(process_message)

Close Socket
++++++++++++

To close an individual socket call the corresponding close function

- `stop_depth_socket`
- `stop_kline_socket`
- `stop_trade_socket`
- `stop_ticker_socket`
- `stop_user_socket`


To stop all sockets and end the manager call `close` after doing this a `start` call would be required to connect any new sockets.

.. code:: python

    bm.close()

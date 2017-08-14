Binance API
========

This is an unofficial Python wrapper for Binance exchange API v1. I am in no way affiliated with Binance, use at your own risk.

Features
--------

- Implementation of General, Market Data and Account endpoints.
- Simple handling of authentication
- No need to generate timestamps yourself, the wrapper does it for you
- Response exception handling

Installation
------------

``binance`` is available on `PYPI <https://pypi.python.org/pypi/python-binance/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-binance

Documentation
-------------

Firstly `register with Binance <https://binance.com>`_.

API Key + Secret
^^^^^^^^^^^^^^^^

If you want to use signed methods then `create an API Key  <https://www.binance.com/userCenter/createApi.html>`_.

Init Client
^^^^^^^^^^^

.. code:: python

    from binance.client import Client
    client = Client(api_key, api_secret)

Exceptions
^^^^^^^^^^

On an API call error a binance.exceptions.BinanceAPIException will be raised.
The exception provides access to the
- `status_code` - response status code
- `response` - response object
- `code` - Binance error code
- `message` - Binance error message
- `request` - request object if available

Making API Calls
^^^^^^^^^^^^^^^^

Every method supports the passing of arbitrary parameters via keyword.
These keyword arguments will be sent directly to the relevant endpoint.
If a required parameter is not supplied, an error will be raised.

Each API method returns a dictionary of the JSON response as per the `Binance API documentation <https://www.binance.com/restapipub.html>`_.
The docstring of each method in the code references the endpoint it implements.

Some methods require a `timestamp` parameter, this is generated for you where required.

Some methods have a `recvWindow` parameter for `timing security, see Binance documentation <https://www.binance.com/restapipub.html#timing-security>`_.

ENUMs
^^^^^

Binance defines Enumerated Types for Order Types, Order Side, Time in Force and Kline intervals.

.. code:: python
    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_2MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'

    TIME_IN_FORCE_GTC = 'GTC'
    TIME_IN_FORCE_IOC = 'IOC'


Examples
^^^^^^^^

Get the server time

.. code:: python

    time_res = client.get_server_time()


Fetch all orders

.. code:: python

    orders = client.get_all_orders(symbol='BNBBTC', limit=10)


Create an order

.. code:: python

    from binance.enums import *
    order = client.create_order(
        symbol='BNBBTC',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=100,
        price='0.00001')

Using Enumerated types

.. code:: python

    from binance.enums import *
    candles = client.get_klines(symbol='BNBBTC', interval=KLINE_INTERVAL_30MINUTE)

Error Handling

.. code:: python

    try:
        client.get_all_orders()
    except BinanceAPIException as e:
        print e.status_code
        print e.message

TODO
----

- Websocket handling
- Stream handling?
- Tests

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

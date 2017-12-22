Market Data Endpoints
=====================


`Get Market Depth <binance.html#binance.client.Client.get_order_book>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    depth = client.get_order_book(symbol='BNBBTC')

`Get Recent Trades <binance.html#binance.client.Client.get_recent_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.get_recent_trades(symbol='BNBBTC')

`Get Historical Trades <binance.html#binance.client.Client.get_historical_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.get_historical_trades(symbol='BNBBTC')

`Get Aggregate Trades <binance.html#binance.client.Client.get_aggregate_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.get_aggregate_trades(symbol='BNBBTC')


`Get Kline/Candlesticks <binance.html#binance.client.Client.get_klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from binance.enums import *
    candles = client.get_klines(symbol='BNBBTC', interval=KLINE_INTERVAL_30MINUTE)

`Get 24hr Ticker <binance.html#binance.client.Client.get_ticker>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    tickers = client.get_ticker()

`Get All Prices <binance.html#binance.client.Client.get_all_tickers>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get last price for all markets.

.. code:: python

    prices = client.get_all_tickers()

`Get Orderbook Tickers <binance.html#binance.client.Client.get_orderbook_tickers>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get first bid and ask entry in the order book for all markets.

.. code:: python

    tickers = client.get_orderbook_tickers()

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-binance/docs/market_data?pixel

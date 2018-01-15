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

    candles = client.get_klines(symbol='BNBBTC', interval=KLINE_INTERVAL_30MINUTE)

`Get Historical Kline/Candlesticks <binance.html#binance.client.Client.get_historical_klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fetch klines for any date range and interval

.. code:: python

    # fetch 1 minute klines from one day ago until now
    from datetime import datetime, timedelta
    from time import time
    klines = client.get_historical_klines("BNBBTC", KLINE_INTERVAL_1MINUTE,
            datetime.utcnow() - timedelta(1))

    # fetch 30 minute klines for the last month of 2017
    klines = client.get_historical_klines("ETHBTC", KLINE_INTERVAL_30MINUTE,
            datetime(2017, 12, 1), datetime(2018, 1, 1))

    # fetch weekly klines since it listed
    klines = client.get_historical_klines("NEOBTC", KLINE_INTERVAL_1WEEK,
            datetime(2017, 1, 1))

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

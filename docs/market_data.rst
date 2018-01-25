Market Data Endpoints
=====================


`Get Market Depth <binance.html#binance.client.Client.order_book>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    depth = client.order_book(symbol='BNBBTC')

`Get Recent Trades <binance.html#binance.client.Client.recent_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.recent_trades(symbol='BNBBTC')

`Get Historical Trades <binance.html#binance.client.Client.historical_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.historical_trades(symbol='BNBBTC')

`Get Aggregate Trades <binance.html#binance.client.Client.aggregate_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.aggregate_trades(symbol='BNBBTC')


`Get Kline/Candlesticks <binance.html#binance.client.Client.klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    candles = client.klines(symbol='BNBBTC',
            interval=bc.KLINE_INTERVAL_30MINUTE)

`Get Historical Kline/Candlesticks <binance.html#binance.client.Client.historical_klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fetch klines for any date range and interval

.. code:: python

    # fetch 1 minute klines from one day ago until now
    from datetime import datetime, timedelta
    from time import time
    klines = client.historical_klines("BNBBTC", bc.KLINE_INTERVAL_1MINUTE,
            datetime.utcnow() - timedelta(1))

    # fetch 30 minute klines for the last month of 2017
    klines = client.historical_klines("ETHBTC", bc.KLINE_INTERVAL_30MINUTE,
            datetime(2017, 12, 1), datetime(2018, 1, 1))

    # fetch weekly klines since it listed
    klines = client.historical_klines("NEOBTC", bc.KLINE_INTERVAL_1WEEK,
            datetime(2017, 1, 1))

`Get 24hr Ticker <binance.html#binance.client.Client.ticker>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    tickers = client.ticker()

`Get All Prices <binance.html#binance.client.Client.all_tickers>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get last price for all markets.

.. code:: python

    prices = client.all_tickers()

`Get Orderbook Tickers <binance.html#binance.client.Client.orderbook_tickers>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get first bid and ask entry in the order book for all markets.

.. code:: python

    tickers = client.orderbook_tickers()

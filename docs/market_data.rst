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

    candles = client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)

`Get Historical Kline/Candlesticks <binance.html#binance.client.Client.get_historical_klines>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fetch klines for any date range and interval

.. code:: python

    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    # fetch 30 minute klines for the last month of 2017
    klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

    # fetch weekly klines since it listed
    klines = client.get_historical_klines("NEOBTC", KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

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

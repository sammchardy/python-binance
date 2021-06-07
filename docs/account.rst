Account Endpoints
=================

Orders
------

Order Validation
^^^^^^^^^^^^^^^^

Binance has a number of rules around symbol pair orders with validation on minimum price, quantity and total order value.

Read more about their specifics in the `Filters <https://binance-docs.github.io/apidocs/spot/en/#filters>`_
section of the official API.

Read `Understanding Binance Order Filters <https://sammchardy.github.io/binance/2021/05/03/binance-order-filters.html>`_
for more information about price and quantity filters on `Binance <https://www.binance.com/?ref=10099792>`_.

It can be helpful to format the output using formatting

.. code:: python

    amount = 0.000234234
    precision = 5
    amt_str = "{:0.0{}f}".format(amount, precision)

Or if you have the tickSize or stepSize then use the helper to round to step size

.. code:: python

    from binance.helpers import round_step_size

    amount = 0.000234234
    tick_size = 0.00001
    rounded_amount = round_step_size(amount, tick_size)


`Fetch all orders <binance.html#binance.client.Client.get_all_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_all_orders(symbol='BNBBTC', limit=10)


`Place an order <binance.html#binance.client.Client.create_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Place an order**

Use the `create_order` function to have full control over creating an order

.. code:: python

    from binance.enums import *
    order = client.create_order(
        symbol='BNBBTC',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=100,
        price='0.00001')

**Place a limit order**

Use the helper functions to easily place a limit buy or sell order

.. code:: python

    order = client.order_limit_buy(
        symbol='BNBBTC',
        quantity=100,
        price='0.00001')

    order = client.order_limit_sell(
        symbol='BNBBTC',
        quantity=100,
        price='0.00001')


**Place a market order**

Use the helper functions to easily place a market buy or sell order

.. code:: python

    order = client.order_market_buy(
        symbol='BNBBTC',
        quantity=100)

    order = client.order_market_sell(
        symbol='BNBBTC',
        quantity=100)

**Place an OCO order**

Use the `create_oco_order` function to have full control over creating an OCO order

.. code:: python

    from binance.enums import *
    order = client.create_oco_order(
        symbol='BNBBTC',
        side=SIDE_SELL,
        stopLimitTimeInForce=TIME_IN_FORCE_GTC,
        quantity=100,
        stopPrice='0.00001',
        price='0.00002')


`Place a test order <binance.html#binance.client.Client.create_test_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creates and validates a new order but does not send it into the exchange.

.. code:: python

    from binance.enums import *
    order = client.create_test_order(
        symbol='BNBBTC',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=100,
        price='0.00001')

`Check order status <binance.html#binance.client.Client.get_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    order = client.get_order(
        symbol='BNBBTC',
        orderId='orderId')


`Cancel an order <binance.html#binance.client.Client.cancel_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    result = client.cancel_order(
        symbol='BNBBTC',
        orderId='orderId')


`Get all open orders <binance.html#binance.client.Client.get_open_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_open_orders(symbol='BNBBTC')

`Get all orders <binance.html#binance.client.Client.get_all_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_all_orders(symbol='BNBBTC')


Account
-------

`Get account info <binance.html#binance.client.Client.get_account>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_account()

`Get asset balance <binance.html#binance.client.Client.get_asset_balance>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    balance = client.get_asset_balance(asset='BTC')

`Get account status <binance.html#binance.client.Client.get_account_status>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    status = client.get_account_status()

`Get account API trading status <binance.html#binance.client.Client.get_account_api_trading_status>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    status = client.get_account_api_trading_status()

`Get trades <binance.html#binance.client.Client.get_my_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.get_my_trades(symbol='BNBBTC')

`Get trade fees <binance.html#binance.client.Client.get_trade_fee>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # get fees for all symbols
    fees = client.get_trade_fee()

    # get fee for one symbol
    fees = client.get_trade_fee(symbol='BNBBTC')

`Get asset details <binance.html#binance.client.Client.get_asset_details>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_asset_details()

`Get dust log <binance.html#binance.client.Client.get_dust_log>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    log = client.get_dust_log()

`Transfer dust <binance.html#binance.client.Client.transfer_dust>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transfer = client.transfer_dust(asset='BNZ')


`Get Asset Dividend History <binance.html#binance.client.Client.get_asset_dividend_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    history = client.get_asset_dividend_history()


`Disable Fast Withdraw Switch <binance.html#binance.client.Client.disable_fast_withdraw_switch>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    client.disable_fast_withdraw_switch()


`Enable Fast Withdraw Switch <binance.html#binance.client.Client.enable_fast_withdraw_switch>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    client.enable_fast_withdraw_switch()

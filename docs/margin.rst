Margin Trading Endpoints
========================

Market Data
-----------

`Get margin asset info <binance.html#binance.client.Client.get_margin_asset>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_asset(asset='BNB')

`Get margin symbol info <binance.html#binance.client.Client.get_margin_symbol>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_symbol(symbol='BTCUSDT')

`Get margin price index <binance.html#binance.client.Client.get_margin_price_index>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_price_index(symbol='BTCUSDT')

Orders
------

Order Validation
^^^^^^^^^^^^^^^^

Binance has a number of rules around symbol pair orders with validation on minimum price, quantity and total order value.

Read more about their specifics in the `Filters <https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#filters>`_
section of the official API.

It can be helpful to format the output using the following snippet

.. code:: python

    amount = 0.000234234
    precision = 5
    amt_str = "{:0.0{}f}".format(amount, precision)


`Fetch all margin_orders <binance.html#binance.client.Client.get_all_margin_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_all_margin_orders(symbol='BNBBTC', limit=10)


`Place a margin order <binance.html#binance.client.Client.create_margin_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Place an order**

Use the `create_margin_order` function to have full control over creating an order

.. code:: python

    from binance.enums import *
    order = client.create_margin_order(
        symbol='BNBBTC',
        side=SIDE_BUY,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=100,
        price='0.00001')


`Check order status <binance.html#binance.client.Client.get_margin_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    order = client.get_margin_order(
        symbol='BNBBTC',
        orderId='orderId')


`Cancel a margin order <binance.html#binance.client.Client.cancel_margin_order>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    result = client.cancel_margin_order(
        symbol='BNBBTC',
        orderId='orderId')


`Get all open margin orders <binance.html#binance.client.Client.get_open_margin_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_open_margin_orders(symbol='BNBBTC')

`Get all margin orders <binance.html#binance.client.Client.get_all_margin_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_all_margin_orders(symbol='BNBBTC')


Account
-------

`Get margin account info <binance.html#binance.client.Client.get_margin_account>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_account()

`Transfer spot to margin <binance.html#binance.client.Client.transfer_spot_to_margin>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.transfer_spot_to_margin(asset='BTC', amount='1.1')

`Transfer margin to spot <binance.html#binance.client.Client.transfer_margin_to_spot>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.transfer_margin_to_spot(asset='BTC', amount='1.1')

`Get max transfer amount <binance.html#binance.client.Client.get_max_margin_transfer>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_max_margin_transfer(asset='BTC')


Trades
-----

`Get all margin trades <binance.html#binance.client.Client.get_margin_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.get_margin_trades(symbol='BNBBTC')

Loans
-----


`Create loan <binance.html#binance.client.Client.create_margin_loan>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.create_margin_loan(asset='BTC', amount='1.1')

`Repay loan <binance.html#binance.client.Client.repay_margin_loan>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.repay_margin_loan(asset='BTC', amount='1.1')

`Get loan details <binance.html#binance.client.Client.get_margin_loan_details>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_margin_loan_details(asset='BTC', txId='100001')

`Get repay details <binance.html#binance.client.Client.get_margin_repay_details>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_margin_repay_details(asset='BTC', txId='100001')

`Get max loan amount <binance.html#binance.client.Client.get_max_margin_loan>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_max_margin_loan(asset='BTC')

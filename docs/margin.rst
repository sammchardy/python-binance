Margin Trading Endpoints
========================

.. note ::  

    **Cross-margin vs isolated margin trading**

    Binance offers both *cross-margin* trading (where all margin is in one account) and *isolated margin* trading (where each pair is a separate margin account).  Make sure you are interacting with the right one.

    Some of the API endpoints apply to the cross-margin or isolated margin accounts only.  Other endpoints, such as the trade execution endpoints, are used for the cross-margin account trades by default, but you can use your isolated margin accounts by using the ``isIsolated`` or ``isolatedSymbol`` parameters.  See the documentation below.

Market Data
-----------

`Get cross-margin asset info <binance.html#binance.client.Client.get_margin_asset>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_asset(asset='BNB')

`Get cross-margin symbol info <binance.html#binance.client.Client.get_margin_symbol>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_symbol(symbol='BTCUSDT')

`Get isolated margin symbol info <binance.html#binance.client.Client.get_isolated_margin_symbol>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_isolated_margin_symbol(symbol='BTCUSDT')

`Get all isolated margin symbols <binance.html#binance.client.Client.get_all_isolated_margin_symbols>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_all_isolated_margin_symbols()

`Get margin price index <binance.html#binance.client.Client.get_margin_price_index>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_price_index(symbol='BTCUSDT')

Orders
------

Cross-margin vs isolated margin orders
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, these trade execution endpoints will create an order using the *cross-margin* account. 

To use the *isolated margin* account for the ``symbol`` you have specified, simply add the ``isIsolated='TRUE'`` parameter to the API calls below in this 'Orders' section.

Order Validation
^^^^^^^^^^^^^^^^

Binance has a number of rules around symbol pair orders with validation on minimum price, quantity and total order value.

Read more about their specifics in the `Filters <https://binance-docs.github.io/apidocs/spot/en/#filters>`_
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

For isolated margin, add the ``isIsolated='TRUE'`` parameter.

`Get all margin orders <binance.html#binance.client.Client.get_all_margin_orders>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    orders = client.get_all_margin_orders(symbol='BNBBTC')

For isolated margin, add the ``isIsolated='TRUE'`` parameter.

Account
-------

`Get cross-margin account info <binance.html#binance.client.Client.get_margin_account>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_margin_account()

`Create isolated margin account <binance.html#binance.client.Client.create_isolated_margin_account>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    account = client.create_isolated_margin_account(base='BTC', quote='ETH')

`Get isolated margin account info <binance.html#binance.client.Client.get_isolated_margin_account>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_isolated_margin_account()

`Transfer spot to cross-margin account <binance.html#binance.client.Client.transfer_spot_to_margin>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.transfer_spot_to_margin(asset='BTC', amount='1.1')

`Transfer cross-margin account to spot <binance.html#binance.client.Client.transfer_margin_to_spot>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.transfer_margin_to_spot(asset='BTC', amount='1.1')

`Transfer spot to isolated margin account <binance.html#binance.client.Client.transfer_spot_to_isolated_margin>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.transfer_spot_to_isolated_margin(asset='BTC', 
                                                            symbol='ETHBTC', amount='1.1')

`Transfer isolated margin account to spot <binance.html#binance.client.Client.transfer_isolated_margin_to_spot>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.transfer_isolated_margin_to_spot(asset='BTC', 
                                                            symbol='ETHBTC', amount='1.1')

`Get max transfer amount <binance.html#binance.client.Client.get_max_margin_transfer>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_max_margin_transfer(asset='BTC')

This max transfer is for the cross-margin account by default.  For isolated margin records, add the ``isolatedSymbol=symbol_name`` parameter.

Trades
-----

`Get all margin trades <binance.html#binance.client.Client.get_margin_trades>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    trades = client.get_margin_trades(symbol='BNBBTC')

For isolated margin trades, add the ``isIsolated='TRUE'`` parameter.


Loans
-----

`Create loan <binance.html#binance.client.Client.create_margin_loan>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.create_margin_loan(asset='BTC', amount='1.1')

This for the cross-margin account by default.  For isolated margin, add the ``isIsolated='TRUE'`` and the ``symbol=symbol_name`` parameters.

`Repay loan <binance.html#binance.client.Client.repay_margin_loan>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transaction = client.repay_margin_loan(asset='BTC', amount='1.1')

This for the cross-margin account by default.  For isolated margin, add the ``isIsolated='TRUE'`` and the ``symbol=symbol_name`` parameters.

`Get loan details <binance.html#binance.client.Client.get_margin_loan_details>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_margin_loan_details(asset='BTC', txId='100001')

This for the cross-margin account by default.  For isolated margin records, add the ``isolatedSymbol=symbol_name`` parameter.

`Get repay details <binance.html#binance.client.Client.get_margin_repay_details>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_margin_repay_details(asset='BTC', txId='100001')

This for the cross-margin account by default.  For isolated margin records, add the ``isolatedSymbol=symbol_name`` parameter.

`Get max loan amount <binance.html#binance.client.Client.get_max_margin_loan>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    details = client.get_max_margin_loan(asset='BTC')

The max loan is for the cross-margin account by default.  For isolated margin records, add the ``isolatedSymbol=symbol_name`` parameter.

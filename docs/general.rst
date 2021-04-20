General Endpoints
=================

`Ping the server <binance.html#binance.client.Client.ping>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    client.ping()

`Get the server time <binance.html#binance.client.Client.get_server_time>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    time_res = client.get_server_time()

`Get system status <binance.html#binance.client.Client.get_system_status>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    status = client.get_system_status()

Returns

.. code-block:: python

    {
        "status": 0,        # 0: normal，1：system maintenance
        "msg": "normal"     # normal or System maintenance.
    }

`Get Exchange Info <binance.html#binance.client.Client.get_exchange_info>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_exchange_info()

`Get Symbol Info <binance.html#binance.client.Client.get_symbol_info>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the exchange info for a particular symbol

.. code:: python

    info = client.get_symbol_info('BNBBTC')

`Get All Coins Info <binance.html#binance.client.Client.get_all_tickers>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get information of coins (available for deposit and withdraw) for user

.. code:: python

    info = client.get_all_tickers()

`Get Get Daily Account Snapshot <binance.html#binance.client.Client.get_account_snapshot>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get daily account snapshot of specific type. Valid types: SPOT/MARGIN/FUTURES.

.. code:: python

    info = client.get_account_snapshot(type='SPOT')

`Get Current Products <binance.html#binance.client.Client.get_products>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This call is deprecated, use the above Exchange Info call

.. code:: python

    products = client.get_products()

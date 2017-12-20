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

`Get Exchange Info <binance.html#binance.client.Client.get_exchange_info>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.get_exchange_info()

`Get Symbol Info <binance.html#binance.client.Client.get_symbol_info>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the exchange info for a particular symbol

.. code:: python

    info = client.get_symbol_info('BNBBTC')

`Get Current Products <binance.html#binance.client.Client.get_products>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This call is deprecated, use the above Exchange Info call

.. code:: python

    products = client.get_products()

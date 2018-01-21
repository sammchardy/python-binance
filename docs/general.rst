General Endpoints
=================

`Ping the server <binance.html#binance.client.Client.ping>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    client.ping()

`Get the server time <binance.html#binance.client.Client.server_time>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    time_res = client.server_time()

`Get Exchange Info <binance.html#binance.client.Client.exchange_info>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    info = client.exchange_info()

`Get Symbol Info <binance.html#binance.client.Client.symbol_info>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the exchange info for a particular symbol

.. code:: python

    info = client.symbol_info('BNBBTC')

`Get Current Products <binance.html#binance.client.Client.products>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This call is deprecated, use the above Exchange Info call

.. code:: python

    products = client.products()

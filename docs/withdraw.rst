Withdraw Endpoints
==================

`Place a withdrawal <binance.html#binance.client.Client.withdraw>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure you enable Withdrawal permissions for your API Key to use this call.

You must have withdrawn to the address through the website and approved the withdrawal via email before you can withdraw using the API.

.. code:: python

    from binance.exceptions import BinanceAPIException
    try:
        # name parameter will be set to the asset value by the client if not passed
        result = client.withdraw(
            coin='ETH',
            address='<eth_address>',
            amount=100)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")

    # passing a name parameter
    result = client.withdraw(
        coin='ETH',
        address='<eth_address>',
        amount=100,
        name='Withdraw')

    # if the coin requires a extra tag or name such as XRP or XMR then pass an `addressTag` parameter.
    result = client.withdraw(
        coin='XRP',
        address='<xrp_address>',
        addressTag='<xrp_address_tag>',
        amount=10000)

`Fetch deposit history <binance.html#binance.client.Client.get_deposit_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    deposits = client.get_deposit_history()
    btc_deposits = client.get_deposit_history(coin='BTC')


`Fetch withdraw history <binance.html#binance.client.Client.get_withdraw_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    withdraws = client.get_withdraw_history()
    btc_withdraws = client.get_withdraw_history(coin='BTC')

`Get deposit address <binance.html#binance.client.Client.get_deposit_address>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    address = client.get_deposit_address(coin='BTC')

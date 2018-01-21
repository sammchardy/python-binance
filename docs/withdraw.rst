Withdraw Endpoints
==================

`Place a withdrawal <binance.html#binance.client.Client.withdraw>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure you enable Withdrawal permissions for your API Key to use this call.

You must have withdrawn to the address through the website and approved the withdrawal via email before you can withdraw using the API.

Raises a `WithdrawException <binance.html#binance.exceptions.WithdrawException>`_ if the withdraw fails.

.. code:: python

    from binance.exceptions import APIException, WithdrawException
    try:
        # name parameter will be set to the asset value by the client if not passed
        result = client.withdraw(
            asset='ETH',
            address='<eth_address>',
            amount=100)
    except APIException as e:
        print(e)
    except WithdrawException as e:
        print(e)
    else:
        print("Success")

    # passing a name parameter
    result = client.withdraw(
        asset='ETH',
        address='<eth_address>',
        amount=100,
        name='Withdraw')

    # if the coin requires a extra tag or name such as XRP or XMR then pass an `addressTag` parameter.
    result = client.withdraw(
        asset='XRP',
        address='<xrp_address>',
        addressTag='<xrp_address_tag>',
        amount=10000)

`Fetch deposit history <binance.html#binance.client.Client.deposit_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    deposits = client.deposit_history()
    btc_deposits = client.deposit_history(asset='BTC')


`Fetch withdraw history <binance.html#binance.client.Client.withdraw_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    withdraws = client.withdraw_history()
    btc_withdraws = client.withdraw_history(asset='BTC')

`Get deposit address <binance.html#binance.client.Client.deposit_address>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    address = client.deposit_address(asset='BTC')

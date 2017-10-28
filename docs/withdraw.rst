Withdraw Endpoints
==================

`Place a withdrawal <binance.html#binance.client.Client.withdraw>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    result = client.withdraw(
        asset='ETH',
        address='<eth_address>',
        amount=100)

    if result['success']:
        print("Success")

`Fetch deposit history <binance.html#binance.client.Client.get_deposit_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    deposits = client.get_deposit_history()
    btc_deposits = client.get_deposit_history(asset='BTC')


`Fetch withdraw history <binance.html#binance.client.Client.get_withdraw_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    withdraws = client.get_withdraw_history()
    btc_withdraws = client.get_withdraw_history(asset='BTC')

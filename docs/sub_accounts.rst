Sub Account Endpoints
=====================


`Get Sub Account list <binance.html#binance.client.Client.get_sub_account_list>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    accounts = client.get_sub_account_list()

`Get Sub Account Transfer History <binance.html#binance.client.Client.get_sub_account_transfer_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    history = client.get_sub_account_transfer_history(email='blah@gmail.com')

`Create Sub Account Transfer <binance.html#binance.client.Client.create_sub_account_transfer>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    transfer = client.create_sub_account_transfer(
        fromEmail='from@gmail.com',
        toEmail='to@gmail.com',
        asset='BNB',
        amount='100'
    )

`Get Sub Account Assets <binance.html#binance.client.Client.get_sub_account_assets>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    assets = client.get_sub_account_assets(email='blah@gmail.com')

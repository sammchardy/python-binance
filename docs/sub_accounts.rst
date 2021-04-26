Sub Account Endpoints
=====================


`Get Sub Account list <binance.html#binance.client.Client.get_sub_account_list>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    accounts = client.get_sub_account_list()

`Get Sub Account Transfer History <binance.html#binance.client.Client.get_sub_account_transfer_history>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    history = client.get_sub_account_transfer_history(fromEmail='blah@gmail.com', toEmail='foo@gmail.com')

`Get Sub Account Assets <binance.html#binance.client.Client.get_sub_account_assets>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    assets = client.get_sub_account_assets(email='blah@gmail.com')

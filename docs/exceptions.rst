Exceptions
==========

ResponseException
------------------------

Raised if a non JSON response is returned

APIException
-------------------

On an API call error a binance.exceptions.APIException will be raised.

The exception provides access to the

- `status_code` - response status code
- `response` - response object
- `code` - Binance error code
- `message` - Binance error message
- `request` - request object if available

.. code:: python

    try:
        client.get_all_orders()
    except APIException as e:
        print e.status_code
        print e.message

OrderException
---------------------

When placing an order parameters are validated to check they fit within the `Binance Trading Rules <https://binance.zendesk.com/hc/en-us/articles/115000594711>`_.

The following exceptions extend `OrderException`.

OrderMinAmountException
------------------------------

Raised if the specified amount isn't a multiple of the trade minimum amount.

OrderMinPriceException
-----------------------------

Raised if the price is lower than the trade minimum price.

OrderTotalPriceException
-------------------------------

Raised if the total is lower than the trade minimum total.

OrderUnknownSymbolException
----------------------------------

Raised if the symbol is not recognised.

OrderInactiveSymbolException
-----------------------------------

Raised if the symbol is inactive.


WithdrawException
------------------------

Raised if the withdraw fails.

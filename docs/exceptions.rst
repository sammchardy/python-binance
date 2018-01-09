Exceptions
==========

BinanceResponseException
------------------------

Raised if a non JSON response is returned

BinanceAPIException
-------------------

On an API call error a binance.exceptions.BinanceAPIException will be raised.

The exception provides access to the

- `status_code` - response status code
- `response` - response object
- `code` - Binance error code
- `message` - Binance error message
- `request` - request object if available

.. code:: python

    try:
        client.get_all_orders()
    except BinanceAPIException as e:
        print e.status_code
        print e.message

BinanceOrderException
---------------------

When placing an order parameters are validated to check they fit within the `Binance Trading Rules <https://binance.zendesk.com/hc/en-us/articles/115000594711>`_.

The following exceptions extend `BinanceOrderException`.

BinanceOrderMinAmountException
------------------------------

Raised if the specified amount isn't a multiple of the trade minimum amount.

BinanceOrderMinPriceException
-----------------------------

Raised if the price is lower than the trade minimum price.

BinanceOrderTotalPriceException
-------------------------------

Raised if the total is lower than the trade minimum total.

BinanceOrderUnknownSymbolException
----------------------------------

Raised if the symbol is not recognised.

BinanceOrderInactiveSymbolException
-----------------------------------

Raised if the symbol is inactive.


BinanceWithdrawException
------------------------

Raised if the withdraw fails.

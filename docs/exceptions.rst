Exceptions
==========

BinanceRequestException
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

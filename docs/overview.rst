Getting Started
===============

Installation
------------

``python-binance`` is available on `PYPI <https://pypi.python.org/pypi/python-binance/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-binance

Register on Binance
-------------------

Firstly `register an account with Binance <https://accounts.binance.com/en/register?ref=10099792>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key  <https://www.binance.com/en/support/faq/360002502072>`_.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from binance.client import Client
    client = Client(api_key, api_secret)

or for Asynchronous client

.. code:: python

    async def main():

        # initialise the client
        client = await AsyncClient.create(api_key, api_secret)

    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

Using the Spot, Futures or Vanilla Options Testnet
--------------------------------------------------

Binance offers a `Spot <https://testnet.binance.vision/>`_,
`Futures <https://testnet.binancefuture.com/>`_
and `Vanilla Options <https://testnet.binanceops.com/>`_ Testnet,
to test interacting with the exchange.

To enable this set the `testnet` parameter passed to the Client to True.

The testnet parameter will also be used by any websocket streams when the client is passed to the BinanceSocketManager.

.. code:: python

    client = Client(api_key, api_secret, testnet=True)

or for Asynchronous client

.. code:: python

    client = await AsyncClient.create(api_key, api_secret, testnet=True)

Using a different TLD
---------------------

If you are interacting with a regional version of Binance which has a different TLD such as `.us` or `.jp' then you
will need to pass this when creating the client, see examples below.

This tld will also be used by any websocket streams when the client is passed to the BinanceSocketManager.

.. code:: python

    client = Client(api_key, api_secret, tld='us')

or for Asynchronous client

.. code:: python

    client = await AsyncClient.create(api_key, api_secret, tld='us')


Making API Calls
----------------

Every method supports the passing of arbitrary parameters via keyword matching those in the `Binance API documentation <https://github.com/binance-exchange/binance-official-api-docs>`_.
These keyword arguments will be sent directly to the relevant endpoint.

Each API method returns a dictionary of the JSON response as per the `Binance API documentation <https://github.com/binance-exchange/binance-official-api-docs>`_.
The docstring of each method in the code references the endpoint it implements.

The Binance API documentation references a `timestamp` parameter, this is generated for you where required.

Some methods have a `recvWindow` parameter for `timing security, see Binance documentation <https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#timing-security>`_.

API Endpoints are rate limited by Binance at 20 requests per second, ask them if you require more.

Async API Calls
---------------

aiohttp is used to handle asyncio REST requests.

Each function available in the normal client is available in the AsyncClient class.

The only difference is to run within an asyncio event loop and await the function like below.

.. code:: python

    import asyncio
    from binance import AsyncClient

    async def main():
        client = await AsyncClient.create()

        # fetch exchange info
        res = await client.get_exchange_info()
        print(json.dumps(res, indent=2))

        await client.close_connection()

    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

Read `Async basics for Binance <https://sammchardy.github.io/binance/2021/05/01/async-binance-basics.html>`_
for more information about asynchronous patterns.

API Rate Limit
--------------

Check the `get_exchange_info() <binance.html#binance.client.Client.get_exchange_info>`_ call for up to date rate limits.

At the current time Binance rate limits are:

- 1200 weights per minute
- 10 orders per second
- 100,000 orders per 24hrs

Some calls have a higher weight than others especially if a call returns information about all symbols.
Read the `official Binance documentation <https://github.com/binance-exchange/binance-official-api-docs>`_ for specific information.

On each request Binance returns `X-MBX-USED-WEIGHT-(intervalNum)(intervalLetter)` and `X-MBX-ORDER-COUNT-(intervalNum)`
headers.

Here are examples to access these

Asynchronous example

.. code:: python

    import asyncio
    from binance import AsyncClient

    api_key = '<api_key>'
    api_secret = '<api_secret>'

    async def main():
        client = await AsyncClient.create(api_key, api_secret)

        res = await client.get_exchange_info()
        print(client.response.headers)

        await client.close_connection()

    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

Synchronous example


.. code:: python

    from binance import Client

    api_key = '<api_key>'
    api_secret = '<api_secret>'

    def main():
        client = Client(api_key, api_secret)

        res = client.get_exchange_info()
        print(client.response.headers)

    if __name__ == "__main__":
        main()
Requests Settings
-----------------

`python-binance` uses the `requests <http://docs.python-requests.org/en/master/>`_ library.

You can set custom requests parameters for all API calls when creating the client.

.. code:: python

    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})

You may also pass custom requests parameters through any API call to override default settings or the above settingsspecify new ones like the example below.

.. code:: python

    # this would result in verify: False and timeout: 5 for the get_all_orders call
    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
    client.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5})

Check out the `requests documentation <http://docs.python-requests.org/en/master/>`_ for all options.

**Proxy Settings**

You can use the Requests Settings method above

.. code:: python

    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080'
    }

    # in the Client instantiation
    client = Client("api-key", "api-secret", {'proxies': proxies})

    # or on an individual call
    client.get_all_orders(symbol='BNBBTC', requests_params={'proxies': proxies})

Or set an environment variable for your proxy if required to work across all requests.

An example for Linux environments from the `requests Proxies documentation <http://docs.python-requests.org/en/master/user/advanced/#proxies>`_ is as follows.

.. code-block:: bash

    $ export HTTP_PROXY="http://10.10.1.10:3128"
    $ export HTTPS_PROXY="http://10.10.1.10:1080"

For Windows environments

.. code-block:: bash

    C:\>set HTTP_PROXY=http://10.10.1.10:3128
    C:\>set HTTPS_PROXY=http://10.10.1.10:1080

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-binance/docs/overview?pixel

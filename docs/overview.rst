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

You may also pass custom requests parameters through any API call to override default settings or the above settings specify new ones like the example below.

.. code:: python

    # this would result in verify: False and timeout: 5 for the get_all_orders call
    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
    client.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5})

Check out the `requests documentation <http://docs.python-requests.org/en/master/>`_ for all options.

**Proxy Settings**

You can use the Requests Settings method above. For websockets python 3.8+ is required

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

Logging
-------

python-binance uses the Python logging module. You can enable logging to help debug issues and monitor your application.

Basic Logging Setup
~~~~~~~~~~~~~~~~~~

To enable debug logging, add this at the start of your script:

.. code:: python

    import logging
    logging.basicConfig(level=logging.DEBUG)

Advanced Logging Setup
~~~~~~~~~~~~~~~~~~~~~

For more detailed logging with timestamps and log levels:

.. code:: python

    import logging

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

Verbose Mode
~~~~~~~~~~~~

Verbose mode provides detailed logging of all HTTP requests and responses, which is particularly useful for debugging API issues, understanding request/response formats, and troubleshooting authentication or network problems.

Method 1: Using the verbose Parameter (Recommended for Quick Debugging)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable verbose mode by passing ``verbose=True`` when creating the client:

.. code:: python

    from binance.client import Client
    import logging

    # Configure logging (optional - for seeing the output)
    logging.basicConfig(level=logging.DEBUG)

    # Enable verbose mode
    client = Client(api_key, api_secret, verbose=True)

    # All API calls will now log detailed information
    server_time = client.get_server_time()

For AsyncClient:

.. code:: python

    import asyncio
    import logging
    from binance.async_client import AsyncClient

    logging.basicConfig(level=logging.DEBUG)

    async def main():
        # Enable verbose mode
        client = await AsyncClient.create(api_key, api_secret, verbose=True)

        # All API calls will now log detailed information
        server_time = await client.get_server_time()

        await client.close_connection()

    if __name__ == "__main__":
        asyncio.run(main())

Method 2: Using Python's Logging Module (Recommended for Production)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For more control over logging configuration, use Python's standard logging module:

.. code:: python

    import logging
    from binance.client import Client

    # Configure logging for binance module
    logging.basicConfig(
        level=logging.INFO,  # Set root level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Enable debug logging for binance specifically
    logging.getLogger('binance.base_client').setLevel(logging.DEBUG)

    # Create client (verbose parameter not needed)
    client = Client(api_key, api_secret)

This approach gives you fine-grained control and integrates with your application's existing logging infrastructure.

What Gets Logged
^^^^^^^^^^^^^^^^

When verbose mode is enabled, you'll see detailed logs for each request including:

- HTTP method and URL
- Request headers and body
- Response status code
- Response headers and body (truncated to 1000 characters)

Example output:

.. code-block:: text

    2025-11-30 22:01:26,957 - binance.base_client - DEBUG -
    Request: GET https://api.binance.com/api/v3/time
    RequestHeaders: {'Accept': 'application/json', 'Content-Type': 'application/json'}
    RequestBody: None
    Response: 200
    ResponseHeaders: {'Content-Type': 'application/json;charset=UTF-8', ...}
    ResponseBody: {"serverTime":1764536487218}

**Note:** Verbose mode should typically be disabled in production environments to minimize overhead and log volume. Use the logging module approach for production with appropriate log levels.

WebSocket Verbose Logging
^^^^^^^^^^^^^^^^^^^^^^^^^^

WebSocket connections support verbose mode just like REST API calls.

Method 1: Using the verbose Parameter (Recommended for Quick Debugging)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code:: python

    import logging
    from binance import AsyncClient, BinanceSocketManager

    # Configure logging to see output
    logging.basicConfig(level=logging.DEBUG)

    async def main():
        client = await AsyncClient.create()

        # Enable verbose mode for WebSocket connections
        bm = BinanceSocketManager(client, verbose=True)

        # WebSocket messages will be logged at DEBUG level
        ts = bm.trade_socket('BTCUSDT')
        async with ts as tscm:
            msg = await tscm.recv()
            print(msg)

        await client.close_connection()

Method 2: Using Python's Logging Module (Recommended for Production)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code:: python

    import logging
    from binance import AsyncClient, BinanceSocketManager

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Enable debug logging for all WebSocket connections
    logging.getLogger('binance.ws').setLevel(logging.DEBUG)

    async def main():
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)

        # WebSocket messages will be logged at DEBUG level
        ts = bm.trade_socket('BTCUSDT')
        async with ts as tscm:
            msg = await tscm.recv()
            print(msg)

        await client.close_connection()

You can also enable logging for specific WebSocket components:

.. code:: python

    # Log only WebSocket API messages
    logging.getLogger('binance.ws.websocket_api').setLevel(logging.DEBUG)

    # Log reconnection events
    logging.getLogger('binance.ws.reconnecting_websocket').setLevel(logging.DEBUG)

    # Log stream events
    logging.getLogger('binance.ws.streams').setLevel(logging.DEBUG)

WebSocket debug logs include:

- Raw received messages
- Connection state changes
- Reconnection attempts
- Subscription events
- Error messages

**Tip:** For comprehensive debugging, enable verbose mode for both REST API and WebSocket connections:

.. code:: python

    import logging
    from binance import AsyncClient, BinanceSocketManager

    logging.basicConfig(level=logging.DEBUG)

    # Enable verbose for both REST API and WebSocket
    client = await AsyncClient.create(verbose=True)
    bm = BinanceSocketManager(client, verbose=True)

For Threaded WebSocket Manager:

.. code:: python

    import logging
    from binance.ws.threaded_stream import ThreadedApiManager

    logging.basicConfig(level=logging.DEBUG)

    # Enable verbose mode for threaded WebSocket manager
    twm = ThreadedApiManager(api_key='your_key', api_secret='your_secret', verbose=True)
    twm.start()

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-binance/docs/overview?pixel

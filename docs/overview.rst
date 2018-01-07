Getting Started
===============

Installation
------------

``python-binance`` is available on `PYPI <https://pypi.python.org/pypi/python-binance/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-binance

**Windows**

If you see errors building Twisted indication Microsoft Visual C++ is required you may need to install the Visual C++ Build Tools
refer to the `Python Wiki on Widows Compilers <https://wiki.python.org/moin/WindowsCompilers>`_ for your relevant version.

Register on Binance
-------------------

Firstly `register an account with Binance <https://www.binance.com/register.html?ref=10099792>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key  <https://www.binance.com/userCenter/createApi.html>`_.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from binance.client import Client
    client = Client(api_key, api_secret)

Making API Calls
----------------

Every method supports the passing of arbitrary parameters via keyword matching those in the`Binance API documentation <https://github.com/binance-exchange/binance-official-api-docs>`_.
These keyword arguments will be sent directly to the relevant endpoint.

Each API method returns a dictionary of the JSON response as per the `Binance API documentation <https://github.com/binance-exchange/binance-official-api-docs>`_.
The docstring of each method in the code references the endpoint it implements.

The Binance API documentation references a `timestamp` parameter, this is generated for you where required.

Some methods have a `recvWindow` parameter for `timing security, see Binance documentation <https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#timing-security>`_.

API Endpoints are rate limited by Binance at 20 requests per second, ask them if you require more.

API Rate Limit
--------------

Check the `get_exchange_info() <binance.html#binance.client.Client.get_exchange_info>`_ call for up to date rate limits.

At the current time Binance rate limits are:

- 1200 requests per minute
- 10 orders per second
- 100,000 orders per 24hrs

Some calls have a higher weight than others especially if a call returns information about all symbols.
Read the `official Binance documentation <https://github.com/binance-exchange/binance-official-api-docs`_ for specific information.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-binance/docs/overview?pixel

Proxy Settings
--------------

`python-binance` uses the `requests <http://docs.python-requests.org/en/master/>`_ library which means you can set environment variable for your proxy if required.
Check out the `requests Proxies documentation <http://docs.python-requests.org/en/master/user/advanced/#proxies>`_ for further details.

An example for Linux environments from the `requests` Proxies documentation is as follows.

.. code-block:: bash

    $ export HTTP_PROXY="http://10.10.1.10:3128"
    $ export HTTPS_PROXY="http://10.10.1.10:1080"

For Windows environments

.. code-block:: bash

    C:\>set HTTP_PROXY=http://10.10.1.10:3128
    C:\>set HTTPS_PROXY=http://10.10.1.10:1080

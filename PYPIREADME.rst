.. image:: https://img.shields.io/pypi/v/python-binance.svg
    :target: https://pypi.python.org/pypi/python-binance

.. image:: https://img.shields.io/pypi/l/python-binance.svg
    :target: https://pypi.python.org/pypi/python-binance

.. image:: https://img.shields.io/travis/sammchardy/python-binance.svg
    :target: https://travis-ci.org/sammchardy/python-binance

.. image:: https://img.shields.io/coveralls/sammchardy/python-binance.svg
    :target: https://coveralls.io/github/sammchardy/python-binance

.. image:: https://img.shields.io/pypi/wheel/python-binance.svg
    :target: https://pypi.python.org/pypi/python-binance

.. image:: https://img.shields.io/pypi/pyversions/python-binance.svg
    :target: https://pypi.python.org/pypi/python-binance

This is an unofficial Python wrapper for the `Binance exchange REST API v3 <https://binance-docs.github.io/apidocs/spot/en>`_. I am in no way affiliated with Binance, use at your own risk.

If you came here looking for the `Binance exchange <https://www.binance.com/?ref=10099792>`_ to purchase cryptocurrencies, then `go here <https://www.binance.com/?ref=10099792>`_.
If you want to automate interactions with Binance stick around.

If you're interested in Binance's new DEX Binance Chain see my `python-binance-chain library <https://github.com/sammchardy/python-binance-chain>`_

Source code
  https://github.com/sammchardy/python-binance

Documentation
  https://python-binance.readthedocs.io/en/latest/

Binance API Telegram
  https://t.me/binance_api_english

Blog with examples including async
  https://sammchardy.github.io

- `Async basics for Binance <https://sammchardy.github.io/binance/2021/05/01/async-binance-basics.html>`_
- `Understanding Binance Order Filters <https://sammchardy.github.io/binance/2021/05/03/binance-order-filters.html>`_

Make sure you update often and check the `Changelog <https://python-binance.readthedocs.io/en/latest/changelog.html>`_ for new features and bug fixes.

Features
--------

- Implementation of all General, Market Data and Account endpoints.
- Asyncio implementation
- Testnet support for Spot, Futures and Vanilla Options
- Simple handling of authentication include RSA keys
- No need to generate timestamps yourself, the wrapper does it for you
- Response exception handling
- Websocket handling with reconnection and multiplexed connections
- Symbol Depth Cache
- Historical Kline/Candle fetching function
- Withdraw functionality
- Deposit addresses
- Margin Trading
- Futures Trading
- Vanilla Options
- Support other domains (.us, .jp, etc)

Upgrading to v1.0.0+
--------------------

The breaking changes include the migration from wapi to sapi endpoints which related to the
wallet endpoints detailed in the `Binance Docs <https://binance-docs.github.io/apidocs/spot/en/#wallet-endpoints>`_

The other breaking change is for websocket streams and the Depth Cache Manager which have been
converted to use Asynchronous Context Managers. See examples in the Async section below or view the
`websockets <https://python-binance.readthedocs.io/en/latest/websockets.html>`_ and
`depth cache <https://python-binance.readthedocs.io/en/latest/depth_cache.html>`_ docs.

Quick Start
-----------

`Register an account with Binance <https://accounts.binance.com/en/register?ref=10099792>`_.

`Generate an API Key <https://www.binance.com/en/my/settings/api-management>`_ and assign relevant permissions.

If you are using an exchange from the US, Japan or other TLD then make sure pass `tld='us'` when creating the
client.

To use the `Spot <https://testnet.binance.vision/>`_ or `Vanilla Options <https://testnet.binanceops.com/>`_ Testnet,
pass `testnet=True` when creating the client.


.. code:: bash

    pip install python-binance


.. code:: python

    from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
    client = Client(api_key, api_secret)

    # get market depth
    depth = client.get_order_book(symbol='BNBBTC')

    # place a test market buy order, to place an actual order use the create_order function
    order = client.create_test_order(
        symbol='BNBBTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=100)

    # get all symbol prices
    prices = client.get_all_tickers()

    # withdraw 100 ETH
    # check docs for assumptions around withdrawals
    from binance.exceptions import BinanceAPIException
    try:
        result = client.withdraw(
            asset='ETH',
            address='<eth_address>',
            amount=100)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")

    # fetch list of withdrawals
    withdraws = client.get_withdraw_history()

    # fetch list of ETH withdrawals
    eth_withdraws = client.get_withdraw_history(coin='ETH')

    # get a deposit address for BTC
    address = client.get_deposit_address(coin='BTC')

    # get historical kline data from any date range

    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    # fetch 30 minute klines for the last month of 2017
    klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

    # fetch weekly klines since it listed
    klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

    # socket manager using threads
    twm = ThreadedWebsocketManager()
    twm.start()

    # depth cache manager using threads
    dcm = ThreadedDepthCacheManager()
    dcm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    def handle_dcm_message(depth_cache):
        print(f"symbol {depth_cache.symbol}")
        print("top 5 bids")
        print(depth_cache.get_bids()[:5])
        print("top 5 asks")
        print(depth_cache.get_asks()[:5])
        print("last update time {}".format(depth_cache.update_time))

    twm.start_kline_socket(callback=handle_socket_message, symbol='BNBBTC')

    dcm.start_depth_cache(callback=handle_dcm_message, symbol='ETHBTC')

    # replace with a current options symbol
    options_symbol = 'BTC-210430-36000-C'
    dcm.start_options_depth_cache(callback=handle_dcm_message, symbol=options_symbol)


For more `check out the documentation <https://python-binance.readthedocs.io/en/latest/>`_.

Async Example
-------------

Read `Async basics for Binance <https://sammchardy.github.io/binance/2021/05/01/async-binance-basics.html>`_
for more information.

.. code:: python

    import asyncio
    import json

    from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

    async def main():

        # initialise the client
        client = await AsyncClient.create()

        # run some simple requests
        print(json.dumps(await client.get_exchange_info(), indent=2))

        print(json.dumps(await client.get_symbol_ticker(symbol="BTCUSDT"), indent=2))

        # initialise websocket factory manager
        bsm = BinanceSocketManager(client)

        # create listener using async with
        # this will exit and close the connection after 5 messages
        async with bsm.trade_socket('ETHBTC') as ts:
            for _ in range(5):
                res = await ts.recv()
                print(f'recv {res}')

        # get historical kline data from any date range

        # fetch 1 minute klines for the last day up until now
        klines = client.get_historical_klines("BNBBTC", AsyncClient.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

        # use generator to fetch 1 minute klines for the last day up until now
        async for kline in await client.get_historical_klines_generator("BNBBTC", AsyncClient.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
            print(kline)

        # fetch 30 minute klines for the last month of 2017
        klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

        # fetch weekly klines since it listed
        klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

        # setup an async context the Depth Cache and exit after 5 messages
        async with DepthCacheManager(client, symbol='ETHBTC') as dcm_socket:
            for _ in range(5):
                depth_cache = await dcm_socket.recv()
                print(f"symbol {depth_cache.symbol} updated:{depth_cache.update_time}")
                print("Top 5 asks:")
                print(depth_cache.get_asks()[:5])
                print("Top 5 bids:")
                print(depth_cache.get_bids()[:5])

        # Vanilla options Depth Cache works the same, update the symbol to a current one
        options_symbol = 'BTC-210430-36000-C'
        async with OptionsDepthCacheManager(client, symbol=options_symbol) as dcm_socket:
            for _ in range(5):
                depth_cache = await dcm_socket.recv()
                count += 1
                print(f"symbol {depth_cache.symbol} updated:{depth_cache.update_time}")
                print("Top 5 asks:")
                print(depth_cache.get_asks()[:5])
                print("Top 5 bids:")
                print(depth_cache.get_bids()[:5])

        await client.close_connection()

    if __name__ == "__main__":

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())


Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance Chain <https://testnet.binance.org/>`_ check out my `python-binance-chain <https://github.com/sammchardy/python-binance-chain>`_ library.

If you use `Kucoin <https://www.kucoin.com/?rcode=E42cWB>`_ check out my `python-kucoin <https://github.com/sammchardy/python-kucoin>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

.. image:: https://ga-beacon.appspot.com/UA-111417213-1/github/python-binance?pixel&useReferer

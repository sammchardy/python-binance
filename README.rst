=======================================
Welcome to python-binance v0.7.11-async
=======================================

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

This is an unofficial Python wrapper for the `Binance exchange REST API v3 <https://github.com/binance/binance-spot-api-docs>`_. I am in no way affiliated with Binance, use at your own risk.

If you came here looking for the `Binance exchange <https://www.binance.com/?ref=10099792>`_ to purchase cryptocurrencies, then `go here <https://www.binance.com/?ref=10099792>`_. If you want to automate interactions with Binance stick around.

If you're interested in Binance's new DEX Binance Chain see my `python-binance-chain library <https://github.com/sammchardy/python-binance-chain>`_

Source code
  https://github.com/sammchardy/python-binance

Documentation
  https://python-binance.readthedocs.io/en/latest/

Binance API Telegram
  https://t.me/binance_api_english

Blog with examples
  https://sammchardy.github.io

Make sure you update often and check the `Changelog <https://python-binance.readthedocs.io/en/latest/changelog.html>`_ for new features and bug fixes.

Features
--------

- Implementation of all General, Market Data and Account endpoints.
- Asyncio implementation
- Simple handling of authentication
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

Quick Start
-----------

`Register an account with Binance <https://accounts.binance.com/en/register?ref=10099792>`_.

`Generate an API Key <https://www.binance.com/en/my/settings/api-management>`_ and assign relevant permissions.

.. code:: bash

    pip install python-binance


.. code:: python

    from binance.client import Client
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
    from binance.exceptions import BinanceAPIException, BinanceWithdrawException
    try:
        result = client.withdraw(
            asset='ETH',
            address='<eth_address>',
            amount=100)
    except BinanceAPIException as e:
        print(e)
    except BinanceWithdrawException as e:
        print(e)
    else:
        print("Success")

    # fetch list of withdrawals
    withdraws = client.get_withdraw_history()

    # fetch list of ETH withdrawals
    eth_withdraws = client.get_withdraw_history(asset='ETH')

    # get a deposit address for BTC
    address = client.get_deposit_address(asset='BTC')

    # start aggregated trade websocket for BNBBTC
    def process_message(msg):
        print("message type: {}".format(msg['e']))
        print(msg)
        # do something

    from binance.websockets import BinanceSocketManager
    bm = BinanceSocketManager(client)
    bm.start_aggtrade_socket('BNBBTC', process_message)
    bm.start()

    # get historical kline data from any date range

    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    # fetch 30 minute klines for the last month of 2017
    klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

    # fetch weekly klines since it listed
    klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

For more `check out the documentation <https://python-binance.readthedocs.io/en/latest/>`_.

Async Example
-------------

.. code:: python

    import asyncio
    import json

    from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

    dcm1 = None
    loop = None

    async def main():
        global dcm1, loop

        # initialise the client
        client = await AsyncClient.create()

        # run some simple requests
        print(json.dumps(await client.get_exchange_info(), indent=2))

        print(json.dumps(await client.get_symbol_ticker(symbol="BTCUSDT"), indent=2))

        # initialise websocket factory manager
        bsm = BinanceSocketManager(client, loop)

        # create listener using async with
        # this will exit and close the connection after 5 messages
        async with bsm.trade_socket('ETHBTC') as ts:
            count = 0
            while count < 5:
                res = await ts.recv()
                print(f'recv {res}')
                if res:
                    count += 1

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
        async with DepthCacheManager(client, loop, 'ETHBTC') as dcm_socket:
            count = 0
            while count < 5:
                depth_cache = await dcm_socket.recv()
                if not depth_cache:
                    continue
                count += 1
                print(f"symbol {depth_cache.symbol} updated:{depth_cache.update_time}")
                print("Top 5 asks:")
                print(depth_cache.get_asks()[:5])
                print("Top 5 bids:")
                print(depth_cache.get_bids()[:5])

        # Vanilla options Depth Cache works the same, update the symbol to a current one
        options_symbol = 'BTC-210430-36000-C'
        async with OptionsDepthCacheManager(client, loop, options_symbol) as dcm_socket:
            count = 0
            while count < 5:
                depth_cache = await dcm_socket.recv()
                if not depth_cache:
                    continue
                count += 1
                print(f"symbol {depth_cache.symbol} updated:{depth_cache.update_time}")
                print("Top 5 asks:")
                print(depth_cache.get_asks()[:5])
                print("Top 5 bids:")
                print(depth_cache.get_bids()[:5])
            print('finished options dcm socket')


        while True:
            print("doing a sleep")
            await asyncio.sleep(20, loop=loop)

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

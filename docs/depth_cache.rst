Depth Cache
===========

To follow the depth cache updates for a symbol use the `DepthCacheManager`. For vanilla options use the
`OptionsDepthCacheManager`.

Create the manager like so, passing the api client, symbol and an optional callback function.

.. code:: python

    from binance.depthcache import DepthCacheManager
    dcm = DepthCacheManager(client, 'BNBBTC')

The `DepthCacheManager` returns an Asynchronous Context Manager which can be used with `async for`
or by interacting with the `__aenter__` and `__aexit__` functions

By default the depth cache will fetch the order book via REST request every 30 minutes.
This duration can be changed by using the `refresh_interval` parameter. To disable the refresh pass 0 or None.
The socket connection will stay open receiving updates to be replayed once the full order book is received.

Share a Socket Manager
----------------------

Here dcm1 and dcm2 share the same instance of BinanceSocketManager

.. code:: python

    from binance.websockets import BinanceSocketManager
    from binance.depthcache import DepthCacheManager
    bm = BinanceSocketManager(client)
    dcm1 = DepthCacheManager(client, 'BNBBTC', bm=bm)
    dcm2 = DepthCacheManager(client, 'ETHBTC', bm=bm)

Websocket Errors
----------------

If the underlying websocket is disconnected and is unable to reconnect None is returned for the depth_cache parameter.

Examples
--------

.. code:: python

    # 1 hour interval refresh
    dcm = DepthCacheManager(client, 'BNBBTC', refresh_interval=60*60)

    # disable refreshing
    dcm = DepthCacheManager(client, 'BNBBTC', refresh_interval=0)

.. code:: python

    async with dcm(client, symbol='ETHBTC') as dcm_socket:
        depth_cache = await dcm_socket.recv()
        print("symbol {}".format(depth_cache.symbol))
        print("top 5 bids")
        print(depth_cache.get_bids()[:5])
        print("top 5 asks")
        print(depth_cache.get_asks()[:5])
        print("last update time {}".format(depth_cache.update_time))

To use the magic `__aenter__` and `__aexit__` functions to use this class without the `async with`

.. code:: python

    dcm = DepthCacheManager(client, 'BNBBTC')

    await dcm.__aenter__()
    depth_cache = await dcm.recv()
    print("symbol {}".format(depth_cache.symbol))
    print("top 5 bids")
    print(depth_cache.get_bids()[:5])
    print("top 5 asks")
    print(depth_cache.get_asks()[:5])
    print("last update time {}".format(depth_cache.update_time))

    # exit the context manager
    await dcm.__aexit__(None, None, None)

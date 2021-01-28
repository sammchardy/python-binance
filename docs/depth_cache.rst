Depth Cache
===========

To follow the depth cache updates for a symbol use the `DepthCacheManager`

Create the manager like so, passing the api client, symbol and an optional callback function.

.. code:: python

    from binance.depthcache import DepthCacheManager
    dcm = DepthCacheManager(client, 'BNBBTC', callback=process_depth)

The callback function receives the current `DepthCache` object which allows access to a pre-sorted
list of bids or asks able to be filtered as required.

Access the symbol value from the `depth_cache` object in case you have multiple caches using the same callback.

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
    dcm1 = DepthCacheManager(client, 'BNBBTC', callback=process_depth1, bm=bm)
    dcm2 = DepthCacheManager(client, 'ETHBTC', callback=process_depth2, bm=bm)

Because they both share the same BinanceSocketManager calling close can close both message streams.

.. code:: python

    # close just dcm1 stream
    dcm1.close()

    # close the underlying socket manager as well
    dcm1.close(close_socket=True)

Websocket Errors
----------------

If the underlying websocket is disconnected and is unable to reconnect None is returned for the depth_cache parameter.

Examples
--------

.. code:: python

    # 1 hour interval refresh
    dcm = DepthCacheManager(client, 'BNBBTC', callback=process_depth, refresh_interval=60*60)

    # disable refreshing
    dcm = DepthCacheManager(client, 'BNBBTC', callback=process_depth, refresh_interval=0)

.. code:: python

    def process_depth(depth_cache):
        if depth_cache is not None:
            print("symbol {}".format(depth_cache.symbol))
            print("top 5 bids")
            print(depth_cache.get_bids()[:5])
            print("top 5 asks")
            print(depth_cache.get_asks()[:5])
            print("last update time {}".format(depth_cache.update_time)
        else:
            # depth cache had an error and needs to be restarted

At any time the current `DepthCache` object can be retrieved from the `DepthCacheManager`

.. code:: python

    depth_cache = dcm.get_depth_cache()
    if depth_cache is not None:
        print("symbol {}".format(depth_cache.symbol))
        print("top 5 bids")
        print(depth_cache.get_bids()[:5])
        print("top 5 asks")
        print(depth_cache.get_asks()[:5])
            print("last update time {}".format(depth_cache.update_time)
    else:
        # depth cache had an error and needs to be restarted

To stop the `DepthCacheManager` from returning messages use the `close` method.
This will close the internal websocket and this instance of the `DepthCacheManager` will not be able to be used again.

.. code:: python

    dcm.close()

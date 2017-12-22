Depth Cache
===========

To follow the depth cache updates for a symbol use the `DepthCacheManager`

Create the manager like so, passing the api client, symbol and callback function.

.. code:: python

    from binance.depthcache import DepthCacheManager
    dcm = DepthCacheManager(client, 'BNBBTC', process_depth)

The callback function receives the current `DepthCache` object which allows access to a pre-sorted
list of bids or asks able to be filtered as required.

Access the symbol value from the `depth_cache` object in case you have multiple caches using the same callback.

.. code:: python

    def process_depth(depth_cache):
        print("symbol {}".format(depth_cache.symbol))
        print("top 5 bids")
        print(depth_cache.get_bids()[:5])
        print("top 5 asks")
        print(depth_cache.get_asks()[:5])

At any time the current `DepthCache` object can be retrieved from the `DepthCacheManager`

.. code:: python

    depth_cache = dcm.get_depth_cache()
    print("symbol {}".format(depth_cache.symbol))
    print("top 5 bids")
    print(depth_cache.get_bids()[:5])
    print("top 5 asks")
    print(depth_cache.get_asks()[:5])

To stop the `DepthCacheManager` from returning messages use the `close` method.
This will close the internal websocket and this instance of the `DepthCacheManager` will not be able to be used again.

.. code:: python

    dcm.close()

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-binance/docs/depth_cache?pixel

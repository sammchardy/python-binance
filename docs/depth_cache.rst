Depth Cache
===========

To follow the depth cache updates for a symbol use the `DepthCacheManager`

Create the manager like so, passing the api client, symbol and callback function.

.. code:: python

    from binance.depthcache import DepthCacheManager
    dcm = DepthCacheManager(client, 'BNBBTC', process_depth)

The callback function receives the current `DepthCache` object which allows access to a pre-sorted
list of bids or asks able to be filtered as required.

.. code:: python

    def process_depth(depth_cache):
        print("top 5 bids")
        print(depth_cache.get_bids()[:5])
        print("top 5 asks")
        print(depth_cache.get_asks()[:5])

At any time the current `DepthCache` object can be retrieved from the `DepthCacheManager`

.. code:: python

    depth_cache = dcm.get_depth_cache()
    print("top 5 bids")
    print(depth_cache.get_bids()[:5])
    print("top 5 asks")
    print(depth_cache.get_asks()[:5])

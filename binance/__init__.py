"""An unofficial Python wrapper for the Binance exchange API v3

.. moduleauthor:: Sam McHardy

"""

__version__ = '1.0.16'

from binance.client import Client, AsyncClient  # noqa
from binance.depthcache import DepthCacheManager, OptionsDepthCacheManager, ThreadedDepthCacheManager  # noqa
from binance.streams import BinanceSocketManager, ThreadedWebsocketManager  # noqa

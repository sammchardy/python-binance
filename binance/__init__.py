"""An unofficial Python wrapper for the Binance exchange API v3

.. moduleauthor:: Sam McHardy

"""

__version__ = '0.7.11-async'

from binance.client import Client, AsyncClient  # noqa
from binance.depthcache import DepthCacheManager, OptionsDepthCacheManager  # noqa
from binance.streams import BinanceSocketManager  # noqa

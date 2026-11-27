from binance.ws.depthcache import DepthCache
from decimal import Decimal
import pytest

TEST_SYMBOL = "BNBBTC"


@pytest.fixture
def fresh_cache():
    return DepthCache(TEST_SYMBOL, Decimal)


def test_add_bids(fresh_cache):
    """Verify basic functionality for adding a bid to the cache"""
    high_bid = [0.111, 489]
    mid_bid = [0.018, 300]
    low_bid = [0.001, 100]
    for bid in [high_bid, low_bid, mid_bid]:
        fresh_cache.add_bid(bid)

    bids = fresh_cache.get_bids()

    assert len(bids) == 3

    assert bids == sorted(bids, reverse=True)

    assert isinstance(bids[0][0], Decimal)
    assert isinstance(bids[0][1], Decimal)


def test_add_asks(fresh_cache):
    """Verify basic functionality for adding an ask to the cache"""
    high_ask = [0.111, 489]
    mid_ask = [0.018, 300]
    low_ask = [0.001, 100]

    for ask in [high_ask, low_ask, mid_ask]:
        fresh_cache.add_ask(ask)

    asks = fresh_cache.get_asks()

    # Three asks should be in the cache
    assert len(asks) == 3

    # Lowest ask price should be first (ascending order)
    assert asks == sorted(asks)

    assert isinstance(asks[0][0], Decimal)
    assert isinstance(asks[0][1], Decimal)


def _stub_client():
    from types import SimpleNamespace

    return SimpleNamespace(tld="com", testnet=False, demo=False, https_proxy=None)


def _socket_manager(client):
    from binance.ws.streams import BinanceSocketManager

    return BinanceSocketManager(client)


@pytest.mark.parametrize("limit", [5, 20])
def test_futures_depth_cache_manager_uses_limit_for_stream(limit):
    """The futures depth stream must subscribe with the requested limit"""
    from binance.ws.depthcache import FuturesDepthCacheManager

    client = _stub_client()
    dcm = FuturesDepthCacheManager(
        client, "BTCUSDT", bm=_socket_manager(client), limit=limit
    )
    socket = dcm._get_socket()

    assert socket._path == f"btcusdt@depth{limit}"


def test_futures_depth_cache_manager_default_limit_stream():
    from binance.ws.depthcache import FuturesDepthCacheManager

    client = _stub_client()
    dcm = FuturesDepthCacheManager(client, "BTCUSDT", bm=_socket_manager(client))
    socket = dcm._get_socket()

    assert socket._path == "btcusdt@depth10"


@pytest.mark.parametrize("limit", [5, 20])
def test_options_depth_cache_manager_uses_limit_for_stream(limit):
    """The options depth stream must subscribe with the requested limit"""
    from binance.ws.depthcache import OptionsDepthCacheManager

    client = _stub_client()
    dcm = OptionsDepthCacheManager(
        client, "BTC-200630-9000-P", bm=_socket_manager(client), limit=limit
    )
    socket = dcm._get_socket()

    assert socket._path == f"btc-200630-9000-p@depth{limit}@500ms"

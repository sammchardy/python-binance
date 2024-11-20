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

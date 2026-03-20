"""Integration tests for USD-M futures WebSocket URL category support.

Tests URL construction for all affected methods across production, testnet, and demo environments.
Also performs a live connection test against the demo environment.
"""

import asyncio
import pytest
import pytest_asyncio

from binance.async_client import AsyncClient
from binance.enums import FuturesType
from binance.ws.streams import BinanceSocketManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ws_url(sock):
    """Extract the full WebSocket URL that would be used for connection."""
    return f"{sock._url}{sock._prefix}{sock._path}"


def _make_bsm(client):
    return BinanceSocketManager(client)


# ---------------------------------------------------------------------------
# Fixtures — one per environment
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def prod_client():
    client = AsyncClient(api_key="x", api_secret="y")
    yield client
    await client.close_connection()


@pytest_asyncio.fixture
async def testnet_client():
    client = AsyncClient(api_key="x", api_secret="y", testnet=True)
    yield client
    await client.close_connection()


@pytest_asyncio.fixture
async def demo_client():
    client = AsyncClient(api_key="x", api_secret="y", demo=True)
    yield client
    await client.close_connection()


# ---------------------------------------------------------------------------
# 1. Market data — Public category (USD-M)
# ---------------------------------------------------------------------------


class TestPublicCategory:
    def test_symbol_ticker_futures_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.symbol_ticker_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/public/stream?streams=btcusdt@bookTicker"
        )

    def test_futures_depth_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_depth_socket("btcusdt", depth="10")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/public/stream?streams=btcusdt@depth10"
        )

    def test_futures_rpi_depth_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_rpi_depth_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/public/stream?streams=btcusdt@rpiDepth@500ms"
        )

    def test_all_ticker_futures_default_bookTicker(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.all_ticker_futures_socket()  # default !bookTicker → public
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/public/stream?streams=!bookTicker"
        )

    def test_futures_depth_socket_default_depth(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_depth_socket("ethusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/public/stream?streams=ethusdt@depth10"
        )


# ---------------------------------------------------------------------------
# 2. Market data — Market category (USD-M)
# ---------------------------------------------------------------------------


class TestMarketCategory:
    def test_aggtrade_futures_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.aggtrade_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=btcusdt@aggTrade"
        )

    def test_kline_futures_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.kline_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/ws/btcusdt_perpetual@continuousKline_1m"
        )

    def test_futures_ticker_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_ticker_socket()
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=!ticker@arr"
        )

    def test_symbol_mark_price_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.symbol_mark_price_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=btcusdt@markPrice@1s"
        )

    def test_symbol_mark_price_socket_slow(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.symbol_mark_price_socket("btcusdt", fast=False)
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=btcusdt@markPrice"
        )

    def test_all_mark_price_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.all_mark_price_socket()
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=!markPrice@arr@1s"
        )

    def test_individual_symbol_ticker_futures_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.individual_symbol_ticker_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=btcusdt@ticker"
        )

    def test_all_ticker_futures_ticker_arr(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.all_ticker_futures_socket("!ticker@arr")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=!ticker@arr"
        )


# ---------------------------------------------------------------------------
# 3. Multiplex socket
# ---------------------------------------------------------------------------


class TestMultiplex:
    def test_futures_multiplex_default_market(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_multiplex_socket(["btcusdt@aggTrade", "ethusdt@aggTrade"])
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/market/stream?streams=btcusdt@aggTrade/ethusdt@aggTrade"
        )

    def test_futures_multiplex_public(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_multiplex_socket(["btcusdt@depth10"], category="public")
        assert (
            _ws_url(sock)
            == "wss://fstream.binance.com/public/stream?streams=btcusdt@depth10"
        )


# ---------------------------------------------------------------------------
# 4. COIN-M streams — no category (unchanged)
# ---------------------------------------------------------------------------


class TestCoinMUnchanged:
    def test_futures_coin_ticker_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.futures_coin_ticker_socket()
        url = _ws_url(sock)
        assert "dstream.binance.com/" in url
        assert "/market/" not in url
        assert "/public/" not in url

    def test_index_price_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.index_price_socket("btcusd")
        url = _ws_url(sock)
        assert "dstream.binance.com/" in url
        assert "/market/" not in url

    def test_aggtrade_futures_coin_m(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.aggtrade_futures_socket(
            "btcusd_perp", futures_type=FuturesType.COIN_M
        )
        url = _ws_url(sock)
        assert "dstream.binance.com/" in url
        assert "/market/" not in url


# ---------------------------------------------------------------------------
# 5. Portfolio margin — unchanged (pm/ prefix, path-based listenKey)
# ---------------------------------------------------------------------------


class TestPortfolioMarginUnchanged:
    def test_portfolio_margin_url_has_pm(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.portfolio_margin_socket()
        assert "fstream.binance.com/pm/" in sock._url
        assert "/private/" not in sock._url


# ---------------------------------------------------------------------------
# 6. Testnet environment — category applied to fstream
# ---------------------------------------------------------------------------


class TestTestnetEnvironment:
    def test_aggtrade_testnet(self, testnet_client):
        bsm = _make_bsm(testnet_client)
        sock = bsm.aggtrade_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://stream.binancefuture.com/market/stream?streams=btcusdt@aggTrade"
        )

    def test_depth_testnet(self, testnet_client):
        bsm = _make_bsm(testnet_client)
        sock = bsm.futures_depth_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://stream.binancefuture.com/public/stream?streams=btcusdt@depth10"
        )


# ---------------------------------------------------------------------------
# 7. Demo environment — category applied to fstream
# ---------------------------------------------------------------------------


class TestDemoEnvironment:
    def test_aggtrade_demo(self, demo_client):
        bsm = _make_bsm(demo_client)
        sock = bsm.aggtrade_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binancefuture.com/market/stream?streams=btcusdt@aggTrade"
        )

    def test_depth_demo(self, demo_client):
        bsm = _make_bsm(demo_client)
        sock = bsm.futures_depth_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binancefuture.com/public/stream?streams=btcusdt@depth10"
        )

    def test_mark_price_demo(self, demo_client):
        bsm = _make_bsm(demo_client)
        sock = bsm.symbol_mark_price_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binancefuture.com/market/stream?streams=btcusdt@markPrice@1s"
        )

    def test_book_ticker_demo(self, demo_client):
        bsm = _make_bsm(demo_client)
        sock = bsm.symbol_ticker_futures_socket("btcusdt")
        assert (
            _ws_url(sock)
            == "wss://fstream.binancefuture.com/public/stream?streams=btcusdt@bookTicker"
        )


# ---------------------------------------------------------------------------
# 8. Spot streams — completely unchanged (no category)
# ---------------------------------------------------------------------------


class TestSpotUnchanged:
    def test_depth_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.depth_socket("btcusdt")
        url = _ws_url(sock)
        assert "stream.binance.com" in url
        assert "/public/" not in url
        assert "/market/" not in url

    def test_kline_socket(self, prod_client):
        bsm = _make_bsm(prod_client)
        sock = bsm.kline_socket("btcusdt")
        url = _ws_url(sock)
        assert "/market/" not in url


# ---------------------------------------------------------------------------
# 9. Live connection test — demo environment
#    Connects to a real WebSocket and verifies data arrives.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_live_demo_market_stream():
    """Connect to demo fstream market WebSocket and verify a message arrives."""
    client = AsyncClient(api_key="x", api_secret="y", demo=True)
    bsm = _make_bsm(client)

    sock = bsm.symbol_mark_price_socket("btcusdt")
    url = _ws_url(sock)
    print(f"\nConnecting to: {url}")

    try:
        async with sock as stream:
            msg = await asyncio.wait_for(stream.recv(), timeout=10)
            assert msg is not None
            # stream?streams= prefix wraps payload in {"stream": ..., "data": ...}
            data = msg.get("data", msg)
            assert "e" in data  # event type field
            print(f"Received message: event={data.get('e')}, symbol={data.get('s')}")
    finally:
        await client.close_connection()


@pytest.mark.asyncio
async def test_live_demo_public_stream():
    """Connect to demo fstream public WebSocket and verify a message arrives."""
    client = AsyncClient(api_key="x", api_secret="y", demo=True)
    bsm = _make_bsm(client)

    sock = bsm.futures_depth_socket("btcusdt")
    url = _ws_url(sock)
    print(f"\nConnecting to: {url}")

    try:
        async with sock as stream:
            msg = await asyncio.wait_for(stream.recv(), timeout=10)
            assert msg is not None
            data = msg.get("data", msg)
            assert "lastUpdateId" in data or "e" in data
            print(f"Received depth message with keys: {list(data.keys())}")
    finally:
        await client.close_connection()

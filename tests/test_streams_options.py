import sys
import pytest
from binance import BinanceSocketManager

pytestmark = [
    pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+"),
    pytest.mark.asyncio
]

# Test constants
OPTION_SYMBOL = "BTC-250328-40000-P"
UNDERLYING_SYMBOL = "BTC"
EXPIRATION_DATE = "250328"
INTERVAL = "1m"
DEPTH = "20"

async def test_options_ticker(clientAsync):
    """Test options ticker socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_ticker_socket(OPTION_SYMBOL)
    async with socket as ts:
        msg = await ts.recv()
        assert msg['e'] == '24hrTicker'
    await clientAsync.close_connection()

async def test_options_ticker_by_expiration(clientAsync):
    """Test options ticker by expiration socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_ticker_by_expiration_socket(UNDERLYING_SYMBOL, EXPIRATION_DATE)
    async with socket as ts:
        msg = await ts.recv()
        assert len(msg) > 0
    await clientAsync.close_connection()

async def test_options_recent_trades(clientAsync):
    """Test options recent trades socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_recent_trades_socket(UNDERLYING_SYMBOL)
    async with socket as ts:
        msg = await ts.recv()
        assert msg['e'] == 'trade'
    await clientAsync.close_connection()

async def test_options_kline(clientAsync):
    """Test options kline socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_kline_socket(OPTION_SYMBOL, INTERVAL)
    async with socket as ts:
        msg = await ts.recv()
        assert msg['e'] == 'kline'
    await clientAsync.close_connection()

async def test_options_depth(clientAsync):
    """Test options depth socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_depth_socket(OPTION_SYMBOL, DEPTH)
    async with socket as ts:
        msg = await ts.recv()
        assert msg['e'] == 'depth'
    await clientAsync.close_connection()

async def test_options_multiplex(clientAsync):
    """Test options multiplex socket"""
    bm = BinanceSocketManager(clientAsync)
    streams = [
        f"{OPTION_SYMBOL}@ticker",
        f"{OPTION_SYMBOL}@trade",
    ]
    socket = bm.options_multiplex_socket(streams)
    async with socket as ts:
        msg = await ts.recv()
        assert 'stream' in msg
    await clientAsync.close_connection()

async def test_options_open_interest(clientAsync):
    """Test options open interest socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_open_interest_socket(UNDERLYING_SYMBOL, EXPIRATION_DATE)
    async with socket as ts:
        msg = await ts.recv()
        assert len(msg) > 0
    await clientAsync.close_connection()

async def test_options_mark_price(clientAsync):
    """Test options mark price socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_mark_price_socket(UNDERLYING_SYMBOL)
    async with socket as ts:
        msg = await ts.recv()
        assert len(msg) > 0
    await clientAsync.close_connection()

async def test_options_index_price(clientAsync):
    """Test options index price socket"""
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_index_price_socket('ETHUSDT')
    async with socket as ts:
        msg = await ts.recv()
        assert msg['e'] == 'index'
    await clientAsync.close_connection()

import sys
import pytest
import logging
from binance import BinanceSocketManager

pytestmark = [
    pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+"),
    pytest.mark.asyncio
]

# Configure logger for this module
logger = logging.getLogger(__name__)

# Test constants
OPTION_SYMBOL = "BTC-251226-60000-P"
UNDERLYING_SYMBOL = "BTC"
EXPIRATION_DATE = "251226"
INTERVAL = "1m"
DEPTH = "20"

async def test_options_ticker(clientAsync):
    """Test options ticker socket"""
    logger.info(f"Starting options ticker test for symbol: {OPTION_SYMBOL}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_ticker_socket(OPTION_SYMBOL)
    async with socket as ts:
        logger.debug("Waiting for ticker message...")
        msg = await ts.recv()
        logger.info(f"Received ticker message: {msg}")
        assert msg['e'] == '24hrTicker'
    logger.info("Options ticker test completed successfully")
    await clientAsync.close_connection()

async def test_options_ticker_by_expiration(clientAsync):
    """Test options ticker by expiration socket"""
    logger.info(f"Starting options ticker by expiration test for {UNDERLYING_SYMBOL}, expiration: {EXPIRATION_DATE}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_ticker_by_expiration_socket(UNDERLYING_SYMBOL, EXPIRATION_DATE)
    async with socket as ts:
        logger.debug("Waiting for ticker by expiration message...")
        msg = await ts.recv()
        logger.info(f"Received {len(msg)} ticker messages")
        assert len(msg) > 0
    logger.info("Options ticker by expiration test completed successfully")
    await clientAsync.close_connection()

async def test_options_recent_trades(clientAsync):
    """Test options recent trades socket"""
    logger.info(f"Starting options recent trades test for {UNDERLYING_SYMBOL}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_recent_trades_socket(UNDERLYING_SYMBOL)
    async with socket as ts:
        logger.debug("Waiting for trade message...")
        msg = await ts.recv()
        logger.info(f"Received trade message: {msg}")
        assert msg['e'] == 'trade'
    logger.info("Options recent trades test completed successfully")
    await clientAsync.close_connection()

async def test_options_kline(clientAsync):
    """Test options kline socket"""
    logger.info(f"Starting options kline test for {OPTION_SYMBOL}, interval: {INTERVAL}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_kline_socket(OPTION_SYMBOL, INTERVAL)
    async with socket as ts:
        logger.debug("Waiting for kline message...")
        msg = await ts.recv()
        logger.info(f"Received kline message: {msg}")
        assert msg['e'] == 'kline'
    logger.info("Options kline test completed successfully")
    await clientAsync.close_connection()

async def test_options_depth(clientAsync):
    """Test options depth socket"""
    logger.info(f"Starting options depth test for {OPTION_SYMBOL}, depth: {DEPTH}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_depth_socket(OPTION_SYMBOL, DEPTH)
    async with socket as ts:
        logger.debug("Waiting for depth message...")
        msg = await ts.recv()
        logger.info(f"Received depth message: {msg}")
        assert msg['e'] == 'depth'
    logger.info("Options depth test completed successfully")
    await clientAsync.close_connection()

async def test_options_multiplex(clientAsync):
    """Test options multiplex socket"""
    streams = [
        f"{OPTION_SYMBOL}@ticker",
        f"{OPTION_SYMBOL}@trade",
    ]
    logger.info(f"Starting options multiplex test with streams: {streams}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_multiplex_socket(streams)
    async with socket as ts:
        logger.debug("Waiting for multiplex message...")
        msg = await ts.recv()
        logger.info(f"Received multiplex message: {msg}")
        assert 'stream' in msg
    logger.info("Options multiplex test completed successfully")
    await clientAsync.close_connection()

async def test_options_open_interest(clientAsync):
    """Test options open interest socket"""
    logger.info(f"Starting options open interest test for {UNDERLYING_SYMBOL}, expiration: {EXPIRATION_DATE}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_open_interest_socket(UNDERLYING_SYMBOL, EXPIRATION_DATE)
    async with socket as ts:
        logger.debug("Waiting for open interest message...")
        msg = await ts.recv()
        logger.info(f"Received open interest message with {len(msg)} items")
        assert len(msg) > 0
    logger.info("Options open interest test completed successfully")
    await clientAsync.close_connection()

async def test_options_mark_price(clientAsync):
    """Test options mark price socket"""
    logger.info(f"Starting options mark price test for {UNDERLYING_SYMBOL}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_mark_price_socket(UNDERLYING_SYMBOL)
    async with socket as ts:
        logger.debug("Waiting for mark price message...")
        msg = await ts.recv()
        logger.info(f"Received mark price message with {len(msg)} items")
        assert len(msg) > 0
    logger.info("Options mark price test completed successfully")
    await clientAsync.close_connection()

async def test_options_index_price(clientAsync):
    """Test options index price socket"""
    symbol = 'ETHUSDT'
    logger.info(f"Starting options index price test for {symbol}")
    bm = BinanceSocketManager(clientAsync)
    socket = bm.options_index_price_socket(symbol)
    async with socket as ts:
        logger.debug("Waiting for index price message...")
        msg = await ts.recv()
        logger.info(f"Received index price message: {msg}")
        assert msg['e'] == 'index'
    logger.info("Options index price test completed successfully")
    await clientAsync.close_connection()

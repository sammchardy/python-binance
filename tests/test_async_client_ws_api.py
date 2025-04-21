import sys
import pytest

pytestmark = [pytest.mark.asyncio(), pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")]

async def test_ws_get_order_book(clientAsync):
    await clientAsync.ws_get_order_book(symbol="BTCUSDT")

async def test_ws_get_recent_trades(clientAsync):
    await clientAsync.ws_get_recent_trades(symbol="BTCUSDT")

async def test_ws_get_historical_trades(clientAsync):
    await clientAsync.ws_get_historical_trades(symbol="BTCUSDT")

async def test_ws_get_aggregate_trades(clientAsync):
    await clientAsync.ws_get_aggregate_trades(symbol="BTCUSDT")

async def test_ws_get_klines(clientAsync):
    await clientAsync.ws_get_klines(symbol="BTCUSDT", interval="1m")

async def test_ws_get_uiKlines(clientAsync):
    await clientAsync.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")

async def test_ws_get_avg_price(clientAsync):
    await clientAsync.ws_get_avg_price(symbol="BTCUSDT")

async def test_ws_get_ticker(clientAsync):
    await clientAsync.ws_get_ticker(symbol="BTCUSDT")

async def test_ws_get_trading_day_ticker(clientAsync):
    await clientAsync.ws_get_trading_day_ticker(symbol="BTCUSDT")

async def test_ws_get_symbol_ticker_window(clientAsync):
    await clientAsync.ws_get_symbol_ticker_window(symbol="BTCUSDT")

async def test_ws_get_symbol_ticker(clientAsync):
    await clientAsync.ws_get_symbol_ticker(symbol="BTCUSDT")

async def test_ws_get_orderbook_ticker(clientAsync):
    await clientAsync.ws_get_orderbook_ticker(symbol="BTCUSDT")

async def test_ws_ping(clientAsync):
    await clientAsync.ws_ping()

async def test_ws_get_time(clientAsync):
    await clientAsync.ws_get_time()

async def test_ws_get_exchange_info(clientAsync):
    await clientAsync.ws_get_exchange_info(symbol="BTCUSDT")

async def test_ws_logon(clientAsync):
    res = await clientAsync.ws_logon()
    apiKey = res.get("apiKey")
    assert apiKey

async def test_ws_user_data_stream_subscribe(clientAsync):
    """Test subscribing to user data stream"""
    await clientAsync.ws_logon()
    await clientAsync.ws_user_data_stream_subscribe()

async def test_ws_user_data_stream_unsubscribe(clientAsync):
    """Test unsubscribing from user data stream"""
    await clientAsync.ws_logon()
    await clientAsync.ws_user_data_stream_subscribe()
    await clientAsync.ws_user_data_stream_unsubscribe()

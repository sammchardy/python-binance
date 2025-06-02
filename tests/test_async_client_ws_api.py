import pytest


@pytest.mark.asyncio()
async def test_ws_get_order_book(clientAsync):
    await clientAsync.ws_get_order_book(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_recent_trades(clientAsync):
    await clientAsync.ws_get_recent_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_historical_trades(clientAsync):
    await clientAsync.ws_get_historical_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_aggregate_trades(clientAsync):
    await clientAsync.ws_get_aggregate_trades(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_klines(clientAsync):
    await clientAsync.ws_get_klines(symbol="BTCUSDT", interval="1m")


@pytest.mark.asyncio()
async def test_ws_get_uiKlines(clientAsync):
    await clientAsync.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")


@pytest.mark.asyncio()
async def test_ws_get_avg_price(clientAsync):
    await clientAsync.ws_get_avg_price(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_ticker(clientAsync):
    await clientAsync.ws_get_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_trading_day_ticker(clientAsync):
    await clientAsync.ws_get_trading_day_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_symbol_ticker_window(clientAsync):
    await clientAsync.ws_get_symbol_ticker_window(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_symbol_ticker(clientAsync):
    await clientAsync.ws_get_symbol_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_get_orderbook_ticker(clientAsync):
    await clientAsync.ws_get_orderbook_ticker(symbol="BTCUSDT")


@pytest.mark.asyncio()
async def test_ws_ping(clientAsync):
    await clientAsync.ws_ping()


@pytest.mark.asyncio()
async def test_ws_get_time(clientAsync):
    await clientAsync.ws_get_time()


@pytest.mark.asyncio()
async def test_ws_get_exchange_info(clientAsync):
    await clientAsync.ws_get_exchange_info(symbol="BTCUSDT")

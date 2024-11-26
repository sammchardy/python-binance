import pytest

pytestmark = [pytest.mark.asyncio]


async def test_clientAsync_initialization(clientAsync):
    assert clientAsync.API_KEY is not None
    assert clientAsync.API_SECRET is not None


@pytest.mark.skip(reason="Endpoint not documented")
async def test_get_products(clientAsync):
    await clientAsync.get_products()


async def test_get_exchange_info(clientAsync):
    await clientAsync.get_exchange_info()


async def test_get_symbol_info(clientAsync):
    await clientAsync.get_symbol_info("BTCUSDT")


async def test_ping(clientAsync):
    await clientAsync.ping()


async def test_get_server_time(clientAsync):
    await clientAsync.get_server_time()


async def test_get_all_tickers(clientAsync):
    await clientAsync.get_all_tickers()


async def test_get_orderbook_tickers(clientAsync):
    await clientAsync.get_orderbook_tickers()


async def test_get_order_book(clientAsync):
    await clientAsync.get_order_book(symbol="BTCUSDT")


async def test_get_recent_trades(clientAsync):
    await clientAsync.get_recent_trades(symbol="BTCUSDT")


async def test_get_historical_trades(clientAsync):
    await clientAsync.get_historical_trades(symbol="BTCUSDT")


async def test_get_aggregate_trades(clientAsync):
    await clientAsync.get_aggregate_trades(symbol="BTCUSDT")


async def test_get_klines(clientAsync):
    await clientAsync.get_klines(symbol="BTCUSDT", interval="1d")


async def test_get_avg_price(clientAsync):
    await clientAsync.get_avg_price(symbol="BTCUSDT")


async def test_get_ticker(clientAsync):
    await clientAsync.get_ticker(symbol="BTCUSDT")


async def test_get_symbol_ticker(clientAsync):
    await clientAsync.get_symbol_ticker(symbol="BTCUSDT")


async def test_get_orderbook_ticker(clientAsync):
    await clientAsync.get_orderbook_ticker(symbol="BTCUSDT")


async def test_get_account(clientAsync):
    await clientAsync.get_account()


async def test_get_asset_balance(clientAsync):
    await clientAsync.get_asset_balance(asset="BTC")


async def test_get_asset_balance_no_asset_provided(clientAsync):
    await clientAsync.get_asset_balance()


async def test_get_my_trades(clientAsync):
    await clientAsync.get_my_trades(symbol="BTCUSDT")


async def test_get_system_status(clientAsync):
    await clientAsync.get_system_status()


# User Stream Endpoints


async def test_stream_get_listen_key_and_close(clientAsync):
    listen_key = await clientAsync.stream_get_listen_key()
    await clientAsync.stream_close(listen_key)


# Quoting interface endpoints


#########################
# Websocket API Requests #
#########################


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
    ticker = await clientAsync.ws_get_ticker(symbol="BTCUSDT")


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

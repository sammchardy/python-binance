import pytest
import sys

pytestmark = [pytest.mark.options, pytest.mark.asyncio, pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")]

@pytest.fixture
def options_symbol(liveClient):
    prices = liveClient.options_price()
    return prices[0]["symbol"]

async def test_options_ping(liveClientAsync):
    await liveClientAsync.options_ping()

async def test_options_time(liveClientAsync):
    await liveClientAsync.options_time()

@pytest.mark.skip(reason="Not implemented")
async def test_options_info(liveClientAsync):
    await liveClientAsync.options_info()

async def test_options_exchange_info(liveClientAsync):
    await liveClientAsync.options_exchange_info()

async def test_options_index_price(liveClientAsync):
    await liveClientAsync.options_index_price(underlying="BTCUSDT")

async def test_options_price(liveClientAsync):
    prices = await liveClientAsync.options_price()

async def test_options_mark_price(liveClientAsync):
    await liveClientAsync.options_mark_price()

async def test_options_order_book(liveClientAsync, options_symbol):
    await liveClientAsync.options_order_book(symbol=options_symbol)

async def test_options_klines(liveClientAsync, options_symbol):
    await liveClientAsync.options_klines(symbol=options_symbol, interval="1m")

async def test_options_recent_trades(liveClientAsync, options_symbol):
    await liveClientAsync.options_recent_trades(symbol=options_symbol)

async def test_options_historical_trades(liveClientAsync, options_symbol):
    await liveClientAsync.options_historical_trades(symbol=options_symbol)

# Account and trading interface endpoints

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_account_info(liveClientAsync):
    await liveClientAsync.options_account_info()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_funds_transfer(liveClientAsync):
    await liveClientAsync.options_funds_transfer()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_positions(liveClientAsync):
    await liveClientAsync.options_positions()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_bill(liveClientAsync):
    await liveClientAsync.options_bill()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_place_order(liveClientAsync):
    await liveClientAsync.options_place_order()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_test_options_place_batch_order(liveClientAsync):
    await liveClientAsync.test_options_place_batch_order()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_cancel_order(liveClientAsync):
    await liveClientAsync.options_cancel_order()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_cancel_batch_order(liveClientAsync):
    await liveClientAsync.options_cancel_batch_order()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_cancel_all_orders(liveClientAsync):
    await liveClientAsync.options_cancel_all_orders()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_query_order(liveClientAsync):
    await liveClientAsync.options_query_order()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_query_pending_orders(liveClientAsync):
    await liveClientAsync.options_query_pending_orders()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_query_order_history(liveClientAsync):
    await liveClientAsync.options_query_order_history()

@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_user_trades(liveClientAsync):
    await liveClientAsync.options_user_trades()

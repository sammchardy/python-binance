import pytest


pytestmark = [pytest.mark.options, pytest.mark.asyncio]


@pytest.fixture
def options_symbol(optionsClient):
    prices = optionsClient.options_price()
    return prices[0]["symbol"]


async def test_options_ping(optionsClientAsync):
    await optionsClientAsync.options_ping()


async def test_options_time(optionsClientAsync):
    await optionsClientAsync.options_time()


@pytest.mark.skip(reason="Not implemented")
async def test_options_info(optionsClientAsync):
    await optionsClientAsync.options_info()


async def test_options_exchange_info(optionsClientAsync):
    await optionsClientAsync.options_exchange_info()


async def test_options_index_price(optionsClientAsync):
    await optionsClientAsync.options_index_price(underlying="BTCUSDT")


async def test_options_price(optionsClientAsync):
    prices = await optionsClientAsync.options_price()


async def test_options_mark_price(optionsClientAsync):
    await optionsClientAsync.options_mark_price()


async def test_options_order_book(optionsClientAsync, options_symbol):
    await optionsClientAsync.options_order_book(symbol=options_symbol)


async def test_options_klines(optionsClientAsync, options_symbol):
    await optionsClientAsync.options_klines(symbol=options_symbol, interval="1m")


async def test_options_recent_trades(optionsClientAsync, options_symbol):
    await optionsClientAsync.options_recent_trades(symbol=options_symbol)


async def test_options_historical_trades(optionsClientAsync, options_symbol):
    await optionsClientAsync.options_historical_trades(symbol=options_symbol)


# Account and trading interface endpoints


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_account_info(optionsClientAsync):
    await optionsClientAsync.options_account_info()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_funds_transfer(optionsClientAsync):
    await optionsClientAsync.options_funds_transfer()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_positions(optionsClientAsync):
    await optionsClientAsync.options_positions()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_bill(optionsClientAsync):
    await optionsClientAsync.options_bill()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_place_order(optionsClientAsync):
    await optionsClientAsync.options_place_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_test_options_place_batch_order(optionsClientAsync):
    await optionsClientAsync.test_options_place_batch_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_cancel_order(optionsClientAsync):
    await optionsClientAsync.options_cancel_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_cancel_batch_order(optionsClientAsync):
    await optionsClientAsync.options_cancel_batch_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_cancel_all_orders(optionsClientAsync):
    await optionsClientAsync.options_cancel_all_orders()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_query_order(optionsClientAsync):
    await optionsClientAsync.options_query_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_query_pending_orders(optionsClientAsync):
    await optionsClientAsync.options_query_pending_orders()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_query_order_history(optionsClientAsync):
    await optionsClientAsync.options_query_order_history()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
async def test_options_user_trades(optionsClientAsync):
    await optionsClientAsync.options_user_trades()

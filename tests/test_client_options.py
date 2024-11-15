import pytest


pytestmark = pytest.mark.options


@pytest.fixture
def options_symbol(optionsClient):
    prices = optionsClient.options_price()
    return prices[0]["symbol"]


def test_options_ping(optionsClient):
    optionsClient.options_ping()


def test_options_time(optionsClient):
    optionsClient.options_time()


@pytest.mark.skip(reason="Not implemented")
def test_options_info(optionsClient):
    optionsClient.options_info()


def test_options_exchange_info(optionsClient):
    optionsClient.options_exchange_info()


def test_options_index_price(optionsClient):
    optionsClient.options_index_price(underlying="BTCUSDT")


def test_options_price(optionsClient):
    optionsClient.options_price()


def test_options_mark_price(optionsClient):
    optionsClient.options_mark_price()


def test_options_order_book(optionsClient, options_symbol):
    optionsClient.options_order_book(symbol=options_symbol)


def test_options_klines(optionsClient, options_symbol):
    optionsClient.options_klines(symbol=options_symbol, interval="1m")


def test_options_recent_trades(optionsClient, options_symbol):
    optionsClient.options_recent_trades(symbol=options_symbol)


def test_options_historical_trades(optionsClient, options_symbol):
    optionsClient.options_historical_trades(symbol=options_symbol)


# Account and trading interface endpoints


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_account_info(optionsClient):
    optionsClient.options_account_info()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_funds_transfer(optionsClient):
    optionsClient.options_funds_transfer()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_positions(optionsClient):
    optionsClient.options_positions()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_bill(optionsClient):
    optionsClient.options_bill()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_place_order(optionsClient):
    optionsClient.options_place_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_test_options_place_batch_order(optionsClient):
    optionsClient.test_options_place_batch_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_cancel_order(optionsClient):
    optionsClient.options_cancel_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_cancel_batch_order(optionsClient):
    optionsClient.options_cancel_batch_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_cancel_all_orders(optionsClient):
    optionsClient.options_cancel_all_orders()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_query_order(optionsClient):
    optionsClient.options_query_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_query_pending_orders(optionsClient):
    optionsClient.options_query_pending_orders()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_query_order_history(optionsClient):
    optionsClient.options_query_order_history()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_user_trades(optionsClient):
    optionsClient.options_user_trades()

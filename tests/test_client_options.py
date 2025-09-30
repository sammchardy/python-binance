import pytest
import sys


pytestmark = [pytest.mark.options, pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")]


@pytest.fixture
def options_symbol(liveClient):
    prices = liveClient.options_price()
    return prices[0]["symbol"]


def test_options_ping(liveClient):
    liveClient.options_ping()


def test_options_time(liveClient):
    liveClient.options_time()


@pytest.mark.skip(reason="Not implemented")
def test_options_info(liveClient):
    liveClient.options_info()


def test_options_exchange_info(liveClient):
    liveClient.options_exchange_info()


def test_options_index_price(liveClient):
    liveClient.options_index_price(underlying="BTCUSDT")


def test_options_price(liveClient):
    liveClient.options_price()


def test_options_mark_price(liveClient):
    liveClient.options_mark_price()


def test_options_order_book(liveClient, options_symbol):
    liveClient.options_order_book(symbol=options_symbol)


def test_options_klines(liveClient, options_symbol):
    liveClient.options_klines(symbol=options_symbol, interval="1m")


def test_options_recent_trades(liveClient, options_symbol):
    liveClient.options_recent_trades(symbol=options_symbol)


def test_options_historical_trades(liveClient, options_symbol):
    liveClient.options_historical_trades(symbol=options_symbol)


# Account and trading interface endpoints


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_account_info(liveClient):
    liveClient.options_account_info()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_funds_transfer(liveClient):
    liveClient.options_funds_transfer()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_positions(liveClient):
    liveClient.options_positions()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_bill(liveClient):
    liveClient.options_bill()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_place_order(liveClient):
    liveClient.options_place_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_test_options_place_batch_order(liveClient):
    liveClient.test_options_place_batch_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_cancel_order(liveClient):
    liveClient.options_cancel_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_cancel_batch_order(liveClient):
    liveClient.options_cancel_batch_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_cancel_all_orders(liveClient):
    liveClient.options_cancel_all_orders()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_query_order(liveClient):
    liveClient.options_query_order()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_query_pending_orders(liveClient):
    liveClient.options_query_pending_orders()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_query_order_history(liveClient):
    liveClient.options_query_order_history()


@pytest.mark.skip(reason="No sandbox to environmnet to test")
def test_options_user_trades(liveClient):
    liveClient.options_user_trades()

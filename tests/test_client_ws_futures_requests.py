from .test_get_order_book import assert_ob


def test_ws_futures_get_order_book(futuresClient):
    orderbook = futuresClient.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


def test_ws_futures_get_all_tickers(futuresClient):
    futuresClient.ws_futures_get_all_tickers()


def test_ws_futures_get_order_book_ticker(futuresClient):
    futuresClient.ws_futures_get_order_book_ticker()


def test_ws_futures_create_order(futuresClient):
    futuresClient.ws_futures_create_order()


def test_ws_futures_edit_order(futuresClient):
    futuresClient.ws_futures_edit_order()


def test_ws_futures_cancel_order(futuresClient):
    futuresClient.ws_futures_cancel_order()


def test_ws_futures_get_order(futuresClient):
    futuresClient.ws_futures_get_order()


def test_ws_futures_v2_account_position(futuresClient):
    futuresClient.ws_futures_v2_account_position()


def test_ws_futures_account_position(futuresClient):
    futuresClient.ws_futures_account_position()


def test_ws_futures_v2_account_balance(futuresClient):
    futuresClient.ws_futures_v2_account_balance()


def test_ws_futures_account_balance(futuresClient):
    futuresClient.ws_futures_account_balance()


def test_ws_futures_v2_account_status(futuresClient):
    futuresClient.ws_futures_v2_account_status()


def test_ws_futures_account_status(futuresClient):
    futuresClient.ws_futures_account_status()

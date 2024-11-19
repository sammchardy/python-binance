import pytest
from binance.exceptions import BinanceAPIException
from .test_get_order_book import assert_ob
from .test_order import assert_contract_order


def test_ws_futures_get_order_book(futuresClient):
    orderbook = futuresClient.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


def test_bad_request(futuresClient):
    with pytest.raises(BinanceAPIException):
        futuresClient.ws_futures_get_order_book()


def test_ws_futures_get_all_tickers(futuresClient):
    futuresClient.ws_futures_get_all_tickers()


def test_ws_futures_get_order_book_ticker(futuresClient):
    futuresClient.ws_futures_get_order_book_ticker()


def test_ws_futures_create_get_edit_cancel_order(futuresClient):
    ticker = futuresClient.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = futuresClient.ws_futures_v2_account_position(symbol="LTCUSDT")
    order = futuresClient.ws_futures_create_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["bidPrice"]) - 2)),
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.ws_futures_edit_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.ws_futures_get_order(
        symbol="LTCUSDT", orderid=order["orderId"]
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.ws_futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )


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

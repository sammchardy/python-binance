import pytest
import sys
from binance.exceptions import BinanceAPIException
from .test_get_order_book import assert_ob
from .test_order import assert_contract_order


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_get_order_book(futuresClient):
    orderbook = futuresClient.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


def test_bad_request(futuresClient):
    with pytest.raises(BinanceAPIException):
        futuresClient.ws_futures_get_order_book()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_get_all_tickers(futuresClient):
    futuresClient.ws_futures_get_all_tickers()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_get_order_book_ticker(futuresClient):
    futuresClient.ws_futures_get_order_book_ticker()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_create_get_edit_cancel_order(futuresClient):
    ticker = futuresClient.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = futuresClient.ws_futures_v2_account_position(symbol="LTCUSDT")
    order = futuresClient.ws_futures_create_order(
        symbol=ticker["symbol"],
        side="SELL",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["bidPrice"]) + 2)),
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


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_v2_account_position(futuresClient):
    futuresClient.ws_futures_v2_account_position()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_account_position(futuresClient):
    futuresClient.ws_futures_account_position()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_v2_account_balance(futuresClient):
    futuresClient.ws_futures_v2_account_balance()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_account_balance(futuresClient):
    futuresClient.ws_futures_account_balance()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_v2_account_status(futuresClient):
    futuresClient.ws_futures_v2_account_status()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_account_status(futuresClient):
    futuresClient.ws_futures_account_status()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_create_cancel_algo_order(futuresClient):
    """Test creating and canceling an algo order via websocket"""
    ticker = futuresClient.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = futuresClient.ws_futures_v2_account_position(symbol="LTCUSDT")

    # Create an algo order
    order = futuresClient.ws_futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )

    assert order["symbol"] == ticker["symbol"]
    assert "algoId" in order
    assert order["algoType"] == "CONDITIONAL"

    # Cancel the algo order
    cancel_result = futuresClient.ws_futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )

    assert cancel_result["algoId"] == order["algoId"]


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_create_conditional_order_auto_routing(futuresClient):
    """Test that conditional order types are automatically routed to algo endpoint"""
    ticker = futuresClient.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = futuresClient.ws_futures_v2_account_position(symbol="LTCUSDT")

    trigger_price = float(ticker["askPrice"]) * 1.5
    order = futuresClient.ws_futures_create_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        quantity=1,
        triggerPrice=trigger_price,
    )

    assert order["symbol"] == ticker["symbol"]
    assert "algoId" in order
    assert order["algoType"] == "CONDITIONAL"

    # Cancel using algoId parameter
    cancel_result = futuresClient.ws_futures_cancel_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )
    assert cancel_result["algoId"] == order["algoId"]


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_futures_conditional_order_with_stop_price(futuresClient):
    """Test that stopPrice is converted to triggerPrice for conditional orders"""
    ticker = futuresClient.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = futuresClient.ws_futures_v2_account_position(symbol="LTCUSDT")

    # Create a TAKE_PROFIT_MARKET order with stopPrice (should be converted to triggerPrice)
    # Use a price above current market price for SELL TAKE_PROFIT
    trigger_price = float(ticker["askPrice"]) * 1.5
    order = futuresClient.ws_futures_create_order(
        symbol=ticker["symbol"],
        side="SELL",
        positionSide=positions[0]["positionSide"],
        type="TAKE_PROFIT_MARKET",
        quantity=1,
        stopPrice=trigger_price,  # This should be converted to triggerPrice
    )

    assert order["symbol"] == ticker["symbol"]
    assert "algoId" in order
    assert order["algoType"] == "CONDITIONAL"

    # Cancel the order
    futuresClient.ws_futures_cancel_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )

import asyncio
import pytest
import sys

from binance.exceptions import BinanceAPIException, BinanceWebsocketUnableToConnect
from .test_get_order_book import assert_ob
from .test_order import assert_contract_order

try:
    from unittest.mock import patch  # Python 3.8+
except ImportError:
    from asynctest import patch  # Python 3.7


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_get_order_book(futuresClientAsync):
    orderbook = await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_concurrent_ws_futures_get_order_book(futuresClientAsync):
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT"]

    async def get_orderbook(symbol):
        orderbook = await futuresClientAsync.ws_futures_get_order_book(symbol=symbol)
        assert_ob(orderbook)
        return orderbook

    tasks = [get_orderbook(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)

    # Verify results
    assert len(results) == len(symbols)
    for orderbook in results:
        assert_ob(orderbook)


@pytest.mark.asyncio()
async def test_bad_request(futuresClientAsync):
    with pytest.raises(BinanceAPIException):
        await futuresClientAsync.ws_futures_get_order_book()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_get_all_tickers(futuresClientAsync):
    await futuresClientAsync.ws_futures_get_all_tickers()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_get_order_book_ticker(futuresClientAsync):
    await futuresClientAsync.ws_futures_get_order_book_ticker()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_create_get_edit_cancel_order_with_orjson(futuresClientAsync):
    if 'orjson' not in sys.modules:
        raise ImportError("orjson is not available")
    
    ticker = await futuresClientAsync.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.ws_futures_v2_account_position(
        symbol="LTCUSDT"
    )
    order = await futuresClientAsync.ws_futures_create_order(
        symbol=ticker["symbol"],
        side="SELL",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(float(ticker["bidPrice"]) + 5),
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.ws_futures_edit_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.ws_futures_get_order(
        symbol="LTCUSDT", orderid=order["orderId"]
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.ws_futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )

@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_create_get_edit_cancel_order_without_orjson(futuresClientAsync):
    with patch.dict('sys.modules', {'orjson': None}):
        ticker = await futuresClientAsync.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
        positions = await futuresClientAsync.ws_futures_v2_account_position(
            symbol="LTCUSDT"
        )
        order = await futuresClientAsync.ws_futures_create_order(
            symbol=ticker["symbol"],
            side="SELL",
            positionSide=positions[0]["positionSide"],
            type="LIMIT",
            timeInForce="GTC",
            quantity=0.1,
            price=str(float(ticker["bidPrice"]) + 5),
        )
        assert_contract_order(futuresClientAsync, order)
        order = await futuresClientAsync.ws_futures_edit_order(
            orderid=order["orderId"],
            symbol=order["symbol"],
            quantity=0.11,
            side=order["side"],
            price=order["price"],
        )
        assert_contract_order(futuresClientAsync, order)
        order = await futuresClientAsync.ws_futures_get_order(
            symbol="LTCUSDT", orderid=order["orderId"]
        )
        assert_contract_order(futuresClientAsync, order)
        order = await futuresClientAsync.ws_futures_cancel_order(
            orderid=order["orderId"], symbol=order["symbol"]
        )


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_v2_account_position(futuresClientAsync):
    await futuresClientAsync.ws_futures_v2_account_position()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_account_position(futuresClientAsync):
    await futuresClientAsync.ws_futures_account_position()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_v2_account_balance(futuresClientAsync):
    await futuresClientAsync.ws_futures_v2_account_balance()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_account_balance(futuresClientAsync):
    await futuresClientAsync.ws_futures_account_balance()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_v2_account_status(futuresClientAsync):
    await futuresClientAsync.ws_futures_v2_account_status()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_account_status(futuresClientAsync):
    await futuresClientAsync.ws_futures_account_status()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_futures_fail_to_connect(futuresClientAsync):
    # Close any existing connection first
    await futuresClientAsync.close_connection()

    # Mock the WebSocket API's connect method to raise an exception
    with patch.object(futuresClientAsync.ws_future, 'connect', side_effect=ConnectionError("Simulated connection failure")):
        with pytest.raises(BinanceWebsocketUnableToConnect):
            await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_create_cancel_algo_order(futuresClientAsync):
    """Test creating and canceling an algo order via websocket async"""
    ticker = await futuresClientAsync.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.ws_futures_v2_account_position(symbol="LTCUSDT")

    # Create an algo order
    order = await futuresClientAsync.ws_futures_create_algo_order(
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
    cancel_result = await futuresClientAsync.ws_futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )

    assert cancel_result["algoId"] == order["algoId"]


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_create_conditional_order_auto_routing(futuresClientAsync):
    """Test that conditional order types are automatically routed to algo endpoint"""
    ticker = await futuresClientAsync.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.ws_futures_v2_account_position(symbol="LTCUSDT")

    # Create a STOP_MARKET order using ws_futures_create_order
    # It should automatically route to the algo endpoint
    # Use a price above current market price for BUY STOP
    trigger_price = float(ticker["askPrice"]) * 1.5
    order = await futuresClientAsync.ws_futures_create_order(
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

    # Cancel the order using algoId
    cancel_result = await futuresClientAsync.ws_futures_cancel_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )
    assert cancel_result["algoId"] == order["algoId"]


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_futures_conditional_order_with_stop_price(futuresClientAsync):
    """Test that stopPrice is converted to triggerPrice for conditional orders"""
    ticker = await futuresClientAsync.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.ws_futures_v2_account_position(symbol="LTCUSDT")

    # Create a TAKE_PROFIT_MARKET order with stopPrice (should be converted to triggerPrice)
    # Use a price above current market price for SELL TAKE_PROFIT
    trigger_price = float(ticker["askPrice"]) * 1.5
    order = await futuresClientAsync.ws_futures_create_order(
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
    await futuresClientAsync.ws_futures_cancel_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )

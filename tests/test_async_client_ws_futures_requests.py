import asyncio
import pytest

from binance.exceptions import BinanceAPIException, BinanceWebsocketUnableToConnect
from .test_get_order_book import assert_ob
from .test_order import assert_contract_order

try:
    from unittest.mock import AsyncMock, patch  # Python 3.8+
except ImportError:
    from asynctest import CoroutineMock as AsyncMock, patch  # Python 3.7


@pytest.mark.asyncio()
async def test_ws_futures_get_order_book(futuresClientAsync):
    orderbook = await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


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


@pytest.mark.asyncio()
async def test_ws_futures_get_all_tickers(futuresClientAsync):
    await futuresClientAsync.ws_futures_get_all_tickers()


@pytest.mark.asyncio()
async def test_ws_futures_get_order_book_ticker(futuresClientAsync):
    await futuresClientAsync.ws_futures_get_order_book_ticker()


@pytest.mark.asyncio()
async def test_ws_futures_create_get_edit_cancel_order(futuresClientAsync):
    ticker = await futuresClientAsync.ws_futures_get_order_book_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.ws_futures_v2_account_position(
        symbol="LTCUSDT"
    )
    order = await futuresClientAsync.ws_futures_create_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(float(ticker["bidPrice"]) - 2),
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


@pytest.mark.asyncio()
async def test_ws_futures_v2_account_position(futuresClientAsync):
    await futuresClientAsync.ws_futures_v2_account_position()


@pytest.mark.asyncio()
async def test_ws_futures_account_position(futuresClientAsync):
    await futuresClientAsync.ws_futures_account_position()


@pytest.mark.asyncio()
async def test_ws_futures_v2_account_balance(futuresClientAsync):
    await futuresClientAsync.ws_futures_v2_account_balance()


@pytest.mark.asyncio()
async def test_ws_futures_account_balance(futuresClientAsync):
    await futuresClientAsync.ws_futures_account_balance()


@pytest.mark.asyncio()
async def test_ws_futures_v2_account_status(futuresClientAsync):
    await futuresClientAsync.ws_futures_v2_account_status()


@pytest.mark.asyncio()
async def test_ws_futures_account_status(futuresClientAsync):
    await futuresClientAsync.ws_futures_account_status()


@pytest.mark.asyncio
async def test_ws_futures_fail_to_connect(futuresClientAsync):
    # Simulate WebSocket connection being closed during the request
    with patch("websockets.connect", new_callable=AsyncMock):
        with pytest.raises(BinanceWebsocketUnableToConnect):
            await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")

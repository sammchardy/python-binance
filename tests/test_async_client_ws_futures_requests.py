import pytest
from .test_get_order_book import assert_ob
from .test_order import assert_contract_order


@pytest.mark.asyncio()
async def test_ws_futures_get_order_book(futuresClientAsync):
    orderbook = await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


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

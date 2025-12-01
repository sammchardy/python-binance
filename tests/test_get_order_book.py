import pytest
import sys
from binance.exceptions import BinanceAPIException


def assert_ob(order_book):
    assert isinstance(order_book, dict)
    assert "lastUpdateId" in order_book
    assert "bids" in order_book
    assert "asks" in order_book

    assert isinstance(order_book["bids"], list)
    assert isinstance(order_book["asks"], list)

    if order_book["bids"]:
        bid = order_book["bids"][0]
        assert len(bid) == 2
        assert all(isinstance(item, str) for item in bid[:2])

    if order_book["asks"]:
        ask = order_book["asks"][0]
        assert len(ask) == 2
        assert all(isinstance(item, str) for item in ask[:2])


def test_get_order_book(client):
    try:
        order_book = client.get_order_book(symbol="BTCUSDT")
        assert_ob(order_book)

    except BinanceAPIException as e:
        pytest.fail(f"API request failed: {str(e)}")


def test_futures_get_order_book(client):
    try:
        order_book = client.futures_order_book(symbol="BTCUSDT")
        assert_ob(order_book)

    except BinanceAPIException as e:
        pytest.fail(f"API request failed: {str(e)}")


def test_get_order_book_with_limit(client):
    try:
        order_book = client.get_order_book(symbol="BTCUSDT", limit=5)

        assert_ob(order_book)
        assert len(order_book["bids"]) <= 5
        assert len(order_book["asks"]) <= 5

    except BinanceAPIException as e:
        pytest.fail(f"API request failed: {str(e)}")


@pytest.mark.asyncio(scope="function")
async def test_get_order_book_async(clientAsync):
    order_book = await clientAsync.get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


@pytest.mark.asyncio(scope="function")
async def test_futures_get_order_book_async(clientAsync):
    try:
        order_book = await clientAsync.futures_order_book(symbol="BTCUSDT")
        assert_ob(order_book)
    except BinanceAPIException as e:
        pytest.fail(f"API request failed: {str(e)}")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio()
async def test_ws_get_order_book(clientAsync):
    order_book = await clientAsync.ws_get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)

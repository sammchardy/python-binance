import requests_mock
import pytest
from aioresponses import aioresponses

from binance import Client, AsyncClient

client = Client(api_key="api_key", api_secret="api_secret", ping=False)


def test_get_headers():
    with requests_mock.mock() as m:
        m.get("https://api.binance.com/api/v3/account", json={}, status_code=200)
        client.get_account()
        headers = m.last_request._request.headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/json"


def test_post_headers():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.create_order(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        headers = m.last_request._request.headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "application/x-www-form-urlencoded"


def test_post_headers_overriden():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.create_order(
            symbol="LTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=0.1,
            headers={"Content-Type": "myvalue"},
        )
        headers = m.last_request._request.headers
        assert "Content-Type" in headers
        assert headers["Content-Type"] == "myvalue"


@pytest.mark.asyncio()
async def test_post_headers_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret"
    )  # reuse client later
    with aioresponses() as m:

        def handler(url, **kwargs):
            headers = kwargs["headers"]
            assert "Content-Type" in headers
            assert headers["Content-Type"] == "application/x-www-form-urlencoded"

        m.post(
            "https://api.binance.com/api/v3/order",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.create_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_post_headers_overriden_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret"
    )  # reuse client later
    with aioresponses() as m:

        def handler(url, **kwargs):
            headers = kwargs["headers"]
            assert "Content-Type" in headers
            assert headers["Content-Type"] == "myvalue"

        m.post(
            "https://api.binance.com/api/v3/order",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.create_order(
            symbol="LTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=0.1,
            headers={"Content-Type": "myvalue"},
        )
        await clientAsync.close_connection()

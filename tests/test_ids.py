import re
import requests_mock
import pytest
from aioresponses import aioresponses

from binance import Client, AsyncClient

client = Client(api_key="api_key", api_secret="api_secret", ping=False)


def test_spot_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.create_order(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        assert url_dict["symbol"] == "LTCUSDT"
        assert url_dict["side"] == "BUY"
        assert url_dict["type"] == "MARKET"
        assert url_dict["quantity"] == "0.1"
        assert url_dict["newClientOrderId"].startswith("x-HNA2TXFJ")


def test_spot_limit_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.order_limit_buy(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        assert url_dict["newClientOrderId"].startswith("x-HNA2TXFJ")


def test_spot_market_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.order_market_buy(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        assert url_dict["newClientOrderId"].startswith("x-HNA2TXFJ")


def test_spot_cancel_replace_id():
    with requests_mock.mock() as m:
        m.post(
            "https://api.binance.com/api/v3/order/cancelReplace",
            json={},
            status_code=200,
        )
        client.cancel_replace_order(
            cancelOrderId="orderId",
            symbol="LTCUSDT",
            side="BUY",
            type="MARKET",
            quantity=0.1,
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        assert url_dict["newClientOrderId"].startswith("x-HNA2TXFJ")


def test_spot_oco_order_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/orderList/oco", json={}, status_code=200)
        client.create_oco_order(
            symbol="LTCUSDT", side="BUY", aboveType="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        assert url_dict["listClientOrderId"].startswith("x-HNA2TXFJ")


def test_swap_id():
    with requests_mock.mock() as m:
        m.post("https://fapi.binance.com/fapi/v1/order", json={}, status_code=200)
        client.futures_create_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        # why lowercase? check this later
        assert url_dict["symbol"] == "LTCUSDT"
        assert url_dict["side"] == "BUY"
        assert url_dict["type"] == "MARKET"
        assert url_dict["quantity"] == "0.1"
        assert url_dict["newClientOrderId"].startswith("x-Cb7ytekJ")


def test_swap_batch_id():
    with requests_mock.mock() as m:
        m.post("https://fapi.binance.com/fapi/v1/batchOrders", json={}, status_code=200)
        order = {"symbol": "LTCUSDT", "side": "BUY", "type": "MARKET", "quantity": 0.1}
        orders = [order, order]
        client.futures_place_batch_order(batchOrders=orders)
        text = m.last_request.text
        assert "x-Cb7ytekJ" in text


def test_coin_id():
    with requests_mock.mock() as m:
        m.post("https://dapi.binance.com/dapi/v1/order", json={}, status_code=200)
        client.futures_coin_create_order(
            symbol="LTCUSD_PERP", side="BUY", type="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        # why lowercase? check this later
        assert url_dict["symbol"] == "LTCUSD_PERP"
        assert url_dict["side"] == "BUY"
        assert url_dict["type"] == "MARKET"
        assert url_dict["quantity"] == "0.1"
        assert url_dict["newClientOrderId"].startswith("x-Cb7ytekJ")


def test_coin_batch_id():
    with requests_mock.mock() as m:
        m.post("https://dapi.binance.com/dapi/v1/batchOrders", json={}, status_code=200)
        order = {
            "symbol": "BTCUSD_PERP",
            "side": "BUY",
            "type": "MARKET",
            "quantity": 0.1,
        }
        orders = [order, order]
        client.futures_coin_place_batch_order(batchOrders=orders)
        text = m.last_request.text
        assert "x-Cb7ytekJ" in text


def test_papi_um_id():
    with requests_mock.mock() as m:
        m.post("https://papi.binance.com/papi/v1/um/order", json={}, status_code=200)
        client.papi_create_um_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        # why lowercase? check this later
        assert url_dict["symbol"] == "LTCUSDT"
        assert url_dict["side"] == "BUY"
        assert url_dict["type"] == "MARKET"
        assert url_dict["quantity"] == "0.1"
        assert url_dict["newClientOrderId"].startswith("x-Cb7ytekJ")


def test_papi_cm_id():
    with requests_mock.mock() as m:
        m.post("https://papi.binance.com/papi/v1/cm/order", json={}, status_code=200)
        client.papi_create_cm_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        url_dict = dict(pair.split("=") for pair in m.last_request.text.split("&"))
        # why lowercase? check this later
        assert url_dict["symbol"] == "LTCUSDT"
        assert url_dict["side"] == "BUY"
        assert url_dict["type"] == "MARKET"
        assert url_dict["quantity"] == "0.1"
        assert url_dict["newClientOrderId"].startswith("x-Cb7ytekJ")


@pytest.mark.asyncio()
async def test_spot_id_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret"
    )  # reuse client later
    with aioresponses() as m:

        def handler(url, **kwargs):
            client_order_id = kwargs["data"][0][1]
            assert client_order_id.startswith("x-HNA2TXFJ")

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
async def test_spot_cancel_replace_id_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret"
    )  # reuse client later
    with aioresponses() as m:

        def handler(url, **kwargs):
            client_order_id = kwargs["data"][0][1]
            assert client_order_id.startswith("x-HNA2TXFJ")

        m.post(
            "https://api.binance.com/api/v3/order/cancelReplace",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.cancel_replace_order(
            orderId="id", symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_swap_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            assert "x-Cb7ytekJ" in kwargs["data"][0][1]

        url_pattern = re.compile(r"https://fapi\.binance\.com/fapi/v1/order")
        m.post(
            url_pattern,
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.futures_create_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()

@pytest.mark.asyncio()
async def test_swap_trigger_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            assert "x-Cb7ytekJ" in kwargs["data"][1][1]

        url_pattern = re.compile(r"https://fapi\.binance\.com/fapi/v1/algoOrder")
        m.post(
            url_pattern,
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.futures_create_order(
            symbol="LTCUSDT", side="BUY", type="STOP_MARKET", quantity=0.1
        )
        await clientAsync.close_connection()

@pytest.mark.asyncio()
async def test_swap_trigger_endpoint_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            # print(kwargs["data"])
            assert "x-Cb7ytekJ" in kwargs["data"][1][1]

        url_pattern = re.compile(r"https://fapi\.binance\.com/fapi/v1/algoOrder")
        m.post(
            url_pattern,
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.futures_create_algo_order(
            symbol="LTCUSDT", side="BUY", type="STOP_MARKET", quantity=0.1
        )
        await clientAsync.close_connection()

@pytest.mark.asyncio()
async def test_papi_um_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            client_order_id = kwargs["data"][0][1]
            assert client_order_id.startswith("x-Cb7ytekJ")

        m.post(
            "https://papi.binance.com/papi/v1/um/order",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.papi_create_um_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_papi_cm_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            client_order_id = kwargs["data"][0][1]
            assert client_order_id.startswith("x-Cb7ytekJ")

        m.post(
            "https://papi.binance.com/papi/v1/cm/order",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.papi_create_cm_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_coin_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            client_order_id = kwargs["data"][0][1]
            assert client_order_id.startswith("x-Cb7ytekJ")

        m.post(
            "https://dapi.binance.com/dapi/v1/order",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.futures_coin_create_order(
            symbol="LTCUSD_PERP", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_spot_oco_id():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:

        def handler(url, **kwargs):
            client_order_id = kwargs["data"][0][1]
            assert client_order_id.startswith("x-HNA2TXFJ")

        m.post(
            "https://api.binance.com/api/v3/orderList/oco",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        await clientAsync.create_oco_order(
            symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_swap_batch_id_async():
    with aioresponses() as m:
        clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")

        def handler(url, **kwargs):
            assert "x-Cb7ytekJ" in kwargs["data"]

        m.post(
            "https://fapi.binance.com/fapi/v1/batchOrders",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        order = {"symbol": "LTCUSDT", "side": "BUY", "type": "MARKET", "quantity": 0.1}
        orders = [order, order]
        await clientAsync.futures_place_batch_order(batchOrders=orders)
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_coin_batch_id_async():
    with aioresponses() as m:
        clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")

        def handler(url, **kwargs):
            assert "x-Cb7ytekJ" in kwargs["data"][0][1]

        m.post(
            "https://dapi.binance.com/dapi/v1/batchOrders",
            payload={"id": 1},
            status=200,
            callback=handler,
        )
        order = {
            "symbol": "LTCUSD_PERP",
            "side": "BUY",
            "type": "MARKET",
            "quantity": 0.1,
        }
        orders = [order, order]
        await clientAsync.futures_coin_place_batch_order(batchOrders=orders)
        await clientAsync.close_connection()

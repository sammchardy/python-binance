import requests_mock
import os, sys
import pytest
from aioresponses import aioresponses
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)


from binance.client import Client, AsyncClient

client = Client(api_key="api_key", api_secret="api_secret", ping=False)

def test_spot_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.create_order(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        url_dict =  dict(pair.split('=') for pair in m.last_request.text.split('&'))
        assert url_dict['symbol'] == 'LTCUSDT'
        assert url_dict['side'] == 'BUY'
        assert url_dict['type'] == 'MARKET'
        assert url_dict['quantity'] == '0.1'
        assert url_dict['newClientOrderId'].startswith('x-R4BD3S82')


def test_spot_limit_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.order_limit_buy(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        url_dict =  dict(pair.split('=') for pair in m.last_request.text.split('&'))
        assert url_dict['newClientOrderId'].startswith('x-R4BD3S82')

def test_spot_market_id():
    with requests_mock.mock() as m:
        m.post("https://api.binance.com/api/v3/order", json={}, status_code=200)
        client.order_market_buy(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        url_dict =  dict(pair.split('=') for pair in m.last_request.text.split('&'))
        assert url_dict['newClientOrderId'].startswith('x-R4BD3S82')

def test_swap_id():
    with requests_mock.mock() as m:
        m.post("https://fapi.binance.com/fapi/v1/order", json={}, status_code=200)
        client.futures_create_order(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        url_dict =  dict(pair.split('=') for pair in m.last_request.query.split('&'))
        # why lowercase? check this later
        assert url_dict['symbol'] == 'ltcusdt'
        assert url_dict['side'] == 'buy'
        assert url_dict['type'] == 'market'
        assert url_dict['quantity'] == '0.1'
        assert url_dict['newClientOrderId'.lower()].startswith('x-xcKtGhcu'.lower())


@pytest.mark.asyncio()
async def test_spot_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret") # reuse client later
    with aioresponses() as m:
        def handler(url, **kwargs):
            client_order_id = kwargs['data'][0][1]
            assert client_order_id.startswith('x-R4BD3S82')
        m.post("https://api.binance.com/api/v3/order", payload={'id': 1}, status=200, callback=handler)
        await clientAsync.create_order(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        await clientAsync.close_connection()


@pytest.mark.asyncio()
async def test_swap_id_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret")
    with aioresponses() as m:
        def handler(url, **kwargs):
            client_order_id = kwargs['data'][0][1]
            assert client_order_id.startswith('x-xcKtGhcu')
        m.post("https://fapi.binance.com/fapi/v1/order", payload={'id': 1}, status=200, callback=handler)
        await clientAsync.futures_create_order(symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1)
        await clientAsync.close_connection()

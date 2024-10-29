
from binance.client import Client, AsyncClient
import os
import pytest


proxies = {}
proxy = os.getenv("PROXY")

def test_papi_ping_sync(client):
    ping_response = client.papi_ping()
    assert ping_response != None

def test_ping_sync(client):
    ping_response = client.ping()
    assert ping_response != None

def test_futures_ping(client):
    ping_response = client.futures_ping()
    assert ping_response != None

def test_coin_ping(client):
    ping_response = client.futures_coin_ping()
    assert ping_response != None

@pytest.mark.asyncio()
async def test_papi_ping_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret", https_proxy=proxy)
    ping_response = await clientAsync.papi_ping()
    assert ping_response != None

@pytest.mark.asyncio()
async def test_ping_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret", https_proxy=proxy)
    ping_response = await clientAsync.ping()
    assert ping_response != None

@pytest.mark.asyncio()
async def test_futures_ping_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret", https_proxy=proxy)
    ping_response = await clientAsync.futures_ping()
    assert ping_response != None

@pytest.mark.asyncio()
async def test_coin_ping_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret", https_proxy=proxy)
    ping_response = await clientAsync.futures_coin_ping()
    assert ping_response != None
import os

import pytest

from binance.client import AsyncClient, Client

proxies = {}
proxy = os.getenv("PROXY")

if proxy:
    proxies = {"http": proxy, "https": proxy}  # tmp: improve this in the future
else:
    print("No proxy set")

client = Client("api_key", "api_secret", {"proxies": proxies})


def test_papi_ping_sync():
    ping_response = client.papi_ping()
    assert ping_response is not None


def test_ping_sync():
    ping_response = client.ping()
    assert ping_response is not None


def test_futures_ping():
    ping_response = client.futures_ping()
    assert ping_response is not None


def test_coin_ping():
    ping_response = client.futures_coin_ping()
    assert ping_response is not None


@pytest.mark.asyncio()
async def test_papi_ping_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret", https_proxy=proxy
    )
    ping_response = await clientAsync.papi_ping()
    assert ping_response is not None


@pytest.mark.asyncio()
async def test_ping_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret", https_proxy=proxy
    )
    ping_response = await clientAsync.ping()
    assert ping_response is not None


@pytest.mark.asyncio()
async def test_futures_ping_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret", https_proxy=proxy
    )
    ping_response = await clientAsync.futures_ping()
    assert ping_response is not None


@pytest.mark.asyncio()
async def test_coin_ping_async():
    clientAsync = AsyncClient(
        api_key="api_key", api_secret="api_secret", https_proxy=proxy
    )
    ping_response = await clientAsync.futures_coin_ping()
    assert ping_response is not None

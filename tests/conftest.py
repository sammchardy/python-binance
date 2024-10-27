import pytest
from binance.client import Client, AsyncClient
import os
import asyncio

proxies = {}
proxy = os.getenv("PROXY")

if proxy:
    proxies = {"http": proxy, 'https': proxy } # tmp: improve this in the future
else:
    print("No proxy set")


@pytest.fixture(scope="module")
def client():
    return Client("test_api_key", "test_api_secret", {'proxies': proxies})

@pytest.fixture(scope="module")
async def clientAsync():
    # for now this is not working inside the tests
    res = await AsyncClient().create(api_key="api_key", api_secret="api_secret", https_proxy=proxy, loop=asyncio.new_event_loop())
    return res

from binance.client import Client, AsyncClient
import os
import pytest

proxies = {}
proxy = os.getenv("PROXY")

if proxy:
    proxies = {"http": proxy, 'https': proxy } # tmp: improve this in the future
else:
    print("No proxy set")

client = Client("api_key", "api_secret", {'proxies': proxies})


def test_ping_sync():
    ping_response = client.papi_ping()
    assert ping_response != None

@pytest.mark.asyncio()
async def test_ping_async():
    clientAsync = AsyncClient(api_key="api_key", api_secret="api_secret", https_proxy=proxy)
    ping_response = await clientAsync.papi_ping()
    assert ping_response != None
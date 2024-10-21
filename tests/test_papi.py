
from binance.client import Client
import os

proxies = {}
proxy = os.getenv("PROXY")

if proxy:
    proxies = {"http": proxy, 'https': proxy } # tmp: improve this in the future
else:
    print("No proxy set")

client = Client("api_key", "api_secret", {'proxies': proxies})

def test_ping_sync():
    pingResponse = client.papi_ping()
    assert pingResponse != None

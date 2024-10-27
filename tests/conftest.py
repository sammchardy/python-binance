import pytest
from binance.client import Client

@pytest.fixture(scope="module")
def client():
    return Client("test_api_key", "test_api_secret", testnet=True)

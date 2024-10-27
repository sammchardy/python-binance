import pytest
from binance.client import Client

@pytest.fixture(scope="module")
def client():
    return Client(testnet=True)

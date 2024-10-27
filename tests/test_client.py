import pytest
from binance.client import Client
from binance.exceptions import BinanceAPIException

def test_client_initialization(test_client):
    assert test_client.API_KEY == 'test_api_key'
    assert test_client.API_SECRET == 'test_api_secret'
    assert test_client.testnet == True

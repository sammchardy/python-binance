from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import pytest
import requests_mock


@pytest.fixture(scope='module')
def client():
    """setup"""

    client = Client('api_key', 'api_secret')
    return client


@requests_mock.Mocker(kw='mock')
def test_get_all_tickers(client, **kwargs):
    expected_response = [{'symbol': 'ETHBTC', 'price': '0.06675400'},
                         {'symbol': 'LTCBTC', 'price': '0.00451500'}]

    kwargs['mock'].get('https://api.binance.com/api/v3/ticker/price', json=expected_response)
    returned_value = client.get_all_tickers()
    assert returned_value == expected_response


@requests_mock.Mocker(kw='mock')
def test_failed_get_all_tickers(client, **kwargs):
    with pytest.raises(BinanceAPIException):
        kwargs['mock'].get('https://api.binance.com/api/v3/ticker/price', status_code=400)
        client.get_all_tickers()

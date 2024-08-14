
import pytest
import requests_mock

from binance.client import Client
from binance.data_client import DataClient
from binance.enums import KLINE_INTERVAL_1MINUTE


@pytest.fixture(scope="module")
def client():
    """Returns a client to use for testing purposes"""
    return Client("api_key", "api_secret")

@pytest.fixture(scope="module")
def data_client():
    """Returns a data client to use for testing purposes"""
    return DataClient("api_key", "api_secret")


#
# KLINES RESPONSE DATA
#


klines_row_1 = [
    1500004800000,
    "0.00005000",
    "0.00005300",
    "0.00001000",
    "0.00004790",
    "663152.00000000",
    1500004859999,
    "30.55108144",
    43,
    "559224.00000000",
    "25.65468144",
    "83431971.04346950",
]

klines_row_2 = [
    1519892340000,
    "0.00099400",
    "0.00099810",
    "0.00099400",
    "0.00099810",
    "4806.04000000",
    1519892399999,
    "4.78553253",
    154,
    "1785.14000000",
    "1.77837524",
    "0",
]

url_1 = "https://api.binance.com/api/v3/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC"
url_2 = "https://api.binance.com/api/v3/klines?interval=1m&limit=1000&startTime=1519862400000&symbol=BNBBTC"
url_3 = "https://api.binance.com/api/v3/klines?interval=1m&limit=1000&startTime=1519892400000&symbol=BNBBTC"

response_1 = [klines_row_1]
response_2 = [klines_row_2 for _ in range(0,500)]
response_3 = []

@pytest.fixture(scope="module")
def historical_klines_response(client):
    with requests_mock.mock() as mock:
        mock.get(url_1, json=response_1)
        mock.get(url_2, json=response_2)
        mock.get(url_3, json=response_3)

        klines = client.get_historical_klines(
            symbol="BNBBTC",
            interval=KLINE_INTERVAL_1MINUTE,
            start_str="1st March 2018"
        )
        #print(klines)
        return klines

@pytest.fixture(scope="module")
def historical_klines_response_df(data_client):
    with requests_mock.mock() as mock:
        mock.get(url_1, json=response_1)
        mock.get(url_2, json=response_2)
        mock.get(url_3, json=response_3)

        klines = data_client.get_historical_klines(
            symbol="BNBBTC",
            interval=KLINE_INTERVAL_1MINUTE,
            start_str="1st March 2018"
        )
        #print(klines)
        return klines

@pytest.fixture(scope="module")
def klines(historical_klines_response):
    """Alias method"""
    return historical_klines_response

@pytest.fixture(scope="module")
def klines_df(historical_klines_response_df):
    """Alias method"""
    return historical_klines_response_df

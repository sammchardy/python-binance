from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import pytest
import requests_mock
import os

proxies = {}
proxy = os.getenv("PROXY")
if proxy:
    proxies = {"http": proxy, "https": proxy}  # tmp: improve this in the future
else:
    print("No proxy set")

client = Client("api_key", "api_secret", {"proxies": proxies})


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(BinanceRequestException):
        with requests_mock.mock() as m:
            m.get(
                "https://www.binance.com/exchange-api/v1/public/asset-service/product/get-products?includeEtf=true",
                text="<head></html>",
            )
            m.get(
                "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true",
                text="<head></html>",
            )
            client.get_products()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(BinanceAPIException):
        with requests_mock.mock() as m:
            json_obj = {"code": 1002, "msg": "Invalid API call"}
            m.get("https://api.binance.com/api/v3/time", json=json_obj, status_code=400)
            client.get_server_time()


def test_api_exception_invalid_json():
    """Test API response Exception"""

    with pytest.raises(BinanceAPIException):
        with requests_mock.mock() as m:
            not_json_str = "<html><body>Error</body></html>"
            m.get(
                "https://api.binance.com/api/v3/time",
                text=not_json_str,
                status_code=400,
            )
            client.get_server_time()

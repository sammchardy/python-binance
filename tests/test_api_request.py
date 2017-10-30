#!/usr/bin/env python
# coding=utf-8

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import pytest
import requests_mock


client = Client('api_key', 'api_secret')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(BinanceRequestException):
        with requests_mock.mock() as m:
            m.get('https://www.binance.com/exchange/public/product', text='<head></html>')
            client.get_products()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(BinanceAPIException):
        with requests_mock.mock() as m:
            json_obj = {"code": 1002, "msg": "Invalid API call"}
            m.get('https://www.binance.com/api/v1/time', json=json_obj, status_code=400)
            client.get_server_time()

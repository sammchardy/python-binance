#!/usr/bin/env python
# coding=utf-8

from binance.client import Client
import pytest
import requests_mock


client = Client('api_key', 'api_secret')


def test_exact_amount():
    """Test Exact amount returned"""

    first_available_res = [[1500004800000, "0.00005000", "0.00005300", "0.00001000", "0.00004790", "663152.00000000", 1500004859999, "30.55108144", 43, "559224.00000000", "25.65468144", "83431971.04346950"]]

    first_res = []
    row = [1519892340000, "0.00099400", "0.00099810", "0.00099400", "0.00099810", "4806.04000000", 1519892399999, "4.78553253", 154, "1785.14000000", "1.77837524", "0"]

    for i in range(0, 500):
        first_res.append(row)

    second_res = []

    with requests_mock.mock() as m:
        m.get('https://api.binance.com/api/v1/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC', json=first_available_res)
        m.get('https://api.binance.com/api/v1/klines?interval=1m&limit=500&startTime=1519862400000&symbol=BNBBTC', json=first_res)
        m.get('https://api.binance.com/api/v1/klines?interval=1m&limit=500&startTime=1519892400000&symbol=BNBBTC', json=second_res)
        client.get_historical_klines(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str="1st March 2018"
        )

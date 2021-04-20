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
        m.get('https://api.binance.com/api/v3/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC', json=first_available_res)
        m.get('https://api.binance.com/api/v3/klines?interval=1m&limit=500&startTime=1519862400000&symbol=BNBBTC', json=first_res)
        m.get('https://api.binance.com/api/v3/klines?interval=1m&limit=500&startTime=1519892400000&symbol=BNBBTC', json=second_res)
        klines = client.get_historical_klines(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str="1st March 2018"
        )
        assert len(klines) == 500


def test_start_and_end_str():
    """Test start_str and end_str work correctly with string"""

    first_available_res = [
        [
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
    ]
    first_res = []
    row = [
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

    for i in range(0, 300):
        first_res.append(row)

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC",
            json=first_available_res,
        )
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=500&startTime=1519862400000&endTime=1519880400000&symbol=BNBBTC",
            json=first_res,
        )
        klines = client.get_historical_klines(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str="1st March 2018",
            end_str="1st March 2018 05:00:00",
        )
        assert len(klines) == 300


def test_start_and_end_timestamp():
    """Test start_str and end_str work correctly with integer timestamp"""

    first_available_res = [
        [
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
    ]
    first_res = []
    row = [
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

    for i in range(0, 300):
        first_res.append(row)

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC",
            json=first_available_res,
        )
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=500&startTime=1519862400000&endTime=1519880400000&symbol=BNBBTC",
            json=first_res,
        )
        klines = client.get_historical_klines(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str=1519862400000,
            end_str=1519880400000,
        )
        assert len(klines) == 300


def test_historical_kline_generator():
    """Test kline historical generator"""

    first_available_res = [
        [
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
    ]
    first_res = []
    row = [
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

    for i in range(0, 300):
        first_res.append(row)

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC",
            json=first_available_res,
        )
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=500&startTime=1519862400000&endTime=1519880400000&symbol=BNBBTC",
            json=first_res,
        )
        klines = client.get_historical_klines_generator(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str=1519862400000,
            end_str=1519880400000,
        )

        for i in range(300):
            assert len(next(klines)) > 0

        with pytest.raises(StopIteration):
            next(klines)


def test_historical_kline_generator_empty_response():
    """Test kline historical generator if an empty list is returned from API"""
    first_available_res = [
        [
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
    ]
    first_res = []

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=1&startTime=0&symbol=BNBBTC",
            json=first_available_res,
        )
        m.get(
            "https://api.binance.com/api/v3/klines?interval=1m&limit=500&startTime=1519862400000&endTime=1519880400000&symbol=BNBBTC",
            json=first_res,
        )
        klines = client.get_historical_klines_generator(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MINUTE,
            start_str=1519862400000,
            end_str=1519880400000,
        )

        with pytest.raises(StopIteration):
            next(klines)


def test_historical_kline_with_month_interval():
    """Test historical klines with one month interval"""

    first_available_res = [
        [
            1498867200000,
            "0.00005000",
            "0.00005480",
            "0.00001000",
            "0.00003654",
            "61059068.00000000",
            1501545599999,
            "2572.23205388",
            33297,
            "33906053.00000000",
            "1442.17447471",
            "100206524.84393587"
        ]
    ]
    first_res = []
    row = [
        1519862400000,
        "0.00101270",
        "0.00167650",
        "0.00083250",
        "0.00159650",
        "122814213.69000000",
        1522540799999,
        "142681.39725065",
        3242765,
        "68994444.35000000",
        "79545.22096745",
        "0"
    ]

    for i in range(0, 8):
        first_res.append(row)

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/api/v1/klines?interval=1M&limit=1&startTime=0&symbol=BNBBTC",
            json=first_available_res,
        )
        m.get(
            "https://api.binance.com/api/v1/klines?interval=1M&limit=500&startTime=1519862400000&endTime=1539234000000&symbol=BNBBTC",
            json=first_res,
        )
        klines = client.get_historical_klines(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MONTH,
            start_str="1st March 2018",
            end_str="11st Oct 2018 05:00:00",
        )
        assert len(klines) == 8


def test_historical_kline_generator_with_month_interval():
    """Test historical klines generator with one month interval"""

    first_available_res = [
        [
            1498867200000,
            "0.00005000",
            "0.00005480",
            "0.00001000",
            "0.00003654",
            "61059068.00000000",
            1501545599999,
            "2572.23205388",
            33297,
            "33906053.00000000",
            "1442.17447471",
            "100206524.84393587"
        ]
    ]
    first_res = []
    row = [
        1519862400000,
        "0.00101270",
        "0.00167650",
        "0.00083250",
        "0.00159650",
        "122814213.69000000",
        1522540799999,
        "142681.39725065",
        3242765,
        "68994444.35000000",
        "79545.22096745",
        "0"
    ]

    for i in range(0, 8):
        first_res.append(row)

    with requests_mock.mock() as m:
        m.get(
            "https://api.binance.com/api/v1/klines?interval=1M&limit=1&startTime=0&symbol=BNBBTC",
            json=first_available_res,
        )
        m.get(
            "https://api.binance.com/api/v1/klines?interval=1M&limit=500&startTime=1519862400000&endTime=1539234000000&symbol=BNBBTC",
            json=first_res,
        )
        klines = client.get_historical_klines_generator(
            symbol="BNBBTC",
            interval=Client.KLINE_INTERVAL_1MONTH,
            start_str=1519862400000,
            end_str=1539234000000,
        )

        for i in range(8):
            assert len(next(klines)) > 0

        with pytest.raises(StopIteration):
            next(klines)

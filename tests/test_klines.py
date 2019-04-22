import pytest
from pprint import pprint
from exchanges.binance.helpers2 import to_date
from kline_data import kline_data
from exchanges.binance import klines


def test_transform_kline_data_to_useful_info():
    result = klines.generate_mcda(kline_data)
    pprint(result)


from datetime import datetime

from binance.decorators import HistoricalKlinesData

from conftest import ohlc_row

def test_historical_klines_decorator():

    obj = HistoricalKlinesData(ohlc_row)
    assert isinstance(obj.open_at, datetime)
    assert isinstance(obj.close_at, datetime)
    assert isinstance(obj.open, float)
    assert isinstance(obj.high, float)
    assert isinstance(obj.low, float)
    assert isinstance(obj.close, float)
    assert isinstance(obj.volume, float)

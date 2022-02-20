
from pandas import DataFrame

from binance.enums import KLINES_RESPONSE_COLUMNS


def test_historical_klines(klines_df):
        assert len(klines_df) == 500
        assert isinstance(klines_df, DataFrame)
        assert klines_df.columns.tolist() == KLINES_RESPONSE_COLUMNS

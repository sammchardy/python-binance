
from pandas import DataFrame

from binance.enums import KLINES_RESPONSE_COLUMNS


def test_historical_klines(historical_klines_response_df):
        klines_df = historical_klines_response_df
        assert len(klines_df) == 500
        assert isinstance(klines_df, DataFrame)
        assert klines_df.columns.tolist() == KLINES_RESPONSE_COLUMNS

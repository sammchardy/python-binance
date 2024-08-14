from pandas import DataFrame

from binance.client import Client
from binance.enums import KLINES_RESPONSE_COLUMNS

class DataClient(Client):

    def get_historical_klines(self, **args):
        klines = super().get_historical_klines(**args)
        return DataFrame(klines, columns=KLINES_RESPONSE_COLUMNS)

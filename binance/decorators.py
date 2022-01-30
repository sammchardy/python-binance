


from functools import cached_property
from datetime import datetime

class HistoricalKlinesData():
    # https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#klinecandlestick-data
    #
    # [
    #   1499040000000,      // Open time
    #   "0.01634790",       // Open
    #   "0.80000000",       // High
    #   "0.01575800",       // Low
    #   "0.01577100",       // Close
    #   "148976.11427815",  // Volume
    #   1499644799999,      // Close time
    #   "2434.19055334",    // Quote asset volume
    #   308,                // Number of trades
    #   "1756.87402397",    // Taker buy base asset volume
    #   "28.46694368",      // Taker buy quote asset volume
    #   "17928899.62484339" // Ignore
    # ]

    def __init__(self, raw_data):
        self.raw_data = raw_data

    @cached_property
    def open_at(self):
        return datetime.fromtimestamp(self.raw_data[0] / 1000)

    @cached_property
    def close_at(self):
        return datetime.fromtimestamp(self.raw_data[6] / 1000)

    @property
    def open(self):
        return float(self.raw_data[1])

    @property
    def high(self):
        return float(self.raw_data[2])

    @property
    def low(self):
        return float(self.raw_data[3])

    @property
    def close(self):
        return float(self.raw_data[4])

    @property
    def volume(self):
        return float(self.raw_data[5])

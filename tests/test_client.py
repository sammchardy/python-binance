from datetime import datetime, timedelta
import logging
import unittest
from binance import Client
from binance.enums import HistoricalKlinesType


class FuturesCoinTest(unittest.TestCase):
    def test_get_historical_klines(self):
        logging.basicConfig(level=logging.DEBUG)
        symbol = 'BTCUSD_PERP'
        interval = '1d'
        start_date = datetime(2021,1,1)
        end_date = datetime.today()
        client = Client()
        klines = client.get_historical_klines(
            symbol,
            interval,
            start_date.strftime('%d %b %Y %H:%M:%S'), 
            end_str = end_date.strftime('%d %b %Y %H:%M:%S'), 
            klines_type=HistoricalKlinesType.FUTURES_COIN)

        data_dates = {datetime.fromtimestamp(kline[0]/1000) for kline in klines}
        expect_dates = {start_date + timedelta(days=x) for x in range((end_date-start_date).days+1)}

        self.assertEqual(data_dates, expect_dates)

        last_kline_time = 0
        for kline in klines:
            self.assertTrue(kline[0] > last_kline_time)
            last_kline_time = kline[0]

        print(klines)


class FuturesTest(unittest.TestCase):
    def test_get_historical_klines(self):
        logging.basicConfig(level=logging.DEBUG)
        symbol = 'BTCUSDT'
        interval = '1d'
        start_date = datetime(2021,1,1)
        end_date = datetime.today()
        client = Client()
        klines = client.get_historical_klines(
            symbol,
            interval,
            start_date.strftime('%d %b %Y %H:%M:%S'), 
            end_str = end_date.strftime('%d %b %Y %H:%M:%S'), 
            klines_type=HistoricalKlinesType.FUTURES)
        
        print(klines)


if __name__ == '__main__':
    unittest.main()

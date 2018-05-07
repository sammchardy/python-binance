import time
import dateparser
import pytz
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import mpl_finance #import candlestick_ohlc

from datetime import datetime
from binance.client import Client
from BinanceKeys import BinanceKey1


api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']

client = Client(api_key, api_secret)
list_of_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT','BNBBTC', 'ETHBTC', 'LTCBTC']


def run():
    # get system status
    #client.ping()
    status = client.get_system_status()
    print("\nExchange Status: ", status)

    #Account Withdrawal History Info
    withdraws = client.get_withdraw_history()
    print("\nClient Withdraw History: ", withdraws)

    #get Exchange Info
    info = client.get_exchange_info()
    print("\nExchange Info (Limits): ", info)

    # place a test market buy order, to place an actual order use the create_order function
    # if '1000 ms ahead of server time' error encountered, visit https://github.com/sammchardy/python-binance/issues/249
    """order = client.create_test_order(
        symbol='BNBBTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=100)"""

    coin_prices(list_of_symbols)
    coin_tickers(list_of_symbols)
    for symbol in list_of_symbols:
        market_depth(symbol)

    #save_historic_klines_datafile("ETHBTC", "1 Dec, 2017", "1 Jan, 2018", Client.KLINE_INTERVAL_30MINUTE)

    #save_historic_klines_datafile("BTCUSDT", "12 hours ago UTC", "Now UTC", Client.KLINE_INTERVAL_1MINUTE)

def market_depth(sym, num_entries=10):
    #Get market depth
    #Retrieve and format market depth (order book) including time-stamp
    i=0     #Used as a counter for number of entries
    print("Order Book: ", convert_time_binance(client.get_server_time()))
    depth = client.get_order_book(symbol=sym)
    print("\n", sym, "\nDepth     ASKS:\n")
    print("Price     Amount")
    for ask in depth['asks']:
        if i<num_entries:
            print(ask)
            i+=1
    j=0     #Secondary Counter for Bids
    print("\n", sym, "\nDepth     BIDS:\n")
    print("Price     Amount")
    for bid in depth['bids']:
        if j<num_entries:
            print(bid)
            j+=1


def coin_prices(watch_list):
    #Will print to screen, prices of coins on 'watch list'
    #returns all prices
    prices = client.get_all_tickers()
    print("\nSelected (watch list) Ticker Prices: ")
    for price in prices:
        if price['symbol'] in watch_list:
            print(price)
    return prices


def coin_tickers(watch_list):
    # Prints to screen tickers for 'watch list' coins
    # Returns list of all price tickers
    tickers = client.get_orderbook_tickers()
    print("\nWatch List Order Tickers: \n")
    for tick in tickers:
        if tick['symbol'] in watch_list:
            print(tick)
    return tickers



def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds

    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str

    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms


def convert_time_binance(gt):
    #Converts from Binance Time Format (milliseconds) to time-struct
    #gt = client.get_server_time()
    print("Binance Time: ", gt)
    print(time.localtime())
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    #print(tt)
    return tt


def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Binance

    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str

    :return: list of OHLCV values

    """
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data

def save_historic_klines_csv(symbol, start, end, interval):
    klines = get_historical_klines(symbol, interval, start, end)
    ochl = []
    list_of_open = []
    three_period_moving_ave = []
    time3=[]
    five_period_moving_ave = []
    ten_period_moving_ave = []
    time10=[]
    with open('Binance_{}_{}-{}.txt'.format(symbol, start, end), 'w') as f:
        f.write('Time, Open, High, Low, Close, Volume\n')
        for kline in klines:
            #print(kline)
            time1 = int(kline[0])
            open1 = float(kline[1])
            Low = float(kline[2])
            High = float(kline[3])
            Close = float(kline[4])
            Volume = float(kline[5])
            format_kline = "{}, {}, {}, {}, {}, {}\n".format(time, open1, High, Low, Close, Volume)
            ochl.append([time1, open1, Close, High, Low, Volume])
            f.write(format_kline)

            #track opening prices, use for calculating moving averages
            list_of_open.append(open1)
                #Calculate three 'period' moving average - Based on Candlestick duration
            if len(list_of_open)>2:
                price3=0
                for pri in list_of_open[-3:]:
                    price3+=pri
                three_period_moving_ave.append(float(price3/3))
                time3.append(time1)
            #Perform Moving Average Calculation for 10 periods
            if len(list_of_open)>9:
                price10=0
                for pri in list_of_open[-10:]:
                    price10+=pri
                ten_period_moving_ave.append(float(price10/10))
                time10.append(time1)

    #Matplotlib visualization how-to from: https://pythonprogramming.net/candlestick-ohlc-graph-matplotlib-tutorial/
    fig, ax = plt.subplots()
    mpl_finance.candlestick_ochl(ax, ochl, width=1)
    plt.plot(time3, three_period_moving_ave, color='green', label='3 Period MA - Open')
    plt.plot(time10, ten_period_moving_ave, color='blue', label='10 Period MA - Open')
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d-%h-%m')) #Converting to date format not working
    ax.set(xlabel='Date', ylabel='Price', title='{} {}-{}'.format(symbol, start, end))
    plt.legend()
    plt.show()

def save_historic_klines_datafile(symbol, start, end, interval):
    #Collects kline historical data , output and saves to file
    klines = get_historical_klines(symbol, interval, start, end)

    # open a file with filename including symbol, interval and start and end converted to milliseconds
    with open(
        "Binance_{}_{}_{}-{}_{}-{}.json".format(
            symbol,
            interval,
            start,
            end,
            date_to_milliseconds(start),
            date_to_milliseconds(end)
        ),
        'w'  # set file write mode
    ) as f:
        f.write(json.dumps(klines))

if __name__ == "__main__":
    run()
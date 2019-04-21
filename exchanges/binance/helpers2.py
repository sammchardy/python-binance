# coding=utf-8

import dateparser
import pytz
from collections import Counter
from datetime import datetime
from itertools import zip_longest


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
    :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         int value of interval in milliseconds
         None if interval prefix is not a decimal integer
         None if interval suffix is not one of m, h, d, w
    """
    seconds_per_unit = {"m": 60, "h": 60 * 60, "d": 24 * 60 * 60, "w": 7 * 24 * 60 * 60}
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None


def to_date(timestamp):
    if type(timestamp) == int:
        return datetime.fromtimestamp(timestamp / 1000)
    return timestamp


def date_transform(result):
    for key in ["time", "updateTime"]:
        result[key] = to_date(result[key])
    return result


def date_greater_than(date, value):
    return value > date


def clean_orders(orders, date_field="time", **kwargs):
    result = [date_transform(x) for x in orders[:]]
    if "_from" in kwargs:
        result = [
            x for x in result if date_greater_than(kwargs["_from"], x[date_field])
        ]
    if "_to" in kwargs:
        result = [x for x in result if date_greater_than(x[date_field], kwargs["_to"])]
    for key in ["status", "side"]:
        if key in kwargs:
            filters = kwargs[key]
            if isinstance(filters, list):
                condition = lambda x: x in [o.upper() for o in filters]
            else:
                condition = lambda x: x == filters.upper()
            result = [x for x in result if condition(x[key])]

    return result


def trade_pairs(orders, **kwargs):
    buys = clean_orders(orders, side="buy", **kwargs)
    sells = clean_orders(orders, side="sell", **kwargs)
    return (
        [int(float(x["price"])) for x in buys],
        [int(float(x["price"])) for x in sells],
    )


def generate_pairs(buy_prices, sell_prices, _range=100):
    buy_from_sell = [x - _range for x in sell_prices]
    sell_from_buy = [x + _range for x in buy_prices]

    result1, indexes1 = build_list(buy_prices, buy_from_sell)
    result2, indexes2 = build_list(sell_from_buy, sell_prices)
    return result1, (indexes1[0], indexes2[1])


def new_trade_check_based_on_range(trade_pairs, _range):
    buy_sales, sell_sales = list(zip(*trade_pairs))
    buy_sales = [o for a in buy_sales for o in a]
    sell_sales = [o for a in sell_sales for o in a]
    result = generate_pairs(buy_sales, sell_sales, _range=_range)
    return [result[0], result[1][0], result[1][1]], _range


def trade_check(arr, index):
    if index == 0:
        return arr[0]
    previous_check = trade_check(arr, index - 1)
    value = arr[index]
    result = set(previous_check).intersection(value)
    shared, not_shared = remove_single_duplicate(value, previous_check, result)
    new_result = [x for x in value if x not in result] + not_shared
    return new_result


def generate_completed_trades(trade_pairs):
    results = [generate_pairs(x[0], x[1], _range=x[2]) for x in trade_pairs]
    new_array_to_check = [x[1] for x in results]
    _range_array = [x[-1] for x in trade_pairs]
    successful_trades = []
    for i in results:
        successful_trades += i[0]
    second_trades = [
        new_trade_check_based_on_range(new_array_to_check, x) for x in set(_range_array)
    ]
    second_successful_trades = [x[0][0] for x in second_trades]
    new_trades = [
        a
        for o in [
            trade_check(second_successful_trades, index)
            for index in range(len(second_successful_trades))
        ]
        for a in o
    ]
    import ipdb

    ipdb.set_trace()
    new_trades += successful_trades
    t_trade_groups = [[[x[0][1], x[0][2], x[1]] for x in second_trades]]
    unsuccessful_trade_group = [a for o in t_trade_groups for a in o]
    return sorted(new_trades)


def get_index(arr, index):
    try:
        result = arr[index]
    except IndexError:
        result = -1
    except KeyError:
        result = -1
    else:
        return result


def build_list(arr1, arr2):
    sold = []
    shared = set(arr1).intersection(arr2)
    not_sold_2 = [x for x in arr2 if x not in shared]
    not_sold_arr1 = [x for x in arr1 if x not in shared]

    c_arr1 = Counter(arr1)
    c_arr2 = Counter(arr2)
    for i in shared:
        v = c_arr2[i]
        u = c_arr1[i]
        diff = v - u
        for j in range(diff):
            not_sold_2.append(i)
        if diff < 0:
            if u == len(arr1):
                for o in range(abs(diff)):
                    not_sold_arr1.append(i)
            else:
                not_sold_arr1.append(i)
        for j in range(min(u, v)):
            sold.append(i)
    return sorted(sold), (sorted(not_sold_arr1), sorted(not_sold_2))


def remove_single_duplicate(arr1, arr2, shared):
    not_sold_2 = []
    sold = []
    not_sold_arr1 = []
    c_arr1 = Counter(arr1)
    c_arr2 = Counter(arr2)
    for i in shared:
        v = c_arr2[i]
        u = c_arr1[i]
        diff = v - u
        for j in range(diff):
            not_sold_2.append(i)
        if diff < 0:
            if u == len(arr1):
                for o in range(abs(diff)):
                    not_sold_arr1.append(i)
            else:
                not_sold_arr1.append(i)
        for j in range(min(u, v)):
            sold.append(i)
    return sold, not_sold_arr1

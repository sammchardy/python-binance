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

    if len(buy_prices) >= len(buy_from_sell):
        result1, indexes1 = build_list(buy_prices, buy_from_sell)
    else:
        result1, indexes1 = build_list(buy_from_sell, buy_prices)
        indexes1 = (indexes1[1], indexes1[0])

    if len(sell_prices) >= len(sell_from_buy):
        result2, indexes2 = build_list(sell_prices, sell_from_buy)
        indexes2 = (indexes2[1], indexes2[0])
    else:
        result2, indexes2 = build_list(sell_from_buy, sell_prices)
    return result1, (indexes1[0], indexes2[1])


def get_index(arr, index):
    try:
        result = arr[index]
    except IndexError:
        result = -1
    else:
        return result


def sold_items(arr2, arr1):
    not_sold = []
    result = sorted(arr2)
    indexes = [i for i, j in enumerate(sorted(arr1)) if j in set(arr2)]
    sold = []
    counter1 = Counter(arr1[:])
    counter2 = Counter(arr2[:])
    merged = set(counter1.keys()).intersection(counter2.keys())
    for i in merged:
        r = min(counter1[i], counter2[i])
        for o in range(r):
            sold.append(i)
    sold = sorted(sold)
    zipped = [o for o in zip_longest(result, sold) if o[0] != o[1]]
    not_sold = [x[0] for x in zipped]
    print(sold)
    print(zipped)
    return sold, indexes, not_sold


def build_list(arr1, arr2):
    sold = []
    sold_index = []
    not_sold_2 = []
    is_subset = False
    if set(arr2).issubset(set(arr1)):
        is_subset = True
        if len(set(arr2)) == 1:
            is_subset = False

    if is_subset:

        sold, indexes, not_sold_2 = sold_items(arr2, arr1)
        storage = []

        for i in indexes:
            ds = sorted(arr1)[i]
            if ds in arr2:
                if ds in storage and i < len(arr2):
                    if ds == sorted(arr2)[i]:
                        sold_index.append(i)
                if ds not in storage:
                    sold_index.append(i)
                    storage.append(ds)
    else:
        sold, indexes, _ = sold_items(arr2, arr1)
        for i, v in enumerate(sorted(arr2)):
            if v == sorted(arr1)[i]:
                # sold.append(v)
                sold_index.append(i)
            else:
                not_sold_2.append(v)
    not_sold_arr1 = [j for i, j in enumerate(sorted(arr1)) if i not in sold_index]
    return sold, (not_sold_arr1, not_sold_2)


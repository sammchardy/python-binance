import asyncio
from decimal import Decimal
import json
from typing import Union, Optional, Dict

import dateparser
import pytz

from datetime import datetime

from binance.exceptions import UnknownDateFormat


def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str, settings={"TIMEZONE": "UTC"})
    if not d:
        raise UnknownDateFormat(date_str)

    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval: str) -> Optional[int]:
    """Convert a Binance interval string to milliseconds

    :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w

    :return:
         int value of interval in milliseconds
         None if interval prefix is not a decimal integer
         None if interval suffix is not one of m, h, d, w

    """
    seconds_per_unit: Dict[str, int] = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None


def round_step_size(
    quantity: Union[float, Decimal], step_size: Union[float, Decimal]
) -> float:
    """Rounds a given quantity to a specific step size

    :param quantity: required
    :param step_size: required

    :return: decimal
    """
    quantity = Decimal(str(quantity))
    return float(quantity - quantity % Decimal(str(step_size)))


def convert_ts_str(ts_str):
    if ts_str is None:
        return ts_str
    if type(ts_str) == int:
        return ts_str
    return date_to_milliseconds(ts_str)


def convert_list_to_json_array(l):
    if l is None:
        return l
    res = json.dumps(l)
    return res.replace(" ", "")


def get_loop():
    """check if there is an event loop in the current thread, if not create one
    inspired by https://stackoverflow.com/questions/46727787/runtimeerror-there-is-no-current-event-loop-in-thread-in-async-apscheduler
    """
    try:
        loop = asyncio.get_event_loop()
        return loop
    except RuntimeError as e:
        if str(e).startswith("There is no current event loop in thread"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        else:
            raise

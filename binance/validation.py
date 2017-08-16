from .enums import *
from .exceptions import *

# https://binance.zendesk.com/hc/en-us/articles/115000594711
TRADE_LIMITS = {
    'ETHBTC': {
        'min_amount': 0.001,
        'min_price': 0.000001,
        'min_order_value': 0.001
    },
    'LTCBTC': {
        'min_amount': 0.01,
        'min_price': 0.000001,
        'min_order_value': 0.001
    },
    'NEOBTC': {
        'min_amount': 0.001,
        'min_price': 0.000001,
        'min_order_value': 0.001
    },
    'BNBBTC': {
        'min_amount': 1,
        'min_price': 0.00000001,
        'min_order_value': 0.001
    },
    'QTUMETH': {
        'min_amount': 0.01,
        'min_price': 0.000001,
        'min_order_value': 0.01
    },
    'SNTETH': {
        'min_amount': 1,
        'min_price': 0.00000001,
        'min_order_value': 0.01
    },
    'EOSETH': {
        'min_amount': 0.01,
        'min_price': 0.000001,
        'min_order_value': 0.01
    },
    'BNTETH': {
        'min_amount': 0.01,
        'min_price': 0.000001,
        'min_order_value': 0.01
    },
    'BCCBTC': {
        'min_amount': 0.001,
        'min_price': 0.000001,
        'min_order_value': 0.001
    },
    'GASBTC': {
        'min_amount': 0.01,
        'min_price': 0.000001,
        'min_order_value': 0.001
    },
    'BTMETH': {
        'min_amount': 1,
        'min_price': 0.00000001,
        'min_order_value': 0.01
    },
    'BNBETH': {
        'min_amount': 1,
        'min_price': 0.00000001,
        'min_order_value': 0.01
    },
    'BTCUSDT': {
        'min_amount': 0.000001,
        'min_price': 0.01,
        'min_order_value': 1
    },
    'ETHUSDT': {
        'min_amount': 0.00001,
        'min_price': 0.01,
        'min_order_value': 1
    },
    'HCCBTC': {
        'min_amount': 1,
        'min_price': 0.00000001,
        'min_order_value': 0.001
    }
}


def validate_order(params):
    limits = TRADE_LIMITS[params['symbol']]
    price = float(params['price'])
    quantity = float(params['quantity'])
    # check price
    if price < limits['min_price'] != 0:
        raise BinanceOrderMinPriceException(limits['min_price'])

    print "quantity: %s min_amount: %s" % (quantity, limits['min_amount'])
    print "mod: %f" % (quantity % limits['min_amount'])
    # check order amount
    if quantity % limits['min_amount'] != 0.0:
        raise BinanceOrderMinAmountException(limits['min_amount'])

    # check order total
    total = float(params['price']) * float(params['quantity'])
    if total < limits['min_order_value']:
        raise BinanceOrderMinTotalException(limits['min_order_value'])

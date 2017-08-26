#!/usr/bin/env python
# coding=utf-8

from .exceptions import BinanceOrderUnknownSymbolException, \
    BinanceOrderInactiveSymbolException, \
    BinanceOrderMinPriceException, \
    BinanceOrderMinAmountException, \
    BinanceOrderMinTotalException

"""
Use details from
https://www.binance.com/exchange/public/product
minTrade means min Amount
ticksize means min price

Notional limits from https://binance.zendesk.com/hc/en-us/articles/115000594711
BTC - 0.001
ETH - 0.01
USDT - 1
"""

NOTIONAL_LIMITS = {
    'BTC': 0.001,
    'ETH': 0.01,
    'USDT': 1
}


def validate_order(params, products):
    print(params)
    if params['symbol'] not in products:
        raise BinanceOrderUnknownSymbolException(params['symbol'])

    limits = products[params['symbol']]

    if not limits['active']:
        raise BinanceOrderInactiveSymbolException(params['symbol'])

    price = float(params['price'])
    quantity = float(params['quantity'])
    # check price
    if price < float(limits['tickSize']):
        raise BinanceOrderMinPriceException(limits['tickSize'])

    # check order amount
    min_trade = float(limits['minTrade'])
    if quantity / min_trade - int(quantity / min_trade) > 0.0:
        raise BinanceOrderMinAmountException(limits['minTrade'])

    # check order total
    total = float(params['price']) * float(params['quantity'])
    notional_total = NOTIONAL_LIMITS[limits['quoteAsset']]
    if total < notional_total:
        raise BinanceOrderMinTotalException(notional_total)

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
BNB - 1
"""

NOTIONAL_LIMITS = {
    'BTC': 0.001,
    'ETH': 0.01,
    'USDT': 1,
    'BNB': 1
}


def validate_order(params, products):
    if params['symbol'] not in products:
        raise BinanceOrderUnknownSymbolException(params['symbol'])

    limits = products[params['symbol']]

    if not limits['active']:
        raise BinanceOrderInactiveSymbolException(params['symbol'])

    # check order amount
    quantity = float(params['quantity'])
    min_trade = float(limits['minTrade'])
    # round here to 8 decimal places to remove any float division strangeness
    qty_per_trade = round(quantity / min_trade, 8)
    if qty_per_trade - int(qty_per_trade) > 0.0:
        raise BinanceOrderMinAmountException(limits['minTrade'])

    if 'price' in params:
        price = float(params['price'])
        # check price
        if price < float(limits['tickSize']):
            raise BinanceOrderMinPriceException(limits['tickSize'])

        # check order total
        if limits['quoteAsset'] in NOTIONAL_LIMITS:
            notional_total = NOTIONAL_LIMITS[limits['quoteAsset']]
            total = float(params['price']) * float(params['quantity'])
            if total < notional_total:
                raise BinanceOrderMinTotalException(notional_total)

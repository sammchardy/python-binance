#!/usr/bin/env python
# coding=utf-8

from binance.validation import validate_order
from binance.exceptions import *
import pytest

products = {
    "INACTV": {
        "quoteAsset": "BTC",
        "symbol": "INACTV",
        "withdrawFee": "0",
        "status": "TRADING",
        "minQty": "1E-8",
        "minTrade": "1.00000000",
        "baseAssetUnit": "",
        "quoteAssetUnit": "฿",
        "decimalPlaces": 8,
        "baseAsset": "BNB",
        "active": False,
        "tickSize": "0.00000001",
        "matchingUnitType": "STANDARD"
    },
    "BNBBTC": {
        "quoteAsset": "BTC",
        "symbol": "BNBBTC",
        "withdrawFee": "0",
        "status": "TRADING",
        "minQty": "1E-8",
        "minTrade": "1.00000000",
        "baseAssetUnit": "",
        "quoteAssetUnit": "฿",
        "decimalPlaces": 8,
        "baseAsset": "BNB",
        "active": True,
        "tickSize": "0.00000001",
        "matchingUnitType": "STANDARD"
    },
    "NEOBTC": {
         "symbol": "NEOBTC",
         "tradedMoney": 2085.15327359,
         "baseAssetUnit": "",
         "active": True,
         "minTrade": "0.01000000",
         "baseAsset": "NEO",
         "activeSell": 447667.17,
         "withdrawFee": "0",
         "tickSize": "0.000001",
         "prevClose": 0.004762,
         "activeBuy": 0,
         "volume": "447667.170000",
         "high": "0.004881",
         "lastAggTradeId": 1653525,
         "decimalPlaces": 8,
         "low": "0.004285",
         "quoteAssetUnit": "฿",
         "matchingUnitType": "STANDARD",
         "close": "0.004628",
         "quoteAsset": "BTC",
         "open": "0.004762",
         "status": "TRADING",
         "minQty": "1E-8"
    }
}


def test_missing_pair():

    with pytest.raises(BinanceOrderUnknownSymbolException):
        params = {
            'symbol': 'NOTFND',
        }
        validate_order(params, products)


def test_inactive_pair():

    with pytest.raises(BinanceOrderInactiveSymbolException):
        params = {
            'symbol': 'INACTV',
        }
        validate_order(params, products)


def test_invalid_price():

    with pytest.raises(BinanceOrderMinPriceException):
        params = {
            'symbol': 'BNBBTC',
            'price': float(products['BNBBTC']['tickSize']) * 0.9,
            'quantity': 5
        }
        validate_order(params, products)


def test_invalid_quantity():

    with pytest.raises(BinanceOrderMinAmountException):
        multiples = [0.9, 1.1]
        for m in multiples:
            params = {
                'symbol': 'BNBBTC',
                'price': float(products['BNBBTC']['tickSize']),
                'quantity': float(products['BNBBTC']['minTrade']) * m
            }
            validate_order(params, products)
    
    # this should be valid
    params = {
        'symbol': 'NEOBTC',
        'price': 0.02,
        'quantity': 2.24
    }
    validate_order(params, products)


def test_invalid_total():

    with pytest.raises(BinanceOrderMinTotalException):
        # BTC 0.001
        params = {
            'symbol': 'BNBBTC',
            'price': 0.00001,
            'quantity': 99      # total 0.00099
        }
        validate_order(params, products)


def test_valid_order():

    params = [
        {
            'symbol': 'BNBBTC',  # min order total
            'price': 0.00001,
            'quantity': 100
        },
        {
            'symbol': 'BNBBTC',  # min price
            'price': float(products['BNBBTC']['tickSize']),
            'quantity': 200000
        },
        {
            'symbol': 'BNBBTC',  # min quantity
            'price': 0.002,
            'quantity': 1
        },
        {
            'symbol': 'BNBBTC',  # min quantity
            'price': 0.002,
            'quantity': 1
        },
    ]
    for p in params:
        validate_order(p, products)

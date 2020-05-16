#!/usr/bin/env python
# coding=utf-8

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
import pytest

client = Client()


def test_invalid_json():
    """Test Invalid response Exception"""

    client.get_products()


def test_api_exception():
    """Test API response Exception"""

    client.get_server_time()


def test_api_exception_invalid_json():
    """Test API response Exception"""

    client.get_server_time()

def test_api_open_interest():
    """Test API open interest"""

    client.futures_open_interest(symbol="BTCUSDT")
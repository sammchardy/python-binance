#!/usr/bin/env python
# coding=utf-8

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
import pytest

client = Client()


def test_run_get_products():
    client.get_products()


def test_run_get_server_time():
    client.get_server_time()


def test_run_futures_open_interest():
    client.futures_open_interest(symbol="BTCUSDT")

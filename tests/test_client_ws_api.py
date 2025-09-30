import sys
import pytest
from binance.client import Client
from .conftest import proxies, api_key, api_secret, testnet
from .test_get_order_book import assert_ob

pytestmark = [pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")]

def test_ws_get_order_book(client):
    orderbook = client.ws_get_order_book(symbol="BTCUSDT")
    assert_ob(orderbook)


def test_ws_get_recent_trades(client):
    client.ws_get_recent_trades(symbol="BTCUSDT")


def test_ws_get_historical_trades(client):
    client.ws_get_historical_trades(symbol="BTCUSDT")


def test_ws_get_aggregate_trades(client):
    client.ws_get_aggregate_trades(symbol="BTCUSDT")


def test_ws_get_klines(client):
    client.ws_get_klines(symbol="BTCUSDT", interval="1m")


def test_ws_get_uiKlines(client):
    client.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")


def test_ws_get_avg_price(client):
    client.ws_get_avg_price(symbol="BTCUSDT")


def test_ws_get_ticker(client):
    client.ws_get_ticker(symbol="BTCUSDT")


def test_ws_get_trading_day_ticker(client):
    client.ws_get_trading_day_ticker(symbol="BTCUSDT")


def test_ws_get_symbol_ticker_window(client):
    client.ws_get_symbol_ticker_window(symbol="BTCUSDT")


def test_ws_get_symbol_ticker(client):
    client.ws_get_symbol_ticker(symbol="BTCUSDT")


def test_ws_get_orderbook_ticker(client):
    client.ws_get_orderbook_ticker(symbol="BTCUSDT")


def test_ws_ping(client):
    client.ws_ping()


def test_ws_get_time(client):
    client.ws_get_time()


def test_ws_get_exchange_info(client):
    client.ws_get_exchange_info(symbol="BTCUSDT")


def test_ws_time_microseconds():
    micro_client = Client(
        api_key,
        api_secret,
        {"proxies": proxies},
        testnet=testnet,
        time_unit="MICROSECOND",
    )
    micro_trades = micro_client.ws_get_recent_trades(symbol="BTCUSDT")
    assert len(str(micro_trades[0]["time"])) >= 16, (
        "WS time should be in microseconds (16+ digits)"
    )


def test_ws_time_milliseconds():
    milli_client = Client(
        api_key,
        api_secret,
        {"proxies": proxies},
        testnet=testnet,
        time_unit="MILLISECOND",
    )
    milli_trades = milli_client.ws_get_recent_trades(symbol="BTCUSDT")
    assert len(str(milli_trades[0]["time"])) == 13, (
        "WS time should be in milliseconds (13 digits)"
    )

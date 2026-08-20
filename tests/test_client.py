import sys
from unittest.mock import MagicMock
import pytest
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .conftest import (
    proxies,
    api_key,
    api_secret,
    testnet,
    call_method_and_assert_uri_contains,
)


def test_client_initialization(client):
    assert client.API_KEY is not None
    assert client.API_SECRET is not None


@pytest.mark.skip(reason="Endpoint not documented")
def test_get_products(client):
    client.get_products()


def test_get_exchange_info(client):
    client.get_exchange_info()


def test_get_symbol_info(client):
    client.get_symbol_info("BTCUSDT")


def test_ping(client):
    call_method_and_assert_uri_contains(client, "ping", "/v3/")


def test_get_server_time(client):
    client.get_server_time()


def test_get_all_tickers(client):
    client.get_all_tickers()


def test_get_orderbook_tickers(client):
    client.get_orderbook_tickers()


def test_get_order_book(client):
    client.get_order_book(symbol="BTCUSDT")


def test_get_recent_trades(client):
    client.get_recent_trades(symbol="BTCUSDT")


def test_get_historical_trades(client):
    client.get_historical_trades(symbol="BTCUSDT")


def test_get_aggregate_trades(client):
    client.get_aggregate_trades(symbol="BTCUSDT")


def test_get_klines(client):
    client.get_klines(symbol="BTCUSDT", interval="1d")


def test_get_ui_klines(client):
    client.get_ui_klines(symbol="BTCUSDT", interval="1d")


def test_get_avg_price(client):
    client.get_avg_price(symbol="BTCUSDT")


def test_get_ticker(client):
    client.get_ticker(symbol="BTCUSDT")


def test_get_symbol_ticker(client):
    client.get_symbol_ticker(symbol="BTCUSDT")


def test_get_orderbook_ticker(client):
    call_method_and_assert_uri_contains(
        client, "get_orderbook_ticker", "/v3/", symbol="BTCUSDT"
    )


def test_get_account(client):
    client.get_account()


def test_get_asset_balance(client):
    client.get_asset_balance(asset="BTC")


def test_get_asset_balance_no_asset_provided(client):
    client.get_asset_balance()


def test_get_my_trades(client):
    client.get_my_trades(symbol="BTCUSDT")


def test_get_system_status(client):
    client.get_system_status()


# User Stream Endpoints


@pytest.mark.skip(reason="Testnet returns 410 Gone")
def test_stream_get_listen_key_and_close(client):
    listen_key = client.stream_get_listen_key()
    client.stream_close(listen_key)


# Quoting interface endpoints
@pytest.mark.skip(reason="Endpoint not working on testnet")
def test_get_account_status(client):
    client.get_account_status()


@pytest.mark.skip(reason="Endpoint not working on testnet")
def test_get_account_api_trading_status(client):
    client.get_account_api_trading_status()


@pytest.mark.skip(reason="Endpoint not working on testnet")
def test_get_account_api_permissions(client):
    client.get_account_api_permissions()


@pytest.mark.skip(reason="Endpoint not working on testnet")
def test_get_dust_assets(client):
    client.get_dust_assets()


#########################
# Websocket API Requests #
#########################


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_order_book(client):
    client.ws_get_order_book(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_recent_trades(client):
    client.ws_get_recent_trades(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_historical_trades(client):
    client.ws_get_historical_trades(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_aggregate_trades(client):
    client.ws_get_aggregate_trades(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_klines(client):
    client.ws_get_klines(symbol="BTCUSDT", interval="1m")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_uiKlines(client):
    client.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_avg_price(client):
    client.ws_get_avg_price(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_ticker(client):
    ticker = client.ws_get_ticker(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_trading_day_ticker(client):
    client.ws_get_trading_day_ticker(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_symbol_ticker_window(client):
    client.ws_get_symbol_ticker_window(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_symbol_ticker(client):
    client.ws_get_symbol_ticker(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_orderbook_ticker(client):
    client.ws_get_orderbook_ticker(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_ping(client):
    client.ws_ping()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_time(client):
    client.ws_get_time()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
def test_ws_get_exchange_info(client):
    client.ws_get_exchange_info(symbol="BTCUSDT")


def test_time_unit_microseconds():
    micro_client = Client(
        api_key,
        api_secret,
        {"proxies": proxies},
        testnet=testnet,
        time_unit="MICROSECOND",
    )
    micro_trades = micro_client.get_recent_trades(symbol="BTCUSDT")
    assert len(str(micro_trades[0]["time"])) >= 16, (
        "Time should be in microseconds (16+ digits)"
    )


def test_time_unit_milloseconds():
    milli_client = Client(
        api_key,
        api_secret,
        {"proxies": proxies},
        testnet=testnet,
        time_unit="MILLISECOND",
    )
    milli_trades = milli_client.get_recent_trades(symbol="BTCUSDT")
    assert len(str(milli_trades[0]["time"])) == 13, (
        "Time should be in milliseconds (13 digits)"
    )


def test_handle_response(client):
    # Test successful JSON response
    mock_response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "text": '{"key": "value"}',
            "json": lambda: {"key": "value"},
        },
    )
    assert client._handle_response(mock_response) == {"key": "value"}

    # Test empty response
    mock_empty_response = type("Response", (), {"status_code": 200, "text": ""})
    assert client._handle_response(mock_empty_response) == {}

    # Test invalid JSON response
    mock_invalid_response = type(
        "Response",
        (),
        {
            "status_code": 200,
            "text": "invalid json",
            "json": lambda: exec("raise ValueError()"),
        },
    )
    with pytest.raises(BinanceRequestException):
        client._handle_response(mock_invalid_response)

    # Test error status code
    mock_error_response = type(
        "Response", (), {"status_code": 400, "text": "error message"}
    )
    with pytest.raises(BinanceAPIException):
        client._handle_response(mock_error_response)


def _no_network_client():
    # aggregate_trade_iter's pagination logic doesn't need a live connection;
    # ping=False avoids the network round-trip Client() otherwise makes.
    return Client(
        api_key, api_secret, {"proxies": proxies}, testnet=testnet, ping=False
    )


def test_aggregate_trade_iter_end_str_stops_at_boundary():
    """Regression test for #497: without end_str the iterator has no way to
    stop, so a long-running collection can grow unbounded. With end_str set,
    it should yield only trades at/before that time and stop without
    fetching further pages."""
    client = _no_network_client()
    client.get_aggregate_trades = MagicMock(
        return_value=[
            {"a": 1, "T": 1000},
            {"a": 2, "T": 2000},
            {"a": 3, "T": 3000},
        ]
    )

    result = list(
        client.aggregate_trade_iter(symbol="BTCUSDT", start_str=500, end_str=2000)
    )

    assert [t["a"] for t in result] == [1, 2]
    client.get_aggregate_trades.assert_called_once()


def test_aggregate_trade_iter_end_str_with_last_id_spans_pages():
    client = _no_network_client()
    client.get_aggregate_trades = MagicMock(
        side_effect=[
            # first page: fromId=100 echoes id 100, then two new trades
            [{"a": 100, "T": 900}, {"a": 101, "T": 1000}, {"a": 102, "T": 2000}],
            # second page: fromId=102 echoes id 102, then trades past end_ts
            [{"a": 102, "T": 2000}, {"a": 103, "T": 2600}, {"a": 104, "T": 3000}],
        ]
    )

    result = list(
        client.aggregate_trade_iter(symbol="BTCUSDT", last_id=100, end_str=2500)
    )

    assert [t["a"] for t in result] == [101, 102]
    assert client.get_aggregate_trades.call_count == 2


def test_aggregate_trade_iter_without_end_str_keeps_old_behavior():
    client = _no_network_client()
    client.get_aggregate_trades = MagicMock(
        side_effect=[
            [{"a": 5, "T": 100}, {"a": 6, "T": 200}],
            [{"a": 6, "T": 200}],  # no new trades after the echoed id -> stop
        ]
    )

    result = list(client.aggregate_trade_iter(symbol="BTCUSDT", last_id=5))

    assert [t["a"] for t in result] == [6]
    assert client.get_aggregate_trades.call_count == 2

import pytest


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
    client.ping()


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


def test_get_avg_price(client):
    client.get_avg_price(symbol="BTCUSDT")


def test_get_ticker(client):
    client.get_ticker(symbol="BTCUSDT")


def test_get_symbol_ticker(client):
    client.get_symbol_ticker(symbol="BTCUSDT")


def test_get_orderbook_ticker(client):
    client.get_orderbook_ticker(symbol="BTCUSDT")


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


def test_ws_get_order_book(client):
    client.ws_get_order_book(symbol="BTCUSDT")


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
    ticker = client.ws_get_ticker(symbol="BTCUSDT")


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

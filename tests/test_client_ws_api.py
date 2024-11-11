from .test_get_order_book import assert_ob


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

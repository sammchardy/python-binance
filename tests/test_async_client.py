import pytest
import sys

from binance.async_client import AsyncClient
from .conftest import proxy, api_key, api_secret, testnet
from binance.exceptions import BinanceAPIException, BinanceRequestException
from aiohttp import ClientResponse, hdrs
from aiohttp.helpers import TimerNoop
from yarl import URL

pytestmark = [pytest.mark.asyncio]


async def test_clientAsync_initialization(clientAsync):
    assert clientAsync.API_KEY is not None
    assert clientAsync.API_SECRET is not None


@pytest.mark.skip(reason="Endpoint not documented")
async def test_get_products(clientAsync):
    await clientAsync.get_products()
    

async def test_get_exchange_info(clientAsync):
    await clientAsync.get_exchange_info()
    
async def test_get_symbol_info(clientAsync):
    await clientAsync.get_symbol_info("BTCUSDT")
    

async def test_ping(clientAsync):
    await clientAsync.ping()
    
async def test_get_server_time(clientAsync):
    await clientAsync.get_server_time()
    
async def test_get_all_tickers(clientAsync):
    await clientAsync.get_all_tickers()

async def test_get_orderbook_tickers(clientAsync):
    await clientAsync.get_orderbook_tickers()
    
async def test_get_order_book(clientAsync):
    await clientAsync.get_order_book(symbol="BTCUSDT")
    
async def test_get_recent_trades(clientAsync):
    await clientAsync.get_recent_trades(symbol="BTCUSDT")


async def test_get_historical_trades(clientAsync):
    await clientAsync.get_historical_trades(symbol="BTCUSDT")
    

async def test_get_aggregate_trades(clientAsync):
    await clientAsync.get_aggregate_trades(symbol="BTCUSDT")
    
async def test_get_klines(clientAsync):
    await clientAsync.get_klines(symbol="BTCUSDT", interval="1d")
    
async def test_get_uiklines(clientAsync):
    await clientAsync.get_ui_klines(symbol="BTCUSDT", interval="1d")
    
async def test_futures_mark_price_klines(clientAsync):
    await clientAsync.futures_mark_price_klines(symbol="BTCUSDT", interval="1h")
    
async def test_futures_index_price_klines(clientAsync):
    await clientAsync.futures_index_price_klines(pair="BTCUSDT", interval="1h")
    
async def test_futures_premium_index_klines(clientAsync):
    await clientAsync.futures_premium_index_klines(symbol="BTCUSDT", interval="1h")
    
@pytest.mark.skip(reason="network error")
async def test_futures_coin_premium_index_klines(clientAsync):
    await clientAsync.futures_coin_premium_index_klines(symbol="BTCUSD", interval="1h")
    
async def test_get_avg_price(clientAsync):
    await clientAsync.get_avg_price(symbol="BTCUSDT")
    
async def test_get_ticker(clientAsync):
    await clientAsync.get_ticker(symbol="BTCUSDT")
    
async def test_get_symbol_ticker(clientAsync):
    await clientAsync.get_symbol_ticker(symbol="BTCUSDT")
    
async def test_get_orderbook_ticker(clientAsync):
    await clientAsync.get_orderbook_ticker(symbol="BTCUSDT")
    
async def test_get_account(clientAsync):
    await clientAsync.get_account()
    
async def test_get_asset_balance(clientAsync):
    await clientAsync.get_asset_balance(asset="BTC")
    
async def test_get_asset_balance_no_asset_provided(clientAsync):
    await clientAsync.get_asset_balance()
    
async def test_get_my_trades(clientAsync):
    await clientAsync.get_my_trades(symbol="BTCUSDT")
    
async def test_get_system_status(clientAsync):
    await clientAsync.get_system_status()
    
# User Stream Endpoints


async def test_stream_get_listen_key_and_close(clientAsync):
    listen_key = await clientAsync.stream_get_listen_key()
    await clientAsync.stream_close(listen_key)
    
# Quoting interface endpoints


#########################
# Websocket API Requests #
#########################


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_order_book(clientAsync):
    await clientAsync.ws_get_order_book(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_recent_trades(clientAsync):
    await clientAsync.ws_get_recent_trades(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_historical_trades(clientAsync):
    await clientAsync.ws_get_historical_trades(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_aggregate_trades(clientAsync):
    await clientAsync.ws_get_aggregate_trades(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_klines(clientAsync):
    await clientAsync.ws_get_klines(symbol="BTCUSDT", interval="1m")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_uiKlines(clientAsync):
    await clientAsync.ws_get_uiKlines(symbol="BTCUSDT", interval="1m")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_avg_price(clientAsync):
    await clientAsync.ws_get_avg_price(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_ticker(clientAsync):
    ticker = await clientAsync.ws_get_ticker(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_trading_day_ticker(clientAsync):
    await clientAsync.ws_get_trading_day_ticker(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_symbol_ticker_window(clientAsync):
    await clientAsync.ws_get_symbol_ticker_window(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_symbol_ticker(clientAsync):
    await clientAsync.ws_get_symbol_ticker(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_orderbook_ticker(clientAsync):
    await clientAsync.ws_get_orderbook_ticker(symbol="BTCUSDT")
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_ping(clientAsync):
    await clientAsync.ws_ping()
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_time(clientAsync):
    await clientAsync.ws_get_time()
    
@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
async def test_ws_get_exchange_info(clientAsync):
    await clientAsync.ws_get_exchange_info(symbol="BTCUSDT")
    
@pytest.mark.skip(reason="can't test margin endpoints")
async def test_margin_next_hourly_interest_rate(clientAsync):
    await clientAsync.margin_next_hourly_interest_rate(
        assets="BTC",
        isIsolated="FALSE"
    )
    
@pytest.mark.skip(reason="can't test margin endpoints")
async def test_margin_interest_history(clientAsync):
    await clientAsync.margin_interest_history(
        asset="BTC",
    )
    
@pytest.mark.skip(reason="can't test margin endpoints")
async def test_margin_borrow_repay(clientAsync):
    await clientAsync.margin_borrow_repay(
        asset="BTC",
        amount=0.1,
        isIsolated="FALSE",
        symbol="BTCUSDT",
        type="BORROW"
    )
        
@pytest.mark.skip(reason="can't test margin endpoints")
async def test_margin_get_borrow_repay_records(clientAsync):
    await clientAsync.margin_get_borrow_repay_records(
        asset="BTC",
        isolatedSymbol="BTCUSDT",
    )
        
@pytest.mark.skip(reason="can't test margin endpoints")
async def test_margin_interest_rate_history(clientAsync):
    await clientAsync.margin_interest_rate_history(
        asset="BTC",
    )
        
@pytest.mark.skip(reason="can't test margin endpoints")
async def test_margin_max_borrowable(clientAsync):
    await clientAsync.margin_max_borrowable(
        asset="BTC",
    )
    
async def test_time_unit_microseconds():
    micro_client = AsyncClient(
        api_key, api_secret, https_proxy=proxy, testnet=testnet, time_unit="MICROSECOND"
    )
    micro_trades = await micro_client.get_recent_trades(symbol="BTCUSDT")
    assert len(str(micro_trades[0]["time"])) >= 16, (
        "Time should be in microseconds (16+ digits)"
    )
    await micro_client.close_connection()

async def test_time_unit_milloseconds():
    milli_client = AsyncClient(
        api_key, api_secret, https_proxy=proxy, testnet=testnet, time_unit="MILLISECOND"
    )
    milli_trades = await milli_client.get_recent_trades(symbol="BTCUSDT")
    assert len(str(milli_trades[0]["time"])) == 13, (
        "Time should be in milliseconds (13 digits)"
    )
    await milli_client.close_connection()


async def test_handle_response(clientAsync):
    # Create base response object
    mock_response = ClientResponse(
        'GET', URL('http://test.com'),
        request_info=None,
        writer=None,
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=clientAsync.loop,
        session=None,
    )
    # Initialize headers
    mock_response._headers = {hdrs.CONTENT_TYPE: 'application/json'}

    # Test successful JSON response
    mock_response.status = 200
    mock_response._body = b'{"key": "value"}'
    assert await clientAsync._handle_response(mock_response) == {"key": "value"}

    # Test empty response
    mock_response.status = 200
    mock_response._body = b''
    assert await clientAsync._handle_response(mock_response) == {}

    # Test invalid JSON response
    mock_response.status = 200
    mock_response._body = b'invalid json'
    with pytest.raises(BinanceRequestException):
        await clientAsync._handle_response(mock_response)

    # Test error status code
    mock_response.status = 400
    mock_response._body = b'error message'
    with pytest.raises(BinanceAPIException):
        await clientAsync._handle_response(mock_response)
    
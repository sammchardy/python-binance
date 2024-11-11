import json
import re
import pytest
import asyncio
from binance import AsyncClient

from binance.exceptions import BinanceAPIException, BinanceWebsocketUnableToConnect
from binance.ws.constants import WSListenerState
from .test_get_order_book import assert_ob


@pytest.mark.asyncio
async def test_ws_api_public_endpoint(clientAsync):
    """Test normal order book request"""
    order_book = await clientAsync.ws_get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


@pytest.mark.asyncio
async def test_ws_api_private_endpoint(clientAsync):
    """Test normal order book request"""
    orders = await clientAsync.ws_get_all_orders(symbol="BTCUSDT")


@pytest.mark.asyncio
async def test_ws_futures_public_endpoint(futuresClientAsync):
    """Test normal order book request"""
    order_book = await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


@pytest.mark.asyncio
async def test_ws_futures_private_endpoint(futuresClientAsync):
    """Test normal order book request"""
    await futuresClientAsync.ws_futures_v2_account_position(symbol="BTCUSDT")


@pytest.mark.asyncio
async def test_ws_get_symbol_ticker(clientAsync):
    """Test symbol ticker request"""
    ticker = await clientAsync.ws_get_symbol_ticker(symbol="BTCUSDT")
    assert "symbol" in ticker
    assert ticker["symbol"] == "BTCUSDT"


@pytest.mark.asyncio
async def test_invalid_request(clientAsync):
    """Test error handling for invalid symbol"""
    with pytest.raises(
        BinanceAPIException,
        match=re.escape(
            "APIError(code=-1100): Illegal characters found in parameter 'symbol'; legal range is '^[A-Z0-9-_.]{1,20}$'."
        ),
    ):
        await clientAsync.ws_get_order_book(symbol="send error")


@pytest.mark.asyncio
async def test_connection_handling(clientAsync):
    """Test connection handling and reconnection"""
    # First request should establish connection
    await clientAsync.ws_get_order_book(symbol="BTCUSDT")
    assert clientAsync.ws_api.ws_state == WSListenerState.STREAMING

    # Force connection close
    await clientAsync.close_connection()
    assert clientAsync.ws_api.ws_state == WSListenerState.EXITING
    assert clientAsync.ws_api.ws is None

    # Next request should reconnect
    order_book = await clientAsync.ws_get_order_book(symbol="LTCUSDT")
    assert_ob(order_book)
    assert clientAsync.ws_api.ws_state == WSListenerState.STREAMING


@pytest.mark.asyncio
async def test_timeout_handling(clientAsync):
    """Test request timeout handling"""
    # Set very short timeout to force timeout error
    original_timeout = clientAsync.ws_api.TIMEOUT
    clientAsync.ws_api.TIMEOUT = 0.0001

    try:
        with pytest.raises(BinanceWebsocketUnableToConnect, match="Request timed out"):
            await clientAsync.ws_get_order_book(symbol="BTCUSDT")
    finally:
        clientAsync.ws_api.TIMEOUT = original_timeout


@pytest.mark.asyncio
async def test_multiple_requests(clientAsync):
    """Test multiple concurrent requests"""
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    tasks = [clientAsync.ws_get_order_book(symbol=symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks)
    assert len(results) == len(symbols)
    for result in results:
        assert_ob(result)


@pytest.mark.asyncio
async def test_testnet_url():
    """Test testnet URL configuration"""
    testnet_client = AsyncClient(testnet=True)
    try:
        assert testnet_client.ws_api._url == testnet_client.WS_API_TESTNET_URL
        order_book = await testnet_client.ws_get_order_book(symbol="BTCUSDT")
        assert_ob(order_book)
    finally:
        await testnet_client.close_connection()


@pytest.mark.asyncio
async def test_message_handling(clientAsync):
    """Test message handling with various message types"""
    # Test valid message
    valid_msg = {"id": "123", "result": {"test": "data"}}
    result = clientAsync.ws_api._handle_message(json.dumps(valid_msg))
    assert result == valid_msg

    # Test message without ID
    no_id_msg = {"data": "test"}
    result = clientAsync.ws_api._handle_message(json.dumps(no_id_msg))
    assert result == no_id_msg

    # Test invalid JSON
    result = clientAsync.ws_api._handle_message("invalid json")
    assert result is None


@pytest.mark.asyncio(scope="function")
async def test_connection_failure(clientAsync):
    """Test handling of connection failures"""
    # Set invalid URL
    clientAsync.ws_api._url = "wss://invalid.url"

    with pytest.raises(BinanceWebsocketUnableToConnect, match="Connection failed"):
        await clientAsync.ws_get_order_book(symbol="BTCUSDT")


@pytest.mark.asyncio(scope="function")
async def test_cleanup_on_exit(clientAsync):
    """Test cleanup of resources on exit"""
    # Create some pending requests
    future = asyncio.Future()
    clientAsync.ws_api._responses["test"] = future

    # Close connection
    await clientAsync.close_connection()

    # Check cleanup
    assert "test" not in clientAsync.ws_api._responses
    assert future.exception() is not None

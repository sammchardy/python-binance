import json
import re
import pytest
import asyncio
from binance import AsyncClient
import os

from binance.exceptions import BinanceAPIException, BinanceWebsocketUnableToConnect
from binance.ws.constants import WSListenerState
from .test_get_order_book import assert_ob

proxy = os.getenv("PROXY")


@pytest.fixture(scope="function")
def client():
    """Fixture to create and cleanup client"""
    return AsyncClient(api_key="api_key", api_secret="api_secret", https_proxy=proxy)


@pytest.mark.asyncio
async def test_get_order_book(client):
    """Test normal order book request"""
    order_book = await client.ws_get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


@pytest.mark.asyncio
async def test_get_symbol_ticker(client):
    """Test symbol ticker request"""
    ticker = await client.ws_get_symbol_ticker(symbol="BTCUSDT")
    assert "symbol" in ticker
    assert ticker["symbol"] == "BTCUSDT"


@pytest.mark.asyncio
async def test_invalid_request(client):
    """Test error handling for invalid symbol"""
    with pytest.raises(
        BinanceAPIException,
        match=re.escape(
            "APIError(code=-1100): Illegal characters found in parameter 'symbol'; legal range is '^[A-Z0-9-_.]{1,20}$'."
        ),
    ):
        await client.ws_get_order_book(symbol="send error")


@pytest.mark.asyncio
async def test_connection_handling(client):
    """Test connection handling and reconnection"""
    # First request should establish connection
    await client.ws_get_order_book(symbol="BTCUSDT")
    assert client.ws_api.ws_state == WSListenerState.STREAMING

    # Force connection close
    await client.close_connection()
    assert client.ws_api.ws_state == WSListenerState.EXITING
    assert client.ws_api.ws is None

    # Next request should reconnect
    order_book = await client.ws_get_order_book(symbol="LTCUSDT")
    assert_ob(order_book)
    assert client.ws_api.ws_state == WSListenerState.STREAMING


@pytest.mark.asyncio
async def test_timeout_handling(client):
    """Test request timeout handling"""
    # Set very short timeout to force timeout error
    original_timeout = client.ws_api.TIMEOUT
    client.ws_api.TIMEOUT = 0.0001

    try:
        with pytest.raises(BinanceWebsocketUnableToConnect, match="Request timed out"):
            await client.ws_get_order_book(symbol="BTCUSDT")
    finally:
        client.ws_api.TIMEOUT = original_timeout


@pytest.mark.asyncio
async def test_multiple_requests(client):
    """Test multiple concurrent requests"""
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    tasks = [client.ws_get_order_book(symbol=symbol) for symbol in symbols]
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
async def test_message_handling(client):
    """Test message handling with various message types"""
    # Test valid message
    valid_msg = {"id": "123", "result": {"test": "data"}}
    result = client.ws_api._handle_message(json.dumps(valid_msg))
    assert result == valid_msg

    # Test message without ID
    no_id_msg = {"data": "test"}
    result = client.ws_api._handle_message(json.dumps(no_id_msg))
    assert result == no_id_msg

    # Test invalid JSON
    result = client.ws_api._handle_message("invalid json")
    assert result is None


@pytest.mark.asyncio(scope="function")
async def test_connection_failure(client):
    """Test handling of connection failures"""
    # Set invalid URL
    client.ws_api._url = "wss://invalid.url"

    with pytest.raises(BinanceWebsocketUnableToConnect, match="Connection failed"):
        await client.ws_get_order_book(symbol="BTCUSDT")


@pytest.mark.asyncio(scope="function")
async def test_cleanup_on_exit(client):
    """Test cleanup of resources on exit"""
    # Create some pending requests
    future = asyncio.Future()
    client.ws_api._responses["test"] = future

    # Close connection
    await client.close_connection()

    # Check cleanup
    assert "test" not in client.ws_api._responses
    assert future.exception() is not None

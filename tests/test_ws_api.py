import json
import sys
import pytest
import asyncio
from binance import AsyncClient

from binance.exceptions import BinanceAPIException, BinanceWebsocketUnableToConnect
from binance.ws.constants import WSListenerState
from .test_get_order_book import assert_ob
from .conftest import proxy


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_api_public_endpoint(clientAsync):
    """Test normal order book request"""
    order_book = await clientAsync.ws_get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_api_private_endpoint(clientAsync):
    """Test normal order book request"""
    orders = await clientAsync.ws_get_all_orders(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_futures_public_endpoint(futuresClientAsync):
    """Test normal order book request"""
    order_book = await futuresClientAsync.ws_futures_get_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_futures_private_endpoint(futuresClientAsync):
    """Test normal order book request"""
    await futuresClientAsync.ws_futures_v2_account_position(symbol="BTCUSDT")


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_get_symbol_ticker(clientAsync):
    """Test symbol ticker request"""
    ticker = await clientAsync.ws_get_symbol_ticker(symbol="BTCUSDT")
    assert "symbol" in ticker
    assert ticker["symbol"] == "BTCUSDT"


@pytest.mark.asyncio
async def test_invalid_request(clientAsync):
    pass
    # """Test error handling for invalid symbol"""
    # with pytest.raises(
    #     BinanceAPIException,
    #     match=re.escape(
    #         "APIError(code=-1100): Illegal characters found in parameter 'symbol'; legal range is \'^[\\\\w\\\\-._&&[^a-z]]{1,50}$\'."
    #     ),
    # ):
        
    #     # {'id': 'a2790cf96b11a8add71ebf', 'status': 400, 'error': {'code': -1100...:-1100,"msg":"Illegal characters found in parameter \'symbol\'; legal range is \'^[\\\\w\\\\-._&&[^a-z]]{1,50}$\'."}'
    #     await clientAsync.ws_get_order_book(symbol="send error")


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
    testnet_client = AsyncClient(testnet=True, https_proxy=proxy)
    try:
        assert testnet_client.ws_api._url == testnet_client.WS_API_TESTNET_URL
        order_book = await testnet_client.ws_get_order_book(symbol="BTCUSDT")
        assert_ob(order_book)
    finally:
        await testnet_client.close_connection()


@pytest.mark.asyncio
async def test_message_handling(clientAsync):
    """Test message handling with various message types"""
    try:
        # Test valid message
        future = asyncio.Future()
        clientAsync.ws_api._responses["123"] = future
        valid_msg = {"id": "123", "status": 200, "result": {"test": "data"}}
        clientAsync.ws_api._handle_message(json.dumps(valid_msg))
        result = await clientAsync.ws_api._responses["123"]
        assert result == valid_msg
    finally:
        await clientAsync.close_connection()

@pytest.mark.asyncio
async def test_message_handling_raise_exception(clientAsync):
    try:
        with pytest.raises(BinanceAPIException):
            future = asyncio.Future()
            clientAsync.ws_api._responses["123"] = future
            valid_msg = {"id": "123", "status": 400, "error": {"code": "0", "msg": "error message"}}
            clientAsync.ws_api._handle_message(json.dumps(valid_msg))
            await future
    finally:
        await clientAsync.close_connection()

@pytest.mark.asyncio
async def test_message_handling_raise_exception_without_id(clientAsync):
    try:
        with pytest.raises(BinanceAPIException):
            future = asyncio.Future()
            clientAsync.ws_api._responses["123"] = future
            valid_msg = {"id": "123", "status": 400, "error": {"code": "0", "msg": "error message"}}
            clientAsync.ws_api._handle_message(json.dumps(valid_msg))
            await future
    finally:
        await clientAsync.close_connection()


@pytest.mark.asyncio
async def test_message_handling_invalid_json(clientAsync):
    try:
        with pytest.raises(json.JSONDecodeError):
            clientAsync.ws_api._handle_message("invalid json")

        with pytest.raises(json.JSONDecodeError):
            clientAsync.ws_api._handle_message("invalid json")
    finally:
        # Ensure cleanup
        await clientAsync.close_connection()


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


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_queue_overflow(clientAsync):
    """WebSocket API should not overflow queue"""
    #
    original_size = clientAsync.ws_api.max_queue_size
    clientAsync.ws_api.max_queue_size = 1

    try:
        # Request multiple order books concurrently
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        tasks = [clientAsync.ws_get_order_book(symbol=symbol) for symbol in symbols]

        # Execute all requests concurrently and wait for results
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check that we got valid responses or expected overflow errors
        valid_responses = [r for r in results if not isinstance(r, Exception)]
        assert len(valid_responses) == len(symbols), "Should get at least one valid response"

        for result in valid_responses:
            assert_ob(result)

    finally:
        # Restore original queue size
        clientAsync.ws_api.MAX_QUEUE_SIZE = original_size


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_ws_api_with_stream(clientAsync):
    """Test combining WebSocket API requests with stream listening"""
    from binance import BinanceSocketManager

    # Create socket manager and trade socket
    bm = BinanceSocketManager(clientAsync)
    ts = bm.trade_socket("BTCUSDT")

    async with ts:
        # Make WS API request while stream is active
        order_book = await clientAsync.ws_get_order_book(symbol="BTCUSDT")
        assert_ob(order_book)

        # Verify we can still receive stream data
        trade = await ts.recv()
        assert "s" in trade  # Symbol
        assert "p" in trade  # Price
        assert "q" in trade  # Quantity

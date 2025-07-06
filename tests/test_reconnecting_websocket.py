import sys
import pytest
import gzip
import json
from unittest.mock import patch, create_autospec, Mock
from binance.ws.reconnecting_websocket import ReconnectingWebsocket
from binance.ws.constants import WSListenerState
from binance.exceptions import BinanceWebsocketUnableToConnect, ReadLoopClosed
from websockets import WebSocketClientProtocol  # type: ignore
from websockets.protocol import State
import asyncio

try:
    from unittest.mock import AsyncMock  # Python 3.8+
except ImportError:
    from asynctest import CoroutineMock as AsyncMock  # Python 3.7


@pytest.mark.asyncio
async def test_init():
    ws = ReconnectingWebsocket(url="wss://test.url", path="/test")
    assert ws._url == "wss://test.url"
    assert ws._path == "/test"
    assert ws.ws_state == WSListenerState.INITIALISING


@pytest.mark.asyncio
async def test_json_dumps():
    ws = ReconnectingWebsocket(url="wss://test.url")
    data = {"key": "value"}
    dumped = ws.json_dumps(data)
    assert isinstance(dumped, (str, bytes))


@pytest.mark.asyncio
async def test_json_loads():
    ws = ReconnectingWebsocket(url="wss://test.url")
    data_str = '{"key": "value"}'
    loaded = ws.json_loads(data_str)
    assert loaded == {"key": "value"}


@pytest.mark.asyncio
async def test_json_loads_invalid():
    ws = ReconnectingWebsocket(url="wss://test.url")
    data_str = "invalid json"
    with pytest.raises(json.JSONDecodeError):
        ws.json_loads(data_str)


@pytest.mark.asyncio
async def test_handle_message():
    ws = ReconnectingWebsocket(url="wss://test.url")
    message = '{"key": "value"}'
    result = ws._handle_message(message)
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_handle_message_binary():
    ws = ReconnectingWebsocket(url="wss://test.url", is_binary=True)
    data = b'{"key": "value"}'
    compressed = gzip.compress(data)
    result = ws._handle_message(compressed)
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_handle_message_invalid_json():
    ws = ReconnectingWebsocket(url="wss://test.url")
    message = "invalid json"
    with pytest.raises(Exception):
        ws._handle_message(message)


@pytest.mark.asyncio
async def test_recv_message():
    ws = ReconnectingWebsocket(url="wss://test.url")
    await ws._queue.put({"test": "data"})
    # Simulate the read loop being active
    ws._handle_read_loop = Mock()
    result = await ws.recv()
    assert result == {"test": "data"}


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_before_reconnect():
    ws = ReconnectingWebsocket(url="wss://test.url")
    ws.ws = AsyncMock()
    ws._conn = AsyncMock()
    ws._reconnects = 0
    await ws.before_reconnect()
    assert ws.ws is None
    ws._conn.__aexit__.assert_awaited()
    assert ws._reconnects == 1


def test_get_reconnect_wait():
    ws = ReconnectingWebsocket(url="wss://test.url")
    wait_time = ws._get_reconnect_wait(2)
    assert 1 <= wait_time <= ws.MAX_RECONNECT_SECONDS


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_connect_max_reconnects_exceeded():
    """Test ws.connect exceeds maximum reconnect attempts."""
    ws = ReconnectingWebsocket(url="wss://test.url")
    ws.MAX_RECONNECTS = 2  # type: ignore # Set max reconnects to a low number for testing
    ws._before_connect = AsyncMock()
    ws._after_connect = AsyncMock()
    ws._conn = AsyncMock()
    exception = Exception("Connection failed")
    ws._conn.__aenter__.side_effect = exception

    with patch.object(ws._log, "error") as mock_log:
        with pytest.raises(BinanceWebsocketUnableToConnect):
            for _ in range(3):  # Exceed MAX_RECONNECTS
                await ws._run_reconnect()
        mock_log.assert_called_with(f"Max reconnections {ws.MAX_RECONNECTS} reached:")

    assert ws._reconnects == ws.MAX_RECONNECTS


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_recieve_invalid_json():
    # Create mock WebSocket client
    mock_socket = create_autospec(WebSocketClientProtocol)
    mock_socket.recv = AsyncMock(return_value="invalid json{")
    mock_socket.state = AsyncMock()

    # Mock websockets.connect to return our mock socket
    with patch("websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_socket

        ws = ReconnectingWebsocket(url="wss://test.url")
        async with ws:
            msg = await ws.recv()
            assert msg["e"] == "error"
            assert msg["type"] == "JSONDecodeError"  # JSON parsing error


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_receive_valid_json():
    # Create mock WebSocket client
    msgRecv = '{"e": "value"}'
    mock_socket = create_autospec(WebSocketClientProtocol)
    mock_socket.recv = AsyncMock(return_value=msgRecv)
    mock_socket.state = AsyncMock()

    # Mock websockets.connect to return our mock socket
    with patch("websockets.connect") as mock_connect:
        mock_connect.return_value.__aenter__.return_value = mock_socket

        ws = ReconnectingWebsocket(url="wss://test.url")
        async with ws:
            msg = await ws.recv()
            assert msg == json.loads(msgRecv)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_connect_fails_to_connect_on_enter_context():
    """Test ws.connect raises a ConnectionClosedError."""
    ws = ReconnectingWebsocket(url="wss://test.url")
    ws._conn = AsyncMock()
    exception = Exception("Connection closed")
    ws._conn.__aenter__.side_effect = exception
    with pytest.raises(Exception):
        await ws.__aenter__()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_connect_fails_to_connect_after_disconnect():
    # Create mock WebSocket client
    mock_socket = create_autospec(WebSocketClientProtocol)
    mock_socket.recv = AsyncMock(side_effect=delayed_return)
    mock_socket.state = AsyncMock()

    # Create mock connect that succeeds first, then fails
    mock_connect = AsyncMock()
    mock_connect.return_value.__aenter__.side_effect = [
        mock_socket,  # First call succeeds
        Exception("Connection failed"),  # Subsequent calls fail
    ]

    with patch("websockets.connect", return_value=mock_connect.return_value):
        ws = ReconnectingWebsocket(url="wss://test.url")
        async with ws as ws:
            assert ws.ws is not None
            msg = await ws.recv()
            ws.ws.state = State.CLOSED
            await ws.ws.close()
            while msg["e"] != "error":
                msg = await ws.recv()
            # Receive the closed message attempting to reconnect
            while msg["type"] == "BinanceWebsocketClosed":
                msg = await ws.recv()
            # After retrying to reconnect, receive BinanceWebsocketUnableToConnect
            assert msg["e"] == "error"
            assert msg["type"] == "BinanceWebsocketUnableToConnect"


async def delayed_return():
    await asyncio.sleep(0.1)  # 100 ms delay
    return '{"e": "value"}'


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_recv_read_loop_closed():
    """Test that recv() raises ReadLoopClosed when read loop is closed."""
    ws = ReconnectingWebsocket(url="wss://test.url")
    
    # Simulate read loop being closed by setting _handle_read_loop to None
    ws._handle_read_loop = None
    
    with pytest.raises(ReadLoopClosed) as exc_info:
        await ws.recv()
    
    assert "Read loop has been closed" in str(exc_info.value)
    assert "please reset the websocket connection" in str(exc_info.value)

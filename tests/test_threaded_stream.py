import pytest
import asyncio

import websockets
from binance.ws.threaded_stream import ThreadedApiManager
from unittest.mock import Mock

# For Python 3.7 compatibility
try:
    from unittest.mock import AsyncMock
except ImportError:
    # Create our own AsyncMock for Python 3.7
    class AsyncMock(Mock):
        async def __call__(self, *args, **kwargs):
            return super(AsyncMock, self).__call__(*args, **kwargs)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def __aiter__(self):
            return self

        async def __anext__(self):
            raise StopAsyncIteration


@pytest.mark.asyncio
async def test_initialization():
    """Test that manager initializes with correct parameters"""
    manager = ThreadedApiManager(
        api_key="test_key",
        api_secret="test_secret",
        tld="com",
        testnet=True,
        requests_params={"timeout": 10},
        session_params={"trust_env": True},
    )

    assert manager._running is True
    assert manager._socket_running == {}
    assert manager._client_params == {
        "api_key": "test_key",
        "api_secret": "test_secret",
        "requests_params": {"timeout": 10},
        "tld": "com",
        "testnet": True,
        "session_params": {"trust_env": True},
        "https_proxy": None,
        "verbose": False,
    }


@pytest.mark.asyncio
async def test_start_and_stop_socket(manager):
    """Test starting and stopping a socket"""
    socket_name = "test_socket"

    # AsyncMock socket creation
    mock_socket = AsyncMock()
    mock_socket.__aenter__ = AsyncMock(return_value=mock_socket)
    mock_socket.__aexit__ = AsyncMock(return_value=None)

    # Track number of recv calls
    recv_count = 0

    async def controlled_recv():
        nonlocal recv_count
        recv_count += 1
        # If we've stopped the socket or read enough times, simulate connection closing
        if not manager._socket_running.get(socket_name) or recv_count > 2:
            raise websockets.exceptions.ConnectionClosed(None, None)
        await asyncio.sleep(0.1)
        return '{"e": "value"}'

    mock_socket.recv = controlled_recv

    # AsyncMock callback
    callback = AsyncMock()

    # Start socket listener
    manager._socket_running[socket_name] = True
    listener_task = asyncio.create_task(
        manager.start_listener(mock_socket, socket_name, callback)
    )

    # Give some time for the listener to start and receive a message
    await asyncio.sleep(0.2)

    # Stop the socket
    manager.stop_socket(socket_name)

    # Wait for the listener task to complete
    try:
        await asyncio.wait_for(listener_task, timeout=1.0)
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
        pass  # These exceptions are expected during shutdown

    assert socket_name not in manager._socket_running


@pytest.mark.asyncio
async def test_socket_listener_timeout(manager):
    """Test socket listener handling timeout"""
    socket_name = "test_socket"

    # AsyncMock socket that times out every time
    mock_socket = AsyncMock()
    mock_socket.__aenter__ = AsyncMock(return_value=mock_socket)
    mock_socket.__aexit__ = AsyncMock(return_value=None)

    async def controlled_recv():
        await asyncio.sleep(0.1)
        raise asyncio.TimeoutError("Simulated Timeout")

    mock_socket.recv = controlled_recv

    callback = AsyncMock()

    # Start socket listener
    manager._socket_running[socket_name] = True
    listener_task = asyncio.create_task(
        manager.start_listener(mock_socket, socket_name, callback)
    )

    # Give some time for a few timeout cycles
    await asyncio.sleep(0.3)

    # Stop the socket
    manager.stop_socket(socket_name)

    # Wait for the listener to finish
    try:
        await asyncio.wait_for(listener_task, timeout=1.0)
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
        listener_task.cancel()

    # Callback should not have been called (no successful messages)
    callback.assert_not_called()
    assert socket_name not in manager._socket_running


@pytest.mark.asyncio
async def test_stop_client(manager):
    """Test stopping the client"""
    # AsyncMock AsyncClient
    mock_client = AsyncMock()
    mock_client.close_connection = AsyncMock()
    manager._client = mock_client

    await manager.stop_client()
    mock_client.close_connection.assert_called_once()


@pytest.mark.asyncio
async def test_stop(manager):
    """Test stopping the manager"""
    socket_name = "test_socket"
    manager._socket_running[socket_name] = True

    manager.stop()

    assert manager._running is False
    assert manager._socket_running[socket_name] is False


@pytest.mark.asyncio
async def test_multiple_sockets(manager):
    """Test managing multiple sockets"""
    socket_names = ["socket1", "socket2", "socket3"]

    # Start multiple sockets
    for name in socket_names:
        manager._socket_running[name] = True

    # Stop all sockets
    manager.stop()

    # Verify all sockets are stopped
    for name in socket_names:
        assert manager._socket_running[name] is False


@pytest.mark.asyncio
async def test_stop_client_when_not_initialized(manager):
    """Test stopping client when it hasn't been initialized"""
    manager._client = None
    await manager.stop_client()  # Should not raise any exception


@pytest.mark.asyncio
async def test_stop_when_already_stopped(manager):
    """Test stopping manager when it's already stopped"""
    manager._running = False
    manager.stop()  # Should not raise any exception or change state
    assert manager._running is False

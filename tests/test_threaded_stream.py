import time
import pytest
import asyncio
from binance.ws.streams import ThreadedWebsocketManager
import os
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


proxy = os.getenv("PROXY")


@pytest.fixture
def manager():
    return ThreadedWebsocketManager(
        api_key="test_key", api_secret="test_secret", testnet=True
    )


def test_threaded_api_manager(manager):
    twm = manager
    symbol = "BNBBTC"

    # twm = ThreadedWebsocketManager(api_key="api_key", api_secret="api_secret")
    # start is required to initialise its internal loop
    twm.start()

    received_ticker = asyncio.Event()
    received_depth = asyncio.Event()
    received_mini_ticker = asyncio.Event()

    def handle_ticker(msg):
        received_ticker.set()  # Signal that we've received a callback

    async def handle_depth(msg):
        received_depth.set()  # Signal that we've received a callback

    def handle_mini_ticker(msg):
        received_mini_ticker.set()  # Signal that we've received a callback

    twm.start_ticker_socket(callback=handle_ticker)

    # multiple sockets can be started
    twm.start_depth_socket(callback=handle_depth, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    streams = ["bnbbtc@miniTicker", "bnbbtc@bookTicker"]
    twm.start_multiplex_socket(callback=handle_mini_ticker, streams=streams)

    # wait for 10 seconds to recieve messages
    # Wait for callbacks to be received
    wait_time = 10
    start_time = time.time()

    while not all([
        received_mini_ticker.is_set(),
        received_depth.is_set(),
        received_ticker.is_set(),
    ]):
        time.sleep(0.1)
        if time.time() - start_time > wait_time:
            pytest.fail(f"Did not receive all callbacks within {wait_time} seconds")

    twm.stop()

    assert received_ticker.is_set(), "Kline Callback was not called"
    assert received_depth.is_set(), "Depth Callback was not called"
    assert received_ticker.is_set(), "Ticker Callback was not called"

    for socket_name in twm._socket_running.keys():
        assert twm._socket_running[socket_name] is False


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
    }


@pytest.mark.asyncio
async def test_start_and_stop_socket(manager):
    """Test starting and stopping a socket"""
    socket_name = "test_socket"

    # AsyncMock socket creation
    mock_socket = AsyncMock()
    mock_socket.__aenter__ = AsyncMock(return_value=mock_socket)
    mock_socket.__aexit__ = AsyncMock(return_value=None)
    mock_socket.recv = AsyncMock(return_value="test_message")

    # AsyncMock callback
    callback = AsyncMock()

    # Start socket listener
    manager._socket_running[socket_name] = True
    asyncio.create_task(manager.start_listener(mock_socket, socket_name, callback))

    # Give some time for the listener to start
    await asyncio.sleep(0.1)

    # Stop the socket
    manager.stop_socket(socket_name)

    # Wait for socket to close
    await asyncio.sleep(0.1)

    assert socket_name not in manager._socket_running


@pytest.mark.asyncio
async def test_socket_listener_timeout(manager):
    """Test socket listener handling timeout"""
    socket_name = "test_socket"

    # AsyncMock socket that times out
    mock_socket = AsyncMock()
    mock_socket.__aenter__ = AsyncMock(return_value=mock_socket)
    mock_socket.__aexit__ = AsyncMock(return_value=None)
    mock_socket.recv = AsyncMock(side_effect=asyncio.TimeoutError)

    callback = AsyncMock()

    # Start socket listener
    manager._socket_running[socket_name] = True
    task = asyncio.create_task(
        manager.start_listener(mock_socket, socket_name, callback)
    )

    # Give some time for a few timeout cycles
    await asyncio.sleep(0.5)

    # Stop the socket
    manager.stop_socket(socket_name)
    await task

    # Callback should not have been called
    callback.assert_not_called()


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
    # Create and set a new event loop
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

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
async def test_socket_listener_empty_message(manager):
    """Test handling of empty messages"""
    socket_name = "test_socket"

    # AsyncMock socket that returns empty message
    mock_socket = AsyncMock()
    mock_socket.__aenter__ = AsyncMock(return_value=mock_socket)
    mock_socket.__aexit__ = AsyncMock(return_value=None)
    mock_socket.recv = AsyncMock(return_value="")

    callback = AsyncMock()

    # Start socket listener
    manager._socket_running[socket_name] = True
    task = asyncio.create_task(
        manager.start_listener(mock_socket, socket_name, callback)
    )

    await asyncio.sleep(0.1)
    manager.stop_socket(socket_name)
    await task

    # Callback should not have been called for empty message
    callback.assert_not_called()


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

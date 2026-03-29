"""
Tests for issue #1678: Connection errors must be propagated to subscription queues.

Verifies that when _read_loop() catches a connection error, the error dict
is delivered to all registered subscription queues (not just the main queue).
"""

import sys
import asyncio
import pytest
from unittest.mock import AsyncMock, PropertyMock

from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import websockets.protocol as ws_protocol

from binance.ws.reconnecting_websocket import ReconnectingWebsocket
from binance.ws.websocket_api import WebsocketAPI
from binance.ws.constants import WSListenerState


# -- Unit tests for _propagate_error --


@pytest.mark.asyncio
async def test_base_propagate_error_puts_on_main_queue():
    """ReconnectingWebsocket._propagate_error should put on self._queue."""
    ws = ReconnectingWebsocket(url="wss://test.url")
    error_msg = {"e": "error", "type": "TestError", "m": "test"}

    await ws._propagate_error(error_msg)

    assert ws._queue.qsize() == 1
    assert await ws._queue.get() == error_msg


@pytest.mark.asyncio
async def test_websocket_api_propagate_error_puts_on_main_and_subscription_queues():
    """WebsocketAPI._propagate_error should put on main queue AND all subscription queues."""
    ws = WebsocketAPI(url="wss://test.url")
    sub_queue_1 = asyncio.Queue()
    sub_queue_2 = asyncio.Queue()
    ws.register_subscription_queue("sub1", sub_queue_1)
    ws.register_subscription_queue("sub2", sub_queue_2)

    error_msg = {"e": "error", "type": "TestError", "m": "test"}
    await ws._propagate_error(error_msg)

    # Main queue gets the error
    assert ws._queue.qsize() == 1
    assert await ws._queue.get() == error_msg

    # Both subscription queues get the error
    assert sub_queue_1.qsize() == 1
    assert await sub_queue_1.get() == error_msg
    assert sub_queue_2.qsize() == 1
    assert await sub_queue_2.get() == error_msg


@pytest.mark.asyncio
async def test_propagate_error_handles_full_subscription_queue():
    """Should not raise when a subscription queue is full."""
    ws = WebsocketAPI(url="wss://test.url")
    full_queue = asyncio.Queue(maxsize=1)
    full_queue.put_nowait({"existing": "msg"})  # Fill it up
    ws.register_subscription_queue("sub_full", full_queue)

    error_msg = {"e": "error", "type": "TestError", "m": "test"}
    await ws._propagate_error(error_msg)

    # Main queue still gets it
    assert ws._queue.qsize() == 1
    # Full subscription queue still has only the old message (error was dropped)
    assert full_queue.qsize() == 1
    assert (await full_queue.get())["existing"] == "msg"


@pytest.mark.asyncio
async def test_propagate_error_with_no_subscriptions():
    """Should work fine when no subscription queues are registered."""
    ws = WebsocketAPI(url="wss://test.url")

    error_msg = {"e": "error", "type": "TestError", "m": "test"}
    await ws._propagate_error(error_msg)

    assert ws._queue.qsize() == 1
    assert await ws._queue.get() == error_msg


# -- Integration tests: _read_loop propagates errors to subscription queues --


def _make_ws_api_with_mock(recv_side_effect):
    """Helper: create a WebsocketAPI with a mocked websocket."""
    ws = WebsocketAPI(url="wss://test.url")
    mock_ws = AsyncMock()
    type(mock_ws).state = PropertyMock(return_value=ws_protocol.State.OPEN)
    mock_ws.recv = recv_side_effect
    mock_ws.close = AsyncMock()
    ws.ws = mock_ws
    ws.ws_state = WSListenerState.STREAMING
    return ws


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_read_loop_connection_closed_error_reaches_subscription_queue():
    """ConnectionClosedError in _read_loop should be delivered to subscription queues."""
    call_count = 0

    async def recv_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ConnectionClosedError(None, None)
        raise asyncio.CancelledError()

    ws = _make_ws_api_with_mock(recv_side_effect)
    sub_queue = asyncio.Queue()
    ws.register_subscription_queue("user_sub", sub_queue)

    try:
        await asyncio.wait_for(ws._read_loop(), timeout=3.0)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass

    assert sub_queue.qsize() >= 1, "Subscription queue should have received the error"
    msg = await sub_queue.get()
    assert msg["e"] == "error"
    assert msg["type"] == "ConnectionClosedError"


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_read_loop_connection_closed_ok_reaches_subscription_queue():
    """ConnectionClosedOK in _read_loop should be delivered to subscription queues."""
    call_count = 0

    async def recv_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ConnectionClosedOK(None, None)
        raise asyncio.CancelledError()

    ws = _make_ws_api_with_mock(recv_side_effect)
    sub_queue = asyncio.Queue()
    ws.register_subscription_queue("user_sub", sub_queue)

    try:
        await asyncio.wait_for(ws._read_loop(), timeout=3.0)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass

    assert sub_queue.qsize() >= 1
    msg = await sub_queue.get()
    assert msg["e"] == "error"
    assert msg["type"] == "ConnectionClosedOK"


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_read_loop_cancelled_error_reaches_subscription_queue():
    """CancelledError in _read_loop should be delivered to subscription queues."""

    async def recv_side_effect():
        raise asyncio.CancelledError()

    ws = _make_ws_api_with_mock(recv_side_effect)
    sub_queue = asyncio.Queue()
    ws.register_subscription_queue("user_sub", sub_queue)

    try:
        await asyncio.wait_for(ws._read_loop(), timeout=3.0)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass

    assert sub_queue.qsize() >= 1
    msg = await sub_queue.get()
    assert msg["e"] == "error"
    assert msg["type"] == "CancelledError"


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_read_loop_fatal_error_reaches_subscription_queue():
    """Generic exceptions in _read_loop should be delivered to subscription queues."""

    async def recv_side_effect():
        raise RuntimeError("something broke")

    ws = _make_ws_api_with_mock(recv_side_effect)
    sub_queue = asyncio.Queue()
    ws.register_subscription_queue("user_sub", sub_queue)

    try:
        await asyncio.wait_for(ws._read_loop(), timeout=3.0)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass

    assert sub_queue.qsize() >= 1
    msg = await sub_queue.get()
    assert msg["e"] == "error"
    assert msg["type"] == "RuntimeError"


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_read_loop_error_reaches_multiple_subscription_queues():
    """Errors should be delivered to ALL registered subscription queues."""

    async def recv_side_effect():
        raise ConnectionClosedError(None, None)

    ws = _make_ws_api_with_mock(recv_side_effect)
    queues = [asyncio.Queue() for _ in range(3)]
    for i, q in enumerate(queues):
        ws.register_subscription_queue(f"sub_{i}", q)

    # Set EXITING after error to stop loop
    original_propagate = ws._propagate_error

    async def propagate_and_exit(error_msg):
        await original_propagate(error_msg)
        ws.ws_state = WSListenerState.EXITING

    ws._propagate_error = propagate_and_exit

    try:
        await asyncio.wait_for(ws._read_loop(), timeout=3.0)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass

    for i, q in enumerate(queues):
        assert q.qsize() >= 1, f"Subscription queue {i} should have received the error"
        msg = await q.get()
        assert msg["e"] == "error"
        assert msg["type"] == "ConnectionClosedError"


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
@pytest.mark.asyncio
async def test_normal_messages_not_duplicated_to_main_queue():
    """Normal subscription messages should go to subscription queue only, not main queue."""
    call_count = 0

    async def recv_side_effect():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return '{"subscriptionId": "user_sub", "event": {"e": "executionReport", "s": "BTCUSDT"}}'
        raise asyncio.CancelledError()

    ws = _make_ws_api_with_mock(recv_side_effect)
    sub_queue = asyncio.Queue()
    ws.register_subscription_queue("user_sub", sub_queue)

    try:
        await asyncio.wait_for(ws._read_loop(), timeout=3.0)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass

    # Normal message should be in subscription queue
    assert sub_queue.qsize() >= 1
    msg = await sub_queue.get()
    assert msg["e"] == "executionReport"

    # Main queue should only have the CancelledError, not the normal message
    while not ws._queue.empty():
        main_msg = await ws._queue.get()
        assert main_msg["e"] == "error", "Main queue should only have error messages"

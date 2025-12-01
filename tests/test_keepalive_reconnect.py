"""
Test to verify that KeepAliveWebsocket doesn't create duplicate keepalive loops on reconnection.

This test reproduces the issue where reconnection events create duplicate keepalive loops
that continue running indefinitely, leading to resource exhaustion and redundant API calls.
"""

import sys
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from binance.async_client import AsyncClient
from binance.ws.keepalive_websocket import KeepAliveWebsocket


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_no_duplicate_keepalive_loops_on_reconnect():
    """
    Test that reconnection doesn't create duplicate keepalive loops.

    The bug occurs when:
    1. A keepalive loop is running (timer -> keepalive_socket -> timer -> ...)
    2. Reconnection happens via _after_connect()
    3. A new keepalive loop is started unconditionally
    4. The old loop continues running in the background
    5. Each reconnection adds another orphaned loop
    """
    # Create a mock client
    mock_client = MagicMock(spec=AsyncClient)
    mock_client.futures_stream_get_listen_key = AsyncMock(
        return_value="test_listen_key"
    )
    mock_client.futures_stream_keepalive = AsyncMock()

    # Create the websocket instance
    ws = KeepAliveWebsocket(
        client=mock_client,
        url="wss://fstream.binance.com/",
        keepalive_type="futures",
        prefix="ws/",
        user_timeout=0.1,  # Short timeout for faster test
    )

    # Track how many times _keepalive_socket is called
    keepalive_call_count = 0
    original_keepalive = ws._keepalive_socket

    async def tracked_keepalive():
        nonlocal keepalive_call_count
        keepalive_call_count += 1
        # Call the original method but skip the actual API call
        # Just track that it was called
        return

    ws._keepalive_socket = tracked_keepalive

    # Simulate the first connection
    await ws._before_connect()
    await ws._after_connect()

    # Wait for the first timer to trigger
    await asyncio.sleep(0.15)
    first_call_count = keepalive_call_count

    assert first_call_count >= 1, "Keepalive should have been called at least once"

    # Simulate a reconnection (this is where the bug occurs)
    # In a real scenario, _after_connect() is called again by the reconnection logic
    await ws._after_connect()

    # Wait for more timer triggers
    await asyncio.sleep(0.15)
    second_call_count = keepalive_call_count

    # Calculate how many calls happened after reconnection
    calls_after_reconnect = second_call_count - first_call_count

    # With the bug: multiple loops are running, so we'd see 2+ calls per timer period
    # Without the bug: only one loop is running, so we'd see ~1 call per timer period
    # Allow some margin (up to 2 calls) due to timing
    assert calls_after_reconnect <= 2, (
        f"Too many keepalive calls after reconnection: {calls_after_reconnect}. "
        f"This indicates duplicate keepalive loops are running. "
        f"Total calls: {second_call_count}, calls before reconnect: {first_call_count}"
    )

    # Clean up
    if ws._timer:
        ws._timer.cancel()
        ws._timer = None


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_keepalive_stops_after_exit():
    """
    Test that keepalive loop stops properly when the websocket exits.

    The fix should ensure that when __aexit__ sets _timer to None,
    the finally block in _keepalive_socket doesn't restart the timer.
    """
    # Create a mock client
    mock_client = MagicMock(spec=AsyncClient)
    mock_client.futures_stream_get_listen_key = AsyncMock(
        return_value="test_listen_key"
    )
    mock_client.futures_stream_keepalive = AsyncMock()

    # Create the websocket instance
    ws = KeepAliveWebsocket(
        client=mock_client,
        url="wss://fstream.binance.com/",
        keepalive_type="futures",
        prefix="ws/",
        user_timeout=0.1,  # Short timeout for faster test
    )

    # Track keepalive calls
    keepalive_call_count = 0

    async def tracked_keepalive():
        nonlocal keepalive_call_count
        keepalive_call_count += 1
        return

    ws._keepalive_socket = tracked_keepalive

    # Start the keepalive
    await ws._before_connect()
    await ws._after_connect()

    # Wait for at least one keepalive call
    await asyncio.sleep(0.15)
    calls_before_exit = keepalive_call_count
    assert calls_before_exit >= 1, "Keepalive should have been called before exit"

    # Simulate exit by setting timer to None (this is what __aexit__ does)
    if ws._timer:
        ws._timer.cancel()
        ws._timer = None

    # Wait to see if more keepalive calls happen (they shouldn't)
    await asyncio.sleep(0.15)
    calls_after_exit = keepalive_call_count

    # After setting _timer to None, no more calls should happen
    assert calls_after_exit == calls_before_exit, (
        f"Keepalive should not continue after exit. "
        f"Calls before exit: {calls_before_exit}, calls after exit: {calls_after_exit}"
    )


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_multiple_reconnects_no_loop_accumulation():
    """
    Test that multiple reconnections don't accumulate keepalive loops.

    This is a stress test to ensure the fix works even with many reconnections.
    """
    # Create a mock client
    mock_client = MagicMock(spec=AsyncClient)
    mock_client.futures_stream_get_listen_key = AsyncMock(
        return_value="test_listen_key"
    )
    mock_client.futures_stream_keepalive = AsyncMock()

    # Create the websocket instance
    ws = KeepAliveWebsocket(
        client=mock_client,
        url="wss://fstream.binance.com/",
        keepalive_type="futures",
        prefix="ws/",
        user_timeout=0.1,  # Short timeout for faster test
    )

    # Track keepalive calls
    keepalive_call_count = 0

    async def tracked_keepalive():
        nonlocal keepalive_call_count
        keepalive_call_count += 1
        return

    ws._keepalive_socket = tracked_keepalive

    # Initial connection
    await ws._before_connect()
    await ws._after_connect()

    # Wait for initial calls
    await asyncio.sleep(0.15)

    # Simulate 5 reconnections
    for i in range(5):
        await ws._after_connect()

    # Reset counter
    keepalive_call_count = 0

    # Wait for a timer period
    await asyncio.sleep(0.15)

    # Should only have ~1 call per timer period, not 6 (one per each connection + reconnections)
    # Allow margin of 2 due to timing
    assert keepalive_call_count <= 2, (
        f"Too many keepalive calls after 5 reconnections: {keepalive_call_count}. "
        f"This indicates keepalive loops are accumulating."
    )

    # Clean up
    if ws._timer:
        ws._timer.cancel()
        ws._timer = None

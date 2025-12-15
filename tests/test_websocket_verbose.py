"""Tests for WebSocket verbose logging"""

import logging
import pytest


def test_websocket_logger_exists():
    """Test that WebSocket loggers can be configured"""
    # Test main WebSocket logger
    ws_logger = logging.getLogger("binance.ws")
    assert ws_logger is not None

    # Test WebSocket API logger
    ws_api_logger = logging.getLogger("binance.ws.websocket_api")
    assert ws_api_logger is not None

    # Test reconnecting WebSocket logger
    ws_reconnect_logger = logging.getLogger("binance.ws.reconnecting_websocket")
    assert ws_reconnect_logger is not None

    # Test streams logger
    ws_streams_logger = logging.getLogger("binance.ws.streams")
    assert ws_streams_logger is not None


def test_websocket_logger_level_configuration():
    """Test that WebSocket logger levels can be set"""
    ws_logger = logging.getLogger("binance.ws.test_config")

    # Set to DEBUG
    ws_logger.setLevel(logging.DEBUG)
    assert ws_logger.level == logging.DEBUG

    # Set to INFO
    ws_logger.setLevel(logging.INFO)
    assert ws_logger.level == logging.INFO

    # Set to WARNING
    ws_logger.setLevel(logging.WARNING)
    assert ws_logger.level == logging.WARNING


def test_combined_logging_configuration():
    """Test that both REST and WebSocket logging can be configured together"""
    # Configure REST verbose logging
    from binance.client import Client

    # This should work without errors
    client = Client(verbose=True, ping=False)
    assert client.verbose is True
    assert client.logger is not None

    # Configure WebSocket logging
    ws_logger = logging.getLogger("binance.ws")
    ws_logger.setLevel(logging.DEBUG)
    assert ws_logger.level == logging.DEBUG

    # Both should be independently configurable
    assert client.logger.level == logging.DEBUG
    assert ws_logger.level == logging.DEBUG


@pytest.mark.asyncio()
async def test_binance_socket_manager_verbose():
    """Test that BinanceSocketManager can be initialized with verbose mode"""
    from binance import AsyncClient, BinanceSocketManager

    client = AsyncClient()

    # Test with verbose=True
    bm_verbose = BinanceSocketManager(client, verbose=True)
    assert bm_verbose.verbose is True

    # Test with verbose=False (default)
    bm_quiet = BinanceSocketManager(client, verbose=False)
    assert bm_quiet.verbose is False

    # Test default
    bm_default = BinanceSocketManager(client)
    assert bm_default.verbose is False

    await client.close_connection()


def test_threaded_websocket_manager_verbose():
    """Test that ThreadedApiManager can be initialized with verbose mode"""
    from binance.ws.threaded_stream import ThreadedApiManager

    # Test with verbose=True
    twm_verbose = ThreadedApiManager(verbose=True)
    assert twm_verbose.verbose is True

    # Test with verbose=False (default)
    twm_quiet = ThreadedApiManager(verbose=False)
    assert twm_quiet.verbose is False

    # Test default
    twm_default = ThreadedApiManager()
    assert twm_default.verbose is False


def test_websocket_manager_sets_logging_level():
    """Test that verbose mode sets the logging level for WebSocket managers"""
    from binance.ws.threaded_stream import ThreadedApiManager

    # Get initial logging level
    ws_logger = logging.getLogger("binance.ws")
    initial_level = ws_logger.level

    # Create manager with verbose=True
    twm = ThreadedApiManager(verbose=True)

    # Check that logging level was set to DEBUG
    assert ws_logger.level == logging.DEBUG

    # Restore initial level
    ws_logger.setLevel(initial_level)

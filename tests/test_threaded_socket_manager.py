from binance import ThreadedWebsocketManager
from binance.client import Client
import asyncio
import time
from .conftest import proxies, api_key, api_secret, proxy
import pytest
import sys

pytestmark = pytest.mark.skipif(
    sys.version_info <= (3, 8),
    reason="These tests require Python 3.8+ for proper websocket proxy support"
)

received_ohlcv = False
received_depth = False

twm: ThreadedWebsocketManager


# Get real symbols from Binance API
client = Client(api_key, api_secret, {"proxies": proxies})
exchange_info = client.get_exchange_info()
symbols = [info['symbol'].lower() for info in exchange_info['symbols']]
streams = [f"{symbol}@bookTicker" for symbol in symbols][0:100]  # Take first 800 symbols


def test_threaded_socket_manager():
    global twm
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True)

    symbol = "BTCUSDT"

    def handle_socket_message(msg):
        global received_ohlcv, received_depth
        print(msg)
        if "e" in msg:
            if msg["e"] == "depthUpdate":
                received_depth = True
            if msg["e"] == "kline":
                received_ohlcv = True
        if received_depth and received_ohlcv:
            twm.stop()

    try:
        twm.start()
        twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
        twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)
        twm.join()
    finally:
        twm.stop()
        time.sleep(2)  # Give time for cleanup to complete


def test_many_symbols_small_queue():
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True, max_queue_size=1)
    
    error_received = False
    msg_received = False
    
    def handle_message(msg):
        nonlocal error_received, msg_received
        if msg.get("e") == "error":
            error_received = True
            print(f"WebSocket error: {msg.get('m', 'Unknown error')}")
            return
        msg_received = True
    
    try:
        twm.start()
        twm.start_multiplex_socket(callback=handle_message, streams=streams)
        time.sleep(10)  # Give some time for errors to occur
        
        assert msg_received, "Should have received messages"
        # assert error_received, "Should have received error messages due to small queue"
    finally:
        # Ensure cleanup happens even if test fails
        twm.stop()
        time.sleep(2)  # Give time for cleanup to complete


def test_many_symbols_adequate_queue():
    # Test with larger queue size that should handle the load
    twm = ThreadedWebsocketManager(api_key, api_secret, max_queue_size=200)
    
    messages_received = 0
    error_received = False
    
    def handle_message(msg):
        nonlocal messages_received, error_received
        if msg.get("e") == "error":
            error_received = True
            print(f"WebSocket error: {msg.get('m', 'Unknown error')}")
            return
            
        messages_received += 1
    
    try:
        twm.start()
        twm.start_futures_multiplex_socket(callback=handle_message, streams=streams)
        time.sleep(10)  # Run for 20 seconds
        
        assert messages_received > 0, "Should have received some messages"
        assert not error_received, "Should not have received any errors"
    finally:
        twm.stop()
        time.sleep(2)  # Give time for cleanup to complete


def test_slow_async_callback_no_error():
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True, max_queue_size=400)
    
    messages_processed = 0
    error_received = False
    
    async def slow_async_callback(msg):
        nonlocal messages_processed, error_received
        if msg.get("e") == "error":
            error_received = True
            print(f"WebSocket error: {msg.get('m', 'Unknown error')}")
            return
            
        await asyncio.sleep(2)  # Simulate slow async processing
        messages_processed += 1
    
    try:
        twm.start()
        twm.start_futures_multiplex_socket(callback=slow_async_callback, streams=streams)
        time.sleep(10)
        
        assert messages_processed > 0, "Should have processed some messages"
        assert not error_received, "Should not have received any errors"
    finally:
        twm.stop()
        time.sleep(2)  # Give time for cleanup to complete


def test_no_internet_connection():
    """Test that socket manager times out when there's no internet connection"""
    # Use an invalid proxy to simulate no internet connection
    invalid_proxy = "http://invalid.proxy:1234"
    
    with pytest.raises(RuntimeError, match="Binance Socket Manager failed to initialize after 5 seconds"):
        twm = ThreadedWebsocketManager(
            api_key, 
            api_secret, 
            https_proxy=invalid_proxy, 
            testnet=True
        )
        
        try:
            twm.start()
            # Try to start a socket - this should timeout
            twm.start_kline_socket(
                callback=lambda x: print(x), 
                symbol="BTCUSDT"
            )
        finally:
            # Cleanup even if test fails
            twm.stop()
            time.sleep(2)  # Give time for cleanup

from binance import ThreadedWebsocketManager
from binance.client import Client
import asyncio
import time
from .conftest import proxies, api_key, api_secret, proxy
import pytest
import sys
import logging

pytestmark = pytest.mark.skipif(
    sys.version_info <= (3, 8),
    reason="These tests require Python 3.8+ for proper websocket proxy support"
)

received_ohlcv = False
received_depth = False

twm: ThreadedWebsocketManager

# Add logger definition before using it
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Get real symbols from Binance API
client = Client(api_key, api_secret, {"proxies": proxies})
exchange_info = client.get_exchange_info()
symbols = [info['symbol'].lower() for info in exchange_info['symbols']]
streams = [f"{symbol}@bookTicker" for symbol in symbols][0:100]  # Take first 800 symbols

def test_threaded_socket_manager():
    logger.debug("Starting test_threaded_socket_manager")
    global twm
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True)

    symbol = "BTCUSDT"

    def handle_socket_message(msg):
        global received_ohlcv, received_depth
        if "e" in msg:
            if msg["e"] == "depthUpdate":
                logger.debug("Received depth update message")
                received_depth = True
            if msg["e"] == "kline":
                logger.debug("Received kline message")
                received_ohlcv = True
        if received_depth and received_ohlcv:
            logger.debug("Received both depth and OHLCV messages, stopping")
            twm.stop()

    try:
        logger.debug("Starting ThreadedWebsocketManager")
        twm.start()
        logger.debug("Starting kline socket for %s", symbol)
        twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
        logger.debug("Starting depth socket for %s", symbol)
        twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)
        twm.join()
    finally:
        logger.debug("Cleaning up test_threaded_socket_manager")
        twm.stop()
        time.sleep(2)


def test_many_symbols_small_queue():
    logger.debug("Starting test_many_symbols_small_queue with queue size 1")
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True, max_queue_size=1)
    
    error_received = False
    msg_received = False
    
    def handle_message(msg):
        nonlocal error_received, msg_received
        if msg.get("e") == "error":
            error_received = True
            logger.debug("Received WebSocket error: %s", msg.get('m', 'Unknown error'))
            return
        msg_received = True
        logger.debug("Received valid message")
    
    try:
        logger.debug("Starting ThreadedWebsocketManager")
        twm.start()
        logger.debug("Starting multiplex socket with %d streams", len(streams))
        twm.start_multiplex_socket(callback=handle_message, streams=streams)
        logger.debug("Waiting 10 seconds for messages")
        time.sleep(10)
        
        assert msg_received, "Should have received messages"
    finally:
        logger.debug("Cleaning up test_many_symbols_small_queue")
        twm.stop()
        time.sleep(2)


def test_many_symbols_adequate_queue():
    logger.debug("Starting test_many_symbols_adequate_queue with queue size 200")
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True, max_queue_size=200)
    
    messages_received = 0
    error_received = False
    
    def handle_message(msg):
        nonlocal messages_received, error_received
        if msg.get("e") == "error":
            error_received = True
            logger.debug("Received WebSocket error: %s", msg.get('m', 'Unknown error'))
            return
            
        messages_received += 1
        if messages_received % 10 == 0:  # Log every 10th message
            logger.debug("Processed %d messages", messages_received)
    
    try:
        logger.debug("Starting ThreadedWebsocketManager")
        twm.start()
        logger.debug("Starting futures multiplex socket with %d streams", len(streams))
        twm.start_futures_multiplex_socket(callback=handle_message, streams=streams)
        logger.debug("Waiting 10 seconds for messages")
        time.sleep(10)
        
        logger.debug("Test completed. Messages received: %d, Errors: %s", messages_received, error_received)
        assert messages_received > 0, "Should have received some messages"
        assert not error_received, "Should not have received any errors"
    finally:
        logger.debug("Cleaning up test_many_symbols_adequate_queue")
        twm.stop()
        time.sleep(2)


def test_slow_async_callback_no_error():
    logger.debug("Starting test_slow_async_callback_no_error with queue size 400")
    twm = ThreadedWebsocketManager(api_key, api_secret, https_proxy=proxy, testnet=True, max_queue_size=400)
    
    messages_processed = 0
    error_received = False
    
    async def slow_async_callback(msg):
        nonlocal messages_processed, error_received
        if msg.get("e") == "error":
            error_received = True
            logger.debug("Received WebSocket error: %s", msg.get('m', 'Unknown error'))
            return
            
        logger.debug("Processing message with 2 second delay")
        await asyncio.sleep(2)
        messages_processed += 1
        logger.debug("Message processed. Total processed: %d", messages_processed)
    
    try:
        logger.debug("Starting ThreadedWebsocketManager")
        twm.start()
        logger.debug("Starting futures multiplex socket with %d streams", len(streams))
        twm.start_futures_multiplex_socket(callback=slow_async_callback, streams=streams)
        logger.debug("Waiting 10 seconds for messages")
        time.sleep(10)
        
        logger.debug("Test completed. Messages processed: %d, Errors: %s", messages_processed, error_received)
        assert messages_processed > 0, "Should have processed some messages"
        assert not error_received, "Should not have received any errors"
    finally:
        logger.debug("Cleaning up test_slow_async_callback_no_error")
        twm.stop()
        time.sleep(2)


def test_no_internet_connection():
    """Test that socket manager times out when there's no internet connection"""
    logger.debug("Starting test_no_internet_connection")
    invalid_proxy = "http://invalid.proxy:1234"
    logger.debug("Using invalid proxy: %s", invalid_proxy)
    
    with pytest.raises(RuntimeError, match="Binance Socket Manager failed to initialize after 5 seconds"):
        twm = ThreadedWebsocketManager(
            api_key, 
            api_secret, 
            https_proxy=invalid_proxy, 
            testnet=True
        )
        
        try:
            logger.debug("Attempting to start ThreadedWebsocketManager with invalid proxy")
            twm.start()
            logger.debug("Attempting to start kline socket (should fail)")
            twm.start_kline_socket(
                callback=lambda x: print(x), 
                symbol="BTCUSDT"
            )
        finally:
            logger.debug("Cleaning up test_no_internet_connection")
            twm.stop()
            time.sleep(2)

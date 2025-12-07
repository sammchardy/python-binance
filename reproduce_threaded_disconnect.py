#!/usr/bin/env python3
"""
Script to reproduce ThreadedWebsocketManager connection issue.

This script demonstrates the bug where ThreadedWebsocketManager fails to
report connection errors to the user when network issues occur.

To reproduce:
1. Connect to a VPN in the US or disconnect from network
2. Run this script
3. Observe that no error is returned to the callback despite connection failure
"""

import time
import logging
from binance import ThreadedWebsocketManager

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def handle_socket_message(msg):
    """
    Callback function to handle websocket messages.

    Expected behavior: Should receive error messages when connection fails
    Actual behavior: No error messages are passed to this callback
    """
    logger.info(f"Received message: {msg}")

    # Check if this is an error message
    if isinstance(msg, dict):
        if msg.get("e") == "error":
            logger.error(f"Error received in callback: {msg}")
        elif "error" in msg:
            logger.error(f"Error in message: {msg['error']}")

    print(f"Message: {msg}")


def main():
    logger.info("Creating ThreadedWebsocketManager...")

    try:
        # Create the websocket manager
        twm = ThreadedWebsocketManager()

        logger.info("Starting ThreadedWebsocketManager...")
        twm.start()

        symbol = "BTCUSDT"
        logger.info(f"Starting kline socket for {symbol}...")

        # Start the kline socket
        # This should fail silently if there are network issues
        socket_result = twm.start_kline_socket(
            callback=handle_socket_message, symbol=symbol
        )

        logger.info(f"Socket started with result: {socket_result}")

        # Wait and monitor for messages or errors
        logger.info("Waiting for messages (will wait 30 seconds)...")

        for i in range(30):
            time.sleep(1)
            if i % 5 == 0:
                logger.info(f"Still waiting... ({i}/30 seconds)")

        logger.info("Stopping websocket manager...")
        twm.stop()

    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        logger.error(f"Exception type: {type(e)}")

        # Try to stop the manager if it was created
        try:
            twm.stop()
        except:
            pass

    logger.info("Script completed")


if __name__ == "__main__":
    print("=" * 60)
    print("ThreadedWebsocketManager Connection Issue Reproduction Script")
    print("=" * 60)
    print("\nTo reproduce the issue:")
    print("1. Disconnect from network or connect to a VPN that blocks Binance")
    print("2. Run this script")
    print("3. Observe that no connection errors are reported to the callback")
    print("\nExpected: Error messages should be passed to the callback")
    print("Actual: No error indication when connection fails")
    print("=" * 60)
    print()

    main()

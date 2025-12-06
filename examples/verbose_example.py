#!/usr/bin/env python
"""
Comprehensive verbose mode example for python-binance

This example demonstrates verbose logging for:
- Synchronous Client (REST API)
- Async Client (REST API)
- WebSocket streams (BinanceSocketManager)
"""

import asyncio
import logging
from binance import Client, AsyncClient, BinanceSocketManager

# Configure logging to see verbose output
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def sync_client_example():
    """Example 1: Synchronous Client with verbose mode"""
    print("\n" + "=" * 80)
    print("Example 1: Synchronous Client (verbose=True)")
    print("=" * 80)

    client = Client(verbose=True)

    # Make API call - will show detailed HTTP logs
    server_time = client.get_server_time()
    print(f"Server time: {server_time['serverTime']}\n")


async def async_client_example():
    """Example 2: Async Client with verbose mode"""
    print("\n" + "=" * 80)
    print("Example 2: Async Client (verbose=True)")
    print("=" * 80)

    client = await AsyncClient.create(verbose=True)

    # Make API call - will show detailed HTTP logs
    ticker = await client.get_symbol_ticker(symbol="BTCUSDT")
    print(f"BTC/USDT price: {ticker['price']}\n")

    await client.close_connection()


async def websocket_example():
    """Example 3: WebSocket with verbose mode"""
    print("\n" + "=" * 80)
    print("Example 3: WebSocket Streams (verbose=True)")
    print("=" * 80)

    client = await AsyncClient.create()

    # Create socket manager with verbose mode
    bm = BinanceSocketManager(client, verbose=True)

    # Start trade socket - will show detailed WebSocket logs
    ts = bm.trade_socket("ETHUSDT")

    print("Receiving 3 trade messages...\n")
    async with ts as tscm:
        for i in range(3):
            msg = await tscm.recv()
            print(f"Trade {i + 1}: Price={msg['p']}, Qty={msg['q']}")

    await client.close_connection()


async def combined_example():
    """Example 4: Combined REST + WebSocket verbose mode"""
    print("\n" + "=" * 80)
    print("Example 4: Combined REST + WebSocket (both verbose=True)")
    print("=" * 80)

    # Enable verbose for both REST and WebSocket
    client = await AsyncClient.create(verbose=True)
    bm = BinanceSocketManager(client, verbose=True)

    # REST API call
    await client.get_server_time()

    # WebSocket stream
    ts = bm.trade_socket("BNBUSDT")
    async with ts as tscm:
        msg = await tscm.recv()
        print(f"BNB/USDT trade: {msg['p']}\n")

    await client.close_connection()


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("Python-Binance Verbose Mode Examples")
    print("=" * 80)
    print("\nThese examples show how to enable verbose logging for debugging:")
    print("- REST API requests/responses (HTTP details)")
    print("- WebSocket messages (connection & data)")
    print("\nWatch the DEBUG logs above each example output.\n")

    # Run sync example
    sync_client_example()

    # Run async examples
    asyncio.run(async_client_example())
    asyncio.run(websocket_example())
    asyncio.run(combined_example())

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)
    print("\nKey takeaways:")
    print("  ✓ Use verbose=True for quick debugging")
    print("  ✓ Works with Client, AsyncClient, and BinanceSocketManager")
    print("  ✓ Shows full HTTP request/response details")
    print("  ✓ Logs WebSocket messages as they arrive")
    print("  ✓ Disable verbose mode in production (it's off by default)")


if __name__ == "__main__":
    main()

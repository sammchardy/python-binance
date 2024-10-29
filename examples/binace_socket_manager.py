import os
import sys
import asyncio
import time

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance import AsyncClient, BinanceSocketManager


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket("BTCUSDT")
    # then start receiving messages
    async with ts as tscm:
        start_time = time.time()
        while time.time() - start_time < 30:
            try:
                res = await tscm.recv()
                print(res)
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    await client.close_connection()
    print("WebSocket connection closed after 10 seconds.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

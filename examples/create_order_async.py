import os
import sys
import asyncio

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance import AsyncClient


# create futures order
async def main():
    api_key = ""  # your api_key here
    secret = ""  # your secret here
    client = AsyncClient(api_key, secret, testnet=True)
    order = await client.futures_create_order(
        symbol="LTCUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.1,
        positionSide="LONG",  # BOTH for One-way Mode ; LONG or SHORT for Hedge Mode
    )
    print(order)
    await client.close_connection()


asyncio.run(main())

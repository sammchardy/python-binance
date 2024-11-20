import os
import sys
import asyncio


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance import AsyncClient

## create order using websockets async
## the API is very similar to the REST API


async def main():
    api_key = ""  # your api_key here
    secret = ""  # your secret here
    client = AsyncClient(api_key, secret, testnet=True)
    order = await client.ws_create_order(
        symbol="LTCUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.1,
    )
    print(order["orderId"])
    await client.close_connection()


asyncio.run(main())

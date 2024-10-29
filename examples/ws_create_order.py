import os
import sys
import asyncio

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance import AsyncClient, BinanceSocketManager


api_key = (
    "u4L8MG2DbshTfTzkx2Xm7NfsHHigvafxeC29HrExEmah1P8JhxXkoOu6KntLICUc"
)  # your api_key here
api_secret = (
    "hBZEqhZUUS6YZkk7AIckjJ3iLjrgEFr5CRtFPp5gjzkrHKKC9DAv4OH25PlT6yq5"
)  # your secret here


async def main():
    client = await AsyncClient.create(api_key, api_secret, testnet=True)
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    # ts = await bm.create_order(
    #     symbol="LTCUSDT",
    #     side="BUY",
    #     type="LIMIT",
    #     price=75,
    #     quantity=1)
    # ts = await bm.create_order(
    #     symbol="LTCUSDTT"
    # )

    ts = bm.get_symbol_ticker(symbol="LTCUSDT")

    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

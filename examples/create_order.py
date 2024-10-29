import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance.client import Client


api_key = ""  # your api_key here
secret = ""  # your secret here
client = Client(api_key, secret, testnet=True)


# create futures order
def create_futures_order():
    order = client.futures_create_order(
        symbol="LTCUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.1,
        positionSide="LONG",  # BOTH for One-way Mode ; LONG or SHORT for Hedge Mode
    )
    print(order)


def create_spot_order():
    order = client.create_order(
        symbol="LTCUSDT", side="BUY", type="LIMIT", price=60, quantity=0.1
    )
    print(order)


def main():
    create_futures_order()
    create_spot_order()


main()

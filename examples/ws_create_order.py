import os
import sys


root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance.client import Client

## create order using websockets sync
## the API is very similar to the REST API


def main():
    api_key = ""  # your api_key here
    secret = ""  # your secret here
    client = Client(api_key, secret, testnet=True)
    order = client.ws_create_order(
        symbol="LTCUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.1,
    )
    print(order["orderId"])


main()

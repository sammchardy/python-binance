import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance import ThreadedWebsocketManager

api_key = "<api_key>"
api_secret = "<api_secret>"


def main():
    symbol = "BNBBTC"

    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        if msg.get("e") == "error":
            print(f"WebSocket error: {msg.get('m', 'Unknown error')}")

            return

        # Process message normally
        print(msg)

    # Store socket names for potential restart
    sockets = []

    # Start kline socket
    kline_socket = twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)
    sockets.append(("kline", kline_socket, symbol))

    # Start depth socket
    depth_socket = twm.start_depth_socket(callback=handle_socket_message, symbol=symbol)
    sockets.append(("depth", depth_socket, symbol))

    # Start multiplex socket
    streams = ["bnbbtc@miniTicker", "bnbbtc@bookTicker"]
    twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    twm.join()


if __name__ == "__main__":
    main()

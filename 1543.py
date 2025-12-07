from binance import ThreadedWebsocketManager

import time
import threading

twm: ThreadedWebsocketManager
symbol = "BTCUSDT"


def handle_socket_message(msg):
    print("handle_socket_message", msg)


def test_threaded_socket_manager():
    """This thread will only process messages"""
    print("test_threaded_socket_manager run")
    print("id:", id(twm))
    print("type:", type(twm))

    # Just wait and process messages
    time.sleep(10)

    print("test_threaded_socket_manager stop")


if __name__ == "__main__":
    # Create and start TWM in main thread
    twm = ThreadedWebsocketManager(api_key="", api_secret="", testnet=False)
    twm.start()
    print("id:", id(twm))
    print("type:", type(twm))

    # Start socket in main thread where TWM was created
    sock_id = twm.start_kline_futures_socket(
        callback=handle_socket_message, symbol=symbol
    )

    # Create thread for processing
    t = threading.Thread(target=test_threaded_socket_manager)
    t.start()
    t.join()

    # Cleanup in main thread
    twm.stop_socket(sock_id)
    twm.stop()
    print("quit")

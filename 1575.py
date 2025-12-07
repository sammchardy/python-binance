from binance import ThreadedWebsocketManager, AsyncClient
import asyncio

api_key = ""
api_secret = ""


async def run_websocket_operations():
    symbol = "BNBBTC"

    # Create async client
    client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)

    try:
        # Get account status using async call
        account = await client.ws_get_symbol_ticker(symbol=symbol)
        print(f"account: {account}")
    finally:
        await client.close_connection()


def handle_socket_message(msg):
    print(f"message type: {msg['e']}")
    # print(msg)


def main():
    # Start ThreadedWebsocketManager
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    twm.start()

    # Start kline socket
    twm.start_kline_socket(callback=handle_socket_message, symbol="BNBBTC")

    # Run async operations in a separate event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_websocket_operations())

    twm.join()


if __name__ == "__main__":
    main()

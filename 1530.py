import asyncio
import sys

sys.path.append(".")
from binance.async_client import AsyncClient
from binance import BinanceSocketManager

# set log level to debug AND PRINT TO CONSOLE
import logging

logging.basicConfig(level=logging.DEBUG)


async def handle_user_socket():
    # Initialize the client
    client = await AsyncClient.create()
    try:
        # Initialize socket manager
        bm = BinanceSocketManager(client)
        # Start user socket with proper context management
        async with bm.ticker_socket() as socket:
            while True:
                res = await socket.recv()
                finished = do_something(res)
                if finished:
                    break
    finally:
        # Ensure client is properly closed
        print("Closing client")
        await client.close_connection()


def do_something(res):
    # Implement your message handling logic here
    print(f"Received message: {res}")
    return True  # Return True when you want to stop the loop


# Run the async function
if __name__ == "__main__":
    asyncio.run(handle_user_socket())

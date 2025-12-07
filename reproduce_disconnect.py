import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager
from binance.ws.reconnecting_websocket import ReconnectingWebsocket

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def run_socket(bm):
    async with bm.multiplex_socket(["btcusdt@kline_1s"]) as tscm:
        logger.info("Websocket started")
        count = 0
        while True:
            try:
                logger.info("Awaiting message...")
                t = await tscm.recv()
                logger.info(f"Message received: {t}")
                count += 1

                if count == 3 or count == 9:
                    logger.info("Simulating connection drop (code 1001)")
                    await tscm.ws.close(code=1001, reason="going away")

                if count == 6:
                    tscm.MAX_RECONNECTS = 0

                if t.get("e") == "error":
                    logger.error(f"Error: {t.get('m')}")
                    # if t.get("type") == "BinanceWebsocketUnableToConnect":
                    #     logger.info("Detected BinanceWebsocketUnableToConnect")
                    #     break

                print(t.get("data"))
                logger.info("Loop continues")

            except Exception as e:
                logger.error(f"Error in socket loop: {e}")
                break


async def main():
    # Set MAX_RECONNECTS to 2 to allow for reconnection attempts
    ReconnectingWebsocket.MAX_RECONNECTS = 5  # type: ignore

    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    reconnect_attempts = 0
    max_reconnects = 2

    try:
        while reconnect_attempts < max_reconnects:
            try:
                await run_socket(bm)
                reconnect_attempts += 1
                logger.info(
                    f"Reconnecting attempt {reconnect_attempts}/{max_reconnects}..."
                )
                if reconnect_attempts < max_reconnects:
                    await asyncio.sleep(2)  # Wait before next reconnection attempt
            except Exception as e:
                logger.error(f"Error during socket operation: {e}")
                reconnect_attempts += 1
                if reconnect_attempts < max_reconnects:
                    await asyncio.sleep(2)
    finally:
        await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())

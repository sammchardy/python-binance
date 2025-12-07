import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager
from binance.ws.reconnecting_websocket import ReconnectingWebsocket

logging.basicConfig(level=logging.DEBUG)

# Explicitly set the log level for the binance package
logging.getLogger("binance").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


async def main():
    # Set MAX_RECONNECTS to 0 to simulate permanent disconnect
    ReconnectingWebsocket.MAX_RECONNECTS = 3

    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    async with bm.multiplex_socket(["btcusdt@kline_1s"]) as tscm:
        logger.info("Websocket started")
        count = 0
        while True:
            logger.info("Awaiting message...")
            t = await tscm.recv()
            logger.info("Message received")
            count += 1
            try:
                if count == 5:
                    logger.info("Simulating connection drop (code 1001)")
                    await tscm.ws.close(code=1001, reason="going away")
                print(t["data"])
            except KeyError as e:
                logger.warning(f"Error: {e} with data {t}")
            logger.info("Loop continues")

    await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())

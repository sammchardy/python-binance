import asyncio
import logging
import subprocess
import time
from binance import AsyncClient, BinanceSocketManager
from binance.ws.reconnecting_websocket import ReconnectingWebsocket

logging.basicConfig(level=logging.DEBUG)

# Explicitly set the log level for the binance package
logging.getLogger("binance").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


async def simulate_network_disconnect():
    """Simulate network disconnect by temporarily disabling network interface"""
    logger.info("=== SIMULATING NETWORK DISCONNECT ===")
    try:
        # Get the active network interface
        result = subprocess.run(
            ["route", "get", "default"], capture_output=True, text=True, check=True
        )
        interface = None
        for line in result.stdout.split("\n"):
            if "interface:" in line:
                interface = line.split(":")[1].strip()
                break

        if not interface:
            logger.error("Could not determine network interface")
            return False

        logger.info(f"Temporarily disabling network interface: {interface}")

        # Disable the network interface
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)

        # Wait for disconnect to take effect
        logger.info("Network interface disabled - waiting 10 seconds...")
        await asyncio.sleep(10)

        # Re-enable the network interface
        logger.info(f"Re-enabling network interface: {interface}")
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)

        # Wait a bit for network to come back up
        await asyncio.sleep(3)
        logger.info("Network interface restored")

    except Exception as e:
        logger.error(f"Network interface manipulation failed: {e}")
        logger.info("This method requires sudo privileges")
        return False

    return True


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    # Test futures kline socket to reproduce the 1001 reconnection issue
    async with bm.multiplex_socket(["btcusdt@kline_1s"]) as tscm:
        logger.info("Futures kline websocket started")
        count = 0
        while True:
            try:
                logger.info("Awaiting message...")
                t = await tscm.recv()
                logger.info("Message received")
                count += 1

                # Simulate realistic network disconnect after receiving some messages
                if count == 5:
                    logger.info("Triggering network disconnect simulation...")
                    # Run network disconnect simulation in background
                    asyncio.create_task(simulate_network_disconnect())

                print(f"Message {count}: {t}")

            except Exception as e:
                logger.error(f"Error occurred: {e}")
                logger.error(f"Error type: {type(e)}")
                # Check if we get the ConnectionClosedOK error
                if "ConnectionClosedOK" in str(e) or "1001" in str(e):
                    logger.error(
                        "Got the 1001 'going away' error - this should trigger reconnection"
                    )
                    logger.error(
                        "Waiting to see if websocket reconnects automatically..."
                    )
                    await asyncio.sleep(5)  # Wait to see if reconnection happens
                else:
                    raise e

    await client.close_connection()


if __name__ == "__main__":
    asyncio.run(main())

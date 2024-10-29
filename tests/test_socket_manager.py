from binance import BinanceSocketManager, AsyncClient
import pytest


def assert_message(msg):
    assert msg["stream"] == "!ticker@arr"
    assert len(msg["data"]) > 0


@pytest.mark.asyncio()
async def test_ticker_socket():
    client = await AsyncClient.create(testnet=True)
    bm = BinanceSocketManager(client)

    ts = bm.futures_ticker_socket()

    async with ts as tscm:
        try:
            res = await tscm.recv()
            assert_message(res)
        except Exception as e:
            print(f"An error occurred: {e}")

    await client.close_connection()

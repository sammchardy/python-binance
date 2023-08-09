from binance.streams import BinanceSocketManager
from binance.client import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_socket_stopped_on_aexit():
    client = AsyncClient()
    bm = BinanceSocketManager(client)
    ts1 = bm.trade_socket('BNBBTC')
    async with ts1:
        pass
    ts2 = bm.trade_socket('BNBBTC')
    assert ts2 is not ts1, "socket should be removed from _conn on exit"
    await client.close_connection()

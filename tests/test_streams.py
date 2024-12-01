import sys
from binance import BinanceSocketManager
import pytest

@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_stopped_on_aexit(clientAsync):
    bm = BinanceSocketManager(clientAsync)
    ts1 = bm.trade_socket("BNBBTC")
    async with ts1:
        pass
    ts2 = bm.trade_socket("BNBBTC")
    assert ts2 is not ts1, "socket should be removed from _conn on exit"
    await clientAsync.close_connection()

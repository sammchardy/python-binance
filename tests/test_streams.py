import sys
from binance import BinanceSocketManager
import pytest

from binance.async_client import AsyncClient
from .conftest import proxy, api_key, api_secret, testnet


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_stopped_on_aexit(clientAsync):
    bm = BinanceSocketManager(clientAsync)
    ts1 = bm.trade_socket("BNBBTC")
    async with ts1:
        pass
    assert bm._conns == {}, "socket should be removed from _conn on exit"
    ts2 = bm.trade_socket("BNBBTC")
    assert ts2 is not ts1, "socket should be removed from _conn on exit"
    await clientAsync.close_connection()

@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_stopped_on_aexit_futures(futuresClientAsync):
    bm = BinanceSocketManager(futuresClientAsync)
    ts1 = bm.futures_user_socket()
    async with ts1:
        pass
    assert bm._conns == {}, "socket should be removed from _conn on exit"
    await futuresClientAsync.close_connection()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_spot_market_time_unit_microseconds():
    clientAsync = AsyncClient(
        api_key, api_secret, https_proxy=proxy, testnet=testnet, time_unit="MICROSECOND"
    )
    bm = BinanceSocketManager(clientAsync)
    ts1 = bm.symbol_ticker_socket("BTCUSDT")
    async with ts1:
        trade = await ts1.recv()
        assert len(str(trade["E"])) >= 16, "Time should be in microseconds (16+ digits)"
    await clientAsync.close_connection()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_spot_market_time_unit_milliseconds():
    clientAsync = AsyncClient(
        api_key, api_secret, https_proxy=proxy, testnet=testnet, time_unit="MILLISECOND"
    )
    bm = BinanceSocketManager(clientAsync)
    ts1 = bm.symbol_ticker_socket("BTCUSDT")
    async with ts1:
        trade = await ts1.recv()
        assert len(str(trade["E"])) == 13, "Time should be in milliseconds (13 digits)"
    await clientAsync.close_connection()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_spot_user_data_time_unit_microseconds():
    clientAsync = AsyncClient(
        api_key, api_secret, https_proxy=proxy, testnet=testnet, time_unit="MICROSECOND"
    )
    bm = BinanceSocketManager(clientAsync)
    ts1 = bm.user_socket()
    async with ts1:
        await clientAsync.create_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        trade = await ts1.recv()
        assert len(str(trade["E"])) >= 16, "Time should be in microseconds (16+ digits)"
    await clientAsync.close_connection()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="websockets_proxy Python 3.8+")
@pytest.mark.asyncio
async def test_socket_spot_user_data_time_unit_milliseconds():
    clientAsync = AsyncClient(
        api_key, api_secret, https_proxy=proxy, testnet=testnet, time_unit="MILLISECOND"
    )
    bm = BinanceSocketManager(clientAsync)
    ts1 = bm.user_socket()
    async with ts1:
        await clientAsync.create_order(
            symbol="LTCUSDT", side="BUY", type="MARKET", quantity=0.1
        )
        trade = await ts1.recv()
        assert len(str(trade["E"])) == 13, "Time should be in milliseconds (13 digits)"
    await clientAsync.close_connection()

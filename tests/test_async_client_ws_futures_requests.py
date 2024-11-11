import pytest
from .test_get_order_book import assert_ob

@pytest.mark.asyncio()
async def test_ws_futures_get_order_book(clientAsync):
    orderbook = await clientAsync.ws_futures_get_order_book(symbol = 'BTCUSDT')
    assert_ob(orderbook)
    
@pytest.mark.asyncio()
async def test_ws_futures_get_all_tickers(clientAsync):
    await clientAsync.ws_futures_get_all_tickers()
    
@pytest.mark.asyncio()
async def test_ws_futures_get_order_book_ticker(clientAsync):
    await clientAsync.ws_futures_get_order_book_ticker()
    
@pytest.mark.asyncio()
async def test_ws_futures_create_order(clientAsync):
    await clientAsync.ws_futures_create_order()
    
@pytest.mark.asyncio()
async def test_ws_futures_edit_order(clientAsync):
    await clientAsync.ws_futures_edit_order()

@pytest.mark.asyncio()
async def test_ws_futures_cancel_order(clientAsync):
    await clientAsync.ws_futures_cancel_order()
    
@pytest.mark.asyncio()
async def test_ws_futures_get_order(clientAsync):
    await clientAsync.ws_futures_get_order()
    
@pytest.mark.asyncio()
async def test_ws_futures_v2_account_position(clientAsync):
    await clientAsync.ws_futures_v2_account_position()

@pytest.mark.asyncio()
async def test_ws_futures_account_position(clientAsync):
    await clientAsync.ws_futures_account_position()
    
@pytest.mark.asyncio()
async def test_ws_futures_v2_account_balance(clientAsync):
    await clientAsync.ws_futures_v2_account_balance()

@pytest.mark.asyncio()
async def test_ws_futures_account_balance(clientAsync):
    await clientAsync.ws_futures_account_balance()

@pytest.mark.asyncio()
async def test_ws_futures_v2_account_status(clientAsync):
    await clientAsync.ws_futures_v2_account_status()
    
@pytest.mark.asyncio()
async def test_ws_futures_account_status(clientAsync):
    await clientAsync.ws_futures_account_status()
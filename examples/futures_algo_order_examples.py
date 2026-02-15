#!/usr/bin/env python
"""
Examples of how to use the Futures Algo Order API.

New Algo Order supports various conditional order types including:
- STOP / STOP_MARKET
- TAKE_PROFIT / TAKE_PROFIT_MARKET
- TRAILING_STOP_MARKET

This example demonstrates the new parameters and features available
for creating advanced algo orders with TP/SL functionality.
"""

from binance.client import Client

# Initialize the client
api_key = '<api_key>'
api_secret = '<api_secret>'
client = Client(api_key, api_secret)


def create_basic_stop_market_order():
    """Create a basic STOP_MARKET algo order"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='STOP_MARKET',
        quantity=0.001,
        triggerPrice=40000,
        workingType='CONTRACT_PRICE'
    )
    print("Basic Stop Market Order:", order)
    return order


def create_take_profit_with_price_protect():
    """Create a TAKE_PROFIT order with price protection enabled"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='TAKE_PROFIT',
        quantity=0.001,
        price=50000,
        triggerPrice=50000,
        timeInForce='GTC',
        priceProtect='TRUE',
        workingType='MARK_PRICE'
    )
    print("Take Profit with Price Protection:", order)
    return order


def create_trailing_stop_market():
    """Create a TRAILING_STOP_MARKET order with activate price and callback rate"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='TRAILING_STOP_MARKET',
        quantity=0.001,
        activatePrice=48000,  # Activate when price reaches this level
        callbackRate=1.0,     # 1% callback rate
    )
    print("Trailing Stop Market:", order)
    return order


def create_stop_with_stp_mode():
    """Create a STOP order with Self-Trade Prevention mode"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='BUY',
        positionSide='LONG',  # For hedge mode
        type='STOP',
        quantity=0.001,
        price=42000,
        triggerPrice=42000,
        timeInForce='GTC',
        selfTradePreventionMode='EXPIRE_MAKER'
    )
    print("Stop Order with STP Mode:", order)
    return order


def create_take_profit_with_price_match():
    """Create a TAKE_PROFIT order with price match parameter"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='TAKE_PROFIT',
        quantity=0.001,
        triggerPrice=50000,
        timeInForce='GTC',
        priceMatch='OPPONENT',  # Match opponent's price
    )
    print("Take Profit with Price Match:", order)
    return order


def create_stop_market_close_position():
    """Create a STOP_MARKET order to close all positions"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='STOP_MARKET',
        closePosition='true',  # Close all current long positions
        triggerPrice=39000,
        priceProtect='TRUE'
    )
    print("Stop Market Close Position:", order)
    return order


def create_stop_with_reduce_only():
    """Create a STOP order with reduce only mode"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='STOP',
        quantity=0.001,
        price=41000,
        triggerPrice=41000,
        timeInForce='GTC',
        reduceOnly='true'  # Only reduce position, not increase
    )
    print("Stop with Reduce Only:", order)
    return order


def create_with_good_till_date():
    """Create an algo order with GTD (Good Till Date) time in force"""
    import time
    # Set expiry to 1 hour from now (timestamp in milliseconds)
    expiry_time = int((time.time() + 3600) * 1000)
    
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='SELL',
        type='TAKE_PROFIT',
        quantity=0.001,
        price=50000,
        triggerPrice=50000,
        timeInForce='GTD',
        goodTillDate=expiry_time
    )
    print("Order with Good Till Date:", order)
    return order


def create_with_result_response():
    """Create an algo order with RESULT response type for detailed information"""
    order = client.futures_create_algo_order(
        symbol='BTCUSDT',
        side='BUY',
        type='STOP_MARKET',
        quantity=0.001,
        triggerPrice=42000,
        newOrderRespType='RESULT'  # Get detailed response
    )
    print("Order with RESULT response:", order)
    return order


def query_algo_order(symbol, algo_id):
    """Query a specific algo order status"""
    order = client.futures_get_algo_order(
        symbol=symbol,
        algoId=algo_id
    )
    print("Algo Order Status:", order)
    return order


def query_open_algo_orders(symbol=None):
    """Query all open algo orders"""
    if symbol:
        orders = client.futures_get_open_algo_orders(symbol=symbol)
    else:
        orders = client.futures_get_open_algo_orders()
    print("Open Algo Orders:", orders)
    return orders


def cancel_algo_order(symbol, algo_id):
    """Cancel a specific algo order"""
    result = client.futures_cancel_algo_order(
        symbol=symbol,
        algoId=algo_id
    )
    print("Cancel Result:", result)
    return result


def cancel_all_algo_orders(symbol):
    """Cancel all open algo orders for a symbol"""
    result = client.futures_cancel_all_algo_open_orders(symbol=symbol)
    print("Cancel All Result:", result)
    return result


if __name__ == '__main__':
    # Example usage
    print("=" * 50)
    print("Futures Algo Order Examples")
    print("=" * 50)
    
    # Create different types of algo orders
    # Uncomment the examples you want to try
    
    # order = create_basic_stop_market_order()
    # order = create_take_profit_with_price_protect()
    # order = create_trailing_stop_market()
    # order = create_stop_with_stp_mode()
    # order = create_take_profit_with_price_match()
    # order = create_with_result_response()
    
    # Query orders
    # orders = query_open_algo_orders('BTCUSDT')
    
    # Cancel orders
    # cancel_algo_order('BTCUSDT', algo_id=12345)
    # cancel_all_algo_orders('BTCUSDT')

from datetime import datetime

import pytest
from .test_order import assert_contract_order
from .test_get_order_book import assert_ob

pytestmark = [pytest.mark.futures, pytest.mark.asyncio]

async def test_futures_ping(futuresClientAsync):
    await futuresClientAsync.futures_ping()

async def test_futures_time(futuresClientAsync):
    await futuresClientAsync.futures_time()
async def test_futures_exchange_info(futuresClientAsync):
    await futuresClientAsync.futures_exchange_info()

async def test_futures_order_book(futuresClientAsync):
    order_book = await futuresClientAsync.futures_order_book(symbol="BTCUSDT")
    assert_ob(order_book)

async def test_futures_rpi_depth(futuresClientAsync):
    rpi_depth = await futuresClientAsync.futures_rpi_depth(symbol="BTCUSDT")
    assert_ob(rpi_depth)

async def test_futures_recent_trades(futuresClientAsync):
    await futuresClientAsync.futures_recent_trades(symbol="BTCUSDT")

async def test_futures_historical_trades(futuresClientAsync):
    await futuresClientAsync.futures_historical_trades(symbol="BTCUSDT")

async def test_futures_aggregate_trades(futuresClientAsync):
    await futuresClientAsync.futures_aggregate_trades(symbol="BTCUSDT")

async def test_futures_klines(futuresClientAsync):
    await futuresClientAsync.futures_klines(symbol="BTCUSDT", interval="1h")

async def test_futures_continuous_klines(futuresClientAsync):
    await futuresClientAsync.futures_continuous_klines(
        pair="BTCUSDT", contractType="PERPETUAL", interval="1h"
    )

async def test_futures_historical_klines(futuresClientAsync):
    await futuresClientAsync.futures_historical_klines(
        symbol="BTCUSDT", interval="1h", start_str=datetime.now().strftime("%Y-%m-%d")
    )

async def test_futures_historical_klines_generator(futuresClientAsync):
    await futuresClientAsync.futures_historical_klines_generator(
        symbol="BTCUSDT", interval="1h", start_str=datetime.now().strftime("%Y-%m-%d")
    )

async def test_futures_mark_price(futuresClientAsync):
    await futuresClientAsync.futures_mark_price()

async def test_futures_funding_rate(futuresClientAsync):
    await futuresClientAsync.futures_funding_rate()

@pytest.mark.skip(reason="No Sandbox Environment to test")
async def test_futures_top_longshort_account_ratio(futuresClientAsync):
    await futuresClientAsync.futures_top_longshort_account_ratio(
        symbol="BTCUSDT", period="5m"
    )

@pytest.mark.skip(reason="No Sandbox Environment to test")
async def test_futures_top_longshort_position_ratio(futuresClientAsync):
    await futuresClientAsync.futures_top_longshort_position_ratio(
        symbol="BTCUSDT", period="5m"
    )

@pytest.mark.skip(reason="No Sandbox Environment to test")
async def test_futures_global_longshort_ratio(futuresClientAsync):
    await futuresClientAsync.futures_global_longshort_ratio(
        symbol="BTCUSDT", period="5m"
    )

@pytest.mark.skip(reason="No Sandbox Environment to test")
async def test_futures_taker_longshort_ratio(futuresClientAsync):
    await futuresClientAsync.futures_taker_longshort_ratio(
        symbol="BTCUSDT", period="5m"
    )

async def test_futures_ticker(futuresClientAsync):
    await futuresClientAsync.futures_ticker()

async def test_futures_symbol_ticker(futuresClientAsync):
    await futuresClientAsync.futures_symbol_ticker()

async def test_futures_orderbook_ticker(futuresClientAsync):
    await futuresClientAsync.futures_orderbook_ticker()

async def test_futures_index_index_price_constituents(futuresClientAsync):
    await futuresClientAsync.futures_index_price_constituents(symbol="BTCUSD")

async def test_futures_liquidation_orders(futuresClientAsync):
    await futuresClientAsync.futures_liquidation_orders()

@pytest.mark.skip(reason="Temporary skip due to issues with api")
async def test_futures_api_trading_status(futuresClientAsync):
    await futuresClientAsync.futures_api_trading_status()

async def test_futures_commission_rate(futuresClientAsync):
    await futuresClientAsync.futures_commission_rate(symbol="BTCUSDT")

async def test_futures_adl_quantile_estimate(futuresClientAsync):
    await futuresClientAsync.futures_adl_quantile_estimate()

async def test_futures_open_interest(futuresClientAsync):
    await futuresClientAsync.futures_open_interest(symbol="BTCUSDT")

async def test_futures_index_info(futuresClientAsync):
    await futuresClientAsync.futures_index_info()

@pytest.mark.skip(reason="No Sandbox Environment to test")
async def test_futures_open_interest_hist(futuresClientAsync):
    await futuresClientAsync.futures_open_interest_hist(symbol="BTCUSDT", period="5m")

async def test_futures_leverage_bracket(futuresClientAsync):
    await futuresClientAsync.futures_leverage_bracket()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_account_transfer(futuresClientAsync):
    await futuresClientAsync.futures_account_transfer()

@pytest.mark.skip(reason="Not implemented")
async def test_transfer_history(client):
    client.transfer_history()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_loan_borrow_history(futuresClientAsync):
    await futuresClientAsync.futures_loan_borrow_history()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_loan_repay_history(futuresClientAsync):
    await futuresClientAsync.futures_loan_repay_history()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_loan_wallet(futuresClientAsync):
    await futuresClientAsync.futures_loan_wallet()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_cross_collateral_adjust_history(futuresClientAsync):
    await futuresClientAsync.futures_cross_collateral_adjust_history()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_cross_collateral_liquidation_history(futuresClientAsync):
    await futuresClientAsync.futures_cross_collateral_liquidation_history()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_loan_interest_history(futuresClientAsync):
    await futuresClientAsync.futures_loan_interest_history()

async def test_futures_create_get_edit_cancel_order(futuresClientAsync):
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    order = await futuresClientAsync.futures_create_order(
        symbol=ticker["symbol"],
        side="SELL",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["lastPrice"]) + 1)),
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.futures_modify_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.futures_get_order(
        symbol=order["symbol"], orderid=order["orderId"]
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )

async def test_futures_create_test_order(futuresClientAsync):
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    await futuresClientAsync.futures_create_test_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["lastPrice"]) - 1, 0)),
    )

async def test_futures_place_batch_order_and_cancel(futuresClientAsync):
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    orders = await futuresClientAsync.futures_place_batch_order(
        batchOrders=[
            {
                "positionSide": positions[0]["positionSide"],
                "price": str(round(float(ticker["lastPrice"]) + 2, 0)),
                "quantity": "0.1",
                "side": "SELL",
                "symbol": ticker["symbol"],
                "timeInForce": "GTC",
                "type": "LIMIT",
            },
            {
                "side": "SELL",
                "type": "LIMIT",
                "positionSide": positions[0]["positionSide"],
                "price": str(round(float(ticker["lastPrice"]) + 2, 0)),
                "quantity": "0.1",
                "symbol": ticker["symbol"],
                "timeInForce": "GTC",
            },
        ]
    )
    for order in orders:
        assert_contract_order(futuresClientAsync, order)

    # Cancel using orderidlist
    order_ids = [order["orderId"] for order in orders][:1]
    cancelled_orders = await futuresClientAsync.futures_cancel_orders(
        symbol=orders[0]["symbol"], orderidlist=order_ids
    )
    for order in cancelled_orders:
        assert_contract_order(futuresClientAsync, order)
    # Cancel using origClientOrderIdList
    client_order_ids = [order["clientOrderId"] for order in orders][1:]
    cancelled_orders = await futuresClientAsync.futures_cancel_orders(
        symbol=orders[0]["symbol"], origclientorderidlist=client_order_ids
    )
    for order in cancelled_orders:
        assert_contract_order(futuresClientAsync, order)

async def test_futures_get_open_orders(futuresClientAsync):
    await futuresClientAsync.futures_get_open_orders()

async def test_futures_get_all_orders(futuresClientAsync):
    orders = futuresClientAsync.futures_get_all_orders()
    print(orders)

async def test_futures_cancel_all_open_orders(futuresClientAsync):
    await futuresClientAsync.futures_cancel_all_open_orders(symbol="LTCUSDT")

async def test_futures_countdown_cancel_all(futuresClientAsync):
    await futuresClientAsync.futures_countdown_cancel_all(
        symbol="LTCUSDT", countdownTime=10
    )

async def test_futures_account_balance(futuresClientAsync):
    await futuresClientAsync.futures_account_balance()

async def test_futures_account(futuresClientAsync):
    await futuresClientAsync.futures_account()

async def test_futures_symbol_adl_risk(futuresClientAsync):
    # Test without symbol (get all)
    adl_risks = await futuresClientAsync.futures_symbol_adl_risk()
    assert isinstance(adl_risks, list)

    # Test with specific symbol (if any symbols available)
    if len(adl_risks) > 0:
        test_symbol = adl_risks[0]["symbol"]
        adl_risk = await futuresClientAsync.futures_symbol_adl_risk(symbol=test_symbol)
        assert isinstance(adl_risk, dict)
        assert "symbol" in adl_risk
        assert "adlRisk" in adl_risk
        assert adl_risk["adlRisk"] in ["low", "medium", "high"]
        assert adl_risk["symbol"] == test_symbol

async def test_futures_change_leverage(futuresClientAsync):
    await futuresClientAsync.futures_change_leverage(symbol="LTCUSDT", leverage=10)

async def test_futures_change_margin_type(futuresClientAsync):
    try:
        await futuresClientAsync.futures_change_margin_type(
            symbol="XRPUSDT", marginType="CROSSED"
        )
    except Exception as e:
        await futuresClientAsync.futures_change_margin_type(
            symbol="XRPUSDT", marginType="ISOLATED"
        )

async def test_futures_position_margin_history(futuresClientAsync):
    position = await futuresClientAsync.futures_position_margin_history(
        symbol="LTCUSDT"
    )

async def test_futures_position_information(futuresClientAsync):
    await futuresClientAsync.futures_position_information()

async def test_futures_account_trades(futuresClientAsync):
    await futuresClientAsync.futures_account_trades()

async def test_futures_income_history(futuresClientAsync):
    await futuresClientAsync.futures_income_history()

async def close_all_futures_positions(futuresClientAsync):
    # Get all open positions
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")

    for position in positions:
        # Check if there is an open position
        if float(position["positionAmt"]) != 0:
            symbol = position["symbol"]
            position_amt = float(position["positionAmt"])
            side = "SELL" if position_amt > 0 else "BUY"

            # Place a market order to close the position
            try:
                print(f"Closing position for {symbol}: {position_amt} units")
                await futuresClientAsync.futures_create_order(
                    symbol=symbol, side=side, type="market", quantity=abs(position_amt)
                )
                print(f"Position for {symbol} closed successfully.")
            except Exception as e:
                print(f"Failed to close position for {symbol}: {e}")

@pytest.mark.skip(reason="Not implemented")
async def test_futures_get_and_change_position_mode(futuresClientAsync):
    mode = await futuresClientAsync.futures_get_position_mode()
    await futuresClientAsync.futures_change_position_mode(
        dualSidePosition=not mode["dualSidePosition"]
    )

@pytest.mark.skip(reason="Not implemented")
async def test_futures_change_multi_assets_mode(futuresClientAsync):
    await futuresClientAsync.futures_change_multi_assets_mode()

async def test_futures_get_multi_assets_mode(futuresClientAsync):
    await futuresClientAsync.futures_get_multi_assets_mode()

async def test_futures_stream_get_listen_key(futuresClientAsync):
    await futuresClientAsync.futures_stream_get_listen_key()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_stream_close(futuresClientAsync):
    await futuresClientAsync.futures_stream_close()

# new methods
async def test_futures_account_config(futuresClientAsync):
    await futuresClientAsync.futures_account_config()

async def test_futures_symbol_config(futuresClientAsync):
    await futuresClientAsync.futures_symbol_config()

# COIN Futures API
async def test_futures_coin_ping(futuresClientAsync):
    await futuresClientAsync.futures_coin_ping()

async def test_futures_coin_time(futuresClientAsync):
    await futuresClientAsync.futures_coin_time()

async def test_futures_coin_exchange_info(futuresClientAsync):
    await futuresClientAsync.futures_coin_exchange_info()

async def test_futures_coin_order_book(futuresClientAsync):
    order_book = await futuresClientAsync.futures_coin_order_book(symbol="BTCUSD_PERP")
    assert_ob(order_book)

async def test_futures_coin_recent_trades(futuresClientAsync):
    await futuresClientAsync.futures_coin_recent_trades(symbol="BTCUSD_PERP")

async def test_futures_coin_historical_trades(futuresClientAsync):
    await futuresClientAsync.futures_coin_historical_trades(symbol="BTCUSD_PERP")

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_aggregate_trades(futuresClientAsync):
    await futuresClientAsync.futures_coin_aggregate_trades(symbol="BTCUSD_PERP")

async def test_futures_coin_klines(futuresClientAsync):
    await futuresClientAsync.futures_coin_klines(symbol="BTCUSD_PERP", interval="1h")

async def test_futures_coin_continous_klines(futuresClientAsync):
    await futuresClientAsync.futures_coin_continous_klines(
        pair="BTCUSD", contractType="PERPETUAL", interval="1h"
    )

async def test_futures_coin_index_price_klines(futuresClientAsync):
    await futuresClientAsync.futures_coin_index_price_klines(
        pair="BTCUSD", interval="1m"
    )

async def test_futures_coin_mark_price_klines(futuresClientAsync):
    await futuresClientAsync.futures_coin_mark_price_klines(
        symbol="BTCUSD_PERP", interval="1m"
    )

async def test_futures_coin_mark_price(futuresClientAsync):
    await futuresClientAsync.futures_coin_mark_price()

@pytest.mark.skip(reason="Giving unknwon error from binance")
async def test_futures_coin_funding_rate(futuresClientAsync):
    await futuresClientAsync.futures_coin_funding_rate(symbol="BTCUSD_PERP")

async def test_futures_coin_ticker(futuresClientAsync):
    await futuresClientAsync.futures_coin_ticker()

async def test_futures_coin_symbol_ticker(futuresClientAsync):
    await futuresClientAsync.futures_coin_symbol_ticker()

async def test_futures_coin_orderbook_ticker(futuresClientAsync):
    await futuresClientAsync.futures_coin_orderbook_ticker()

async def test_futures_coin_index_index_price_constituents(futuresClientAsync):
    await futuresClientAsync.futures_coin_index_price_constituents(symbol="BTCUSD")

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_liquidation_orders(futuresClientAsync):
    await futuresClientAsync.futures_coin_liquidation_orders()

async def test_futures_coin_open_interest(futuresClientAsync):
    await futuresClientAsync.futures_coin_open_interest(symbol="BTCUSD_PERP")

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_open_interest_hist(futuresClientAsync):
    await futuresClientAsync.futures_coin_open_interest_hist(symbol="BTCUSD_PERP")

async def test_futures_coin_leverage_bracket(futuresClientAsync):
    await futuresClientAsync.futures_coin_leverage_bracket()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_create_order(futuresClientAsync):
    positions = await futuresClientAsync.futures_coin_position_information()
    ticker = await futuresClientAsync.futures_coin_ticker(symbol=positions[0]["symbol"])
    order = await futuresClientAsync.futures_coin_create_order(
        symbol=positions[0]["symbol"],
        side="BUY",
        type="LIMIT",
        timeInForce="GTC",
        quantity=1,
        price=str(round(float(ticker[0]["lastPrice"]) - 1, 0)),
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.futures_modify_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.futures_get_order(
        symbol=order["symbol"], orderid=order["orderId"]
    )
    assert_contract_order(futuresClientAsync, order)
    order = await futuresClientAsync.futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_place_batch_order(futuresClientAsync):
    await futuresClientAsync.futures_coin_place_batch_order()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_get_order(futuresClientAsync):
    await futuresClientAsync.futures_coin_get_order()

async def test_futures_coin_get_open_orders(futuresClientAsync):
    await futuresClientAsync.futures_coin_get_open_orders()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_get_all_orders(futuresClientAsync):
    await futuresClientAsync.futures_coin_get_all_orders()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_cancel_order(futuresClientAsync):
    await futuresClientAsync.futures_coin_cancel_order()

async def test_futures_coin_cancel_all_open_orders(futuresClientAsync):
    await futuresClientAsync.futures_coin_cancel_all_open_orders(symbol="BTCUSD_PERP")

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_cancel_orders(futuresClientAsync):
    await futuresClientAsync.futures_coin_cancel_orders()

async def test_futures_coin_account_balance(futuresClientAsync):
    await futuresClientAsync.futures_coin_account_balance()

async def test_futures_coin_account(futuresClientAsync):
    await futuresClientAsync.futures_coin_account()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_change_leverage(futuresClientAsync):
    await futuresClientAsync.futures_coin_change_leverage(symbol="XRPUSDT", leverage=10)

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_change_margin_type(futuresClientAsync):
    await futuresClientAsync.futures_coin_change_margin_type()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_change_position_margin(futuresClientAsync):
    await futuresClientAsync.futures_coin_change_position_margin()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_position_margin_history(futuresClientAsync):
    await futuresClientAsync.futures_coin_position_margin_history()

async def test_futures_coin_position_information(futuresClientAsync):
    await futuresClientAsync.futures_coin_position_information()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_account_trades(futuresClientAsync):
    await futuresClientAsync.futures_coin_account_trades()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_income_history(futuresClientAsync):
    await futuresClientAsync.futures_coin_income_history()

@pytest.mark.skip(reason="Not implemented")
async def test_futures_coin_change_position_mode(futuresClientAsync):
    await futuresClientAsync.futures_coin_change_position_mode()

async def test_futures_coin_get_position_mode(futuresClientAsync):
    await futuresClientAsync.futures_coin_get_position_mode()

async def test_futures_coin_stream_close(futuresClientAsync):
    listen_key = await futuresClientAsync.futures_coin_stream_get_listen_key()
    await futuresClientAsync.futures_coin_stream_close(listenKey=listen_key)

@pytest.mark.skip(reason="No sandbox support")
async def test_futures_coin_account_order_history_download(futuresClientAsync):
    await futuresClientAsync.futures_coin_account_order_download()

@pytest.mark.skip(reason="No sandbox support")
async def test_futures_coin_account_order_download_id(futuresClientAsync):
    await futuresClientAsync.futures_coin_account_order_download_link(downloadId="123")

@pytest.mark.skip(reason="No sandbox support")
async def test_futures_coin_account_trade_history_download(futuresClientAsync):
    await futuresClientAsync.futures_coin_account_trade_history_download()

@pytest.mark.skip(reason="No sandbox support")
async def test_futures_coin_account_trade_download_id(futuresClientAsync):
    await futuresClientAsync.futures_coin_account_trade_history_download_link(
        downloadId="123"
    )


# Algo Orders (Conditional Orders) Async Tests


async def test_futures_create_algo_order_async(futuresClientAsync):
    """Test creating an algo/conditional order async"""
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    order = await futuresClientAsync.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    assert order["symbol"] == ticker["symbol"]
    assert "algoId" in order
    # Clean up
    await futuresClientAsync.futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )


async def test_futures_create_order_auto_routes_conditional_async(futuresClientAsync):
    """Test that futures_create_order automatically routes conditional orders async"""
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    order = await futuresClientAsync.futures_create_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="TAKE_PROFIT_MARKET",
        quantity=1,
        stopPrice=10,
    )
    assert order["symbol"] == ticker["symbol"]
    assert "algoId" in order
    # Clean up
    await futuresClientAsync.futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )


async def test_futures_get_algo_order_async(futuresClientAsync):
    """Test getting a specific algo order async"""
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    order = await futuresClientAsync.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    algo_id = order["algoId"]
    fetched_order = await futuresClientAsync.futures_get_algo_order(
        symbol=ticker["symbol"], algoId=algo_id
    )
    assert fetched_order["algoId"] == algo_id
    # Clean up
    await futuresClientAsync.futures_cancel_algo_order(symbol=ticker["symbol"], algoId=algo_id)


async def test_futures_get_all_algo_orders_async(futuresClientAsync):
    """Test getting all algo orders history async"""
    orders = await futuresClientAsync.futures_get_all_algo_orders(symbol="LTCUSDT")
    assert isinstance(orders, list)


async def test_futures_get_open_algo_orders_async(futuresClientAsync):
    """Test getting open algo orders async"""
    orders = await futuresClientAsync.futures_get_open_algo_orders(symbol="LTCUSDT")
    assert isinstance(orders, list)


async def test_futures_cancel_algo_order_async(futuresClientAsync):
    """Test canceling an algo order async"""
    ticker = await futuresClientAsync.futures_ticker(symbol="LTCUSDT")
    positions = await futuresClientAsync.futures_position_information(symbol="LTCUSDT")
    order = await futuresClientAsync.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    algo_id = order["algoId"]
    result = await futuresClientAsync.futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=algo_id
    )
    assert result["algoId"] == algo_id


async def test_futures_cancel_all_algo_open_orders_async(futuresClientAsync):
    """Test canceling all open algo orders async"""
    result = await futuresClientAsync.futures_cancel_all_algo_open_orders(symbol="LTCUSDT")
    assert "code" in result or "msg" in result


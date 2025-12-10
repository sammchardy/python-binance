from datetime import datetime
import re

import pytest
import requests_mock
from .test_order import assert_contract_order
from .test_get_order_book import assert_ob


def test_futures_ping(futuresClient):
    futuresClient.futures_ping()


def test_futures_time(futuresClient):
    futuresClient.futures_time()


def test_futures_exchange_info(futuresClient):
    futuresClient.futures_exchange_info()


def test_futures_order_book(futuresClient):
    order_book = futuresClient.futures_order_book(symbol="BTCUSDT")
    assert_ob(order_book)


def test_futures_rpi_depth(futuresClient):
    rpi_depth = futuresClient.futures_rpi_depth(symbol="BTCUSDT")
    assert_ob(rpi_depth)


def test_futures_recent_trades(futuresClient):
    futuresClient.futures_recent_trades(symbol="BTCUSDT")


def test_futures_historical_trades(futuresClient):
    futuresClient.futures_historical_trades(symbol="BTCUSDT")


def test_futures_aggregate_trades(futuresClient):
    futuresClient.futures_aggregate_trades(symbol="BTCUSDT")


def test_futures_klines(futuresClient):
    futuresClient.futures_klines(symbol="BTCUSDT", interval="1h")


def test_futures_mark_price_klines(futuresClient):
    futuresClient.futures_mark_price_klines(symbol="BTCUSDT", interval="1h")


def test_futures_index_price_klines(futuresClient):
    futuresClient.futures_index_price_klines(pair="BTCUSDT", interval="1h")


def test_futures_premium_index_klines(futuresClient):
    futuresClient.futures_premium_index_klines(symbol="BTCUSDT", interval="1h")


def test_futures_continuous_klines(futuresClient):
    futuresClient.futures_continuous_klines(
        pair="BTCUSDT", contractType="PERPETUAL", interval="1h"
    )


def test_futures_historical_klines(futuresClient):
    futuresClient.futures_historical_klines(
        symbol="BTCUSDT", interval="1h", start_str=datetime.now().strftime("%Y-%m-%d")
    )


def test_futures_historical_klines_generator(futuresClient):
    futuresClient.futures_historical_klines_generator(
        symbol="BTCUSDT", interval="1h", start_str=datetime.now().strftime("%Y-%m-%d")
    )


def test_futures_mark_price(futuresClient):
    futuresClient.futures_mark_price()


def test_futures_funding_rate(futuresClient):
    futuresClient.futures_funding_rate()


@pytest.mark.skip(reason="No Sandbox Environment to test")
def test_futures_top_longshort_account_ratio(futuresClient):
    futuresClient.futures_top_longshort_account_ratio(symbol="BTCUSDT", period="5m")


@pytest.mark.skip(reason="No Sandbox Environment to test")
def test_futures_top_longshort_position_ratio(futuresClient):
    futuresClient.futures_top_longshort_position_ratio(symbol="BTCUSDT", period="5m")


@pytest.mark.skip(reason="No Sandbox Environment to test")
def test_futures_global_longshort_ratio(futuresClient):
    futuresClient.futures_global_longshort_ratio(symbol="BTCUSDT", period="5m")


@pytest.mark.skip(reason="No Sandbox Environment to test")
def test_futures_taker_longshort_ratio(futuresClient):
    futuresClient.futures_taker_longshort_ratio(symbol="BTCUSDT", period="5m")


def test_futures_ticker(futuresClient):
    futuresClient.futures_ticker()


def test_futures_symbol_ticker(futuresClient):
    futuresClient.futures_symbol_ticker()


def test_futures_orderbook_ticker(futuresClient):
    futuresClient.futures_orderbook_ticker()


def test_futures_index_index_price_constituents(futuresClient):
    futuresClient.futures_index_price_constituents(symbol="BTCUSD")


def test_futures_liquidation_orders(futuresClient):
    futuresClient.futures_liquidation_orders()


@pytest.mark.skip(reason="Fails in demo environment")
def test_futures_api_trading_status(futuresClient):
    futuresClient.futures_api_trading_status()


def test_futures_commission_rate(futuresClient):
    futuresClient.futures_commission_rate(symbol="BTCUSDT")


def test_futures_adl_quantile_estimate(futuresClient):
    futuresClient.futures_adl_quantile_estimate()


def test_futures_open_interest(futuresClient):
    futuresClient.futures_open_interest(symbol="BTCUSDT")


def test_futures_index_info(futuresClient):
    futuresClient.futures_index_info()


@pytest.mark.skip(reason="No Sandbox Environment to test")
def test_futures_open_interest_hist(futuresClient):
    futuresClient.futures_open_interest_hist(symbol="BTCUSDT", period="5m")


def test_futures_leverage_bracket(futuresClient):
    futuresClient.futures_leverage_bracket()


@pytest.mark.skip(reason="Not implemented")
def test_futures_account_transfer(futuresClient):
    futuresClient.futures_account_transfer()


@pytest.mark.skip(reason="Not implemented")
def test_transfer_history(client):
    client.transfer_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_borrow_history(futuresClient):
    futuresClient.futures_loan_borrow_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_repay_history(futuresClient):
    futuresClient.futures_loan_repay_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_wallet(futuresClient):
    futuresClient.futures_loan_wallet()


@pytest.mark.skip(reason="Not implemented")
def test_futures_cross_collateral_adjust_history(futuresClient):
    futuresClient.futures_cross_collateral_adjust_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_cross_collateral_liquidation_history(futuresClient):
    futuresClient.futures_cross_collateral_liquidation_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_loan_interest_history(futuresClient):
    futuresClient.futures_loan_interest_history()


def test_futures_create_get_edit_cancel_order(futuresClient):
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    order = futuresClient.futures_create_order(
        symbol=ticker["symbol"],
        side="SELL",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["lastPrice"]) + 2)),
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_modify_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_get_order(
        symbol=order["symbol"], orderid=order["orderId"]
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )


def test_futures_create_test_order(futuresClient):
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    futuresClient.futures_create_test_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="LIMIT",
        timeInForce="GTC",
        quantity=0.1,
        price=str(round(float(ticker["lastPrice"]) - 1, 0)),
    )


def test_futures_place_batch_order_and_cancel(futuresClient):
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    orders = futuresClient.futures_place_batch_order(
        batchOrders=[
            {
                "symbol": ticker["symbol"],
                "side": "SELL",
                "positionSide": positions[0]["positionSide"],
                "type": "LIMIT",
                "timeInForce": "GTC",
                "quantity": "0.1",
                "price": str(round(float(ticker["lastPrice"]) + 2, 0)),
            },
            {
                "symbol": ticker["symbol"],
                "type": "LIMIT",
                "side": "SELL",
                "price": str(round(float(ticker["lastPrice"]) + 2, 0)),
                "positionSide": positions[0]["positionSide"],
                "timeInForce": "GTC",
                "quantity": "0.1",
            },
        ]
    )
    for order in orders:
        assert_contract_order(futuresClient, order)
    # Cancel using orderidlist
    order_ids = [order["orderId"] for order in orders][:1]
    cancelled_orders = futuresClient.futures_cancel_orders(
        symbol=orders[0]["symbol"], orderidlist=order_ids
    )
    for order in cancelled_orders:
        assert_contract_order(futuresClient, order)
    # Cancel using origClientOrderIdList
    client_order_ids = [order["clientOrderId"] for order in orders][1:]
    cancelled_orders = futuresClient.futures_cancel_orders(
        symbol=orders[0]["symbol"], origclientorderidlist=client_order_ids
    )
    for order in cancelled_orders:
        assert_contract_order(futuresClient, order)


def test_futures_get_open_orders(futuresClient):
    futuresClient.futures_get_open_orders()


def test_futures_get_all_orders(futuresClient):
    orders = futuresClient.futures_get_all_orders()
    print(orders)


def test_futures_cancel_all_open_orders(futuresClient):
    futuresClient.futures_cancel_all_open_orders(symbol="LTCUSDT")


def test_futures_countdown_cancel_all(futuresClient):
    futuresClient.futures_countdown_cancel_all(symbol="LTCUSDT", countdownTime=10)


def test_futures_account_balance(futuresClient):
    futuresClient.futures_account_balance()


def test_futures_account(futuresClient):
    futuresClient.futures_account()


def test_futures_symbol_adl_risk(futuresClient):
    # Test without symbol (get all)
    adl_risks = futuresClient.futures_symbol_adl_risk()
    assert isinstance(adl_risks, list)

    # Test with specific symbol (if any symbols available)
    if len(adl_risks) > 0:
        test_symbol = adl_risks[0]["symbol"]
        adl_risk = futuresClient.futures_symbol_adl_risk(symbol=test_symbol)
        assert isinstance(adl_risk, dict)
        assert "symbol" in adl_risk
        assert "adlRisk" in adl_risk
        assert adl_risk["adlRisk"] in ["low", "medium", "high"]
        assert adl_risk["symbol"] == test_symbol


def test_futures_change_leverage(futuresClient):
    futuresClient.futures_change_leverage(symbol="LTCUSDT", leverage=10)


def test_futures_change_margin_type(futuresClient):
    try:
        futuresClient.futures_change_margin_type(symbol="XRPUSDT", marginType="CROSSED")
    except Exception as e:
        futuresClient.futures_change_margin_type(
            symbol="XRPUSDT", marginType="ISOLATED"
        )


def test_futures_position_margin_history(futuresClient):
    position = futuresClient.futures_position_margin_history(symbol="LTCUSDT")
    print(position)


def test_futures_position_information(futuresClient):
    futuresClient.futures_position_information()


def test_futures_account_trades(futuresClient):
    futuresClient.futures_account_trades()


def test_futures_income_history(futuresClient):
    futuresClient.futures_income_history()


def close_all_futures_positions(futuresClient):
    # Get all open positions
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")

    for position in positions:
        # Check if there is an open position
        if float(position["positionAmt"]) != 0:
            symbol = position["symbol"]
            position_amt = float(position["positionAmt"])
            side = "SELL" if position_amt > 0 else "BUY"

            # Place a market order to close the position
            try:
                print(f"Closing position for {symbol}: {position_amt} units")
                futuresClient.futures_create_order(
                    symbol=symbol, side=side, type="market", quantity=abs(position_amt)
                )
                print(f"Position for {symbol} closed successfully.")
            except Exception as e:
                print(f"Failed to close position for {symbol}: {e}")


@pytest.mark.skip(reason="Not implemented")
def test_futures_get_and_change_position_mode(futuresClient):
    mode = futuresClient.futures_get_position_mode()
    futuresClient.futures_change_position_mode(
        dualSidePosition=not mode["dualSidePosition"]
    )


@pytest.mark.skip(reason="Not implemented")
def test_futures_change_multi_assets_mode(futuresClient):
    futuresClient.futures_change_multi_assets_mode()


def test_futures_get_multi_assets_mode(futuresClient):
    futuresClient.futures_get_multi_assets_mode()


def test_futures_stream_get_listen_key(futuresClient):
    futuresClient.futures_stream_get_listen_key()


@pytest.mark.skip(reason="Not implemented")
def test_futures_stream_close(futuresClient):
    futuresClient.futures_stream_close()


# new methods
def test_futures_account_config(futuresClient):
    futuresClient.futures_account_config()


def test_futures_symbol_config(futuresClient):
    futuresClient.futures_symbol_config()


# COIN Futures API
def test_futures_coin_ping(futuresClient):
    futuresClient.futures_coin_ping()


def test_futures_coin_time(futuresClient):
    futuresClient.futures_coin_time()


def test_futures_coin_exchange_info(futuresClient):
    futuresClient.futures_coin_exchange_info()


def test_futures_coin_order_book(futuresClient):
    order_book = futuresClient.futures_coin_order_book(symbol="BTCUSD_PERP")
    assert_ob(order_book)


def test_futures_coin_recent_trades(futuresClient):
    futuresClient.futures_coin_recent_trades(symbol="BTCUSD_PERP")


def test_futures_coin_historical_trades(futuresClient):
    futuresClient.futures_coin_historical_trades(symbol="BTCUSD_PERP")


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_aggregate_trades(futuresClient):
    futuresClient.futures_coin_aggregate_trades(symbol="BTCUSD_PERP")


def test_futures_coin_klines(futuresClient):
    futuresClient.futures_coin_klines(symbol="BTCUSD_PERP", interval="1h")


def test_futures_coin_continous_klines(futuresClient):
    futuresClient.futures_coin_continous_klines(
        pair="BTCUSD", contractType="PERPETUAL", interval="1h"
    )


def test_futures_coin_index_price_klines(futuresClient):
    futuresClient.futures_coin_index_price_klines(pair="BTCUSD", interval="1h")


def test_futures_coin_mark_price_klines(futuresClient):
    futuresClient.futures_coin_mark_price_klines(symbol="BTCUSD_PERP", interval="1h")


def test_futures_coin_mark_price(futuresClient):
    futuresClient.futures_coin_mark_price()


@pytest.mark.skip(reason="Giving unknwon error from binance")
def test_futures_coin_funding_rate(futuresClient):
    futuresClient.futures_coin_funding_rate(symbol="BTCUSD_PERP")


def test_futures_coin_ticker(futuresClient):
    futuresClient.futures_coin_ticker()


def test_futures_coin_symbol_ticker(futuresClient):
    futuresClient.futures_coin_symbol_ticker()


def test_futures_coin_orderbook_ticker(futuresClient):
    futuresClient.futures_coin_orderbook_ticker()


def test_futures_coin_index_index_price_constituents(futuresClient):
    futuresClient.futures_coin_index_price_constituents(symbol="BTCUSD")


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_liquidation_orders(futuresClient):
    futuresClient.futures_coin_liquidation_orders(limit=5)


def test_futures_coin_open_interest(futuresClient):
    futuresClient.futures_coin_open_interest(symbol="BTCUSD_PERP")


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_open_interest_hist(futuresClient):
    futuresClient.futures_coin_open_interest_hist(symbol="BTCUSD_PERP")


def test_futures_coin_leverage_bracket(futuresClient):
    futuresClient.futures_coin_leverage_bracket()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_create_order(futuresClient):
    positions = futuresClient.futures_coin_position_information()
    ticker = futuresClient.futures_coin_ticker(symbol=positions[0]["symbol"])
    order = futuresClient.futures_coin_create_order(
        symbol=positions[0]["symbol"],
        side="BUY",
        type="LIMIT",
        timeInForce="GTC",
        quantity=1,
        price=str(round(float(ticker[0]["lastPrice"]) - 1, 0)),
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_modify_order(
        orderid=order["orderId"],
        symbol=order["symbol"],
        quantity=0.11,
        side=order["side"],
        price=order["price"],
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_get_order(
        symbol=order["symbol"], orderid=order["orderId"]
    )
    assert_contract_order(futuresClient, order)
    order = futuresClient.futures_cancel_order(
        orderid=order["orderId"], symbol=order["symbol"]
    )


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_place_batch_order(futuresClient):
    futuresClient.futures_coin_place_batch_order()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_get_order(futuresClient):
    futuresClient.futures_coin_get_order()


def test_futures_coin_get_open_orders(futuresClient):
    futuresClient.futures_coin_get_open_orders()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_get_all_orders(futuresClient):
    futuresClient.futures_coin_get_all_orders()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_cancel_order(futuresClient):
    futuresClient.futures_coin_cancel_order()


def test_futures_coin_cancel_all_open_orders(futuresClient):
    futuresClient.futures_coin_cancel_all_open_orders(symbol="BTCUSD_PERP")


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_cancel_orders(futuresClient):
    futuresClient.futures_coin_cancel_orders()


def test_futures_coin_account_balance(futuresClient):
    futuresClient.futures_coin_account_balance()


def test_futures_coin_account(futuresClient):
    futuresClient.futures_coin_account()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_leverage(futuresClient):
    futuresClient.futures_coin_change_leverage(symbol="XRPUSDT", leverage=10)


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_margin_type(futuresClient):
    futuresClient.futures_coin_change_margin_type()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_position_margin(futuresClient):
    futuresClient.futures_coin_change_position_margin()


def test_futures_coin_position_margin_history(futuresClient):
    futuresClient.futures_coin_position_margin_history(symbol="LTCUSD_PERP")


def test_futures_coin_position_information(futuresClient):
    futuresClient.futures_coin_position_information()


def test_futures_coin_account_trades(futuresClient):
    futuresClient.futures_coin_account_trades()


def test_futures_coin_income_history(futuresClient):
    futuresClient.futures_coin_income_history()


@pytest.mark.skip(reason="Not implemented")
def test_futures_coin_change_position_mode(futuresClient):
    futuresClient.futures_coin_change_position_mode()


def test_futures_coin_get_position_mode(futuresClient):
    futuresClient.futures_coin_get_position_mode()


def test_futures_coin_stream_close(futuresClient):
    listen_key = futuresClient.futures_coin_stream_get_listen_key()
    futuresClient.futures_coin_stream_close(listenKey=listen_key)


########################################################
# Test block trades
########################################################


@pytest.mark.skip(reason="No sandbox support")
def test_futures_coin_account_order_history_download(futuresClient):
    futuresClient.futures_coin_account_order_download()


@pytest.mark.skip(reason="No sandbox support")
def test_futures_coin_account_order_download_id(futuresClient):
    futuresClient.futures_coin_account_order_download_link(downloadId="123")


@pytest.mark.skip(reason="No sandbox support")
def test_futures_coin_account_trade_history_download(futuresClient):
    futuresClient.futures_coin_account_trade_history_download()


@pytest.mark.skip(reason="No sandbox support")
def test_futures_coin_account_trade_download_id(futuresClient):
    futuresClient.futures_coin_account_trade_history_download_link(downloadId="123")


def test_futures_coin_account_order_history_download_mock(futuresClient):
    expected_response = {
        "avgCostTimestampOfLast30d": 7241837,
        "downloadId": "546975389218332672",
    }
    url_pattern = re.compile(
        r"https://[^/]+/dapi/v1/order/asyn"
        r"\?recvWindow=\d+"
        r"&timestamp=\d+"
        r"&signature=[a-f0-9]{64}"
    )

    with requests_mock.mock() as m:
        m.get(
            url_pattern,
            json=expected_response,
        )
        response = futuresClient.futures_coin_account_order_history_download()
        assert response == expected_response


def test_futures_coin_account_order_download_id_mock(futuresClient):
    expected_response = {"link": "hello"}
    url_pattern = re.compile(
        r"https://[^/]+/dapi/v1/order/asyn/id"
        r"\?downloadId=123"
        r"&recvWindow=\d+"
        r"&timestamp=\d+"
        r"&signature=.+"
    )
    with requests_mock.mock() as m:
        m.get(
            url_pattern,
            json=expected_response,
        )

        response = futuresClient.futures_coin_accout_order_history_download_link(
            downloadId="123"
        )
        assert response == expected_response


def test_futures_coin_account_trade_history_download_id_mock(futuresClient):
    expected_response = {
        "avgCostTimestampOfLast30d": 7241837,
        "downloadId": "546975389218332672",
    }
    url_pattern = re.compile(
        r"https://[^/]+/dapi/v1/trade/asyn"
        r"\?recvWindow=\d+"
        r"&timestamp=\d+"
        r"&signature=[a-f0-9]{64}"
    )

    with requests_mock.mock() as m:
        m.get(
            url_pattern,
            json=expected_response,
        )
        response = futuresClient.futures_coin_account_trade_history_download()
        assert response == expected_response


def test_futures_coin_account_trade_history_download_link_mock(futuresClient):
    expected_response = {"link": "hello"}
    url_pattern = re.compile(
        r"https://[^/]+/dapi/v1/trade/asyn/id"
        r"\?downloadId=123"
        r"&recvWindow=\d+"
        r"&timestamp=\d+"
        r"&signature=.+"
    )
    with requests_mock.mock() as m:
        m.get(
            url_pattern,
            json=expected_response,
        )

        response = futuresClient.futures_coin_account_trade_history_download_link(
            downloadId="123"
        )
        assert response == expected_response


# Algo Orders (Conditional Orders) Tests


def test_futures_create_algo_order(futuresClient):
    """Test creating an algo/conditional order"""
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    order = futuresClient.futures_create_algo_order(
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
    # Clean up - cancel the algo order
    futuresClient.futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )


def test_futures_create_order_auto_routes_conditional(futuresClient):
    """Test that futures_create_order automatically routes conditional orders to algo endpoint"""
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    # Create a conditional order using the regular create_order method
    order = futuresClient.futures_create_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="TAKE_PROFIT_MARKET",
        quantity=1,
        stopPrice=10,
    )
    # Verify it was created as an algo order
    assert order["symbol"] == ticker["symbol"]
    assert "algoId" in order
    # Clean up
    futuresClient.futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=order["algoId"]
    )


def test_futures_get_algo_order(futuresClient):
    """Test getting a specific algo order"""
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    # Create an algo order first
    order = futuresClient.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    algo_id = order["algoId"]
    # Get the order
    fetched_order = futuresClient.futures_get_algo_order(
        symbol=ticker["symbol"], algoId=algo_id
    )
    assert fetched_order["algoId"] == algo_id
    assert fetched_order["symbol"] == ticker["symbol"]
    # Clean up
    futuresClient.futures_cancel_algo_order(symbol=ticker["symbol"], algoId=algo_id)


def test_futures_get_order_with_conditional_param(futuresClient):
    """Test getting algo order using futures_get_order with conditional=True"""
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    # Create an algo order
    order = futuresClient.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    algo_id = order["algoId"]
    # Get the order using futures_get_order with conditional=True
    fetched_order = futuresClient.futures_get_order(
        symbol=ticker["symbol"], algoId=algo_id, conditional=True
    )
    assert fetched_order["algoId"] == algo_id
    # Clean up
    futuresClient.futures_cancel_algo_order(symbol=ticker["symbol"], algoId=algo_id)


def test_futures_get_all_algo_orders(futuresClient):
    """Test getting all algo orders history"""
    orders = futuresClient.futures_get_all_algo_orders(symbol="LTCUSDT")
    assert isinstance(orders, list)


def test_futures_get_all_orders_with_conditional_param(futuresClient):
    """Test getting all algo orders using futures_get_all_orders with conditional=True"""
    orders = futuresClient.futures_get_all_orders(symbol="LTCUSDT", conditional=True)
    assert isinstance(orders, list)


def test_futures_get_open_algo_orders(futuresClient):
    """Test getting open algo orders"""
    orders = futuresClient.futures_get_open_algo_orders(symbol="LTCUSDT")
    assert isinstance(orders, list)


def test_futures_get_open_orders_with_conditional_param(futuresClient):
    """Test getting open algo orders using futures_get_open_orders with conditional=True"""
    orders = futuresClient.futures_get_open_orders(symbol="LTCUSDT", conditional=True)
    assert isinstance(orders, list)


def test_futures_cancel_algo_order(futuresClient):
    """Test canceling an algo order"""
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    # Create an algo order
    order = futuresClient.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    algo_id = order["algoId"]
    # Cancel the order
    result = futuresClient.futures_cancel_algo_order(
        symbol=ticker["symbol"], algoId=algo_id
    )
    assert result["algoId"] == algo_id


def test_futures_cancel_order_with_conditional_param(futuresClient):
    """Test canceling algo order using futures_cancel_order with conditional=True"""
    ticker = futuresClient.futures_ticker(symbol="LTCUSDT")
    positions = futuresClient.futures_position_information(symbol="LTCUSDT")
    # Create an algo order
    order = futuresClient.futures_create_algo_order(
        symbol=ticker["symbol"],
        side="BUY",
        positionSide=positions[0]["positionSide"],
        type="STOP_MARKET",
        algoType="CONDITIONAL",
        quantity=1,
        triggerPrice=1000,
    )
    algo_id = order["algoId"]
    # Cancel using futures_cancel_order with conditional=True
    result = futuresClient.futures_cancel_order(
        symbol=ticker["symbol"], algoId=algo_id, conditional=True
    )
    assert result["algoId"] == algo_id


def test_futures_cancel_all_algo_open_orders(futuresClient):
    """Test canceling all open algo orders"""
    result = futuresClient.futures_cancel_all_algo_open_orders(symbol="LTCUSDT")
    # Should return success response
    assert "code" in result or "msg" in result


def test_futures_cancel_all_open_orders_with_conditional_param(futuresClient):
    """Test canceling all algo orders using futures_cancel_all_open_orders with conditional=True"""
    result = futuresClient.futures_cancel_all_open_orders(
        symbol="LTCUSDT", conditional=True
    )
    # Should return success response
    assert "code" in result or "msg" in result


from datetime import datetime

from binance.helpers2 import (
    clean_orders,
    trade_pairs,
    generate_pairs,
    generate_completed_trades,
)
import scenarios

data = [
    {
        "symbol": "BTCUSDT",
        "orderId": 196908059,
        "clientOrderId": "and_712cedf528214dcfbe5ef10905887d1e",
        "price": "4230.00000000",
        "origQty": "0.07404400",
        "executedQty": "0.07404400",
        "cummulativeQuoteQty": "313.20612000",
        "status": "FILLED",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "BUY",
        "stopPrice": "0.00000000",
        "icebergQty": "0.00000000",
        "time": 1543535910230,
        "updateTime": 1543538091949,
        "isWorking": True,
    },
    {
        "symbol": "BTCUSDT",
        "orderId": 197075082,
        "clientOrderId": "and_47c03ae8d8294111aef6e955a10410fd",
        "price": "4333.00000000",
        "origQty": "0.07350100",
        "executedQty": "0.00000000",
        "cummulativeQuoteQty": "0.00000000",
        "status": "CANCELED",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "side": "SELL",
        "stopPrice": "0.00000000",
        "icebergQty": "0.00000000",
        "time": 1543555555401,
        "updateTime": 1543557761829,
        "isWorking": True,
    },
]


def test_transform_date():
    result = clean_orders(data)
    assert result[0]["time"].year == 2018


def test_filter_data_by_date():
    result = clean_orders(
        data, _from=datetime(2018, 11, 30, 7), date_field="updateTime"
    )
    assert len(result) == 1
    assert result[0]["clientOrderId"] == "and_47c03ae8d8294111aef6e955a10410fd"
    result = clean_orders(data, _to=datetime(2018, 11, 30, 7), date_field="updateTime")
    assert len(result) == 1
    assert result[0]["clientOrderId"] == "and_712cedf528214dcfbe5ef10905887d1e"


def test_completed_trades():
    result = clean_orders(data, status="FILLED")
    assert len(result) == 1
    assert result[0]["clientOrderId"] == "and_712cedf528214dcfbe5ef10905887d1e"
    result = clean_orders(data, side="buy")
    assert len(result) == 1
    assert result[0]["clientOrderId"] == "and_712cedf528214dcfbe5ef10905887d1e"
    result = clean_orders(data, side="sell", status="filled")
    assert len(result) == 0
    result = clean_orders(data, side=["sell", "buy"])
    assert len(result) == 2
    result = clean_orders(data, side=["sell", "buy"], status=["filled"])
    assert len(result) == 1


def test_buy_and_sell_pair():
    result = clean_orders(data, status=["filled"])
    pairs = trade_pairs(result)
    assert pairs[0] == [4230]
    assert pairs[1] == []
    paris = trade_pairs(data)
    assert paris[0] == [4230]
    assert paris[1] == [4333]


def test_pair_trades():
    sample = [5200, 5300, 5200, 5250, 5230, 5300, 5220], [5250, 5270, 5280, 5240]
    for i in scenarios.sample_size:
        result = generate_pairs(*i["data"], _range=50)
        assert result[0] == sorted(i["result"][0])
        assert result[1][0] == sorted(i["result"][1][0])
        assert result[1][1] == sorted(i["result"][1][1])


# def test_determine_pending_and_completed_trades():
#     for i in scenarios.batches_with_different_rates:
#         result = generate_completed_trades(i["data"])
#         assert result == sorted(i["final_result"][0])
#         # import ipdb

#         # ipdb.set_trace()
#         # assert result[1] == i["final_result"][1]


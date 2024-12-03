import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from binance.client import Client


api_key = ""  # your api_key here
secret = ""  # your secret here
client = Client(api_key, secret, testnet=True)


# create oco order
def create_oco_order():
    order = client.create_oco_order(
        symbol="LTCUSDT",
        side="SELL",
        quantity=0.3,
        aboveType="LIMIT_MAKER",
        belowType="STOP_LOSS",
        abovePrice=200,
        belowStopPrice=120,
    )
    print(order)
    # {
    #     "orderListId": 9365,
    #     "contingencyType": "OCO",
    #     "listStatusType": "EXEC_STARTED",
    #     "listOrderStatus": "EXECUTING",
    #     "listClientOrderId": "x-HNA2TXFJa9965a63237a3621d3f9df",
    #     "transactionTime": 1733229295138,
    #     "symbol": "LTCUSDT",
    #     "orders": [
    #         {
    #             "symbol": "LTCUSDT",
    #             "orderId": 5836416,
    #             "clientOrderId": "MxXFhDAC8h13wH8X3rXNKG",
    #         },
    #         {
    #             "symbol": "LTCUSDT",
    #             "orderId": 5836417,
    #             "clientOrderId": "a2UltweB2UB1XOdUTqOrzw",
    #         },
    #     ],
    #     "orderReports": [
    #         {
    #             "symbol": "LTCUSDT",
    #             "orderId": 5836416,
    #             "orderListId": 9365,
    #             "clientOrderId": "MxXFhDAC8h13wH8X3rXNKG",
    #             "transactTime": 1733229295138,
    #             "price": "0.00000000",
    #             "origQty": "0.30000000",
    #             "executedQty": "0.00000000",
    #             "origQuoteOrderQty": "0.00000000",
    #             "cummulativeQuoteQty": "0.00000000",
    #             "status": "NEW",
    #             "timeInForce": "GTC",
    #             "type": "STOP_LOSS",
    #             "side": "SELL",
    #             "stopPrice": "120.00000000",
    #             "workingTime": -1,
    #             "selfTradePreventionMode": "EXPIRE_MAKER",
    #         },
    #         {
    #             "symbol": "LTCUSDT",
    #             "orderId": 5836417,
    #             "orderListId": 9365,
    #             "clientOrderId": "a2UltweB2UB1XOdUTqOrzw",
    #             "transactTime": 1733229295138,
    #             "price": "200.00000000",
    #             "origQty": "0.30000000",
    #             "executedQty": "0.00000000",
    #             "origQuoteOrderQty": "0.00000000",
    #             "cummulativeQuoteQty": "0.00000000",
    #             "status": "NEW",
    #             "timeInForce": "GTC",
    #             "type": "LIMIT_MAKER",
    #             "side": "SELL",
    #             "workingTime": 1733229295138,
    #             "selfTradePreventionMode": "EXPIRE_MAKER",
    #         },
    #     ],
    # }


def main():
    create_oco_order()

main()

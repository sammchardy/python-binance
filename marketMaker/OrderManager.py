from collections import defaultdict
from enum import Enum

from binance.client import Client
from binance.exceptions import BinanceAPIException

class Action(Enum):
    NOACTION = 0
    BUY = 1
    SELL = 2
    BUYTOCOVER = 3
    SELLTOCOVER = 4


class OrderManager:
    def __init__(self, tc: Client):
        self.syms = set(['ETH', 'BTC', 'USD', 'BNB'])
        self.openOrders = defaultdict(lambda: defaultdict(dict))
        self.openPos = defaultdict(lambda: defaultdict(float))
        self.tc = tc
        self.status = defaultdict(lambda: defaultdict(float))

    def getOpenPosition(self, sym):
        return self.openPos.get(sym, 0.0)

    def processOrderUpdate(self, msg):
        thissym = msg['s']
        side = Action[msg['S']]

        if msg['x'] == 'NEW':
            self.openOrders[thissym][side][msg['i']] = msg
            self.openPos[thissym][side] += float(msg['q'])

        if msg['x'] in ['FILLED', 'EXPIRED', 'CANCELED'] and msg['i'] in self.openOrders[thissym][side]:
            self.openPos[thissym][side] -= float(msg['q'])
            self.openOrders[thissym][side].pop(msg['i'])
        return

    def cancelAllOrder(self, sym):
        self.cancelOrder(Action.BUY, sym)
        self.cancelOrder(Action.SELL, sym)

    def cancelOrder(self, side, sym):
        ordersToCancel = list(self.openOrders[sym][side])
        for orderId in ordersToCancel:
            try:
                self.tc.cancel_order(symbol=sym, orderId=orderId, recvWindow=20000)
            except BinanceAPIException as e:
                if e.code == -2011: # order track lost
                    print("Order lost track")
                continue




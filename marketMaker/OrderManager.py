from enum import Enum
from binance.client import Client


class Action(Enum):
        NOACTION = 0
        BUY = 1
        SELL = 2
        BUYTOCOVER = 3
        SELLTOCOVER = 4


class OrderManager:
    def __init__(self, tc: Client ):
        self.syms = set(['ETH','BTC','USD','BNB'])
        self.openOrders = {}
        self.openPos = {}
        self.tc = tc

    def getOpenPosition(self, sym):
        return self.openPos.get(sym, 0.0)


    def processOrderUpdate(self, msg):
        thissym = msg['s']
        side = Action[msg['S']]

        if not thissym in self.openOrders:
            self.openOrders[thissym] = {}
        if not side in self.openOrders[thissym]:
            self.openOrders[thissym][side] = {}

        if not thissym in self.openPos:
            self.openPos[thissym] = {}
        if not side in self.openPos[thissym]:
            self.openPos[thissym][side] = 0


        if msg['x'] == 'NEW':
            self.openOrders[thissym][side][msg['i']] = msg
            self.openPos[thissym][side] += float(msg['q'])


        if msg['x'] in ['FILLED','EXPIRED','CANCELED'] and msg['i'] in self.openOrders[thissym][side]:
            self.openPos[thissym][side] -= float(msg['q'])
            self.openOrders[thissym][side].pop(msg['i'])
        return



    def cancelAllOrder(self, sym):
        self.cancelOrder(Action.BUY, sym)
        self.cancelOrder(Action.SELL, sym)

    def cancelOrder(self, side , sym):
        if ( not sym in self.openOrders ) or ( not side in self.openOrders[sym]):
            return # nothing to cancel
        ordersToCancel = list(self.openOrders[sym][side])
        for orderId in ordersToCancel:
            self.tc.cancel_order(symbol=sym, orderId = orderId, recvWindow = 2000)








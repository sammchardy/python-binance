from enum import Enum



class Action(Enum):
        NOACTION = 0
        BUY = 1
        SELL = 2
        BUYTOCOVER = 3
        SELLTOCOVER = 4


class OrderManager:
    def __init__(self):
        self.syms = set(['ETH','BTC','USD','BNB'])
        self.openOrders = {}
        self.openPos = {}

    def getOpenPosition(self, sym):
        return self.openpos.get(sym, 0.0)


    def processOrderUpdate(self, msg):
        thissym = msg['s']
        side = msg['S']

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





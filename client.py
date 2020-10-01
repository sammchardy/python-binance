import time
from marketMaker.OrderManager import *
import pandas as pd

from binance.client import Client
from binance.websockets import BinanceSocketManager
from marketMaker.PortfolioManager import  *
import zmq
import json
from datetime import datetime
from util import *

class Signal:

    def __init__(self):
        self.seqNum = 0
        self.action = Action.NOACTION
        self.signalPrice = 0.0

    def update(self, action, price):
        self.action = action
        self.seqNum += 1
        self.price = price

signal = Signal()


def order_handling():
    lastSeqNum = -1
    while True:
        if lastSeqNum < signal.seqNum:
            lastSeqNum = signal.seqNum
            if signal.action == Action.NOACTION:
                continue
            if signal.action == Action.BUY:
                if pm.getPosition('BNB') >= 1.0:
                    continue








keys = pd.read_csv('./tradingkey.csv')
print(keys)
print(keys['key'][0],keys['key'][1])

context = zmq.Context()
client = context.socket(zmq.SUB)
client.connect(connEndPoint)
client.setsockopt_string(zmq.SUBSCRIBE, connTopic)

tc = Client(keys['key'][0], keys['key'][1],tld = 'us')

pm = PortfolioManager()
bm = BinanceSocketManager(tc)
om = OrderManager()

def processmymsg(msg: dict):
    print(msg)
    if msg.get('e','') == 'outboundAccountPosition':
        pm.processPositionUpdate(msg)
        return
    if msg.get('e','') == 'executionReport':
        om.processOrderUpdate(msg)
        return
    return



bm.start_user_socket(processmymsg)
bm.start()

time.sleep(3)




#tc.order_limit_buy(symbol='BNBUSD', quantity = 0.5, price = 22,recvWindow=10000)

print("step3")



print("step1")

#tc.order_limit_sell(symbol='BNBUSD', quantity = 0.5, price = 40, recvWindow=10000)

print("step2")

import numpy as np

class ewma:
    def __init__(self, period):
        self.value = 0.0
        self.decay = np.exp(-1. / period)
        self.init = 1
    
    def update(self, cv):
        self.value = self.value * self.decay + (1-self.decay) * cv + self.init * self.decay * cv
        self.init = 0

class LastTradeManager:
    def __init__(self):
        self.lt = {}
    def update(self, symbol, value):
        self.lt[symbol] = value
    def get(self, symbol):
        return self.lt[symbol]

class EwmaManager:
    def __init__(self):
        self.ewmapool = {}
    def register(self, symbol, period):
        self.ewmapool.setdefault(symbol,{})
        self.ewmapool[symbol].setdefault(period, ewma(period))
        
    def updateSymbol(self, symbol, period,value):
        try:
          self.ewmapool[symbol][period].update(value)
        except:
          print("not found ")

    def updateSymbolAll(self, symbol,value):
        #try:
          for ema in self.ewmapool[symbol]:
            self.ewmapool[symbol][ema].update(value)
        #except:
         # print("not found ")
    def getValue(self, symbol):
        return [(x, self.ewmapool[symbol][x].value) for x in self.ewmapool[symbol]]

    def getValue(self, symbol, period):
        return self.ewmapool[symbol][period].value

ewmaManager = EwmaManager()
ewmaManager.register('ETHUSDT',100)
ewmaManager.register('ETHUSDT',500)
ewmaManager.register('ETHUSDT',500)
ewmaManager.register('ETHUSDT',1000)

ewmaManager.register('BTCUSDT',100)
ewmaManager.register('BTCUSDT',500)
ewmaManager.register('BNBUSDT',100)
ewmaManager.register('BNBUSDT',1000)

ewmaManager.register('BNBUSDT',500)
ewmaManager.register('LTCUSDT',1)


#time.sleep(10000);



print(ewmaManager.ewmapool)
lastTradeManager = LastTradeManager();
print(tc.get_account_status())
print(tc.get_asset_details())
pos = tc.get_asset_balance(asset='BNB')
pm.positions['BNB'] = float(pos['free'])+float(pos['locked'])

def aftertrade():
    print("trade")


def getReturn(symbol, period):
    return np.log(lastTradeManager.get(symbol)/ewmaManager.getValue(symbol,period))

print(tc.get_asset_balance(asset='ETH',recvWindow=10000))
print(tc.get_account_status(recvWindow=10000))
noExistingOrder = True
lastorder = {}
while True:
    # Thanks @seym45 for a fix    
    try:
        str = client.recv_string()
        _, data = str.split(connTopic)
        res = json.loads(data)
    except zmq.ZMQError as error:
        print(error)
        continue
    
    if 'T' in res.keys():
        updateTime = datetime.fromtimestamp(res['T']/1000)
        if updateTime.second == 0:
            print("updateTime:", updateTime) #prints periodly

  #  print(res.keys())
    if 'p' in res.keys():
        lastTradeManager.update(res['s'], float(res['p']))
        #print('lasttrade', res['s'])
     #   print(lastTradeManager.lt)
  #        print(res['s'], res['p'], ewmaManager.getValue(res['s']))
    else:
        try:
  #          print(res['bids'][0])
            ewmaManager.updateSymbolAll('ETHUSDT', lastTradeManager.get('ETHUSDT'))
 #           print(ewmaManager.getValue('ETHUSDT'))
 #           print(ewmaManager.getValue('BNBUSDT'))
            bid = float(res['bids'][0][0])
            ask = float(res['asks'][0][0])
            smid = 0.5*(bid+ask)
            ewmaManager.updateSymbolAll('BNBUSDT', smid)


            print('{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}'.format(bid,ask, smid,getReturn('ETHUSDT',100)*100, getReturn('ETHUSDT',500)*100, getReturn('BNBUSDT',100)*100, getReturn('BNBUSDT',500)*100))
            signal = 100*(0.008*getReturn('BNBUSDT',100) - 0.2863*getReturn('BNBUSDT',500)-0.0177*getReturn('BNBUSDT',1000)
                  -0.3832*getReturn('ETHUSDT',100) + 0.9956*getReturn('ETHUSDT',500)-0.4885*getReturn('ETHUSDT',1000))
            print('{:.2f}'.format(signal))

            if  pm.getPosition('BNB') < 4:
             #   print(tc.get_asset_balance('BNB'))
                mybid = bid - 0.05
                om.cancelOrder(Action.BUY, 'BNBUSD')
                tc.order_limit_buy(symbol='BNBUSD', price = mybid, quantity=1.0, recvWindow=10000)

            if  pm.getPosition('BNB') > 10.0:
                myask = ask + 0.2
                om.cancelOrder(Action.SELL,'BNBUSD')
                tc.order_limit_sell(symbol = 'BNBUSD', price = myask, quantity = 1.0, recvWindow = 10000)

            prevbid = bid
            prevask = ask

        except Exception as e:
            print(e)
            pass

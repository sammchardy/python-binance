import socket
import pickle
from datetime import timezone, datetime
import binance
from binance.client import Client
from binance.websockets import BinanceSocketManager

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


api_key = '94V1LhT5WYbX8c991G5BWufZn0xLaIgA1qovZPScuXbisVNnqSCnV3qvkcscDG4I';
api_secret = 'Rbjo7QGS4Wnt3wFdygLcPaCqlRin3iGwAtxybVNRsb7NJyDZyR4QuAomgCeNddnc';
tc = Client(api_key, api_secret,tld = 'us')

bm = BinanceSocketManager(tc)
def processmymsg(msg):
    print(msg)

print(bm.start_user_socket(processmymsg))
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
print(ewmaManager.ewmapool)
lastTradeManager = LastTradeManager();
def getReturn(symbol, period):
    return np.log(lastTradeManager.get(symbol)/ewmaManager.getValue(symbol,period))

client.bind(("", 37020))
print(tc.get_asset_balance(asset='ETH',recvWindow=10000))
print(tc.get_account_status(recvWindow=10000))
noExistingOrder = True
while True:
    # Thanks @seym45 for a fix
    data, addr = client.recvfrom(1024)
    res = pickle.loads(data)
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
            if signal > -0.80 and noExistingOrder:
             #   print(tc.get_asset_balance('BNB'))
                print(tc.order_limit_buy(symbol='BNBUSD', quantity=1.0, price=10.0, recvWindow=10000))

                noExistingOrder = False

        except Exception as e:
            print(str(e))
            pass


    #print(type(res))
    
    #print(int(datetime.now(tz=timezone.utc).timestamp() * 1000))

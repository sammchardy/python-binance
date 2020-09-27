import binance
from binance.client import Client
import pickle

api_key = '94V1LhT5WYbX8c991G5BWufZn0xLaIgA1qovZPScuXbisVNnqSCnV3qvkcscDG4I';
api_secret = 'Rbjo7QGS4Wnt3wFdygLcPaCqlRin3iGwAtxybVNRsb7NJyDZyR4QuAomgCeNddnc';
client = Client(api_key, api_secret,tld = 'us')
#print(client.get_all_tickers())
#print(client.order_limit_buy(symbol='ETHUSD',price=130.0,quantity=0.1, newClientOrderId = 'ADASFDS'))
#print(client.get_open_orders())
#for order in client.get_open_orders():
#    print(order['orderId'])
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


def parseMsg(msg):
    print(msg.split(','))

client.bind(("", 37020))
while True:
    # Thanks @seym45 for a fix
    data, addr = client.recvfrom(1024)
    res = pickle.loads(data)
    if res['s'] == 'ETHUSDT':
        print(res['p'],res['q'])
#    if(res['s'])
#        print()
#    parseMsg(str(data))

#try:
#    print(client.cancel_order(symbol = 'ETHUSD', origClientOrderId = 'ADASFDS'))
#except  binance.exceptions.BinanceAPIException as e:
#    print(e)
#    client.
#client.create_test_order()
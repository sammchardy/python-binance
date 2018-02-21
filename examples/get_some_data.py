import os

from binance.client import Client
import certifi

from twisted.internet import defer, reactor

# make sure your cert is verifiable
os.environ['SSL_CERT_FILE'] = certifi.where()

client = Client("", "")
print client


@defer.inlineCallbacks
def main():
    try:
        # get market depth
        depth = yield client.get_order_book(symbol='BNBBTC')
        print 'depth', depth
    except Exception as e:
        print e

    reactor.stop()



# call this function when running
reactor.callWhenRunning(main)

# run the event loop
reactor.run()

#!/usr/bin/env python3

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

import logging
from binance.ws.depthcache import ThreadedDepthCacheManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
        dcm = ThreadedDepthCacheManager()
        dcm.start()
        
        def handle_depth_cache(depth_cache):
            if isinstance(depth_cache, dict) and depth_cache.get('e') == 'error':
                logger.error(f"Received depth cache error in callback: {depth_cache}")
                type = depth_cache.get('type')
                if type == 'BinanceWebsocketClosed':
                    # Automatically attempts to reconnect
                    return
                logger.error(f"Error received - Closing depth cache: {depth_cache}")
                dcm.stop()
                return
                 
            logger.info(f"symbol {depth_cache.symbol}")
            logger.info(depth_cache.get_bids()[:5])
            
        dcm.start_depth_cache(handle_depth_cache, symbol='BNBBTC')
        dcm.join()


if __name__ == "__main__":
   main()

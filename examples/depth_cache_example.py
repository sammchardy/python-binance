#!/usr/bin/env python3

import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

import asyncio
import logging
from binance import AsyncClient
from binance.ws.depthcache import DepthCacheManager 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def main():
    # Initialize the client
    client = await AsyncClient.create()

    # Symbol to monitor
    symbol = 'BTCUSDT'
    
    # Create a depth cache manager instance
    async with DepthCacheManager(
        client=client,
        symbol=symbol,
    ) as dcm:
        logger.info(f"Started depth cache for {symbol}")
        
        # Monitor depth cache updates for 1 minute
        for _ in range(100):  # 6 iterations * 10 seconds = 1 minute
            depth_cache = await dcm.recv()
            if isinstance(depth_cache, dict) and depth_cache.get('e') == 'error':
                logger.error(f"Received depth cache error in callback: {depth_cache}")
                if type == 'BinanceWebsocketClosed':
                    # ignore as attempts to reconnect
                    continue
                break
            
            # Get current bids and asks
            bids = depth_cache.get_bids()[:5]  # Top 5 bids
            asks = depth_cache.get_asks()[:5]  # Top 5 asks
            
            logger.info("Top 5 bids:")
            for bid in bids:
                logger.info(f"Price: {bid[0]}, Quantity: {bid[1]}")
            
            logger.info("Top 5 asks:")
            for ask in asks:
                logger.info(f"Price: {ask[0]}, Quantity: {ask[1]}")
            
            logger.info(f"Last update time: {depth_cache.update_time}")
                
    # Close the client
    await client.close_connection()

if __name__ == '__main__':
    # Run the async example
    asyncio.run(main())

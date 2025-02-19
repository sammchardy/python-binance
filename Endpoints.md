> :warning: **Disclaimer**: 

 > * Before using the endpoints, please check the [API documentation](https://binance-docs.github.io/apidocs/#change-log) to be informed about the latest changes or possible bugs/problems. 

 > * Not all parameters are mandatory. Some parameters are only mandatory in specific conditions/types. Check the official documentation the type of each parameter and to know if a parameter is mandatory or optional. 

 > * This documentation only includes methods in client.py file. Websocket methods haven't (yet) been covered.
 
### [Spot/Margin/Saving/Mining Endpoints](https://binance-docs.github.io/apidocs/spot/en/)
- *Wallet Endpoints*
  - **GET /sapi/v1/system/status** (Fetch system status.)
    ```python 
    client.get_system_status()
    ```
  - **GET /sapi/v1/capital/config/getall (HMAC SHA256)** (Get information of coins (available for deposit and withdraw) for user.)
    ```python 
    client.get_all_coins_info()
    ```
  - **GET /sapi/v1/accountSnapshot (HMAC SHA256)** (Daily Account Snapshot (USER_DATA).)
    ```python 
    client.get_account_snapshot(type='SPOT')
    ```
  - **POST /sapi/v1/account/disableFastWithdrawSwitch (HMAC SHA256)** (Disable Fast Withdraw Switch (USER_DATA).)
    ```python 
    client.disable_fast_withdraw_switch(type='SPOT')
    ``` 
  - **POST /sapi/v1/account/enableFastWithdrawSwitch (HMAC SHA256)** (Enable Fast Withdraw Switch (USER_DATA).)
    ```python 
    client.enable_fast_withdraw_switch(type='SPOT')
    ```
  - **POST /sapi/v1/capital/withdraw/apply (HMAC SHA256)** (Withdraw: Submit a withdraw request.)
    ```python 
    client.withdraw(coin, 
        withdrawOrderId, 
        network, 
        address, 
        addressTag, 
        amount, 
        transactionFeeFlag, 
        name, 
        recvWindow)
    ```
  - **GET /sapi/v1/capital/deposit/hisrec (HMAC SHA256)** (Fetch Deposit History(supporting network) (USER_DATA).)
    ```python 
    client.get_deposit_history(coin, status, startTime, endTime, recvWindow)
    ```
  - **GET /sapi/v1/capital/withdraw/history (HMAC SHA256)** (Fetch Withdraw History (supporting network) (USER_DATA).)
    ```python 
    client.get_withdraw_history(coin, status, startTime, endTime, recvWindow)
    ```
  - **GET /sapi/v1/capital/deposit/address (HMAC SHA256)** (Fetch deposit address with network.)
    ```python 
    client.get_deposit_address(coin, status, recvWindow)
    ```
  - **GET /sapi/v1/account/status** (Fetch account status detail.)
    ```python 
    client.get_account_status(recvWindow)
    ```
  - **GET /sapi/account/apiTradingStatus** (Fetch account api trading status detail.)
    ```python 
    client.get_account_api_trading_status(recvWindow)
    ```
  - **GET /sapi/v1/asset/dribblet (HMAC SHA256)** (DustLog: Fetch small amounts of assets exchanged BNB records.)
    ```python 
    client.get_dust_log(recvWindow)
    ```
  - **Post /sapi/v1/asset/dust (HMAC SHA256)** (Dust Transfer: Convert dust assets to BNB.)
    ```python 
    client.transfer_dust(asset, recvWindow)
    ```
  - **Get /sapi/v1/asset/assetDividend (HMAC SHA256)** (Query asset dividend record.)
    ```python 
    client.get_asset_dividend_history(asset, startTime, endTime, limit, recvWindow)
    ```
  - **GET /sapi/v1/asset/assetDetail (HMAC SHA256)** (Fetch details of assets supported on Binance.)
    ```python 
    client.get_asset_details(recvWindow)
    ```
  - **GET /sapi/v1/asset/tradeFee (HMAC SHA256)** (Fetch trade fee, values in percentage.)
    ```python 
    client.get_trade_fee(symbol, recvWindow)
    ```
- *Market Data Endpoints*
  - **GET /api/v3/ping** (Test connectivity to the Rest API.)
    ```python 
    client.ping()
    ```
  - **GET /api/v3/time** (Test connectivity to the Rest API and get the current server time.)
    ```python 
    client.get_server_time()
    ```
  - **GET /api/v3/exchangeInfo** (Current exchange trading rules and symbol information.)
    ```python 
    client.get_exchange_info()
    ```
  - **GET /api/v3/depth** (Get the Order Book for the market.)
    ```python 
    client.get_order_book(symbol, limit)
    ```
  - **GET /api/v3/trades** (Get recent trades (up to last 500))
    ```python 
    client.get_recent_trades(symbol, limit)
    ```
  - **GET /api/v3/historicalTrades** (Get older market trades.)
    ```python 
    client.get_historical_trades(symbol, limit, fromId)
    ``` 
  - **GET /api/v3/aggTrades** (Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.)
    ```python 
    client.get_aggregate_trades(symbol, fromId, startTime, endTime, limit)
    
    # Wrapper function: Iterate over aggregate trade data from (start_time or last_id) the end of the history so far:
    client.aggregate_trade_iter(symbol, start_str, last_id)
    ```
  - **GET /api/v3/klines** (Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.)
    ```python 
    client.get_klines(symbol, interval, startTime, endTime, limit)
    
    # Wrapper function: Iterate over klines data from client.get_klines()
    client.get_historical_klines(symbol, interval, start_str, end_str, limit)
    ```
  - **GET /api/v3/avgPrice** (Current average price for a symbol.)
    ```python 
    client.get_avg_price(symbol)
    ```
  - **GET /api/v3/ticker/24hr** (24 hour rolling window price change statistics. **Careful** when accessing this with no symbol.)
    ```python 
    client.get_ticker(symbol)
    ```
  - **GET /api/v3/ticker/price** (Latest price for a symbol or symbols.)
    ```python 
    client.get_symbol_ticker(symbol)
    ```
  - **GET /api/v3/ticker/bookTicker** (Best price/qty on the order book for a symbol or symbols.)
    ```python 
    client.get_orderbook_ticker(symbol)
    ```
- *Spot Account/Trade Endpoints*
  - **POST /api/v3/order/test (HMAC SHA256)** (Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.)
    ```python 
    client.create_test_order(symbol, 
        side, 
        type, 
        timeInForce, 
        quantity, 
        quoteOrderQty, 
        price, 
        newClientOrderId, 
        stopPrice, 
        icebergQty, 
        newOrderRespType, 
        recvWindow)
    ```
  - **POST /api/v3/order (HMAC SHA256)** (Send in a new order.)
    ```python 
    client.create_order(symbol, 
        side, 
        type, 
        timeInForce, 
        quantity, 
        quoteOrderQty, 
        price, 
        newClientOrderId, 
        stopPrice, 
        icebergQty, 
        newOrderRespType, 
        recvWindow)
        
    ## Wrapper functions:
    # Send in a new limit order. 
    # Default parameters: timeInForce=Client.TIME_IN_FORCE_GTC, type=Client.ORDER_TYPE_LIMIT
    client.order_limit(symbol, 
        side,
        quantity, 
        price, 
        newClientOrderId, 
        stopPrice, 
        icebergQty, 
        newOrderRespType, 
        recvWindow)
    
    # Send in a new limit buy order. 
    # Default parameters: timeInForce=Client.TIME_IN_FORCE_GTC, type=Client.ORDER_TYPE_LIMIT, side=Client.SIDE_BUY
    client.order_limit_buy(symbol, 
        quantity, 
        price, 
        newClientOrderId, 
        stopPrice, 
        icebergQty, 
        newOrderRespType, 
        recvWindow) 
    
    # Send in a new limit sell order. 
    # Default parameters: timeInForce=Client.TIME_IN_FORCE_GTC, type=Client.ORDER_TYPE_LIMIT, side= Client.SIDE_SELL
    client.order_limit_sell(symbol, 
        quantity, 
        price, 
        newClientOrderId, 
        stopPrice, 
        icebergQty, 
        newOrderRespType, 
        recvWindow)
        
    # Send in a new market order. 
    # Default parameters: type=Client.ORDER_TYPE_MARKET
    client.order_market(symbol, 
        side, 
        quantity, 
        quoteOrderQty, 
        newClientOrderId, 
        newOrderRespType, 
        recvWindow)
        
    # Send in a new market buy order. 
    # Default parameters: type=Client.ORDER_TYPE_MARKET, side=Client.SIDE_BUY
    client.order_market_buy(symbol, 
        quantity, 
        quoteOrderQty, 
        newClientOrderId, 
        newOrderRespType, 
        recvWindow)
    
    # Send in a new market sell order. 
    # Default parameters: type=Client.ORDER_TYPE_MARKET, side=Client.SIDE_SELL
    client.order_market_sell(symbol, 
        quantity, 
        quoteOrderQty, 
        newClientOrderId, 
        newOrderRespType, 
        recvWindow)
    ```
  - **DELETE /api/v3/order (HMAC SHA256)** (Cancel an active order.)
    ```python 
    client.cancel_order(symbol, orderId, origClientOrderId, newClientOrderId, recvWindow)
    ```
  - **DELETE api/v3/openOrders** (Cancels all active orders on a symbol. This includes OCO orders.)
  
    > :warning: Not yet implemented
  - **GET /api/v3/order (HMAC SHA256)** (Check an order's status.)
    ```python 
    client.get_order(symbol, orderId, origClientOrderId, recvWindow)
    ```
  - **GET /api/v3/openOrders (HMAC SHA256)** (Get all open orders on a symbol. **Careful** when accessing this with no symbol.)
    ```python 
    client.get_open_orders(symbol, recvWindow)
    ```
  - **GET /api/v3/allOrders (HMAC SHA256)** (Get all account orders; active, canceled, or filled.)
    ```python 
    client.get_all_orders(symbol, orderId, startTime, endTime, limit, recvWindow)
    ```
  - **POST /api/v3/order/oco (HMAC SHA256)** (Send in a new OCO order)
    ```python 
    client.create_oco_order(symbol, 
        listClientOrderId, 
        side, 
        quantity, 
        limitClientOrderId, 
        price, 
        limitIcebergQty, 
        stopClientOrderId, 
        stopPrice, 
        stopLimitPrice, 
        stopIcebergQty, 
        stopLimitTimeInForce, 
        newOrderRespType, 
        recvWindow)
    
    ## Wrapper Functions:
    
    # Send in a new OCO buy order. Default parameter: type=Client.SIDE_BUY
    client.order_oco_buy(symbol, 
        listClientOrderId, 
        quantity, 
        limitClientOrderId, 
        price, 
        limitIcebergQty, 
        stopClientOrderId, 
        stopPrice, 
        stopLimitPrice, 
        stopIcebergQty, 
        stopLimitTimeInForce, 
        newOrderRespType, 
        recvWindow)
        
    # Send in a new OCO sell order. Default parameter: type=Client.SIDE_SELL
    client.order_oco_sell(symbol, 
        listClientOrderId, 
        quantity, 
        limitClientOrderId, 
        price, 
        limitIcebergQty, 
        stopClientOrderId, 
        stopPrice, 
        stopLimitPrice, 
        stopIcebergQty, 
        stopLimitTimeInForce, 
        newOrderRespType, 
        recvWindow)
    ```
  - **DELETE /api/v3/orderList (HMAC SHA256)** (Cancel OCO: Cancel an entire Order List)
   
    > :warning: Not yet implemented
  - **GET /api/v3/orderList (HMAC SHA256)** (Query OCO: Retrieves a specific OCO based on provided optional parameters)
  
    > :warning: Not yet implemented
  - **GET /api/v3/allOrderList (HMAC SHA256)** (Retrieves all OCO based on provided optional parameters)
  
    > :warning: Not yet implemented
  - **GET /api/v3/openOrderList (HMAC SHA256)** (Query Open OCO (USER_DATA))
  
    > :warning: Not yet implemented
  - **GET /api/v3/account (HMAC SHA256)** (Get current account information.)
    ```python 
    client.get_account(recvWindow)
    ```
  - **GET /api/v3/myTrades (HMAC SHA256)** (Get trades for a specific account and symbol.)
    ```python 
    client.get_my_trades(symbol, startTime, endTime, fromId, limit, recvWindow)
    ```
- *Margin Account/Trade*
  - **POST /sapi/v1/margin/transfer (HMAC SHA256)** (Execute transfer between margin account and spot account(MARGIN).)
    ```python 
    client.transfer_margin_to_spot(asset, amount, recvWindow)
    client.transfer_spot_to_margin(asset, amount, recvWindow)
    ```
  - **POST /sapi/v1/margin/loan (HMAC SHA256)** (Apply for a loan(MARGIN).)
    ```python 
    client.create_margin_loan(asset, isIsolated, symbol, amount, recvWindow)
    ```
  - **POST /sapi/v1/margin/repay (HMAC SHA256)** (Repay loan for margin account (MARGIN).)
    ```python 
    client.repay_margin_loan(asset, isIsolated, symbol, amount, recvWindow)
    ```
  - **GET /sapi/v1/margin/asset** (Query Margin Asset (MARKET_DATA).)
    ```python 
    client.get_margin_asset(asset)
    ```
  - **GET /sapi/v1/margin/pair** (Query Cross Margin Pair (MARKET_DATA).)
    ```python 
    client.get_margin_symbol(symbol)
    ```
  - **GET /sapi/v1/margin/allAssets** (Get All Cross Margin Assets (MARKET_DATA).)
    ```python 
    client.get_margin_all_assets()
    ```
  - **GET /sapi/v1/margin/allPairs** (Get All Cross Margin Pairs (MARKET_DATA).)
    ```python 
    client.get_margin_all_pairs()
    ```
  - **GET /sapi/v1/margin/priceIndex** (Query Margin PriceIndex (MARKET_DATA).)
    ```python 
    client.get_margin_price_index(symbol)
    ```
  - **POST /sapi/v1/margin/order (HMAC SHA256)** (Post a new order for margin account.)
    ```python 
    client.create_margin_order(symbol,
        isIsolated,
        side, 
        type, 
        quantity, 
        price, 
        stopPrice, 
        newClientOrderId,
        icebergQty,
        newOrderRespType,
        sideEffectType,
        timeInForce, 
        recvWindow)
    ```
  - **DELETE /sapi/v1/margin/order (HMAC SHA256)** (Cancel an active order for margin account.)
    ```python 
    client.cancel_margin_order(symbol, 
        isIsolated, 
        orderId, 
        origClientOrderId, 
        newClientOrderId, 
        recvWindow)
    ```
  - **GET /sapi/v1/margin/transfer (HMAC SHA256)** (Get Cross Margin Transfer History (USER_DATA).)
    ```python 
    client.transfer_margin_to_spot(asset, amount, recvWindow)
    client.transfer_spot_to_margin(asset, amount, recvWindow)
    ```
  - **GET /sapi/v1/margin/loan (HMAC SHA256)** (Query Loan Record (USER_DATA).)
    ```python 
    client.get_margin_loan_details(asset, isolatedSymbol, txId, startTime, endTime, current, size, recvWindow)
    ```
  - **GET /sapi/v1/margin/repay (HMAC SHA256)** (Query repay record (USER_DATA).)
    ```python 
    client.get_margin_repay_details(asset, isolatedSymbol, txId, startTime, endTime, current, size, recvWindow)
    ```
  - **GET /sapi/v1/margin/interestHistory (HMAC SHA256)** (Get Interest History (USER_DATA).)
    ```python 
    client.get_margin_interest_history(asset, isolatedSymbol, startTime, endTime, current, size, archived, recvWindow)
    ```
  - **GET /sapi/v1/margin/forceLiquidationRec (HMAC SHA256)** (Get Force Liquidation Record (USER_DATA).)
    ```python 
    client.get_margin_force_liquidation_rec(isolatedSymbol, startTime, endTime, current, size, recvWindow)
    ```
  - **GET /sapi/v1/margin/account (HMAC SHA256)** (Query Cross Margin Account Details (USER_DATA).)
    ```python 
    client.get_margin_account(recvWindow)
    ```
  - **GET /sapi/v1/margin/order (HMAC SHA256)** (Query Margin Account's Order (USER_DATA).)
    ```python 
    client.get_margin_order(symbol, isIsolated, orderId, origClientOrderId, recvWindow)
    ```
  - **GET /sapi/v1/margin/openOrders (HMAC SHA256)** (Query Margin Account's Open Order (USER_DATA).)
    ```python 
    client.get_open_margin_orders(symbol, isIsolated, recvWindow)
    ```
  - **GET /sapi/v1/margin/allOrders (HMAC SHA256)** (Query Margin Account's All Order (USER_DATA).)
    ```python 
    client.get_all_margin_orders(symbol, isIsolated, orderId, startTime, endTime, limit, recvWindow)
    ```
  - **GET /sapi/v1/margin/myTrades (HMAC SHA256)** (Query Margin Account's Trade List (USER_DATA).)
    ```python 
    client.get_margin_trades(symbol, isIsolated, startTime, endTime, fromId, limit, recvWindow)
    ```
  - **GET /sapi/v1/margin/maxBorrowable (HMAC SHA256)** (Query Max Borrow amount for an asset (USER_DATA).)
    ```python 
    client.get_max_margin_loan(asset, isolatedSymbol, recvWindow)
    ```
  - **GET /sapi/v1/margin/maxTransferable (HMAC SHA256)** (Query Max Transfer-Out Amount (USER_DATA).)
    ```python 
    client.get_max_margin_transfer(asset, isolatedSymbol, recvWindow)
    ```
  - **POST /sapi/v1/margin/isolated/create (HMAC SHA256)** (Create Isolated Margin Account (MARGIN).)
    ```python 
    client.create_isolated_margin_account(base, quote, recvWindow)
    ```
  - **POST /sapi/v1/margin/isolated/transfer (HMAC SHA256)** (Isolated Margin Account Transfer (MARGIN).)
    ```python 
    client.transfer_spot_to_isolated_margin(asset, symbol, amount, recvWindow)
    client.transfer_isolated_margin_to_spot(asset, symbol, amount, recvWindow)
    ```
  - **GET /sapi/v1/margin/isolated/transfer (HMAC SHA256)** (Get Isolated Margin Transfer History (USER_DATA).)
  
    > :warning: Not yet implemented
  - **GET /sapi/v1/margin/isolated/account (HMAC SHA256)** (Query Isolated Margin Account Info (USER_DATA).)
    ```python 
    client.get_isolated_margin_account(symbols, recvWindow)
    ```
  - **GET /sapi/v1/margin/isolated/pair (HMAC SHA256)** (Query Isolated Margin Symbol (USER_DATA).)
    ```python 
    client.get_isolated_margin_symbol(symbol, recvWindow)
    ```
  - **GET /sapi/v1/margin/isolated/allPairs (HMAC SHA256)** (Get All Isolated Margin Symbol (USER_DATA).)
    ```python 
    client.get_all_isolated_margin_symbols(recvWindow)
    ```
  - **POST /sapi/v1/margin/manual-liquidation (HMAC SHA256)** (Margin manual liquidation (MARGIN).)
    ```python 
    client.margin_manual_liquidation(type)
    ```
- *User Data Streams*
  - **POST /api/v3/userDataStream** (Create a ListenKey (Spot) (USER_STREAM): Start a new user data stream.)
    ```python 
    client.stream_get_listen_key()
    ```
  - **PUT /api/v3/userDataStream** (Ping/Keep-alive a ListenKey (Spot) (USER_STREAM).)
    ```python 
    client.stream_keepalive(listenKey)
    ```
  - **DELETE /api/v3/userDataStream** (Close a ListenKey (Spot) (USER_STREAM).)
    ```python 
    client.stream_close(listenKey)
    ```
  - **POST /sapi/v1/userDataStream** (Create a ListenKey (Margin).)
    ```python 
    client.margin_stream_get_listen_key()
    ```
  - **PUT /sapi/v1/userDataStream** (Ping/Keep-alive a ListenKey (Margin).)
    ```python 
    client.margin_stream_keepalive(listenKey)
    ```
  - **DELETE /sapi/v1/userDataStream** (Close a ListenKey (Margin).)
    ```python 
    client.margin_stream_close(listenKey)
    ```
  - **POST /sapi/v1/userDataStream/isolated** (Create a ListenKey (Isolated).)
    ```python 
    client.isolated_margin_stream_get_listen_key(symbol)
    ```
  - **PUT /sapi/v1/userDataStream/isolated** (Ping/Keep-alive a ListenKey (Isolated).)
    ```python 
    client.isolated_margin_stream_keepalive(symbol, listenKey)
    ```
  - **DELETE /sapi/v1/userDataStream/isolated** (Close a ListenKey (Isolated).)
    ```python 
    client.isolated_margin_stream_close(symbol, listenKey)
    ```
- *Savings Endpoints*
  - **GET /sapi/v1/lending/daily/product/list (HMAC SHA256)** (Get Flexible Product List (USER_DATA).)
    ```python 
    client.get_lending_product_list(status, featured, recvWindow)
    ```
  - **GET /sapi/v1/lending/daily/userLeftQuota (HMAC SHA256)** (Get Left Daily Purchase Quota of Flexible Product (USER_DATA).)
    ```python 
    client.get_lending_daily_quota_left(productId, recvWindow)
    ```
  - **POST /sapi/v1/lending/daily/purchase (HMAC SHA256)** (Purchase Flexible Product (USER_DATA).)
    ```python 
    client.purchase_lending_product(productId, amount, recvWindow)
    ```
  - **GET /sapi/v1/lending/daily/userRedemptionQuota (HMAC SHA256)** (Get Left Daily Redemption Quota of Flexible Product (USER_DATA).)
    ```python 
    client.get_lending_daily_redemption_quota(productId, type, recvWindow)
    ```
  - **POST /sapi/v1/lending/daily/redeem (HMAC SHA256)** (Redeem Flexible Product (USER_DATA).)
    ```python 
    client.redeem_lending_product(productId, amount, type, recvWindow)
    ```
  - **GET /sapi/v1/lending/daily/token/position (HMAC SHA256)** (Get Flexible Product Position (USER_DATA).)
    ```python 
    client.get_lending_position(asset, recvWindow)
    ```
  - **GET /sapi/v1/lending/project/list (HMAC SHA256)** (Get Fixed and Activity Project List (USER_DATA).)
    ```python 
    client.get_fixed_activity_project_list(asset, type, status, isSortAsc, sortBy, current, size, recvWindow)
    ```
  - **POST /sapi/v1/lending/customizedFixed/purchase (HMAC SHA256)** (Purchase Fixed/Activity Project (USER_DATA).)

    > :warning: Not yet implemented
  - **GET /sapi/v1/lending/project/position/list (HMAC SHA256)** (Get Fixed/Activity Project Position (USER_DATA).)

    > :warning: Not yet implemented
  - **GET /sapi/v1/lending/union/account (HMAC SHA256)** (Lending Account (USER_DATA).)
    ```python 
    client.get_lending_account(recvWindow)
    ```
  - **GET /sapi/v1/lending/union/purchaseRecord (HMAC SHA256)** (Get Purchase Record (USER_DATA).)
    ```python 
    client.get_lending_purchase_history(lendingType, asset, startTime, endTime, current, size, recvWindow)
    ```
  - **GET /sapi/v1/lending/union/redemptionRecord (HMAC SHA256)** (Get Redemption Record (USER_DATA).)
    ```python 
    client.get_lending_redemption_history(lendingType, asset, startTime, endTime, current, size, recvWindow)
    ```
  - **GET /sapi/v1/lending/union/interestHistory (HMAC SHA256)** (Get Interest History (USER_DATA).)
    ```python 
    client.get_lending_interest_history(lendingType, asset, startTime, endTime, current, size, recvWindow)
    ```
  - **POST /sapi/v1/lending/positionChanged (HMAC SHA256)** (Change Fixed/Activity Position to Daily Position (USER_DATA).)
    ```python 
    client.change_fixed_activity_to_daily_position(projectId, lot, positionId, recvWindow)
    ```
- *Mining Endpoints*
    > :warning: Not yet implemented
- *Sub-Account Endpoints*
  - **GET /sapi/v1/sub-account/list (HMAC SHA256)** (Query Sub-account List (For Master Account).)
    ```python 
    client.get_sub_account_list(email, isFreeze, page, limit, recvWindow)
    ```
  - **GET /sapi/v1/sub-account/sub/transfer/history (HMAC SHA256)** (Query Sub-account Spot Asset Transfer History (For Master Account).)
    ```python 
    client.get_sub_account_transfer_history(fromEmail, toEmail, startTime, endTime, page, limit, recvWindow)
    ```
  - **GET /sapi/v1/sub-account/assets (HMAC SHA256)** (Query Sub-account Assets (For Master Account).)
    ```python 
    client.get_sub_account_assets(email, recvWindow)
    ```
  > :warning: The rest of methods for Sub-Account Endpoints are not yet implemented
- *BLVT Endpoints*
    > :warning: Not yet implemented
- *BSwap Endpoints*
    > :warning: Not yet implemented
### [USDT-M Futures](https://binance-docs.github.io/apidocs/futures/en/)
- *Market Data Endpoints*
  - **GET /fapi/v1/ping** (Test connectivity to the Rest API.)
    ```python 
    client.futures_ping()
    ```
  - **GET /fapi/v1/time** (Test connectivity to the Rest API and get the current server time.)
    ```python 
    client.futures_time()
    ```
  - **GET /fapi/v1/exchangeInfo** (Current exchange trading rules and symbol information.)
    ```python 
    client.futures_exchange_info()
    ```
  - **GET /fapi/v1/depth** (Get the Order Book for the market.)
    ```python 
    client.futures_order_book(symbol, limit)
    ```
  - **GET /fapi/v1/trades** (Get recent trades.)
    ```python 
    client.futures_recent_trades(symbol, limit)
    ```
  - **GET /fapi/v1/historicalTrades** (Get older market historical trades (MARKET_DATA).)
    ```python 
    client.futures_historical_trades(symbol, limit, fromId)
    ```
  - **GET /fapi/v1/aggTrades** (Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated.)
    ```python 
    client.futures_aggregate_trades(symbol, fromId, startTime, endTime, limit)
    ```
  - **GET /fapi/v1/klines** (Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.)
    ```python 
    client.futures_klines(symbol, interval, startTime, endTime, limit)
    ```
  - **GET /fapi/v1/premiumIndex** (Get Mark Price and Funding Rate.)
    ```python 
    client.futures_mark_price(symbol)
    ```
  - **GET /fapi/v1/fundingRate** (Get Funding Rate History.)
    ```python 
    client.futures_funding_rate(symbol, startTime, endTime, limit)
    ```
  - **GET /fapi/v1/ticker/24hr** (24 hour rolling window price change statistics. **Careful** when accessing this with no symbol.)
    ```python 
    client.futures_ticker(symbol)
    ```
  - **GET /fapi/v1/ticker/price** (Latest price for a symbol or symbols.)
    ```python 
    client.futures_symbol_ticker(symbol)
    ```
  - **GET /fapi/v1/ticker/bookTicker** (Best price/qty on the order book for a symbol or symbols.)
    ```python 
    client.futures_orderbook_ticker(symbol)
    ``` 
  - **GET /fapi/v1/allForceOrders** (Get all Liquidation Orders.)
    > :warning: Probably broken, python code below is implemented on v1/ticker/allForceOrders endpoint.
    ```python 
    client.futures_liquidation_orders(symbol, startTime, endTime, limit)
    ``` 
  - **GET /fapi/v1/openInterest** (Get present open interest of a specific symbol.)
    ```python 
    client.futures_open_interest(symbol)
    ``` 
  - **GET /futures/data/openInterestHist** (Open Interest Statistics.)
    ```python 
    client.futures_open_interest_hist(symbol, period, limit, startTime, endTime)
    ``` 
  - **GET /futures/data/topLongShortAccountRatio** (Top Trader Long/Short Ratio (Accounts) (MARKET_DATA).)
    ```python 
    client.futures_top_longshort_account_ratio(symbol, period, limit, startTime, endTime)
    ``` 
  - **GET /futures/data/topLongShortPositionRatio** (Top Trader Long/Short Ratio (Positions).)
    ```python
    client.futures_top_longshort_position_ratio(symbol, period, limit, startTime, endTime)
    ```
  - **GET /futures/data/globalLongShortAccountRatio** (Long/Short Ratio.)
    ```python
    client.futures_global_longshort_ratio(symbol, period, limit, startTime, endTime)
    ```
  - **GET /futures/data/takerlongshortRatio** (Taker Buy/Sell Volume.)
    ```python
    client.futures_taker_longshort_ratio(symbol, period, limit, startTime, endTime)
    ```
  - **GET /fapi/v1/lvtKlines** (Historical BLVT NAV Kline/Candlestick.)

    > :warning: Not yet implemented
  - **GET /fapi/v1/indexInfo** (Composite Index Symbol Information.)

    > :warning: Not yet implemented
- *Account/trades Endpoints*
  - **POST /sapi/v1/futures/transfer (HMAC SHA256)** (New Future Account Transfer (FUTURES): Execute transfer between spot account and futures account.)
    ```python 
    client.futures_account_transfer(asset, amount, type, recvWindow)
    ```
  - **GET /sapi/v1/futures/transfer (HMAC SHA256)** (Get Future Account Transaction History List (USER_DATA).)
    ```python 
    client.transfer_history(asset, startTime, endTime, current, size, recvWindow)
    ```
  - **POST /fapi/v1/positionSide/dual (HMAC SHA256)** (Change user's position mode (Hedge Mode or One-way Mode ) on _**EVERY symbol**_.)
    ```python 
    client.futures_change_position_mode(dualSidePosition, recvWindow)
    ```
  - **GET /fapi/v1/positionSide/dual (HMAC SHA256)** (Get user's position mode (Hedge Mode or One-way Mode ) on _**EVERY symbol**_.)
    ```python 
    client.futures_get_position_mode(recvWindow)
    ```
  - **POST /fapi/v1/order (HMAC SHA256)** (Send in a new order (TRADE).)
    ```python 
    client.futures_create_order(symbol, 
                                side,
                                positionSide,
                                type, 
                                timeInForce, 
                                quantity,
                                reduceOnly,
                                price, 
                                newClientOrderId, 
                                stopPrice,
                                closePosition,
                                activationPrice,
                                callbackRate,
                                workingType,
                                priceProtect,
                                newOrderRespType,
                                recvWindow)
    ```
  - **POST /fapi/v1/batchOrders (HMAC SHA256)** (Place Multiple Orders (TRADE).)

    > :warning: Not yet implemented
  - **GET /fapi/v1/order (HMAC SHA256)** (Query Order (USER_DATA): Check an order's status.)
    ```python 
    client.futures_get_order(symbol, orderId, origClientOrderId, recvWindow)
    ```
  - **DELETE /fapi/v1/order (HMAC SHA256)** (Cancel an active order (TRADE).)
    ```python 
    client.futures_cancel_order(symbol, orderId, origClientOrderId, recvWindow)
    ```
  - **DELETE /fapi/v1/allOpenOrders (HMAC SHA256)** (Cancel All Open Orders (TRADE).)
    ```python 
    client.futures_cancel_all_open_orders(symbol, recvWindow)
    ```
  - **DELETE /fapi/v1/batchOrders (HMAC SHA256)** (Cancel Multiple Orders (TRADE).)
    ```python 
    client.futures_cancel_orders(symbol, orderIdList, origClientOrderIdList, recvWindow)
    ```
  - **POST /fapi/v1/countdownCancelAll (HMAC SHA256)** (Cancel all open orders of the specified symbol at the end of the specified countdown (TRADE).)

    > :warning: Not yet implemented
  - **GET /fapi/v1/openOrder (HMAC SHA256)** (Query Current Open Order (USER_DATA).)
  
    > :warning: Not yet implemented
  - **GET /fapi/v1/openOrders (HMAC SHA256)** (Get all open orders on a symbol. **Careful** when accessing this with no symbol (USER_DATA).)
    ```python 
    client.futures_get_open_orders(symbol, recvWindow)
    ```
  - **GET /fapi/v1/allOrders (HMAC SHA256)** (Get all account orders; active, canceled, or filled (USER_DATA).)
    ```python 
    client.futures_get_all_orders(symbol, orderId, startTime, endTime, limit, recvWindow)
    ```
  - **GET /fapi/v2/balance (HMAC SHA256)** (Futures Account Balance V2 (USER_DATA).)
    > :warning: Probably broken, python code below is implemented on v1 endpoint.
    ```python 
    client.futures_account_balance(recvWindow)
    ```
  - **GET /fapi/v2/account (HMAC SHA256)** (Account Information V2: Get current account information (USER_DATA).)
    > :warning: Probably broken, python code below is implemented on v1 endpoint.
    ```python 
    client.futures_account(recvWindow)
    ```
  - **POST /fapi/v1/leverage (HMAC SHA256)** (Change user's initial leverage of specific symbol market (TRADE).)
    ```python 
    client.futures_change_leverage(symbol, leverage, recvWindow)
    ```
  - **POST /fapi/v1/marginType (HMAC SHA256)** (Change the margin type for a symbol (TRADE).)
    ```python 
    client.futures_change_margin_type(symbol, marginType, recvWindow)
    ```
  - **POST /fapi/v1/positionMargin (HMAC SHA256)** (Modify Isolated Position Margin (TRADE).)
    ```python 
    client.futures_change_position_margin(symbol, positionSide, amount, type, recvWindow)
    ```
  - **GET /fapi/v1/positionMargin/history (HMAC SHA256)** (Get Position Margin Change History (TRADE).)
    ```python 
    client.futures_position_margin_history(symbol, type, startTime, endTime, limit, recvWindow)
    ```
  - **GET /fapi/v2/positionRisk (HMAC SHA256)** (Position Information V2: Get current position information (USER_DATA).)
    > :warning: Probably broken, python code below is implemented on v1 endpoint.
    ```python 
    client.futures_position_information(symbol, recvWindow)
    ```
  - **GET /fapi/v1/userTrades (HMAC SHA256)** (Account Trade List: Get trades for a specific account and symbol (USER_DATA).)
    ```python 
    client.futures_account_trades(symbol, startTime, endTime, fromId, limit, recvWindow)
    ```
  - **GET /fapi/v1/income (HMAC SHA256)** (Get Income History (USER_DATA).)
    ```python 
    client.futures_income_history(symbol, incomeType, startTime, endTime, limit, recvWindow)
    ```
  - **GET /fapi/v1/leverageBracket** (Notional and Leverage Brackets (USER_DATA).)
    > :warning: Probably broken, python code below is implemented on ticker/leverageBracket endpoint.
    ```python 
    client.futures_leverage_bracket(symbol, recvWindow)
    ```
  - **GET /fapi/v1/adlQuantile** (Position ADL Quantile Estimation (USER_DATA).)

    > :warning: Not yet implemented
  - **GET /fapi/v1/forceOrders** (User's Force Orders (USER_DATA).)

    > :warning: Not yet implemented
  - **GET /fapi/v1/apiTradingStatus** (User API Trading Quantitative Rules Indicators (USER_DATA).)

    > :warning: Not yet implemented
- *User Data Streams*
    > :warning: Not yet implemented
### [Vanilla Options](https://binance-docs.github.io/apidocs/voptions/en/)
- *Quoting interface*
  - **GET /vapi/v1/ping** (Test connectivity)
    ```python 
    client.options_ping()
    ```
  - **GET /vapi/v1/time** (Get server time)
    ```python 
    client.options_time()
    ```
  - **GET /vapi/v1/optionInfo** (Get current trading pair info)
    ```python 
    client.options_info()
    ```
  - **GET /vapi/v1/exchangeInfo** (Get current limit info and trading pair info)
    ```python 
    client.options_exchange_info()
    ```
  - **GET /vapi/v1/index** (Get the spot index price)
    ```python 
    client.options_index_price(underlying)
    ```
  - **GET /vapi/v1/ticker** (Get the latest price)
    ```python 
    client.options_price(symbol)
    ```
  - **GET /vapi/v1/mark** (Get the latest mark price)
    ```python 
    client.options_mark_price(symbol)
    ```
  - **GET /vapi/v1/depth** (Depth information)
    ```python 
    client.options_order_book(symbol, limit)
    ```
  - **GET /vapi/v1/klines** (Candle data)
    ```python 
    client.options_klines(symbol, interval, startTime, endTime, limit)
    ```
  - **GET /vapi/v1/trades** (Recently completed Option trades)
    ```python 
    client.options_recent_trades(symbol, limit)
    ```
  - **GET /vapi/v1/historicalTrades** (Query trade history)
    ```python 
    client.options_historical_trades(symbol, fromId, limit)
    ```
- *Account and trading interface*
  - **GET /vapi/v1/account (HMAC SHA256)** (Account asset info (USER_DATA))
    ```python 
    client.options_account_info(recvWindow)
    ```
  - **POST /vapi/v1/transfer (HMAC SHA256)** (Funds transfer (USER_DATA))
    ```python 
    client.options_funds_transfer(currency, type, amount, recvWindow)
    ```
  - **GET /vapi/v1/position (HMAC SHA256)** (Option holdings info (USER_DATA))
    ```python 
    client.options_positions(symbol, recvWindow)
    ```
  - **POST /vapi/v1/bill (HMAC SHA256)** (Account funding flow (USER_DATA))
    ```python 
    client.options_bill(currency, recordId, startTime, endTime, limit, recvWindow)
    ```
  - **POST /vapi/v1/order (HMAC SHA256)** (Option order (TRADE))
    ```python 
    client.options_place_order(symbol, side, type, quantity, price, timeInForce, reduceOnly, postOnly, \
        newOrderRespType, clientOrderId, recvWindow, recvWindow)
    ```
  - **POST /vapi/v1/batchOrders (HMAC SHA256)** (Place Multiple Option orders (TRADE))
    ```python 
    client.options_place_batch_order(orders, recvWindow)
    ```
  - **DELETE /vapi/v1/order (HMAC SHA256)** (Cancel Option order (TRADE))
    ```python 
    client.options_cancel_order(symbol, orderId, clientOrderId, recvWindow)
    ```
  - **DELETE /vapi/v1/batchOrders (HMAC SHA256)** (Cancel Multiple Option orders (TRADE))
    ```python 
    client.options_cancel_batch_order(symbol, orderIds, clientOrderIds, recvWindow)
    ```
  - **DELETE /vapi/v1/allOpenOrders (HMAC SHA256)** (Cancel all Option orders (TRADE))
    ```python 
    client.options_cancel_all_orders(symbol, recvWindow)
    ```
  - **GET /vapi/v1/order (HMAC SHA256)** (Query Option order (TRADE))
    ```python 
    client.options_query_order(symbol, orderId, clientOrderId, recvWindow)
    ```
  - **GET /vapi/v1/openOrders (HMAC SHA256)** (Query current pending Option orders (TRADE))
    ```python 
    client.options_query_pending_orders(symbol, orderId, startTime, endTime, limit, recvWindow)
    ```
  - **GET /vapi/v1/historyOrders (HMAC SHA256)** (Query Option order history (TRADE))
    ```python 
    client.options_query_order_history(symbol, orderId, startTime, endTime, limit, recvWindow)
    ```
  - **GET /vapi/v1/userTrades (HMAC SHA256)** (Option Trade List (USER_DATA))
    ```python 
    client.options_user_trades(symbol, fromId, startTime, endTime, limit, recvWindow)
    ```
### [COIN-M Futures](https://binance-docs.github.io/apidocs/delivery/en/)
> :warning: Not yet implemented
### [USDT-M Futures testnet](https://binance-docs.github.io/apidocs/testnet/en/)
> :warning: Not yet implemented  
### [COIN-M Futures testnet](https://binance-docs.github.io/apidocs/delivery_testnet/en/)
> :warning: Not yet implemented  
	- **GET /sapi/v1/loan/vip/ongoing/orders**
    ```python
    client.margin_v1_get_loan_vip_ongoing_orders(**params)
    ```

	- **GET /sapi/v1/mining/payment/other**
    ```python
    client.margin_v1_get_mining_payment_other(**params)
    ```

	- **GET /dapi/v1/income/asyn/id**
    ```python
    client.futures_coin_v1_get_income_asyn_id(**params)
    ```

	- **GET /sapi/v1/simple-earn/flexible/history/subscriptionRecord**
    ```python
    client.margin_v1_get_simple_earn_flexible_history_subscription_record(**params)
    ```

	- **POST /sapi/v1/lending/auto-invest/one-off**
    ```python
    client.margin_v1_post_lending_auto_invest_one_off(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/commission/coinFutures**
    ```python
    client.margin_v1_post_broker_sub_account_api_commission_coin_futures(**params)
    ```

	- **POST /papi/v1/repay-futures-negative-balance**
    ```python
    client.papi_v1_post_repay_futures_negative_balance(**params)
    ```

	- **POST /eapi/v1/block/order/execute**
    ```python
    client.options_v1_post_block_order_execute(**params)
    ```

	- **GET /sapi/v1/margin/dust**
    ```python
    client.margin_v1_get_margin_dust(**params)
    ```

	- **GET /dapi/v1/trades**
    ```python
    client.futures_coin_v1_get_trades(**params)
    ```

	- **POST /api/v3/orderList/otoco**
    ```python
    client.v3_post_order_list_otoco(**params)
    ```

	- **GET /fapi/v1/order/asyn**
    ```python
    client.futures_v1_get_order_asyn(**params)
    ```

	- **GET /sapi/v1/asset/custody/transfer-history**
    ```python
    client.margin_v1_get_asset_custody_transfer_history(**params)
    ```

	- **POST /fapi/v1/order/test**
    ```python
    client.futures_v1_post_order_test(**params)
    ```

	- **POST /sapi/v1/broker/subAccount/blvt**
    ```python
    client.margin_v1_post_broker_sub_account_blvt(**params)
    ```

	- **POST /sapi/v1/sol-staking/sol/redeem**
    ```python
    client.margin_v1_post_sol_staking_sol_redeem(**params)
    ```

	- **GET /eapi/v1/countdownCancelAll**
    ```python
    client.options_v1_get_countdown_cancel_all(**params)
    ```

	- **GET /sapi/v1/margin/tradeCoeff**
    ```python
    client.margin_v1_get_margin_trade_coeff(**params)
    ```

	- **GET /sapi/v1/sub-account/futures/positionRisk**
    ```python
    client.margin_v1_get_sub_account_futures_position_risk(**params)
    ```

	- **GET /dapi/v1/orderAmendment**
    ```python
    client.futures_coin_v1_get_order_amendment(**params)
    ```

	- **GET /papi/v1/margin/openOrders**
    ```python
    client.papi_v1_get_margin_open_orders(**params)
    ```

	- **GET /sapi/v1/margin/available-inventory**
    ```python
    client.margin_v1_get_margin_available_inventory(**params)
    ```

	- **POST /sapi/v1/account/apiRestrictions/ipRestriction/ipList**
    ```python
    client.margin_v1_post_account_api_restrictions_ip_restriction_ip_list(**params)
    ```

	- **GET /sapi/v2/eth-staking/account**
    ```python
    client.margin_v2_get_eth_staking_account(**params)
    ```

	- **POST /papi/v1/asset-collection**
    ```python
    client.papi_v1_post_asset_collection(**params)
    ```

	- **GET /papi/v1/um/trade/asyn/id**
    ```python
    client.papi_v1_get_um_trade_asyn_id(**params)
    ```

	- **POST /sapi/v1/staking/redeem**
    ```python
    client.margin_v1_post_staking_redeem(**params)
    ```

	- **GET /sapi/v1/loan/income**
    ```python
    client.margin_v1_get_loan_income(**params)
    ```

	- **GET /eapi/v1/depth**
    ```python
    client.options_v1_get_depth(**params)
    ```

	- **GET /dapi/v1/pmAccountInfo**
    ```python
    client.futures_coin_v1_get_pm_account_info(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/queryTransLogForInvestor**
    ```python
    client.margin_v1_get_managed_subaccount_query_trans_log_for_investor(**params)
    ```

	- **POST /sapi/v1/dci/product/auto_compound/edit-status**
    ```python
    client.margin_v1_post_dci_product_auto_compound_edit_status(**params)
    ```

	- **GET /fapi/v1/trade/asyn**
    ```python
    client.futures_v1_get_trade_asyn(**params)
    ```

	- **GET /sapi/v1/loan/vip/request/interestRate**
    ```python
    client.margin_v1_get_loan_vip_request_interest_rate(**params)
    ```

	- **GET /fapi/v1/fundingInfo**
    ```python
    client.futures_v1_get_funding_info(**params)
    ```

	- **GET /sapi/v2/loan/flexible/repay/rate**
    ```python
    client.margin_v2_get_loan_flexible_repay_rate(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/plan/id**
    ```python
    client.margin_v1_get_lending_auto_invest_plan_id(**params)
    ```

	- **POST /sapi/v1/loan/adjust/ltv**
    ```python
    client.margin_v1_post_loan_adjust_ltv(**params)
    ```

	- **GET /sapi/v1/bnbBurn**
    ```python
    client.margin_v1_get_bnb_burn(**params)
    ```

	- **GET /papi/v1/um/order**
    ```python
    client.papi_v1_get_um_order(**params)
    ```

	- **GET /sapi/v1/mining/statistics/user/status**
    ```python
    client.margin_v1_get_mining_statistics_user_status(**params)
    ```

	- **POST /sapi/v1/staking/purchase**
    ```python
    client.margin_v1_post_staking_purchase(**params)
    ```

	- **POST /sapi/v1/giftcard/redeemCode**
    ```python
    client.margin_v1_post_giftcard_redeem_code(**params)
    ```

	- **GET /eapi/v1/userTrades**
    ```python
    client.options_v1_get_user_trades(**params)
    ```

	- **GET /sapi/v1/broker/transfer/futures**
    ```python
    client.margin_v1_get_broker_transfer_futures(**params)
    ```

	- **POST /sapi/v1/algo/spot/newOrderTwap**
    ```python
    client.margin_v1_post_algo_spot_new_order_twap(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/target-asset/list**
    ```python
    client.margin_v1_get_lending_auto_invest_target_asset_list(**params)
    ```

	- **GET /sapi/v1/capital/deposit/address/list**
    ```python
    client.margin_v1_get_capital_deposit_address_list(**params)
    ```

	- **POST /sapi/v1/broker/subAccount/bnbBurn/marginInterest**
    ```python
    client.margin_v1_post_broker_sub_account_bnb_burn_margin_interest(**params)
    ```

	- **POST /sapi/v2/loan/flexible/repay**
    ```python
    client.margin_v2_post_loan_flexible_repay(**params)
    ```

	- **GET /sapi/v2/loan/flexible/loanable/data**
    ```python
    client.margin_v2_get_loan_flexible_loanable_data(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/permission**
    ```python
    client.margin_v1_post_broker_sub_account_api_permission(**params)
    ```

	- **GET /sapi/v1/dci/product/positions**
    ```python
    client.margin_v1_get_dci_product_positions(**params)
    ```

	- **POST /sapi/v1/convert/limit/cancelOrder**
    ```python
    client.margin_v1_post_convert_limit_cancel_order(**params)
    ```

	- **GET /sapi/v1/margin/exchange-small-liability-history**
    ```python
    client.margin_v1_get_margin_exchange_small_liability_history(**params)
    ```

	- **GET /sapi/v1/mining/hash-transfer/config/details/list**
    ```python
    client.margin_v1_get_mining_hash_transfer_config_details_list(**params)
    ```

	- **GET /sapi/v1/mining/hash-transfer/profit/details**
    ```python
    client.margin_v1_get_mining_hash_transfer_profit_details(**params)
    ```

	- **GET /sapi/v1/broker/subAccount**
    ```python
    client.margin_v1_get_broker_sub_account(**params)
    ```

	- **GET /sapi/v1/portfolio/balance**
    ```python
    client.margin_v1_get_portfolio_balance(**params)
    ```

	- **POST /sapi/v1/sub-account/eoptions/enable**
    ```python
    client.margin_v1_post_sub_account_eoptions_enable(**params)
    ```

	- **POST /papi/v1/ping**
    ```python
    client.papi_v1_post_ping(**params)
    ```

	- **GET /sapi/v1/loan/loanable/data**
    ```python
    client.margin_v1_get_loan_loanable_data(**params)
    ```

	- **POST /sapi/v1/eth-staking/wbeth/unwrap**
    ```python
    client.margin_v1_post_eth_staking_wbeth_unwrap(**params)
    ```

	- **PUT /fapi/v1/order**
    ```python
    client.futures_v1_put_order(**params)
    ```

	- **GET /sapi/v1/eth-staking/eth/history/stakingHistory**
    ```python
    client.margin_v1_get_eth_staking_eth_history_staking_history(**params)
    ```

	- **GET /papi/v1/um/conditional/openOrder**
    ```python
    client.papi_v1_get_um_conditional_open_order(**params)
    ```

	- **GET /dapi/v1/openOrders**
    ```python
    client.futures_coin_v1_get_open_orders(**params)
    ```

	- **GET /eapi/v1/order**
    ```python
    client.options_v1_get_order(**params)
    ```

	- **POST /sapi/v1/convert/acceptQuote**
    ```python
    client.margin_v1_post_convert_accept_quote(**params)
    ```

	- **GET /sapi/v1/staking/stakingRecord**
    ```python
    client.margin_v1_get_staking_staking_record(**params)
    ```

	- **GET /sapi/v1/broker/rebate/recentRecord**
    ```python
    client.margin_v1_get_broker_rebate_recent_record(**params)
    ```

	- **GET /eapi/v1/block/order/orders**
    ```python
    client.options_v1_get_block_order_orders(**params)
    ```

	- **GET /sapi/v1/asset/transfer**
    ```python
    client.margin_v1_get_asset_transfer(**params)
    ```

	- **GET /sapi/v1/loan/vip/collateral/account**
    ```python
    client.margin_v1_get_loan_vip_collateral_account(**params)
    ```

	- **GET /sapi/v1/algo/spot/openOrders**
    ```python
    client.margin_v1_get_algo_spot_open_orders(**params)
    ```

	- **POST /sapi/v1/loan/repay**
    ```python
    client.margin_v1_post_loan_repay(**params)
    ```

	- **POST /sapi/v1/margin/isolated/account**
    ```python
    client.margin_v1_post_margin_isolated_account(**params)
    ```

	- **GET /dapi/v1/fundingInfo**
    ```python
    client.futures_coin_v1_get_funding_info(**params)
    ```

	- **GET /papi/v1/cm/leverageBracket**
    ```python
    client.papi_v1_get_cm_leverage_bracket(**params)
    ```

	- **POST /sapi/v1/simple-earn/locked/subscribe**
    ```python
    client.margin_v1_post_simple_earn_locked_subscribe(**params)
    ```

	- **GET /sapi/v1/margin/leverageBracket**
    ```python
    client.margin_v1_get_margin_leverage_bracket(**params)
    ```

	- **GET /sapi/v2/portfolio/collateralRate**
    ```python
    client.margin_v2_get_portfolio_collateral_rate(**params)
    ```

	- **POST /sapi/v2/loan/flexible/adjust/ltv**
    ```python
    client.margin_v2_post_loan_flexible_adjust_ltv(**params)
    ```

	- **GET /sapi/v1/convert/orderStatus**
    ```python
    client.margin_v1_get_convert_order_status(**params)
    ```

	- **POST /sapi/v1/margin/dust**
    ```python
    client.margin_v1_post_margin_dust(**params)
    ```

	- **GET /sapi/v1/broker/subAccountApi/ipRestriction**
    ```python
    client.margin_v1_get_broker_sub_account_api_ip_restriction(**params)
    ```

	- **GET /papi/v1/um/conditional/allOrders**
    ```python
    client.papi_v1_get_um_conditional_all_orders(**params)
    ```

	- **PUT /eapi/v1/block/order/create**
    ```python
    client.options_v1_put_block_order_create(**params)
    ```

	- **POST /sapi/v1/dci/product/subscribe**
    ```python
    client.margin_v1_post_dci_product_subscribe(**params)
    ```

	- **GET /fapi/v1/income/asyn/id**
    ```python
    client.futures_v1_get_income_asyn_id(**params)
    ```

	- **GET /dapi/v1/positionRisk**
    ```python
    client.futures_coin_v1_get_position_risk(**params)
    ```

	- **POST /eapi/v1/countdownCancelAll**
    ```python
    client.options_v1_post_countdown_cancel_all(**params)
    ```

	- **POST /papi/v1/repay-futures-switch**
    ```python
    client.papi_v1_post_repay_futures_switch(**params)
    ```

	- **POST /sapi/v1/mining/hash-transfer/config/cancel**
    ```python
    client.margin_v1_post_mining_hash_transfer_config_cancel(**params)
    ```

	- **GET /sapi/v1/broker/subAccount/depositHist**
    ```python
    client.margin_v1_get_broker_sub_account_deposit_hist(**params)
    ```

	- **POST /eapi/v1/block/order/create**
    ```python
    client.options_v1_post_block_order_create(**params)
    ```

	- **GET /sapi/v1/capital/deposit/subAddress**
    ```python
    client.margin_v1_get_capital_deposit_sub_address(**params)
    ```

	- **GET /sapi/v1/mining/payment/list**
    ```python
    client.margin_v1_get_mining_payment_list(**params)
    ```

	- **GET /fapi/v1/pmAccountInfo**
    ```python
    client.futures_v1_get_pm_account_info(**params)
    ```

	- **GET /dapi/v1/adlQuantile**
    ```python
    client.futures_coin_v1_get_adl_quantile(**params)
    ```

	- **GET /eapi/v1/income/asyn/id**
    ```python
    client.options_v1_get_income_asyn_id(**params)
    ```

	- **POST /api/v3/cancelReplace**
    ```python
    client.v3_post_cancel_replace(**params)
    ```

	- **PUT /papi/v1/um/order**
    ```python
    client.papi_v1_put_um_order(**params)
    ```

	- **GET /sapi/v1/sub-account/futures/accountSummary**
    ```python
    client.margin_v1_get_sub_account_futures_account_summary(**params)
    ```

	- **GET /papi/v1/um/symbolConfig**
    ```python
    client.papi_v1_get_um_symbol_config(**params)
    ```

	- **GET /papi/v1/um/userTrades**
    ```python
    client.papi_v1_get_um_user_trades(**params)
    ```

	- **GET /sapi/v1/staking/productList**
    ```python
    client.margin_v1_get_staking_product_list(**params)
    ```

	- **POST /sapi/v1/asset/get-funding-asset**
    ```python
    client.margin_v1_post_asset_get_funding_asset(**params)
    ```

	- **POST /sapi/v1/bnbBurn**
    ```python
    client.margin_v1_post_bnb_burn(**params)
    ```

	- **POST /papi/v1/um/order**
    ```python
    client.papi_v1_post_um_order(**params)
    ```

	- **GET /dapi/v1/order/asyn**
    ```python
    client.futures_coin_v1_get_order_asyn(**params)
    ```

	- **GET /sapi/v1/c2c/orderMatch/listUserOrderHistory**
    ```python
    client.margin_v1_get_c2c_order_match_list_user_order_history(**params)
    ```

	- **POST /sapi/v1/simple-earn/flexible/subscribe**
    ```python
    client.margin_v1_post_simple_earn_flexible_subscribe(**params)
    ```

	- **POST /sapi/v1/broker/transfer/futures**
    ```python
    client.margin_v1_post_broker_transfer_futures(**params)
    ```

	- **POST /api/v3/order/cancelReplace**
    ```python
    client.v3_post_order_cancel_replace(**params)
    ```

	- **POST /sapi/v1/sol-staking/sol/stake**
    ```python
    client.margin_v1_post_sol_staking_sol_stake(**params)
    ```

	- **POST /sapi/v1/loan/borrow**
    ```python
    client.margin_v1_post_loan_borrow(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/info**
    ```python
    client.margin_v1_get_managed_subaccount_info(**params)
    ```

	- **POST /sapi/v1/lending/auto-invest/plan/edit-status**
    ```python
    client.margin_v1_post_lending_auto_invest_plan_edit_status(**params)
    ```

	- **GET /fapi/v1/symbolConfig**
    ```python
    client.futures_v1_get_symbol_config(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/history/unclaimedRewards**
    ```python
    client.margin_v1_get_sol_staking_sol_history_unclaimed_rewards(**params)
    ```

	- **POST /sapi/v1/asset/convert-transfer/queryByPage**
    ```python
    client.margin_v1_post_asset_convert_transfer_query_by_page(**params)
    ```

	- **GET /sapi/v1/sub-account/universalTransfer**
    ```python
    client.margin_v1_get_sub_account_universal_transfer(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/history/boostRewardsHistory**
    ```python
    client.margin_v1_get_sol_staking_sol_history_boost_rewards_history(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/one-off/status**
    ```python
    client.margin_v1_get_lending_auto_invest_one_off_status(**params)
    ```

	- **GET /sapi/v1/asset/ledger-transfer/cloud-mining/queryByPage**
    ```python
    client.margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page(**params)
    ```

	- **DELETE /sapi/v1/margin/orderList**
    ```python
    client.margin_v1_delete_margin_order_list(**params)
    ```

	- **GET /sapi/v1/mining/pub/coinList**
    ```python
    client.margin_v1_get_mining_pub_coin_list(**params)
    ```

	- **GET /sapi/v2/loan/flexible/repay/history**
    ```python
    client.margin_v2_get_loan_flexible_repay_history(**params)
    ```

	- **GET /fapi/v3/account**
    ```python
    client.futures_v3_get_account(**params)
    ```

	- **POST /api/v3/sor/order**
    ```python
    client.v3_post_sor_order(**params)
    ```

	- **POST /sapi/v1/capital/deposit/credit-apply**
    ```python
    client.margin_v1_post_capital_deposit_credit_apply(**params)
    ```

	- **PUT /fapi/v1/batchOrder**
    ```python
    client.futures_v1_put_batch_order(**params)
    ```

	- **GET /sapi/v1/fiat/payments**
    ```python
    client.margin_v1_get_fiat_payments(**params)
    ```

	- **GET /api/v3/myPreventedMatches**
    ```python
    client.v3_get_my_prevented_matches(**params)
    ```

	- **GET /dapi/v1/forceOrders**
    ```python
    client.futures_coin_v1_get_force_orders(**params)
    ```

	- **POST /sapi/v1/asset/transfer**
    ```python
    client.margin_v1_post_asset_transfer(**params)
    ```

	- **GET /sapi/v1/mining/statistics/user/list**
    ```python
    client.margin_v1_get_mining_statistics_user_list(**params)
    ```

	- **GET /api/v3/ticker/tradingDay**
    ```python
    client.v3_get_ticker_trading_day(**params)
    ```

	- **GET /sapi/v1/mining/worker/detail**
    ```python
    client.margin_v1_get_mining_worker_detail(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/fetch-future-asset**
    ```python
    client.margin_v1_get_managed_subaccount_fetch_future_asset(**params)
    ```

	- **GET /dapi/v1/pmExchangeInfo**
    ```python
    client.futures_coin_v1_get_pm_exchange_info(**params)
    ```

	- **POST /sapi/v1/convert/getQuote**
    ```python
    client.margin_v1_post_convert_get_quote(**params)
    ```

	- **GET /api/v3/uiKlines**
    ```python
    client.v3_get_ui_klines(**params)
    ```

	- **GET /sapi/v1/margin/rateLimit/order**
    ```python
    client.margin_v1_get_margin_rate_limit_order(**params)
    ```

	- **GET /sapi/v1/localentity/vasp**
    ```python
    client.margin_v1_get_localentity_vasp(**params)
    ```

	- **GET /fapi/v1/commissionRate**
    ```python
    client.futures_v1_get_commission_rate(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/history/rateHistory**
    ```python
    client.margin_v1_get_sol_staking_sol_history_rate_history(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/ipRestriction**
    ```python
    client.margin_v1_post_broker_sub_account_api_ip_restriction(**params)
    ```

	- **GET /eapi/v1/block/user-trades**
    ```python
    client.options_v1_get_block_user_trades(**params)
    ```

	- **GET /dapi/v1/order/asyn/id**
    ```python
    client.futures_coin_v1_get_order_asyn_id(**params)
    ```

	- **GET /sapi/v1/sol-staking/account**
    ```python
    client.margin_v1_get_sol_staking_account(**params)
    ```

	- **GET /sapi/v1/account/info**
    ```python
    client.margin_v1_get_account_info(**params)
    ```

	- **POST /sapi/v1/sub-account/transfer/subToMaster**
    ```python
    client.margin_v1_post_sub_account_transfer_sub_to_master(**params)
    ```

	- **POST /sapi/v1/portfolio/repay-futures-switch**
    ```python
    client.margin_v1_post_portfolio_repay_futures_switch(**params)
    ```

	- **GET /sapi/v1/giftcard/buyCode/token-limit**
    ```python
    client.margin_v1_get_giftcard_buy_code_token_limit(**params)
    ```

	- **GET /sapi/v1/capital/deposit/subHisrec**
    ```python
    client.margin_v1_get_capital_deposit_sub_hisrec(**params)
    ```

	- **POST /sapi/v1/loan/vip/borrow**
    ```python
    client.margin_v1_post_loan_vip_borrow(**params)
    ```

	- **GET /papi/v1/um/order/asyn/id**
    ```python
    client.papi_v1_get_um_order_asyn_id(**params)
    ```

	- **GET /papi/v1/cm/account**
    ```python
    client.papi_v1_get_cm_account(**params)
    ```

	- **DELETE /papi/v1/um/conditional/order**
    ```python
    client.papi_v1_delete_um_conditional_order(**params)
    ```

	- **GET /sapi/v2/loan/flexible/ltv/adjustment/history**
    ```python
    client.margin_v2_get_loan_flexible_ltv_adjustment_history(**params)
    ```

	- **DELETE /eapi/v1/allOpenOrdersByUnderlying**
    ```python
    client.options_v1_delete_all_open_orders_by_underlying(**params)
    ```

	- **PUT /papi/v1/cm/order**
    ```python
    client.papi_v1_put_cm_order(**params)
    ```

	- **GET /sapi/v1/broker/subAccount/futuresSummary**
    ```python
    client.margin_v1_get_broker_sub_account_futures_summary(**params)
    ```

	- **GET /dapi/v1/continuousKlines**
    ```python
    client.futures_coin_v1_get_continuous_klines(**params)
    ```

	- **GET /fapi/v1/accountConfig**
    ```python
    client.futures_v1_get_account_config(**params)
    ```

	- **DELETE /dapi/v1/batchOrders**
    ```python
    client.futures_coin_v1_delete_batch_orders(**params)
    ```

	- **GET /sapi/v1/broker/subAccount/spotSummary**
    ```python
    client.margin_v1_get_broker_sub_account_spot_summary(**params)
    ```

	- **GET /papi/v1/margin/openOrderList**
    ```python
    client.papi_v1_get_margin_open_order_list(**params)
    ```

	- **POST /sapi/v1/sub-account/blvt/enable**
    ```python
    client.margin_v1_post_sub_account_blvt_enable(**params)
    ```

	- **GET /dapi/v1/trade/asyn**
    ```python
    client.futures_coin_v1_get_trade_asyn(**params)
    ```

	- **GET /sapi/v1/algo/spot/historicalOrders**
    ```python
    client.margin_v1_get_algo_spot_historical_orders(**params)
    ```

	- **GET /sapi/v1/loan/vip/repay/history**
    ```python
    client.margin_v1_get_loan_vip_repay_history(**params)
    ```

	- **GET /eapi/v1/openInterest**
    ```python
    client.options_v1_get_open_interest(**params)
    ```

	- **GET /papi/v1/um/adlQuantile**
    ```python
    client.papi_v1_get_um_adl_quantile(**params)
    ```

	- **GET /eapi/v1/account**
    ```python
    client.options_v1_get_account(**params)
    ```

	- **POST /sapi/v1/sub-account/universalTransfer**
    ```python
    client.margin_v1_post_sub_account_universal_transfer(**params)
    ```

	- **GET /papi/v1/margin/allOrderList**
    ```python
    client.papi_v1_get_margin_all_order_list(**params)
    ```

	- **GET /fapi/v2/ticker/price**
    ```python
    client.futures_v2_get_ticker_price(**params)
    ```

	- **GET /sapi/v1/loan/borrow/history**
    ```python
    client.margin_v1_get_loan_borrow_history(**params)
    ```

	- **GET /papi/v1/um/account**
    ```python
    client.papi_v1_get_um_account(**params)
    ```

	- **POST /sapi/v1/lending/auto-invest/redeem**
    ```python
    client.margin_v1_post_lending_auto_invest_redeem(**params)
    ```

	- **POST /sapi/v1/managed-subaccount/deposit**
    ```python
    client.margin_v1_post_managed_subaccount_deposit(**params)
    ```

	- **GET /dapi/v1/fundingRate**
    ```python
    client.futures_coin_v1_get_funding_rate(**params)
    ```

	- **GET /fapi/v1/trade/asyn/id**
    ```python
    client.futures_v1_get_trade_asyn_id(**params)
    ```

	- **DELETE /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList**
    ```python
    client.margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list(**params)
    ```

	- **GET /sapi/v1/copyTrading/futures/userStatus**
    ```python
    client.margin_v1_get_copy_trading_futures_user_status(**params)
    ```

	- **GET /papi/v1/um/income**
    ```python
    client.papi_v1_get_um_income(**params)
    ```

	- **GET /papi/v1/um/openOrders**
    ```python
    client.papi_v1_get_um_open_orders(**params)
    ```

	- **GET /eapi/v1/marginAccount**
    ```python
    client.options_v1_get_margin_account(**params)
    ```

	- **GET /dapi/v1/premiumIndex**
    ```python
    client.futures_coin_v1_get_premium_index(**params)
    ```

	- **POST /sapi/v1/localentity/withdraw/apply**
    ```python
    client.margin_v1_post_localentity_withdraw_apply(**params)
    ```

	- **GET /sapi/v1/margin/orderList**
    ```python
    client.margin_v1_get_margin_order_list(**params)
    ```

	- **GET /papi/v1/um/feeBurn**
    ```python
    client.papi_v1_get_um_fee_burn(**params)
    ```

	- **GET /fapi/v1/multiAssetsMargin**
    ```python
    client.futures_v1_get_multi_assets_margin(**params)
    ```

	- **GET /sapi/v1/giftcard/verify**
    ```python
    client.margin_v1_get_giftcard_verify(**params)
    ```

	- **GET /sapi/v1/asset/wallet/balance**
    ```python
    client.margin_v1_get_asset_wallet_balance(**params)
    ```

	- **POST /sapi/v1/algo/futures/newOrderTwap**
    ```python
    client.margin_v1_post_algo_futures_new_order_twap(**params)
    ```

	- **GET /sapi/v1/margin/crossMarginCollateralRatio**
    ```python
    client.margin_v1_get_margin_cross_margin_collateral_ratio(**params)
    ```

	- **POST /sapi/v2/eth-staking/eth/stake**
    ```python
    client.margin_v2_post_eth_staking_eth_stake(**params)
    ```

	- **POST /sapi/v1/loan/flexible/repay/history**
    ```python
    client.margin_v1_post_loan_flexible_repay_history(**params)
    ```

	- **GET /dapi/v1/exchangeInfo**
    ```python
    client.futures_coin_v1_get_exchange_info(**params)
    ```

	- **POST /sapi/v1/sub-account/futures/enable**
    ```python
    client.margin_v1_post_sub_account_futures_enable(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/index/info**
    ```python
    client.margin_v1_get_lending_auto_invest_index_info(**params)
    ```

	- **GET /sapi/v2/sub-account/futures/positionRisk**
    ```python
    client.margin_v2_get_sub_account_futures_position_risk(**params)
    ```

	- **GET /sapi/v1/sub-account/margin/account**
    ```python
    client.margin_v1_get_sub_account_margin_account(**params)
    ```

	- **GET /papi/v1/rateLimit/order**
    ```python
    client.papi_v1_get_rate_limit_order(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/history/redemptionHistory**
    ```python
    client.margin_v1_get_sol_staking_sol_history_redemption_history(**params)
    ```

	- **GET /fapi/v1/markPriceKlines**
    ```python
    client.futures_v1_get_mark_price_klines(**params)
    ```

	- **GET /sapi/v1/broker/rebate/futures/recentRecord**
    ```python
    client.margin_v1_get_broker_rebate_futures_recent_record(**params)
    ```

	- **GET /sapi/v3/broker/subAccount/futuresSummary**
    ```python
    client.margin_v3_get_broker_sub_account_futures_summary(**params)
    ```

	- **GET /dapi/v1/aggTrades**
    ```python
    client.futures_coin_v1_get_agg_trades(**params)
    ```

	- **GET /eapi/v1/exchangeInfo**
    ```python
    client.options_v1_get_exchange_info(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/target-asset/roi/list**
    ```python
    client.margin_v1_get_lending_auto_invest_target_asset_roi_list(**params)
    ```

	- **GET /sapi/v1/broker/universalTransfer**
    ```python
    client.margin_v1_get_broker_universal_transfer(**params)
    ```

	- **POST /sapi/v1/sub-account/futures/transfer**
    ```python
    client.margin_v1_post_sub_account_futures_transfer(**params)
    ```

	- **PUT /fapi/v1/batchOrders**
    ```python
    client.futures_v1_put_batch_orders(**params)
    ```

	- **POST /eapi/v1/countdownCancelAllHeartBeat**
    ```python
    client.options_v1_post_countdown_cancel_all_heart_beat(**params)
    ```

	- **GET /sapi/v1/loan/collateral/data**
    ```python
    client.margin_v1_get_loan_collateral_data(**params)
    ```

	- **GET /sapi/v1/margin/borrow-repay**
    ```python
    client.margin_v1_get_margin_borrow_repay(**params)
    ```

	- **GET /sapi/v1/loan/repay/history**
    ```python
    client.margin_v1_get_loan_repay_history(**params)
    ```

	- **GET /dapi/v2/leverageBracket**
    ```python
    client.futures_coin_v2_get_leverage_bracket(**params)
    ```

	- **GET /fapi/v1/indexPriceKlines**
    ```python
    client.futures_v1_get_index_price_klines(**params)
    ```

	- **POST /sapi/v1/convert/limit/placeOrder**
    ```python
    client.margin_v1_post_convert_limit_place_order(**params)
    ```

	- **GET /fapi/v1/convert/exchangeInfo**
    ```python
    client.futures_v1_get_convert_exchange_info(**params)
    ```

	- **GET /dapi/v1/historicalTrades**
    ```python
    client.futures_coin_v1_get_historical_trades(**params)
    ```

	- **DELETE /sapi/v1/broker/subAccountApi/ipRestriction/ipList**
    ```python
    client.margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list(**params)
    ```

	- **GET /sapi/v1/staking/personalLeftQuota**
    ```python
    client.margin_v1_get_staking_personal_left_quota(**params)
    ```

	- **POST /sapi/v1/sub-account/virtualSubAccount**
    ```python
    client.margin_v1_post_sub_account_virtual_sub_account(**params)
    ```

	- **GET /sapi/v1/staking/position**
    ```python
    client.margin_v1_get_staking_position(**params)
    ```

	- **GET /papi/v1/um/income/asyn/id**
    ```python
    client.papi_v1_get_um_income_asyn_id(**params)
    ```

	- **PUT /sapi/v1/localentity/deposit/provide-info**
    ```python
    client.margin_v1_put_localentity_deposit_provide_info(**params)
    ```

	- **POST /sapi/v1/portfolio/mint**
    ```python
    client.margin_v1_post_portfolio_mint(**params)
    ```

	- **POST /sapi/v1/sub-account/transfer/subToSub**
    ```python
    client.margin_v1_post_sub_account_transfer_sub_to_sub(**params)
    ```

	- **GET /fapi/v1/orderAmendment**
    ```python
    client.futures_v1_get_order_amendment(**params)
    ```

	- **POST /sapi/v1/sol-staking/sol/claim**
    ```python
    client.margin_v1_post_sol_staking_sol_claim(**params)
    ```

	- **GET /sapi/v1/account/apiRestrictions**
    ```python
    client.margin_v1_get_account_api_restrictions(**params)
    ```

	- **GET /papi/v1/um/allOrders**
    ```python
    client.papi_v1_get_um_all_orders(**params)
    ```

	- **POST /sapi/v1/giftcard/createCode**
    ```python
    client.margin_v1_post_giftcard_create_code(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/rebalance/history**
    ```python
    client.margin_v1_get_lending_auto_invest_rebalance_history(**params)
    ```

	- **GET /sapi/v1/loan/repay/collateral/rate**
    ```python
    client.margin_v1_get_loan_repay_collateral_rate(**params)
    ```

	- **GET /sapi/v1/mining/payment/uid**
    ```python
    client.margin_v1_get_mining_payment_uid(**params)
    ```

	- **GET /sapi/v2/loan/flexible/borrow/history**
    ```python
    client.margin_v2_get_loan_flexible_borrow_history(**params)
    ```

	- **POST /sapi/v1/asset/dust**
    ```python
    client.margin_v1_post_asset_dust(**params)
    ```

	- **GET /sapi/v1/capital/contract/convertible-coins**
    ```python
    client.margin_v1_get_capital_contract_convertible_coins(**params)
    ```

	- **POST /sapi/v1/asset/dust-btc**
    ```python
    client.margin_v1_post_asset_dust_btc(**params)
    ```

	- **GET /papi/v1/um/conditional/openOrders**
    ```python
    client.papi_v1_get_um_conditional_open_orders(**params)
    ```

	- **GET /sapi/v1/sub-account/spotSummary**
    ```python
    client.margin_v1_get_sub_account_spot_summary(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/permission/vanillaOptions**
    ```python
    client.margin_v1_post_broker_sub_account_api_permission_vanilla_options(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/redeem/history**
    ```python
    client.margin_v1_get_lending_auto_invest_redeem_history(**params)
    ```

	- **GET /fapi/v3/positionRisk**
    ```python
    client.futures_v3_get_position_risk(**params)
    ```

	- **GET /dapi/v1/klines**
    ```python
    client.futures_coin_v1_get_klines(**params)
    ```

	- **GET /sapi/v2/localentity/withdraw/history**
    ```python
    client.margin_v2_get_localentity_withdraw_history(**params)
    ```

	- **GET /sapi/v1/eth-staking/eth/history/redemptionHistory**
    ```python
    client.margin_v1_get_eth_staking_eth_history_redemption_history(**params)
    ```

	- **POST /eapi/v1/transfer**
    ```python
    client.options_v1_post_transfer(**params)
    ```

	- **GET /fapi/v1/feeBurn**
    ```python
    client.futures_v1_get_fee_burn(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/index/user-summary**
    ```python
    client.margin_v1_get_lending_auto_invest_index_user_summary(**params)
    ```

	- **POST /sapi/v2/loan/flexible/borrow**
    ```python
    client.margin_v2_post_loan_flexible_borrow(**params)
    ```

	- **DELETE /dapi/v1/order**
    ```python
    client.futures_coin_v1_delete_order(**params)
    ```

	- **POST /sapi/v3/asset/getUserAsset**
    ```python
    client.margin_v3_post_asset_get_user_asset(**params)
    ```

	- **POST /sapi/v1/loan/vip/repay**
    ```python
    client.margin_v1_post_loan_vip_repay(**params)
    ```

	- **GET /sapi/v2/sub-account/futures/accountSummary**
    ```python
    client.margin_v2_get_sub_account_futures_account_summary(**params)
    ```

	- **GET /dapi/v1/commissionRate**
    ```python
    client.futures_coin_v1_get_commission_rate(**params)
    ```

	- **GET /papi/v1/um/conditional/orderHistory**
    ```python
    client.papi_v1_get_um_conditional_order_history(**params)
    ```

	- **GET /fapi/v3/balance**
    ```python
    client.futures_v3_get_balance(**params)
    ```

	- **GET /sapi/v1/convert/assetInfo**
    ```python
    client.margin_v1_get_convert_asset_info(**params)
    ```

	- **POST /api/v3/sor/order/test**
    ```python
    client.v3_post_sor_order_test(**params)
    ```

	- **GET /sapi/v1/giftcard/cryptography/rsa-public-key**
    ```python
    client.margin_v1_get_giftcard_cryptography_rsa_public_key(**params)
    ```

	- **POST /sapi/v1/broker/universalTransfer**
    ```python
    client.margin_v1_post_broker_universal_transfer(**params)
    ```

	- **GET /dapi/v1/allOrders**
    ```python
    client.futures_coin_v1_get_all_orders(**params)
    ```

	- **POST /sapi/v1/margin/borrow-repay**
    ```python
    client.margin_v1_post_margin_borrow_repay(**params)
    ```

	- **GET /fapi/v1/assetIndex**
    ```python
    client.futures_v1_get_asset_index(**params)
    ```

	- **GET /api/v3/rateLimit/order**
    ```python
    client.v3_get_rate_limit_order(**params)
    ```

	- **GET /papi/v1/um/orderAmendment**
    ```python
    client.papi_v1_get_um_order_amendment(**params)
    ```

	- **GET /sapi/v1/account/apiRestrictions/ipRestriction**
    ```python
    client.margin_v1_get_account_api_restrictions_ip_restriction(**params)
    ```

	- **POST /sapi/v1/broker/subAccount/bnbBurn/spot**
    ```python
    client.margin_v1_post_broker_sub_account_bnb_burn_spot(**params)
    ```

	- **POST /papi/v1/um/conditional/order**
    ```python
    client.papi_v1_post_um_conditional_order(**params)
    ```

	- **PUT /dapi/v1/batchOrders**
    ```python
    client.futures_coin_v1_put_batch_orders(**params)
    ```

	- **DELETE /api/v3/openOrders**
    ```python
    client.v3_delete_open_orders(**params)
    ```

	- **GET /sapi/v1/margin/delist-schedule**
    ```python
    client.margin_v1_get_margin_delist_schedule(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/permission/universalTransfer**
    ```python
    client.margin_v1_post_broker_sub_account_api_permission_universal_transfer(**params)
    ```

	- **GET /papi/v1/cm/positionRisk**
    ```python
    client.papi_v1_get_cm_position_risk(**params)
    ```

	- **GET /papi/v1/cm/income**
    ```python
    client.papi_v1_get_cm_income(**params)
    ```

	- **POST /sapi/v1/giftcard/buyCode**
    ```python
    client.margin_v1_post_giftcard_buy_code(**params)
    ```

	- **GET /fapi/v1/balance**
    ```python
    client.futures_v1_get_balance(**params)
    ```

	- **GET /api/v3/myAllocations**
    ```python
    client.v3_get_my_allocations(**params)
    ```

	- **GET /papi/v1/margin/order**
    ```python
    client.papi_v1_get_margin_order(**params)
    ```

	- **GET /sapi/v1/loan/ltv/adjustment/history**
    ```python
    client.margin_v1_get_loan_ltv_adjustment_history(**params)
    ```

	- **POST /dapi/v1/batchOrders**
    ```python
    client.futures_coin_v1_post_batch_orders(**params)
    ```

	- **GET /sapi/v1/localentity/withdraw/history**
    ```python
    client.margin_v1_get_localentity_withdraw_history(**params)
    ```

	- **GET /sapi/v1/sub-account/status**
    ```python
    client.margin_v1_get_sub_account_status(**params)
    ```

	- **POST /sapi/v2/sub-account/subAccountApi/ipRestriction**
    ```python
    client.margin_v2_post_sub_account_sub_account_api_ip_restriction(**params)
    ```

	- **GET /dapi/v1/trade/asyn/id**
    ```python
    client.futures_coin_v1_get_trade_asyn_id(**params)
    ```

	- **GET /fapi/v1/rateLimit/order**
    ```python
    client.futures_v1_get_rate_limit_order(**params)
    ```

	- **GET /sapi/v1/broker/subAccountApi/commission/futures**
    ```python
    client.margin_v1_get_broker_sub_account_api_commission_futures(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/history/stakingHistory**
    ```python
    client.margin_v1_get_sol_staking_sol_history_staking_history(**params)
    ```

	- **DELETE /sapi/v1/algo/spot/order**
    ```python
    client.margin_v1_delete_algo_spot_order(**params)
    ```

	- **GET /papi/v1/repay-futures-switch**
    ```python
    client.papi_v1_get_repay_futures_switch(**params)
    ```

	- **POST /sapi/v1/margin/max-leverage**
    ```python
    client.margin_v1_post_margin_max_leverage(**params)
    ```

	- **DELETE /sapi/v1/account/apiRestrictions/ipRestriction/ipList**
    ```python
    client.margin_v1_delete_account_api_restrictions_ip_restriction_ip_list(**params)
    ```

	- **POST /sapi/v1/capital/contract/convertible-coins**
    ```python
    client.margin_v1_post_capital_contract_convertible_coins(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/marginAsset**
    ```python
    client.margin_v1_get_managed_subaccount_margin_asset(**params)
    ```

	- **GET /sapi/v3/sub-account/assets**
    ```python
    client.margin_v3_get_sub_account_assets(**params)
    ```

	- **GET /fapi/v1/continuousKlines**
    ```python
    client.futures_v1_get_continuous_klines(**params)
    ```

	- **GET /sapi/v1/sub-account/futures/internalTransfer**
    ```python
    client.margin_v1_get_sub_account_futures_internal_transfer(**params)
    ```

	- **GET /sapi/v1/capital/withdraw/apply**
    ```python
    client.margin_v1_get_capital_withdraw_apply(**params)
    ```

	- **POST /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList**
    ```python
    client.margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list(**params)
    ```

	- **POST /sapi/v1/staking/setAutoStaking**
    ```python
    client.margin_v1_post_staking_set_auto_staking(**params)
    ```

	- **POST /fapi/v1/feeBurn**
    ```python
    client.futures_v1_post_fee_burn(**params)
    ```

	- **POST /sapi/v1/simple-earn/flexible/redeem**
    ```python
    client.margin_v1_post_simple_earn_flexible_redeem(**params)
    ```

	- **GET /sapi/v1/broker/subAccount/marginSummary**
    ```python
    client.margin_v1_get_broker_sub_account_margin_summary(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/plan/list**
    ```python
    client.margin_v1_get_lending_auto_invest_plan_list(**params)
    ```

	- **GET /sapi/v1/loan/vip/loanable/data**
    ```python
    client.margin_v1_get_loan_vip_loanable_data(**params)
    ```

	- **POST /sapi/v1/margin/exchange-small-liability**
    ```python
    client.margin_v1_post_margin_exchange_small_liability(**params)
    ```

	- **GET /sapi/v2/loan/flexible/collateral/data**
    ```python
    client.margin_v2_get_loan_flexible_collateral_data(**params)
    ```

	- **POST /papi/v1/margin/repay-debt**
    ```python
    client.papi_v1_post_margin_repay_debt(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/history/bnsolRewardsHistory**
    ```python
    client.margin_v1_get_sol_staking_sol_history_bnsol_rewards_history(**params)
    ```

	- **GET /sapi/v1/convert/limit/queryOpenOrders**
    ```python
    client.margin_v1_get_convert_limit_query_open_orders(**params)
    ```

	- **GET /api/v3/account/commission**
    ```python
    client.v3_get_account_commission(**params)
    ```

	- **GET /sapi/v1/margin/interestRateHistory**
    ```python
    client.margin_v1_get_margin_interest_rate_history(**params)
    ```

	- **POST /api/v3/orderList/oco**
    ```python
    client.v3_post_order_list_oco(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/query-trans-log**
    ```python
    client.margin_v1_get_managed_subaccount_query_trans_log(**params)
    ```

	- **POST /sapi/v2/broker/subAccountApi/ipRestriction**
    ```python
    client.margin_v2_post_broker_sub_account_api_ip_restriction(**params)
    ```

	- **GET /papi/v1/um/positionRisk**
    ```python
    client.papi_v1_get_um_position_risk(**params)
    ```

	- **POST /sapi/v1/sub-account/margin/transfer**
    ```python
    client.margin_v1_post_sub_account_margin_transfer(**params)
    ```

	- **GET /fapi/v1/positionRisk**
    ```python
    client.futures_v1_get_position_risk(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/all/asset**
    ```python
    client.margin_v1_get_lending_auto_invest_all_asset(**params)
    ```

	- **POST /fapi/v1/convert/acceptQuote**
    ```python
    client.futures_v1_post_convert_accept_quote(**params)
    ```

	- **GET /sapi/v1/spot/delist-schedule**
    ```python
    client.margin_v1_get_spot_delist_schedule(**params)
    ```

	- **GET /sapi/v1/dci/product/accounts**
    ```python
    client.margin_v1_get_dci_product_accounts(**params)
    ```

	- **GET /sapi/v1/sub-account/subAccountApi/ipRestriction**
    ```python
    client.margin_v1_get_sub_account_sub_account_api_ip_restriction(**params)
    ```

	- **GET /papi/v1/um/accountConfig**
    ```python
    client.papi_v1_get_um_account_config(**params)
    ```

	- **GET /papi/v1/cm/adlQuantile**
    ```python
    client.papi_v1_get_cm_adl_quantile(**params)
    ```

	- **GET /sapi/v1/sub-account/transaction-statistics**
    ```python
    client.margin_v1_get_sub_account_transaction_statistics(**params)
    ```

	- **PUT /fapi/v1/listenKey**
    ```python
    client.futures_v1_put_listen_key(**params)
    ```

	- **GET /sapi/v1/margin/openOrderList**
    ```python
    client.margin_v1_get_margin_open_order_list(**params)
    ```

	- **GET /api/v3/acccount**
    ```python
    client.v3_get_acccount(**params)
    ```

	- **GET /sapi/v1/fiat/orders**
    ```python
    client.margin_v1_get_fiat_orders(**params)
    ```

	- **GET /papi/v1/margin/allOrders**
    ```python
    client.papi_v1_get_margin_all_orders(**params)
    ```

	- **POST /sapi/v1/sub-account/margin/enable**
    ```python
    client.margin_v1_post_sub_account_margin_enable(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/deposit/address**
    ```python
    client.margin_v1_get_managed_subaccount_deposit_address(**params)
    ```

	- **DELETE /sapi/v1/margin/isolated/account**
    ```python
    client.margin_v1_delete_margin_isolated_account(**params)
    ```

	- **GET /sapi/v2/portfolio/account**
    ```python
    client.margin_v2_get_portfolio_account(**params)
    ```

	- **GET /sapi/v1/simple-earn/locked/history/redemptionRecord**
    ```python
    client.margin_v1_get_simple_earn_locked_history_redemption_record(**params)
    ```

	- **GET /fapi/v1/order/asyn/id**
    ```python
    client.futures_v1_get_order_asyn_id(**params)
    ```

	- **POST /sapi/v1/managed-subaccount/withdraw**
    ```python
    client.margin_v1_post_managed_subaccount_withdraw(**params)
    ```

	- **GET /sapi/v1/convert/tradeFlow**
    ```python
    client.margin_v1_get_convert_trade_flow(**params)
    ```

	- **GET /sapi/v1/localentity/deposit/history**
    ```python
    client.margin_v1_get_localentity_deposit_history(**params)
    ```

	- **POST /sapi/v1/eth-staking/wbeth/wrap**
    ```python
    client.margin_v1_post_eth_staking_wbeth_wrap(**params)
    ```

	- **POST /sapi/v1/simple-earn/locked/setRedeemOption**
    ```python
    client.margin_v1_post_simple_earn_locked_set_redeem_option(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/ipRestriction/ipList**
    ```python
    client.margin_v1_post_broker_sub_account_api_ip_restriction_ip_list(**params)
    ```

	- **POST /sapi/v1/broker/subAccountApi/commission/futures**
    ```python
    client.margin_v1_post_broker_sub_account_api_commission_futures(**params)
    ```

	- **GET /papi/v1/margin/myTrades**
    ```python
    client.papi_v1_get_margin_my_trades(**params)
    ```

	- **GET /sapi/v1/pay/transactions**
    ```python
    client.margin_v1_get_pay_transactions(**params)
    ```

	- **GET /papi/v1/um/leverageBracket**
    ```python
    client.papi_v1_get_um_leverage_bracket(**params)
    ```

	- **GET /papi/v1/margin/orderList**
    ```python
    client.papi_v1_get_margin_order_list(**params)
    ```

	- **GET /dapi/v1/allForceOrders**
    ```python
    client.futures_coin_v1_get_all_force_orders(**params)
    ```

	- **GET /sapi/v1/margin/isolated/accountLimit**
    ```python
    client.margin_v1_get_margin_isolated_account_limit(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/history/list**
    ```python
    client.margin_v1_get_lending_auto_invest_history_list(**params)
    ```

	- **GET /dapi/v1/account**
    ```python
    client.futures_coin_v1_get_account(**params)
    ```

	- **GET /dapi/v1/markPriceKlines**
    ```python
    client.futures_coin_v1_get_mark_price_klines(**params)
    ```

	- **POST /sapi/v1/loan/customize/margin_call**
    ```python
    client.margin_v1_post_loan_customize_margin_call(**params)
    ```

	- **GET /sapi/v1/broker/subAccount/bnbBurn/status**
    ```python
    client.margin_v1_get_broker_sub_account_bnb_burn_status(**params)
    ```

	- **DELETE /eapi/v1/block/order/create**
    ```python
    client.options_v1_delete_block_order_create(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/accountSnapshot**
    ```python
    client.margin_v1_get_managed_subaccount_account_snapshot(**params)
    ```

	- **GET /fapi/v1/constituents**
    ```python
    client.futures_v1_get_constituents(**params)
    ```

	- **GET /dapi/v1/indexPriceKlines**
    ```python
    client.futures_coin_v1_get_index_price_klines(**params)
    ```

	- **GET /sapi/v1/broker/subAccountApi/commission/coinFutures**
    ```python
    client.margin_v1_get_broker_sub_account_api_commission_coin_futures(**params)
    ```

	- **GET /sapi/v2/broker/subAccount/futuresSummary**
    ```python
    client.margin_v2_get_broker_sub_account_futures_summary(**params)
    ```

	- **GET /sapi/v1/sub-account/transfer/subUserHistory**
    ```python
    client.margin_v1_get_sub_account_transfer_sub_user_history(**params)
    ```

	- **POST /sapi/v1/sub-account/futures/internalTransfer**
    ```python
    client.margin_v1_post_sub_account_futures_internal_transfer(**params)
    ```

	- **GET /sapi/v1/loan/ongoing/orders**
    ```python
    client.margin_v1_get_loan_ongoing_orders(**params)
    ```

	- **GET /sapi/v2/loan/flexible/ongoing/orders**
    ```python
    client.margin_v2_get_loan_flexible_ongoing_orders(**params)
    ```

	- **GET /eapi/v1/block/order/execute**
    ```python
    client.options_v1_get_block_order_execute(**params)
    ```

	- **GET /papi/v2/um/account**
    ```python
    client.papi_v2_get_um_account(**params)
    ```

	- **POST /sapi/v1/margin/order/oco**
    ```python
    client.margin_v1_post_margin_order_oco(**params)
    ```

	- **GET /api/v1/portfolio/negative-balance-exchange-record**
    ```python
    client.v1_get_portfolio_negative_balance_exchange_record(**params)
    ```

	- **POST /sapi/v1/algo/futures/newOrderVp**
    ```python
    client.margin_v1_post_algo_futures_new_order_vp(**params)
    ```

	- **DELETE /papi/v1/um/order**
    ```python
    client.papi_v1_delete_um_order(**params)
    ```

	- **POST /fapi/v1/convert/getQuote**
    ```python
    client.futures_v1_post_convert_get_quote(**params)
    ```

	- **GET /sapi/v1/algo/spot/subOrders**
    ```python
    client.margin_v1_get_algo_spot_sub_orders(**params)
    ```

	- **GET /dapi/v1/userTrades**
    ```python
    client.futures_coin_v1_get_user_trades(**params)
    ```

	- **POST /papi/v1/um/feeBurn**
    ```python
    client.papi_v1_post_um_fee_burn(**params)
    ```

	- **POST /sapi/v1/portfolio/redeem**
    ```python
    client.margin_v1_post_portfolio_redeem(**params)
    ```

	- **POST /fapi/v1/multiAssetsMargin**
    ```python
    client.futures_v1_post_multi_assets_margin(**params)
    ```

	- **POST /sapi/v1/lending/auto-invest/plan/add**
    ```python
    client.margin_v1_post_lending_auto_invest_plan_add(**params)
    ```

	- **GET /eapi/v1/historyOrders**
    ```python
    client.options_v1_get_history_orders(**params)
    ```

	- **GET /sapi/v1/lending/auto-invest/source-asset/list**
    ```python
    client.margin_v1_get_lending_auto_invest_source_asset_list(**params)
    ```

	- **GET /sapi/v1/margin/allOrderList**
    ```python
    client.margin_v1_get_margin_all_order_list(**params)
    ```

	- **POST /sapi/v1/eth-staking/eth/redeem**
    ```python
    client.margin_v1_post_eth_staking_eth_redeem(**params)
    ```

	- **GET /sapi/v1/broker/rebate/historicalRecord**
    ```python
    client.margin_v1_get_broker_rebate_historical_record(**params)
    ```

	- **GET /sapi/v1/simple-earn/locked/history/subscriptionRecord**
    ```python
    client.margin_v1_get_simple_earn_locked_history_subscription_record(**params)
    ```

	- **PUT /dapi/v1/order**
    ```python
    client.futures_coin_v1_put_order(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/asset**
    ```python
    client.margin_v1_get_managed_subaccount_asset(**params)
    ```

	- **GET /sapi/v1/sol-staking/sol/quota**
    ```python
    client.margin_v1_get_sol_staking_sol_quota(**params)
    ```

	- **POST /sapi/v1/loan/vip/renew**
    ```python
    client.margin_v1_post_loan_vip_renew(**params)
    ```

	- **POST /dapi/v1/order**
    ```python
    client.futures_coin_v1_post_order(**params)
    ```

	- **GET /sapi/v1/managed-subaccount/queryTransLogForTradeParent**
    ```python
    client.margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent(**params)
    ```

	- **GET /sapi/v1/simple-earn/flexible/history/redemptionRecord**
    ```python
    client.margin_v1_get_simple_earn_flexible_history_redemption_record(**params)
    ```

	- **GET /sapi/v1/sub-account/margin/accountSummary**
    ```python
    client.margin_v1_get_sub_account_margin_account_summary(**params)
    ```

	- **GET /sapi/v1/margin/dribblet**
    ```python
    client.margin_v1_get_margin_dribblet(**params)
    ```

	- **GET /eapi/v1/exerciseHistory**
    ```python
    client.options_v1_get_exercise_history(**params)
    ```

	- **GET /sapi/v1/convert/exchangeInfo**
    ```python
    client.margin_v1_get_convert_exchange_info(**params)
    ```

	- **GET /sapi/v1/eth-staking/eth/history/wbethRewardsHistory**
    ```python
    client.margin_v1_get_eth_staking_eth_history_wbeth_rewards_history(**params)
    ```

	- **GET /sapi/v1/simple-earn/locked/position**
    ```python
    client.margin_v1_get_simple_earn_locked_position(**params)
    ```

	- **GET /sapi/v1/mining/pub/algoList**
    ```python
    client.margin_v1_get_mining_pub_algo_list(**params)
    ```

	- **GET /dapi/v1/ticker/bookTicker**
    ```python
    client.futures_coin_v1_get_ticker_book_ticker(**params)
    ```

	- **GET /eapi/v1/blockTrades**
    ```python
    client.options_v1_get_block_trades(**params)
    ```

	- **GET /sapi/v1/copyTrading/futures/leadSymbol**
    ```python
    client.margin_v1_get_copy_trading_futures_lead_symbol(**params)
    ```

	- **GET /papi/v1/cm/orderAmendment**
    ```python
    client.papi_v1_get_cm_order_amendment(**params)
    ```

	- **GET /sapi/v4/sub-account/assets**
    ```python
    client.margin_v4_get_sub_account_assets(**params)
    ```

	- **GET /sapi/v1/mining/worker/list**
    ```python
    client.margin_v1_get_mining_worker_list(**params)
    ```

	- **DELETE /sapi/v1/margin/openOrders**
    ```python
    client.margin_v1_delete_margin_open_orders(**params)
    ```

	- **GET /dapi/v1/constituents**
    ```python
    client.futures_coin_v1_get_constituents(**params)
    ```

	- **GET /sapi/v1/dci/product/list**
    ```python
    client.margin_v1_get_dci_product_list(**params)
    ```

	- **GET /fapi/v1/convert/orderStatus**
    ```python
    client.futures_v1_get_convert_order_status(**params)
    ```


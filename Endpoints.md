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

    > :warning: Not yet implemented
  - **GET /futures/data/topLongShortAccountRatio** (Top Trader Long/Short Ratio (Accounts) (MARKET_DATA).)

    > :warning: Not yet implemented
  - **GET /futures/data/topLongShortPositionRatio** (Top Trader Long/Short Ratio (Positions).)

    > :warning: Not yet implemented
  - **GET /futures/data/globalLongShortAccountRatio** (Long/Short Ratio.)

    > :warning: Not yet implemented
  - **GET /futures/data/takerlongshortRatio** (Taker Buy/Sell Volume.)

    > :warning: Not yet implemented
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

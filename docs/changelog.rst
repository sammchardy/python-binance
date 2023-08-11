Changelog
=========

v1.0.19 - 2023-08-11
^^^^^^^^^^^^^^^^^^^^

**Added**

- some new futures and margin endpoints
- pass session_params to streams for AsyncClient

**Fixed**

- removed debug statements
- options testnet URL
- accessing msg variable before assignment

v1.0.18 - 2023-08-09
^^^^^^^^^^^^^^^^^^^^

**Added**

- TRAILING_STOP_MARKET option for orders

**Fixed**

- futures api endpoint versions
- margin endpoint request methods


v1.0.17 - 2023-02-21
^^^^^^^^^^^^^^^^^^^^

**Added**

- RSA key authentication
- Support for api1, api2, api3, api4 base endpoints
- binance.us staking endpoints
- Options ticker by expiration socket
- Staking endpoints
- Pay and Convert endpoints
- Futures index info endpoint
- Open OCO Orders endpoint
- Param to pass session params to aiohttp.ClientSession

**Updated**

- Some margin endpoint versions
- Support testnet for more streams

**Fixed**

- Indefinite websocket reconnect loop
- Crash on parsing code from some errors

v1.0.16 - 2022-04-09
^^^^^^^^^^^^^^^^^^^^

**Added**

- pass limit param to all kline functions
- increase default for kline functions from 500 to 1000
- add HistoricalKlinesType.FUTURES_COIN as option for kline functions
- testnet URL for coin_futures_socket

**Updated**

- round_step_size more accurate

**Fixed**

- remove deprecated loop param
- websockets unpinned
- hanging websockets in exiting state
- check start_ts after end_ts for klines
- multi assets margin params


v1.0.15 - 2021-09-27
^^^^^^^^^^^^^^^^^^^^

**Added**

- Enable/disable margin account for symbol endpoints
- Top trader long/short positions endpoint
- Global long/short ratio endpoint

**Fixed**

- fix websockets to 9.1
- websocket reconnect updates
- fix futures kline sockets


v1.0.14 - 2021-09-08
^^^^^^^^^^^^^^^^^^^^

**Fixed**

- websocket reconnecting

v1.0.13 - 2021-09-08
^^^^^^^^^^^^^^^^^^^^

**Added**

- Futures Depth Cache Manager
- Futures kline websocket stream
- Coin Futures User websocket stream
- New Margin endpoints
- Margin OCO order endpoints
- Fiat endpoints
- C2C endpoints
- Account API permissions endpoint

**Fixed**

- changed `asset` to `coin` in withdraw endpoint


v1.0.12 - 2021-06-03
^^^^^^^^^^^^^^^^^^^^

**Added**

- coin futures batch order function

**Fixed**

- threaded websockets on python3.9
- filter out None params in request kwargs
- deconflict streams with same name on different websocket urls
- reduce close timeout on websocket close to short time to reduce waiting


v1.0.10 - 2021-05-13
^^^^^^^^^^^^^^^^^^^^

**Added**

- futures multi-asset margin mode endpoints
- optional symbol param to get_all_tickers

**Fixed**

- start_multiplex_socket remove lower case filter on stream names

v1.0.9 - 2021-05-12
^^^^^^^^^^^^^^^^^^^

**Fixed**

- start_book_ticker_socket and start_multiplex_socket to call correct async function

v1.0.8 - 2021-05-11
^^^^^^^^^^^^^^^^^^^

**Added**

- old style websocket and depth cache managers as option without interacting with asyncio

**Fixed**

- fixed issue with get_historical_klines in Client
- remove print debug line

v1.0.7
^^^^^^

**Fixed**

- remove version param from get_sub_account_assets

v1.0.6
^^^^^^

**Fixed**

- fix time for authenticated stream keepalive

v1.0.5
^^^^^^

**Fixed**

- Restored access to last response on client

v1.0.4
^^^^^^

**Added**

- Futures Testnet support
- Kline type for fetching historical klines

**Fixed**

- Spot Testnet websocket URL

v1.0.3
^^^^^^

**Added**

- Spot Testnet support

v1.0.2
^^^^^^

**Added**

- start of typing to client and websockets

**Fixed**

- end_str, limit, spot params in kline fetching
- drop None values in params passed

**Updated**

- more examples in docs

v1.0.1
^^^^^^

**Fixed**

- restored params for Client and AsyncClient classes

v1.0.0
^^^^^^

**Added**

- Async support for all REST endpoints
- USDⓈ-M and Coin-M Futures websocket streams
- Websockets use same tld as Client
- convert type option for DepthCache

**Breaking Changes**

- Supports only py3.6+
- All wapi calls changed to sapi
- Websockets have changed to use Asynchronous context managers

**Fixed**

- get_historical_klines params

v0.7.11
^^^^^^^

**Added**
- Vanilla Options REST endpoints
- Vanilla Options websockets
- Futures order type enums

**Updated**

- websocket keep-alive functions for different socket types
- dependencies

**Fixed**

- change to User-Agent to avoid connection issues

v0.7.5.dev
^^^^^^^^^^
**Changed**
- Stock json lib to ujson (https://github.com/sammchardy/python-binance/pull/383)

v0.7.5 - 2020-02-06
^^^^^^^^^^^^^^^^^^^

**Added**

- Futures REST endpoints
- Lending REST endpoints
- OCO Orders function `create_oco_order`, `order_oco_buy`, `order_oco_sell`
- Average Price function `get_avg_price`
- Support for other domains (.us, .jp, etc)

**Updated**

- dependencies

**Fixed**

- websocket keepalive callback not found

v0.7.4 - 2019-09-22
^^^^^^^^^^^^^^^^^^^

**Added**

- symbol book ticker websocket streams
- margin websocket stream

**Updated**

- can call Client without any params
- make response a property of the Client class so you can access response properties after a request

**Fixed**

- issue with None value params causing errors

v0.7.3 - 2019-08-12
^^^^^^^^^^^^^^^^^^^

**Added**

- sub account endpoints
- dust transfer endpoint
- asset divident history endpoint

**Removed**

- deprecated withdraw fee endpoint

v0.7.2 - 2019-08-01
^^^^^^^^^^^^^^^^^^^

**Added**

- margin trading endpoints

**Fixed**

- depth cache clearing bug

v0.7.1 - 2019-01-23
^^^^^^^^^^^^^^^^^^^

**Added**

- limit param to DepthCacheManager
- limit param to get_historical_klines
- update_time to DepthCache class

**Updated**

- test coverage

**Fixed**

- super init in Websocket class
- removal of request params from signature
- empty set issue in aggregate_trade_iter


v0.7.0 - 2018-08-08
^^^^^^^^^^^^^^^^^^^

**Added**

- get_asset_details endpoint
- get_dust_log endpoint
- get_trade_fee endpoint
- ability for multiple DepthCacheManagers to share a BinanceSocketManager
- get_historial_klines_generator function
- custom socket timeout param for BinanceSocketManager

**Updated**

- general dependency version
- removed support for python3.3

**Fixed**

- add a super init on BinanceClientProtocol

v0.6.9 - 2018-04-27
^^^^^^^^^^^^^^^^^^^

**Added**

- timestamp in milliseconds to `get_historical_klines` function
- timestamp in milliseconds to `aggregate_trade_iter` function

**Fixed**

- Don't close user stream listen key on socket close

v0.6.8 - 2018-03-29
^^^^^^^^^^^^^^^^^^^

**Added**

- `get_withdraw_fee` function

**Fixed**

- Remove unused LISTENKEY_NOT_EXISTS
- Optimise the historical klines function to reduce requests
- Issue with end_time in aggregate trade iterator

v0.6.7 - 2018-03-14
^^^^^^^^^^^^^^^^^^^

**Fixed**

- Issue with `get_historical_klines` when response had exactly 500 results
- Changed BinanceResponseException to BinanceRequestException
- Set default code value in BinanceApiException properly

v0.6.6 - 2018-02-17
^^^^^^^^^^^^^^^^^^^

**Fixed**

- User stream websocket keep alive strategy updated

v0.6.5 - 2018-02-13
^^^^^^^^^^^^^^^^^^^

**Fixed**

- `get_historical_klines` response for month interval

v0.6.4 - 2018-02-09
^^^^^^^^^^^^^^^^^^^

**Added**

- system status endpoint `get_system_status`

v0.6.3 - 2018-01-29
^^^^^^^^^^^^^^^^^^^

**Added**

- mini ticker socket function `start_miniticker_socket`
- aggregate trade iterator `aggregate_trade_iter`

**Fixes**

- clean up `interval_to_milliseconds` logic
- general doc and file cleanups

v0.6.2 - 2018-01-12
^^^^^^^^^^^^^^^^^^^

**Fixes**

- fixed handling Binance errors that aren't JSON objects

v0.6.1 - 2018-01-10
^^^^^^^^^^^^^^^^^^^

**Fixes**

- added missing dateparser dependency to setup.py
- documentation fixes

v0.6.0 - 2018-01-09
^^^^^^^^^^^^^^^^^^^

New version because why not.

**Added**

- get_historical_klines function to fetch klines for any date range
- ability to override requests parameters globally
- error on websocket disconnect
- example related to blog post

**Fixes**

- documentation fixes

v0.5.17 - 2018-01-08
^^^^^^^^^^^^^^^^^^^^

**Added**

- check for name parameter in withdraw, set to asset parameter if not passed

**Update**

- Windows install error documentation

**Removed**

- reference to disable_validation in documentation

v0.5.16 - 2018-01-06
^^^^^^^^^^^^^^^^^^^^

**Added**

- addressTag documentation to withdraw function
- documentation about requests proxy environment variables

**Update**

- FAQ for signature error with solution to regenerate API key
- change create_order to create_test_order in example

**Fixed**

- reference to BinanceAPIException in documentation

v0.5.15 - 2018-01-03
^^^^^^^^^^^^^^^^^^^^

**Fixed**

- removed all references to WEBSOCKET_DEPTH_1 enum

v0.5.14 - 2018-01-02
^^^^^^^^^^^^^^^^^^^^

**Added**

- Wait for depth cache socket to start
- check for sequential depth cache messages

**Updated**

- documentation around depth websocket and diff and partial responses

**Removed**

- Removed unused WEBSOCKET_DEPTH_1 enum
- removed unused libraries and imports

v0.5.13 - 2018-01-01
^^^^^^^^^^^^^^^^^^^^

**Fixed**

- Signature invalid error

v0.5.12 - 2017-12-29
^^^^^^^^^^^^^^^^^^^^

**Added**

- get_asset_balance helper function to fetch an individual asset's balance

**Fixed**

- added timeout to requests call to prevent hanging
- changed variable type to str for price parameter when creating an order
- documentation fixes

v0.5.11 - 2017-12-28
^^^^^^^^^^^^^^^^^^^^

**Added**

- refresh interval parameter to depth cache to keep it fresh, set default at 30 minutes

**Fixed**

- watch depth cache socket before fetching order book to replay any messages

v0.5.10 - 2017-12-28
^^^^^^^^^^^^^^^^^^^^

**Updated**

- updated dependencies certifi and cryptography to help resolve signature error

v0.5.9 - 2017-12-26
^^^^^^^^^^^^^^^^^^^

**Fixed**

- fixed websocket reconnecting, was no distinction between manual close or network error

v0.5.8 - 2017-12-25
^^^^^^^^^^^^^^^^^^^

**Changed**

- change symbol parameter to optional for get_open_orders function
- added listenKey parameter to stream_close function

**Added**

- get_account_status function that was missed

v0.5.7 - 2017-12-24
^^^^^^^^^^^^^^^^^^^

**Changed**

- change depth cache callback parameter to optional

**Added**

- note about stopping Twisted reactor loop to exit program

v0.5.6 - 2017-12-20
^^^^^^^^^^^^^^^^^^^

**Added**

- get_symbol_info function to simplify getting info about a particular symbol

v0.5.5 - 2017-12-19
^^^^^^^^^^^^^^^^^^^

**Changed**

- Increased default limit for order book on depth cache from 10 to 500

v0.5.4 - 2017-12-14
^^^^^^^^^^^^^^^^^^^

**Added**

- symbol property made public on DepthCache class

**Changed**

- Enums now also accessible from binance.client.Client and binance.websockets.BinanceSocketManager

v0.5.3 - 2017-12-09
^^^^^^^^^^^^^^^^^^^

**Changed**

- User stream refresh timeout from 50 minutes to 30 minutes
- User stream socket listen key change check simplified

v0.5.2 - 2017-12-08
^^^^^^^^^^^^^^^^^^^

**Added**

- start_multiplex_socket function to BinanceSocketManager to create multiplexed streams

v0.5.1 - 2017-12-06
^^^^^^^^^^^^^^^^^^^

**Added**

- Close method for DepthCacheManager

**Fixes**

- Fixed modifying array error message when closing the BinanceSocketManager

v0.5.0 - 2017-12-05
^^^^^^^^^^^^^^^^^^^

Updating to match new API documentation

**Added**

- Recent trades endpoint
- Historical trades endpoint
- Order response type option
- Check for invalid user stream listen key in socket to keep connected

**Fixes**

- Fixed exchange info endpoint as it was renamed slightly

v0.4.3 - 2017-12-04
^^^^^^^^^^^^^^^^^^^

**Fixes**

- Fixed stopping sockets where they were reconnecting
- Fixed websockets unable to be restarted after close
- Exception in parsing non-JSON websocket message

v0.4.2 - 2017-11-30
^^^^^^^^^^^^^^^^^^^

**Removed**

- Removed websocket update time as 0ms option is not available

v0.4.1 - 2017-11-24
^^^^^^^^^^^^^^^^^^^

**Added**

- Reconnecting websockets, automatic retry on disconnect

v0.4.0 - 2017-11-19
^^^^^^^^^^^^^^^^^^^

**Added**

- Get deposit address endpoint
- Upgraded withdraw endpoints to v3
- New exchange info endpoint with rate limits and full symbol info

**Removed**

- Order validation to return at a later date

v0.3.8 - 2017-11-17
^^^^^^^^^^^^^^^^^^^

**Fixes**

- Fix order validation for market orders
- WEBSOCKET_DEPTH_20 value, 20 instead of 5
- General tidy up

v0.3.7 - 2017-11-16
^^^^^^^^^^^^^^^^^^^

**Fixes**

- Fix multiple depth caches sharing a cache by initialising bid and ask objects each time

v0.3.6 - 2017-11-15
^^^^^^^^^^^^^^^^^^^

**Fixes**

- check if Reactor is already running

v0.3.5 - 2017-11-06
^^^^^^^^^^^^^^^^^^^

**Added**

- support for BNB market

**Fixes**

- fixed error if new market type is created that we don't know about

v0.3.4 - 2017-10-31
^^^^^^^^^^^^^^^^^^^

**Added**

- depth parameter to depth socket
- interval parameter to kline socket
- update time parameter for compatible sockets
- new enums for socket depth and update time values
- better websocket documentation

**Changed**

- Depth Cache Manager uses 0ms socket update time
- connection key returned when creating socket, this key is then used to stop it

**Fixes**

- General fixes

v0.3.3 - 2017-10-31
^^^^^^^^^^^^^^^^^^^

**Fixes**

- Fixes for broken tests

v0.3.2 - 2017-10-30
^^^^^^^^^^^^^^^^^^^

**Added**

- More test coverage of requests

**Fixes**

- Order quantity validation fix

v0.3.1 - 2017-10-29
^^^^^^^^^^^^^^^^^^^

**Added**

- Withdraw exception handler with translation of obscure error

**Fixes**

- Validation fixes

v0.3.0 - 2017-10-29
^^^^^^^^^^^^^^^^^^^

**Added**

- Withdraw endpoints
- Order helper functions

v0.2.0 - 2017-10-27
^^^^^^^^^^^^^^^^^^^

**Added**

- Symbol Depth Cache

v0.1.6 - 2017-10-25
^^^^^^^^^^^^^^^^^^^

**Changes**

- Upgrade to v3 signed endpoints
- Update function documentation


v0.1.5 - 2017-09-12
^^^^^^^^^^^^^^^^^^^

**Changes**

- Added get_all_tickers call
- Added get_orderbook_tickers call
- Added some FAQs

**Fixes**

- Fix error in enum value

v0.1.4 - 2017-09-06
^^^^^^^^^^^^^^^^^^^

**Changes**

- Added parameter to disable client side order validation

v0.1.3 - 2017-08-26
^^^^^^^^^^^^^^^^^^^

**Changes**

- Updated documentation

**Fixes**

- Small bugfix

v0.1.2 - 2017-08-25
^^^^^^^^^^^^^^^^^^^

**Added**

- Travis.CI and Coveralls support

**Changes**

- Validation for pairs using public endpoint

v0.1.1 - 2017-08-17
^^^^^^^^^^^^^^^^^^^

**Added**

- Validation for HSR/BTC pair

v0.1.0 - 2017-08-16
^^^^^^^^^^^^^^^^^^^

Websocket release

**Added**

- Websocket manager
- Order parameter validation
- Order and Symbol enums
- API Endpoints for Data Streams

v0.0.2 - 2017-08-14
^^^^^^^^^^^^^^^^^^^

Initial version

**Added**

- General, Market Data and Account endpoints

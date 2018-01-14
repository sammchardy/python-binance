Changelog
=========

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

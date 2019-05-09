# coding=utf-8

import aiohttp
import asyncio
import time

from .helpers import date_to_milliseconds, interval_to_milliseconds, convert_ts_str
from .exceptions import BinanceAPIException, BinanceRequestException, BinanceWithdrawException
from .client import BaseClient, Client


class AsyncClient(BaseClient):

    @classmethod
    async def create(cls, api_key, api_secret, requests_params=None):

        self = AsyncClient(api_key, api_secret, requests_params)

        await self.ping()

        return self

    def _init_session(self):

        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession(
            loop=loop,
            headers=self._get_headers()
        )
        return session

    async def _request(self, method, uri, signed, force_params=False, **kwargs):

        kwargs = self._get_request_kwargs(method, signed, force_params, **kwargs)

        async with getattr(self.session, method)(uri, **kwargs) as response:
            return await self._handle_response(response)

    async def _handle_response(self, response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status).startswith('2'):
            raise BinanceAPIException(response, response.status, await response.text())
        try:
            return await response.json()
        except ValueError:
            txt = await response.text()
            raise BinanceRequestException('Invalid Response: {}'.format(txt))

    async def _request_api(self, method, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        uri = self._create_api_uri(path, signed, version)
        return await self._request(method, uri, signed, **kwargs)

    async def _request_withdraw_api(self, method, path, signed=False, **kwargs):
        uri = self._create_withdraw_api_uri(path)
        return await self._request(method, uri, signed, True, **kwargs)

    async def _request_website(self, method, path, signed=False, **kwargs):
        uri = self._create_website_uri(path)
        return await self._request(method, uri, signed, **kwargs)

    async def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return await self._request_api('get', path, signed, version, **kwargs)

    async def _post(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return await self._request_api('post', path, signed, version, **kwargs)

    async def _put(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return await self._request_api('put', path, signed, version, **kwargs)

    async def _delete(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return await self._request_api('delete', path, signed, version, **kwargs)

    # Exchange Endpoints

    async def get_products(self):
        products = await self._request_website('get', 'exchange/public/product')
        return products
    get_products.__doc__ = Client.get_products.__doc__

    async def get_exchange_info(self):
        return await self._get('exchangeInfo')
    get_exchange_info.__doc__ = Client.get_exchange_info.__doc__

    async def get_symbol_info(self, symbol):
        res = await self.get_exchange_info()

        for item in res['symbols']:
            if item['symbol'] == symbol.upper():
                return item

        return None
    get_symbol_info.__doc__ = Client.get_symbol_info.__doc__

    # General Endpoints

    async def ping(self):
        return await self._get('ping')
    ping.__doc__ = Client.ping.__doc__

    async def get_server_time(self):
        return await self._get('time')
    get_server_time.__doc__ = Client.get_server_time.__doc__

    # Market Data Endpoints

    async def get_all_tickers(self):
        return await self._get('ticker/allPrices')
    get_all_tickers.__doc__ = Client.get_all_tickers.__doc__

    async def get_orderbook_tickers(self):
        return await self._get('ticker/allBookTickers')
    get_orderbook_tickers.__doc__ = Client.get_orderbook_tickers.__doc__

    async def get_order_book(self, **params):
        return await self._get('depth', data=params)
    get_order_book.__doc__ = Client.get_order_book.__doc__

    async def get_recent_trades(self, **params):
        return await self._get('trades', data=params)
    get_recent_trades.__doc__ = Client.get_recent_trades.__doc__

    async def get_historical_trades(self, **params):
        return await self._get('historicalTrades', data=params)
    get_historical_trades.__doc__ = Client.get_historical_trades.__doc__

    async def get_aggregate_trades(self, **params):
        return await self._get('aggTrades', data=params)
    get_aggregate_trades.__doc__ = Client.get_aggregate_trades.__doc__

    async def aggregate_trade_iter(self, symbol, start_str=None, last_id=None):
        if start_str is not None and last_id is not None:
            raise ValueError(
                'start_time and last_id may not be simultaneously specified.')

        # If there's no last_id, get one.
        if last_id is None:
            # Without a last_id, we actually need the first trade.  Normally,
            # we'd get rid of it. See the next loop.
            if start_str is None:
                trades = await self.get_aggregate_trades(symbol=symbol, fromId=0)
            else:
                # The difference between startTime and endTime should be less
                # or equal than an hour and the result set should contain at
                # least one trade.
                start_ts = convert_ts_str(start_str)
                # If the resulting set is empty (i.e. no trades in that interval)
                # then we just move forward hour by hour until we find at least one
                # trade or reach present moment
                while True:
                    end_ts = start_ts + (60 * 60 * 1000)
                    trades = await self.get_aggregate_trades(
                        symbol=symbol,
                        startTime=start_ts,
                        endTime=end_ts)
                    if len(trades) > 0:
                        break
                    # If we reach present moment and find no trades then there is
                    # nothing to iterate, so we're done
                    if end_ts > int(time.time() * 1000):
                        return
                    start_ts = end_ts
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]

        while True:
            # There is no need to wait between queries, to avoid hitting the
            # rate limit. We're using blocking IO, and as long as we're the
            # only thread running calls like this, Binance will automatically
            # add the right delay time on their end, forcing us to wait for
            # data. That really simplifies this function's job. Binance is
            # fucking awesome.
            trades = await self.get_aggregate_trades(symbol=symbol, fromId=last_id)
            # fromId=n returns a set starting with id n, but we already have
            # that one. So get rid of the first item in the result set.
            trades = trades[1:]
            if len(trades) == 0:
                return
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]
    aggregate_trade_iter.__doc__ = Client.aggregate_trade_iter.__doc__

    async def get_klines(self, **params):
        return await self._get('klines', data=params)
    get_klines.__doc__ = Client.get_klines.__doc__

    async def _get_earliest_valid_timestamp(self, symbol, interval):
        kline = await self.get_klines(
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=int(time.time() * 1000)
        )
        return kline[0][0]
    _get_earliest_valid_timestamp.__doc__ = Client._get_earliest_valid_timestamp.__doc__

    async def get_historical_klines(self, symbol, interval, start_str, end_str=None, limit=500):
        # init our list
        output_data = []

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # convert our date strings to milliseconds
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        first_valid_ts = await self._get_earliest_valid_timestamp(symbol, interval)
        start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = await self.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
            )

            # handle the case where exactly the limit amount of data was returned last loop
            if not len(temp_data):
                break

            # append this loops data to our output data
            output_data += temp_data

            # set our start timestamp using the last value in the array
            start_ts = temp_data[-1][0]

            idx += 1
            # check if we received less than the required limit and exit the loop
            if len(temp_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts += timeframe

            # sleep after every 3rd call to be kind to the API
            if idx % 3 == 0:
                await asyncio.sleep(1)

        return output_data
    get_historical_klines.__doc__ = Client.get_historical_klines.__doc__

    async def get_historical_klines_generator(self, symbol, interval, start_str, end_str=None, limit=500):
        """Get Historical Klines from Binance

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 500; max 1000.
        :type limit: int

        :return: generator of OHLCV values

        """

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # convert our date strings to milliseconds
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        first_valid_ts = await self._get_earliest_valid_timestamp(symbol, interval)
        start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            output_data = await self.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
            )

            # handle the case where exactly the limit amount of data was returned last loop
            if not len(output_data):
                break

            # yield data
            for o in output_data:
                yield o

            # set our start timestamp using the last value in the array
            start_ts = output_data[-1][0]

            idx += 1
            # check if we received less than the required limit and exit the loop
            if len(output_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts += timeframe

            # sleep after every 3rd call to be kind to the API
            if idx % 3 == 0:
                await asyncio.sleep(1)
    get_historical_klines_generator.__doc__ = Client.get_historical_klines_generator.__doc__

    async def get_ticker(self, **params):
        return await self._get('ticker/24hr', data=params)
    get_ticker.__doc__ = Client.get_ticker.__doc__

    async def get_symbol_ticker(self, **params):
        return await self._get('ticker/price', data=params, version=self.PRIVATE_API_VERSION)
    get_symbol_ticker.__doc__ = Client.get_symbol_ticker.__doc__

    async def get_orderbook_ticker(self, **params):
        return await self._get('ticker/bookTicker', data=params, version=self.PRIVATE_API_VERSION)
    get_orderbook_ticker.__doc__ = Client.get_orderbook_ticker.__doc__

    # Account Endpoints

    async def create_order(self, **params):
        return await self._post('order', True, data=params)
    create_order.__doc__ = Client.create_order.__doc__

    async def order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update({
            'type': self.ORDER_TYPE_LIMIT,
            'timeInForce': timeInForce
        })
        return await self.create_order(**params)
    order_limit.__doc__ = Client.order_limit.__doc__

    async def order_limit_buy(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update({
            'side': self.SIDE_BUY,
        })
        return await self.order_limit(timeInForce=timeInForce, **params)
    order_limit_buy.__doc__ = Client.order_limit_buy.__doc__

    async def order_limit_sell(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update({
            'side': self.SIDE_SELL
        })
        return await self.order_limit(timeInForce=timeInForce, **params)
    order_limit_sell.__doc__ = Client.order_limit_sell.__doc__

    async def order_market(self, **params):
        params.update({
            'type': self.ORDER_TYPE_MARKET
        })
        return await self.create_order(**params)
    order_market.__doc__ = Client.order_market.__doc__

    async def order_market_buy(self, **params):
        params.update({
            'side': self.SIDE_BUY
        })
        return await self.order_market(**params)
    order_market_buy.__doc__ = Client.order_market_buy.__doc__

    async def order_market_sell(self, **params):
        params.update({
            'side': self.SIDE_SELL
        })
        return await self.order_market(**params)
    order_market_sell.__doc__ = Client.order_market_sell.__doc__

    async def create_test_order(self, **params):
        return await self._post('order/test', True, data=params)
    create_test_order.__doc__ = Client.create_test_order.__doc__

    async def get_order(self, **params):
        return await self._get('order', True, data=params)
    get_order.__doc__ = Client.get_order.__doc__

    async def get_all_orders(self, **params):
        return await self._get('allOrders', True, data=params)
    get_all_orders.__doc__ = Client.get_all_orders.__doc__

    async def cancel_order(self, **params):
        return await self._delete('order', True, data=params)
    cancel_order.__doc__ = Client.cancel_order.__doc__

    async def get_open_orders(self, **params):
        return await self._get('openOrders', True, data=params)
    get_open_orders.__doc__ = Client.get_open_orders.__doc__

    # User Stream Endpoints
    async def get_account(self, **params):
        return await self._get('account', True, data=params)
    get_account.__doc__ = Client.get_account.__doc__

    async def get_asset_balance(self, asset, **params):
        res = await self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            for bal in res['balances']:
                if bal['asset'].lower() == asset.lower():
                    return bal
        return None
    get_asset_balance.__doc__ = Client.get_asset_balance.__doc__

    async def get_my_trades(self, **params):
        return await self._get('myTrades', True, data=params)
    get_my_trades.__doc__ = Client.get_my_trades.__doc__

    async def get_system_status(self):
        return await self._request_withdraw_api('get', 'systemStatus.html')
    get_system_status.__doc__ = Client.get_system_status.__doc__

    async def get_account_status(self, **params):
        res = await self._request_withdraw_api('get', 'accountStatus.html', True, data=params)
        if not res['success']:
            raise BinanceWithdrawException(res['msg'])
        return res
    get_account_status.__doc__ = Client.get_account_status.__doc__

    # Withdraw Endpoints

    async def withdraw(self, **params):
        # force a name for the withdrawal if one not set
        if 'asset' in params and 'name' not in params:
            params['name'] = params['asset']
        res = await self._request_withdraw_api('post', 'withdraw.html', True, data=params)
        if not res['success']:
            raise BinanceWithdrawException(res['msg'])
        return res
    withdraw.__doc__ = Client.withdraw.__doc__

    async def get_deposit_history(self, **params):
        return await self._request_withdraw_api('get', 'depositHistory.html', True, data=params)
    get_deposit_history.__doc__ = Client.get_deposit_history.__doc__

    async def get_withdraw_history(self, **params):
        return await self._request_withdraw_api('get', 'withdrawHistory.html', True, data=params)
    get_withdraw_history.__doc__ = Client.get_withdraw_history.__doc__

    async def get_deposit_address(self, **params):
        return await self._request_withdraw_api('get', 'depositAddress.html', True, data=params)
    get_deposit_address.__doc__ = Client.get_deposit_address.__doc__

    async def get_withdraw_fee(self, **params):
        return await self._request_withdraw_api('get', 'withdrawFee.html', True, data=params)
    get_withdraw_fee.__doc__ = Client.get_withdraw_fee.__doc__

    # User Stream Endpoints

    async def stream_get_listen_key(self):
        res = await self._post('userDataStream', False, data={})
        return res['listenKey']
    stream_get_listen_key.__doc__ = Client.stream_get_listen_key.__doc__

    async def stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._put('userDataStream', False, data=params)
    stream_keepalive.__doc__ = Client.stream_keepalive.__doc__

    async def stream_close(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._delete('userDataStream', False, data=params)
    stream_close.__doc__ = Client.stream_close.__doc__

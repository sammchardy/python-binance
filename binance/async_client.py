import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, quote
import time
import aiohttp
import yarl

from binance.enums import HistoricalKlinesType
from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
    NotImplementedException,
)
from binance.helpers import (
    convert_list_to_json_array,
    convert_ts_str,
    get_loop,
    interval_to_milliseconds,
)
from .base_client import BaseClient
from .client import Client


class AsyncClient(BaseClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None,
        tld: str = "com",
        base_endpoint: str = BaseClient.BASE_ENDPOINT_DEFAULT,
        testnet: bool = False,
        loop=None,
        session_params: Optional[Dict[str, Any]] = None,
        private_key: Optional[Union[str, Path]] = None,
        private_key_pass: Optional[str] = None,
        https_proxy: Optional[str] = None,
        time_unit: Optional[str] = None,
    ):
        self.https_proxy = https_proxy
        self.loop = loop or get_loop()
        self._session_params: Dict[str, Any] = session_params or {}
        super().__init__(
            api_key,
            api_secret,
            requests_params,
            tld,
            base_endpoint,
            testnet,
            private_key,
            private_key_pass,
            time_unit=time_unit,
        )

    @classmethod
    async def create(
        cls,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None,
        tld: str = "com",
        base_endpoint: str = BaseClient.BASE_ENDPOINT_DEFAULT,
        testnet: bool = False,
        loop=None,
        session_params: Optional[Dict[str, Any]] = None,
        https_proxy: Optional[str] = None,
    ):
        self = cls(
            api_key,
            api_secret,
            requests_params,
            tld,
            base_endpoint,
            testnet,
            loop,
            session_params,
        )
        self.https_proxy = https_proxy  # move this to the constructor

        try:
            await self.ping()

            # calculate timestamp offset between local and binance server
            res = await self.get_server_time()
            self.timestamp_offset = res["serverTime"] - int(time.time() * 1000)

            return self
        except Exception:
            # If ping throw an exception, the current self must be cleaned
            # else, we can receive a "asyncio:Unclosed client session"
            await self.close_connection()
            raise

    def _init_session(self) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession(
            loop=self.loop, headers=self._get_headers(), **self._session_params
        )
        return session

    async def close_connection(self):
        if self.session:
            assert self.session
            await self.session.close()
        if self.ws_api:
            await self.ws_api.close()
            self._ws_api = None

    async def _request(
        self, method, uri: str, signed: bool, force_params: bool = False, **kwargs
    ):
        # this check needs to be done before __get_request_kwargs to avoid
        # polluting the signature
        headers = {}
        if method.upper() in ["POST", "PUT", "DELETE"]:
            headers.update({"Content-Type": "application/x-www-form-urlencoded"})

        if "data" in kwargs:
            for key in kwargs["data"]:
                if key == "headers":
                    headers.update(kwargs["data"][key])
                    del kwargs["data"][key]
                    break

        kwargs = self._get_request_kwargs(method, signed, force_params, **kwargs)

        if method == "get":
            # url encode the query string
            if "params" in kwargs:
                uri = f"{uri}?{kwargs['params']}"
                kwargs.pop("params")

        data = kwargs.get("data")
        if data is not None:
            del kwargs["data"]

        if (
            signed and self.PRIVATE_KEY and data
        ):  # handle issues with signing using eddsa/rsa and POST requests
            dict_data = Client.convert_to_dict(data)
            signature = dict_data["signature"] if "signature" in dict_data else None
            if signature:
                del dict_data["signature"]
            url_encoded_data = urlencode(dict_data)
            data = f"{url_encoded_data}&signature={signature}"

        async with getattr(self.session, method)(
            yarl.URL(uri, encoded=True),
            proxy=self.https_proxy,
            headers=headers,
            data=data,
            **kwargs,
        ) as response:
            self.response = response
            return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not str(response.status).startswith("2"):
            raise BinanceAPIException(response, response.status, await response.text())
        
        if response.text == "":
            return {}

        try:
            return await response.json()
        except ValueError:
            txt = await response.text()
            raise BinanceRequestException(f"Invalid Response: {txt}")

    async def _request_api(
        self,
        method,
        path,
        signed=False,
        version=BaseClient.PUBLIC_API_VERSION,
        **kwargs,
    ):
        uri = self._create_api_uri(path, signed, version)
        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_api_uri(path, version=version)
        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_data_api(
        self, method, path, signed=False, **kwargs
    ) -> Dict:
        uri = self._create_futures_data_api_uri(path)
        force_params = kwargs.pop("force_params", True)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_coin_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_coin_api_url(path, version=version)
        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_futures_coin_data_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_futures_coin_data_api_url(path, version=version)

        force_params = kwargs.pop("force_params", True)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_options_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_options_api_uri(path)
        force_params = kwargs.pop("force_params", True)

        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_margin_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_margin_api_uri(path, version)

        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_papi_api(
        self, method, path, signed=False, version=1, **kwargs
    ) -> Dict:
        version = self._get_version(version, **kwargs)
        uri = self._create_papi_api_uri(path, version)

        force_params = kwargs.pop("force_params", False)
        return await self._request(method, uri, signed, force_params, **kwargs)

    async def _request_website(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_website_uri(path)
        return await self._request(method, uri, signed, **kwargs)

    async def _get(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        return await self._request_api("get", path, signed, version, **kwargs)

    async def _post(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request_api("post", path, signed, version, **kwargs)

    async def _put(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request_api("put", path, signed, version, **kwargs)

    async def _delete(
        self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ) -> Dict:
        return await self._request_api("delete", path, signed, version, **kwargs)

    # Exchange Endpoints

    async def get_products(self) -> Dict:
        products = await self._request_website(
            "get",
            "bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true",
        )
        return products

    get_products.__doc__ = Client.get_products.__doc__

    async def get_exchange_info(self) -> Dict:
        return await self._get("exchangeInfo", version=self.PRIVATE_API_VERSION)

    get_exchange_info.__doc__ = Client.get_exchange_info.__doc__

    async def get_symbol_info(self, symbol) -> Optional[Dict]:
        res = await self.get_exchange_info()

        for item in res["symbols"]:
            if item["symbol"] == symbol.upper():
                return item

        return None

    get_symbol_info.__doc__ = Client.get_symbol_info.__doc__

    # General Endpoints

    async def ping(self) -> Dict:
        return await self._get("ping", version=self.PRIVATE_API_VERSION)

    ping.__doc__ = Client.ping.__doc__

    async def get_server_time(self) -> Dict:
        return await self._get("time", version=self.PRIVATE_API_VERSION)

    get_server_time.__doc__ = Client.get_server_time.__doc__

    # Market Data Endpoints

    async def get_all_tickers(
        self, symbol: Optional[str] = None
    ) -> List[Dict[str, str]]:
        params = {}
        if symbol:
            params["symbol"] = symbol
        response = await self._get(
            "ticker/price", version=self.PRIVATE_API_VERSION, data=params
        )
        if isinstance(response, list) and all(isinstance(item, dict) for item in response):
            return response
        raise TypeError("Expected a list of dictionaries")

    get_all_tickers.__doc__ = Client.get_all_tickers.__doc__

    async def get_orderbook_tickers(self, **params) -> Dict:
        data = {}
        if "symbol" in params:
            data["symbol"] = params["symbol"]
        elif "symbols" in params:
            data["symbols"] = params["symbols"]
        return await self._get(
            "ticker/bookTicker", data=data, version=self.PRIVATE_API_VERSION
        )

    get_orderbook_tickers.__doc__ = Client.get_orderbook_tickers.__doc__

    async def get_order_book(self, **params) -> Dict:
        return await self._get("depth", data=params, version=self.PRIVATE_API_VERSION)

    get_order_book.__doc__ = Client.get_order_book.__doc__

    async def get_recent_trades(self, **params) -> Dict:
        return await self._get("trades", data=params)

    get_recent_trades.__doc__ = Client.get_recent_trades.__doc__

    async def get_historical_trades(self, **params) -> Dict:
        return await self._get(
            "historicalTrades", data=params, version=self.PRIVATE_API_VERSION
        )

    get_historical_trades.__doc__ = Client.get_historical_trades.__doc__

    async def get_aggregate_trades(self, **params) -> Dict:
        return await self._get(
            "aggTrades", data=params, version=self.PRIVATE_API_VERSION
        )

    get_aggregate_trades.__doc__ = Client.get_aggregate_trades.__doc__

    async def aggregate_trade_iter(self, symbol, start_str=None, last_id=None):
        if start_str is not None and last_id is not None:
            raise ValueError(
                "start_time and last_id may not be simultaneously specified."
            )

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
                        symbol=symbol, startTime=start_ts, endTime=end_ts
                    )
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

    async def get_ui_klines(self, **params) -> Dict:
        return await self._get("uiKlines", data=params, version=self.PRIVATE_API_VERSION)

    get_ui_klines.__doc__ = Client.get_ui_klines.__doc__

    async def get_klines(self, **params) -> Dict:
        return await self._get("klines", data=params, version=self.PRIVATE_API_VERSION)

    get_klines.__doc__ = Client.get_klines.__doc__

    async def _klines(
        self, klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT, **params
    ) -> Dict:
        if "endTime" in params and not params["endTime"]:
            del params["endTime"]
        if HistoricalKlinesType.SPOT == klines_type:
            return await self.get_klines(**params)
        elif HistoricalKlinesType.FUTURES == klines_type:
            return await self.futures_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN == klines_type:
            return await self.futures_coin_klines(**params)
        elif HistoricalKlinesType.FUTURES_MARK_PRICE == klines_type:
            return await self.futures_mark_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_INDEX_PRICE == klines_type:
            return await self.futures_index_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN_MARK_PRICE == klines_type:
            return await self.futures_coin_mark_price_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN_INDEX_PRICE == klines_type:
            return await self.futures_coin_index_price_klines(**params)
        else:
            raise NotImplementedException(klines_type)

    _klines.__doc__ = Client._klines.__doc__

    async def _get_earliest_valid_timestamp(
        self,
        symbol,
        interval,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        kline = await self._klines(
            klines_type=klines_type,
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=int(time.time() * 1000),
        )
        return kline[0][0]

    _get_earliest_valid_timestamp.__doc__ = Client._get_earliest_valid_timestamp.__doc__

    async def get_historical_klines(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        return await self._historical_klines(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=klines_type,
        )

    get_historical_klines.__doc__ = Client.get_historical_klines.__doc__

    async def _historical_klines(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=None,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        initial_limit_set = True
        if limit is None:
            limit = 1000
            initial_limit_set = False

        # init our list
        output_data = []

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # establish first available start timestamp
        start_ts = convert_ts_str(start_str)
        if start_ts is not None:
            first_valid_ts = await self._get_earliest_valid_timestamp(
                symbol, interval, klines_type
            )
            start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)
        if end_ts and start_ts and end_ts <= start_ts:
            return output_data

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = await self._klines(
                klines_type=klines_type,
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts,
            )

            # append this loops data to our output data
            if temp_data:
                output_data += temp_data

            # check if output_data is greater than limit and truncate if needed and break loop
            if initial_limit_set and len(output_data) > limit:
                output_data = output_data[:limit]
                break

            # handle the case where exactly the limit amount of data was returned last loop
            # or check if we received less than the required limit and exit the loop
            if not len(temp_data) or len(temp_data) < limit:
                # exit the while loop
                break

            # set our start timestamp using the last value in the array
            # and increment next call by our timeframe
            start_ts = temp_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                await asyncio.sleep(1)

        return output_data

    _historical_klines.__doc__ = Client._historical_klines.__doc__

    async def get_historical_klines_generator(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=1000,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        return self._historical_klines_generator(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=klines_type,
        )

    get_historical_klines_generator.__doc__ = (
        Client.get_historical_klines_generator.__doc__
    )

    async def _historical_klines_generator(
        self,
        symbol,
        interval,
        start_str=None,
        end_str=None,
        limit=1000,
        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT,
    ):
        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = await self._get_earliest_valid_timestamp(
                symbol, interval, klines_type
            )
            start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)
        if end_ts and start_ts and end_ts <= start_ts:
            return

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            output_data = await self._klines(
                klines_type=klines_type,
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts,
            )

            # yield data
            if output_data:
                for o in output_data:
                    yield o

            # handle the case where exactly the limit amount of data was returned last loop
            # check if we received less than the required limit and exit the loop
            if not len(output_data) or len(output_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts = output_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                await asyncio.sleep(1)

    _historical_klines_generator.__doc__ = Client._historical_klines_generator.__doc__

    async def get_avg_price(self, **params):
        return await self._get(
            "avgPrice", data=params, version=self.PRIVATE_API_VERSION
        )

    get_avg_price.__doc__ = Client.get_avg_price.__doc__

    async def get_ticker(self, **params):
        return await self._get(
            "ticker/24hr", data=params, version=self.PRIVATE_API_VERSION
        )

    get_ticker.__doc__ = Client.get_ticker.__doc__

    async def get_symbol_ticker(self, **params):
        return await self._get(
            "ticker/price", data=params, version=self.PRIVATE_API_VERSION
        )

    get_symbol_ticker.__doc__ = Client.get_symbol_ticker.__doc__

    async def get_symbol_ticker_window(self, **params):
        return await self._get("ticker", data=params, version=self.PRIVATE_API_VERSION)

    get_symbol_ticker_window.__doc__ = Client.get_symbol_ticker_window.__doc__

    async def get_orderbook_ticker(self, **params):
        return await self._get(
            "ticker/bookTicker", data=params, version=self.PRIVATE_API_VERSION
        )

    get_orderbook_ticker.__doc__ = Client.get_orderbook_ticker.__doc__

    # Account Endpoints

    async def create_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._post("order", True, data=params)

    create_order.__doc__ = Client.create_order.__doc__

    async def order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update({"type": self.ORDER_TYPE_LIMIT, "timeInForce": timeInForce})
        return await self.create_order(**params)

    order_limit.__doc__ = Client.order_limit.__doc__

    async def order_limit_buy(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        params.update({
            "side": self.SIDE_BUY,
        })
        return await self.order_limit(timeInForce=timeInForce, **params)

    order_limit_buy.__doc__ = Client.order_limit_buy.__doc__

    async def order_limit_sell(
        self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params
    ):
        params.update({"side": self.SIDE_SELL})
        return await self.order_limit(timeInForce=timeInForce, **params)

    order_limit_sell.__doc__ = Client.order_limit_sell.__doc__

    async def order_market(self, **params):
        params.update({"type": self.ORDER_TYPE_MARKET})
        return await self.create_order(**params)

    order_market.__doc__ = Client.order_market.__doc__

    async def order_market_buy(self, **params):
        params.update({"side": self.SIDE_BUY})
        return await self.order_market(**params)

    order_market_buy.__doc__ = Client.order_market_buy.__doc__

    async def order_market_sell(self, **params):
        params.update({"side": self.SIDE_SELL})
        return await self.order_market(**params)

    order_market_sell.__doc__ = Client.order_market_sell.__doc__

    async def order_oco_buy(self, **params):
        params.update({"side": self.SIDE_BUY})
        return await self.create_oco_order(**params)

    order_oco_buy.__doc__ = Client.order_oco_buy.__doc__

    async def order_oco_sell(self, **params):
        params.update({"side": self.SIDE_SELL})
        return await self.create_oco_order(**params)

    order_oco_sell.__doc__ = Client.order_oco_sell.__doc__

    async def create_test_order(self, **params):
        return await self._post("order/test", True, data=params)

    create_test_order.__doc__ = Client.create_test_order.__doc__

    async def get_order(self, **params):
        return await self._get("order", True, data=params)

    get_order.__doc__ = Client.get_order.__doc__

    async def get_all_orders(self, **params):
        return await self._get("allOrders", True, data=params)

    get_all_orders.__doc__ = Client.get_all_orders.__doc__

    async def cancel_order(self, **params):
        return await self._delete("order", True, data=params)

    cancel_order.__doc__ = Client.cancel_order.__doc__

    async def get_open_orders(self, **params):
        return await self._get("openOrders", True, data=params)

    get_open_orders.__doc__ = Client.get_open_orders.__doc__

    async def get_open_oco_orders(self, **params):
        return await self._get("openOrderList", True, data=params)

    get_open_oco_orders.__doc__ = Client.get_open_oco_orders.__doc__

    # User Stream Endpoints
    async def get_account(self, **params):
        return await self._get("account", True, data=params)

    get_account.__doc__ = Client.get_account.__doc__

    async def get_asset_balance(self, asset=None, **params):
        res = await self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            if asset:
                for bal in res["balances"]:
                    if bal["asset"].lower() == asset.lower():
                        return bal
            else:
                return res["balances"]
        return None

    get_asset_balance.__doc__ = Client.get_asset_balance.__doc__

    async def get_my_trades(self, **params):
        return await self._get("myTrades", True, data=params)

    get_my_trades.__doc__ = Client.get_my_trades.__doc__

    async def get_current_order_count(self, **params):
        return await self._get("rateLimit/order", True, data=params)

    get_current_order_count.__doc__ = Client.get_current_order_count.__doc__

    async def get_prevented_matches(self, **params):
        return await self._get("myPreventedMatches", True, data=params)

    get_prevented_matches.__doc__ = Client.get_prevented_matches.__doc__

    async def get_allocations(self, **params):
        return await self._get("myAllocations", True, data=params)

    get_allocations.__doc__ = Client.get_allocations.__doc__

    async def get_system_status(self):
        return await self._request_margin_api("get", "system/status")

    get_system_status.__doc__ = Client.get_system_status.__doc__

    async def get_account_status(self, **params):
        return await self._request_margin_api(
            "get", "account/status", True, data=params
        )

    get_account_status.__doc__ = Client.get_account_status.__doc__

    async def get_account_api_trading_status(self, **params):
        return await self._request_margin_api(
            "get", "account/apiTradingStatus", True, data=params
        )

    get_account_api_trading_status.__doc__ = (
        Client.get_account_api_trading_status.__doc__
    )

    async def get_account_api_permissions(self, **params):
        return await self._request_margin_api(
            "get", "account/apiRestrictions", True, data=params
        )

    get_account_api_permissions.__doc__ = Client.get_account_api_permissions.__doc__

    async def get_dust_assets(self, **params):
        return await self._request_margin_api(
            "post", "asset/dust-btc", True, data=params
        )

    get_dust_assets.__doc__ = Client.get_dust_assets.__doc__

    async def get_dust_log(self, **params):
        return await self._request_margin_api(
            "get", "asset/dribblet", True, data=params
        )

    get_dust_log.__doc__ = Client.get_dust_log.__doc__

    async def transfer_dust(self, **params):
        return await self._request_margin_api("post", "asset/dust", True, data=params)

    transfer_dust.__doc__ = Client.transfer_dust.__doc__

    async def get_asset_dividend_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/assetDividend", True, data=params
        )

    get_asset_dividend_history.__doc__ = Client.get_asset_dividend_history.__doc__

    async def make_universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    make_universal_transfer.__doc__ = Client.make_universal_transfer.__doc__

    async def query_universal_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/transfer", signed=True, data=params
        )

    query_universal_transfer_history.__doc__ = (
        Client.query_universal_transfer_history.__doc__
    )

    async def get_trade_fee(self, **params):
        if self.tld == "us":
            endpoint = "asset/query/trading-fee"
        else:
            endpoint = "asset/tradeFee"
        return await self._request_margin_api("get", endpoint, True, data=params)

    get_trade_fee.__doc__ = Client.get_trade_fee.__doc__

    async def get_asset_details(self, **params):
        return await self._request_margin_api(
            "get", "asset/assetDetail", True, data=params
        )

    get_asset_details.__doc__ = Client.get_asset_details.__doc__

    async def get_spot_delist_schedule(self, **params):
        return await self._request_margin_api(
            "get", "/spot/delist-schedule", signed=True, data=params
        )

    # Withdraw Endpoints

    async def withdraw(self, **params):
        # force a name for the withdrawal if one not set
        if "coin" in params and "name" not in params:
            params["name"] = params["coin"]
        return await self._request_margin_api(
            "post", "capital/withdraw/apply", True, data=params
        )

    withdraw.__doc__ = Client.withdraw.__doc__

    async def get_deposit_history(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/hisrec", True, data=params
        )

    get_deposit_history.__doc__ = Client.get_deposit_history.__doc__

    async def get_withdraw_history(self, **params):
        return await self._request_margin_api(
            "get", "capital/withdraw/history", True, data=params
        )

    get_withdraw_history.__doc__ = Client.get_withdraw_history.__doc__

    async def get_withdraw_history_id(self, withdraw_id, **params):
        result = await self.get_withdraw_history(**params)

        for entry in result:
            if "id" in entry and entry["id"] == withdraw_id:
                return entry

        raise Exception("There is no entry with withdraw id", result)

    get_withdraw_history_id.__doc__ = Client.get_withdraw_history_id.__doc__

    async def get_deposit_address(
        self, coin: str, network: Optional[str] = None, **params
    ):
        params["coin"] = coin
        if network:
            params["network"] = network
        return await self._request_margin_api(
            "get", "capital/deposit/address", True, data=params
        )

    get_deposit_address.__doc__ = Client.get_deposit_address.__doc__

    # User Stream Endpoints

    async def stream_get_listen_key(self):
        res = await self._post("userDataStream", False, data={})
        return res["listenKey"]

    stream_get_listen_key.__doc__ = Client.stream_get_listen_key.__doc__

    async def stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._put("userDataStream", False, data=params)

    stream_keepalive.__doc__ = Client.stream_keepalive.__doc__

    async def stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._delete("userDataStream", False, data=params)

    stream_close.__doc__ = Client.stream_close.__doc__

    # Margin Trading Endpoints
    async def get_margin_account(self, **params):
        return await self._request_margin_api(
            "get", "margin/account", True, data=params
        )

    get_margin_account.__doc__ = Client.get_margin_account.__doc__

    async def get_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/account", True, data=params
        )

    get_isolated_margin_account.__doc__ = Client.get_isolated_margin_account.__doc__

    async def enable_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "post", "margin/isolated/account", True, data=params
        )

    enable_isolated_margin_account.__doc__ = (
        Client.enable_isolated_margin_account.__doc__
    )

    async def disable_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "delete", "margin/isolated/account", True, data=params
        )

    disable_isolated_margin_account.__doc__ = (
        Client.disable_isolated_margin_account.__doc__
    )

    async def get_enabled_isolated_margin_account_limit(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/accountLimit", True, data=params
        )

    get_enabled_isolated_margin_account_limit.__doc__ = (
        Client.get_enabled_isolated_margin_account_limit.__doc__
    )

    async def get_margin_dustlog(self, **params):
        return await self._request_margin_api(
            "get", "margin/dribblet", True, data=params
        )

    get_margin_dustlog.__doc__ = Client.get_margin_dustlog.__doc__

    async def get_margin_dust_assets(self, **params):
        return await self._request_margin_api("get", "margin/dust", True, data=params)

    get_margin_dust_assets.__doc__ = Client.get_margin_dust_assets.__doc__

    async def transfer_margin_dust(self, **params):
        return await self._request_margin_api("post", "margin/dust", True, data=params)

    transfer_margin_dust.__doc__ = Client.transfer_margin_dust.__doc__

    async def get_cross_margin_collateral_ratio(self, **params):
        return await self._request_margin_api(
            "get", "margin/crossMarginCollateralRatio", True, data=params
        )

    get_cross_margin_collateral_ratio.__doc__ = (
        Client.get_cross_margin_collateral_ratio.__doc__
    )

    async def get_small_liability_exchange_assets(self, **params):
        return await self._request_margin_api(
            "get", "margin/exchange-small-liability", True, data=params
        )

    get_small_liability_exchange_assets.__doc__ = (
        Client.get_small_liability_exchange_assets.__doc__
    )

    async def exchange_small_liability_assets(self, **params):
        return await self._request_margin_api(
            "post", "margin/exchange-small-liability", True, data=params
        )

    exchange_small_liability_assets.__doc__ = (
        Client.exchange_small_liability_assets.__doc__
    )

    async def get_small_liability_exchange_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/exchange-small-liability-history", True, data=params
        )

    get_small_liability_exchange_history.__doc__ = (
        Client.get_small_liability_exchange_history.__doc__
    )

    async def get_future_hourly_interest_rate(self, **params):
        return await self._request_margin_api(
            "get", "margin/next-hourly-interest-rate", True, data=params
        )

    get_future_hourly_interest_rate.__doc__ = (
        Client.get_future_hourly_interest_rate.__doc__
    )

    async def get_margin_capital_flow(self, **params):
        return await self._request_margin_api(
            "get", "margin/capital-flow", True, data=params
        )

    get_margin_capital_flow.__doc__ = Client.get_margin_capital_flow.__doc__

    async def get_margin_delist_schedule(self, **params):
        return await self._request_margin_api(
            "get", "margin/delist-schedule", True, data=params
        )

    get_margin_delist_schedule.__doc__ = Client.get_margin_delist_schedule.__doc__

    async def get_margin_asset(self, **params):
        return await self._request_margin_api("get", "margin/asset", data=params)

    get_margin_asset.__doc__ = Client.get_margin_asset.__doc__

    async def get_margin_symbol(self, **params):
        return await self._request_margin_api("get", "margin/pair", data=params)

    get_margin_symbol.__doc__ = Client.get_margin_symbol.__doc__

    async def get_margin_all_assets(self, **params):
        return await self._request_margin_api("get", "margin/allAssets", data=params)

    get_margin_all_assets.__doc__ = Client.get_margin_all_assets.__doc__

    async def get_margin_all_pairs(self, **params):
        return await self._request_margin_api("get", "margin/allPairs", data=params)

    get_margin_all_pairs.__doc__ = Client.get_margin_all_pairs.__doc__

    async def create_isolated_margin_account(self, **params):
        return await self._request_margin_api(
            "post", "margin/isolated/create", signed=True, data=params
        )

    create_isolated_margin_account.__doc__ = (
        Client.create_isolated_margin_account.__doc__
    )

    async def get_isolated_margin_symbol(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/pair", signed=True, data=params
        )

    get_isolated_margin_symbol.__doc__ = Client.get_isolated_margin_symbol.__doc__

    async def get_all_isolated_margin_symbols(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolated/allPairs", signed=True, data=params
        )

    get_all_isolated_margin_symbols.__doc__ = (
        Client.get_all_isolated_margin_symbols.__doc__
    )

    async def get_isolated_margin_fee_data(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolatedMarginData", True, data=params
        )

    get_isolated_margin_fee_data.__doc__ = Client.get_isolated_margin_fee_data.__doc__

    async def get_isolated_margin_tier_data(self, **params):
        return await self._request_margin_api(
            "get", "margin/isolatedMarginTier", True, data=params
        )

    get_isolated_margin_tier_data.__doc__ = Client.get_isolated_margin_tier_data.__doc__

    async def margin_manual_liquidation(self, **params):
        return await self._request_margin_api(
            "get", "margin/manual-liquidation", True, data=params
        )

    margin_manual_liquidation.__doc__ = Client.margin_manual_liquidation.__doc__

    async def toggle_bnb_burn_spot_margin(self, **params):
        return await self._request_margin_api(
            "post", "bnbBurn", signed=True, data=params
        )

    toggle_bnb_burn_spot_margin.__doc__ = Client.toggle_bnb_burn_spot_margin.__doc__

    async def get_bnb_burn_spot_margin(self, **params):
        return await self._request_margin_api(
            "get", "bnbBurn", signed=True, data=params
        )

    get_bnb_burn_spot_margin.__doc__ = Client.get_bnb_burn_spot_margin.__doc__

    async def get_margin_price_index(self, **params):
        return await self._request_margin_api("get", "margin/priceIndex", data=params)

    get_margin_price_index.__doc__ = Client.get_margin_price_index.__doc__

    async def transfer_margin_to_spot(self, **params):
        params["type"] = 2
        return await self._request_margin_api(
            "post", "margin/transfer", signed=True, data=params
        )

    transfer_margin_to_spot.__doc__ = Client.transfer_margin_to_spot.__doc__

    async def transfer_spot_to_margin(self, **params):
        params["type"] = 1
        return await self._request_margin_api(
            "post", "margin/transfer", signed=True, data=params
        )

    transfer_spot_to_margin.__doc__ = Client.transfer_spot_to_margin.__doc__

    async def transfer_isolated_margin_to_spot(self, **params):
        params["transFrom"] = "ISOLATED_MARGIN"
        params["transTo"] = "SPOT"
        return await self._request_margin_api(
            "post", "margin/isolated/transfer", signed=True, data=params
        )

    transfer_isolated_margin_to_spot.__doc__ = (
        Client.transfer_isolated_margin_to_spot.__doc__
    )

    async def transfer_spot_to_isolated_margin(self, **params):
        params["transFrom"] = "SPOT"
        params["transTo"] = "ISOLATED_MARGIN"
        return await self._request_margin_api(
            "post", "margin/isolated/transfer", signed=True, data=params
        )

    transfer_spot_to_isolated_margin.__doc__ = (
        Client.transfer_spot_to_isolated_margin.__doc__
    )

    async def create_margin_loan(self, **params):
        return await self._request_margin_api(
            "post", "margin/loan", signed=True, data=params
        )

    create_margin_loan.__doc__ = Client.create_margin_loan.__doc__

    async def repay_margin_loan(self, **params):
        return await self._request_margin_api(
            "post", "margin/repay", signed=True, data=params
        )

    repay_margin_loan.__doc__ = Client.repay_margin_loan.__doc__

    async def create_margin_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._request_margin_api(
            "post", "margin/order", signed=True, data=params
        )

    create_margin_order.__doc__ = Client.create_margin_order.__doc__

    async def cancel_margin_order(self, **params):
        return await self._request_margin_api(
            "delete", "margin/order", signed=True, data=params
        )

    cancel_margin_order.__doc__ = Client.cancel_margin_order.__doc__

    async def cancel_all_open_margin_orders(self, **params):
        return await self._request_margin_api(
            "delete", "margin/openOrders", signed=True, data=params
        )

    cancel_all_open_margin_orders.__doc__ = Client.cancel_all_open_margin_orders.__doc__

    async def set_margin_max_leverage(self, **params):
        return await self._request_margin_api(
            "post", "margin/max-leverage", signed=True, data=params
        )

    set_margin_max_leverage.__doc__ = Client.set_margin_max_leverage.__doc__

    async def get_margin_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/transfer", signed=True, data=params
        )

    get_margin_transfer_history.__doc__ = Client.get_margin_transfer_history.__doc__

    async def get_margin_loan_details(self, **params):
        return await self._request_margin_api(
            "get", "margin/loan", signed=True, data=params
        )

    get_margin_loan_details.__doc__ = Client.get_margin_loan_details.__doc__

    async def get_margin_repay_details(self, **params):
        return await self._request_margin_api(
            "get", "margin/repay", signed=True, data=params
        )

    async def get_cross_margin_data(self, **params):
        return await self._request_margin_api(
            "get", "margin/crossMarginData", signed=True, data=params
        )

    async def get_margin_interest_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/interestHistory", signed=True, data=params
        )

    async def get_margin_force_liquidation_rec(self, **params):
        return await self._request_margin_api(
            "get", "margin/forceLiquidationRec", signed=True, data=params
        )

    async def get_margin_order(self, **params):
        return await self._request_margin_api(
            "get", "margin/order", signed=True, data=params
        )

    async def get_open_margin_orders(self, **params):
        return await self._request_margin_api(
            "get", "margin/openOrders", signed=True, data=params
        )

    async def get_all_margin_orders(self, **params):
        return await self._request_margin_api(
            "get", "margin/allOrders", signed=True, data=params
        )

    async def get_margin_trades(self, **params):
        return await self._request_margin_api(
            "get", "margin/myTrades", signed=True, data=params
        )

    async def get_max_margin_loan(self, **params):
        return await self._request_margin_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )

    async def get_max_margin_transfer(self, **params):
        return await self._request_margin_api(
            "get", "margin/maxTransferable", signed=True, data=params
        )

    # Margin OCO

    async def create_margin_oco_order(self, **params):
        return await self._request_margin_api(
            "post", "margin/order/oco", signed=True, data=params
        )

    async def cancel_margin_oco_order(self, **params):
        return await self._request_margin_api(
            "delete", "margin/orderList", signed=True, data=params
        )

    async def get_margin_oco_order(self, **params):
        return await self._request_margin_api(
            "get", "margin/orderList", signed=True, data=params
        )

    async def get_open_margin_oco_orders(self, **params):
        return await self._request_margin_api(
            "get", "margin/openOrderList", signed=True, data=params
        )

    # Cross-margin

    async def margin_stream_get_listen_key(self):
        res = await self._request_margin_api(
            "post", "userDataStream", signed=False, data={}
        )
        return res["listenKey"]

    async def margin_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_margin_api(
            "put", "userDataStream", signed=False, data=params
        )

    async def margin_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_margin_api(
            "delete", "userDataStream", signed=False, data=params
        )

        # Isolated margin

    async def isolated_margin_stream_get_listen_key(self, symbol):
        params = {"symbol": symbol}
        res = await self._request_margin_api(
            "post", "userDataStream/isolated", signed=False, data=params
        )
        return res["listenKey"]

    async def isolated_margin_stream_keepalive(self, symbol, listenKey):
        params = {"symbol": symbol, "listenKey": listenKey}
        return await self._request_margin_api(
            "put", "userDataStream/isolated", signed=False, data=params
        )

    async def isolated_margin_stream_close(self, symbol, listenKey):
        params = {"symbol": symbol, "listenKey": listenKey}
        return await self._request_margin_api(
            "delete", "userDataStream/isolated", signed=False, data=params
        )

    # Simple Earn Endpoints

    async def get_simple_earn_flexible_product_list(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/flexible/list", signed=True, data=params
        )

    get_simple_earn_flexible_product_list.__doc__ = (
        Client.get_simple_earn_flexible_product_list.__doc__
    )

    async def get_simple_earn_locked_product_list(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/locked/list", signed=True, data=params
        )

    get_simple_earn_locked_product_list.__doc__ = (
        Client.get_simple_earn_locked_product_list.__doc__
    )

    async def subscribe_simple_earn_flexible_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/flexible/subscribe", signed=True, data=params
        )

    subscribe_simple_earn_flexible_product.__doc__ = (
        Client.subscribe_simple_earn_flexible_product.__doc__
    )

    async def subscribe_simple_earn_locked_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/locked/subscribe", signed=True, data=params
        )

    subscribe_simple_earn_locked_product.__doc__ = (
        Client.subscribe_simple_earn_locked_product.__doc__
    )

    async def redeem_simple_earn_flexible_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/flexible/redeem", signed=True, data=params
        )

    redeem_simple_earn_flexible_product.__doc__ = (
        Client.redeem_simple_earn_flexible_product.__doc__
    )

    async def redeem_simple_earn_locked_product(self, **params):
        return await self._request_margin_api(
            "post", "simple-earn/locked/redeem", signed=True, data=params
        )

    redeem_simple_earn_locked_product.__doc__ = (
        Client.redeem_simple_earn_locked_product.__doc__
    )

    async def get_simple_earn_flexible_product_position(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/flexible/position", signed=True, data=params
        )

    get_simple_earn_flexible_product_position.__doc__ = (
        Client.get_simple_earn_flexible_product_position.__doc__
    )

    async def get_simple_earn_locked_product_position(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/locked/position", signed=True, data=params
        )

    get_simple_earn_locked_product_position.__doc__ = (
        Client.get_simple_earn_locked_product_position.__doc__
    )

    async def get_simple_earn_account(self, **params):
        return await self._request_margin_api(
            "get", "simple-earn/account", signed=True, data=params
        )

    get_simple_earn_account.__doc__ = Client.get_simple_earn_account.__doc__

    # Lending Endpoints

    async def get_fixed_activity_project_list(self, **params):
        return await self._request_margin_api(
            "get", "lending/project/list", signed=True, data=params
        )

    async def change_fixed_activity_to_daily_position(self, **params):
        return await self._request_margin_api(
            "post", "lending/positionChanged", signed=True, data=params
        )

    # Staking Endpoints

    async def get_staking_product_list(self, **params):
        return await self._request_margin_api(
            "get", "staking/productList", signed=True, data=params
        )

    async def purchase_staking_product(self, **params):
        return await self._request_margin_api(
            "post", "staking/purchase", signed=True, data=params
        )

    async def redeem_staking_product(self, **params):
        return await self._request_margin_api(
            "post", "staking/redeem", signed=True, data=params
        )

    async def get_staking_position(self, **params):
        return await self._request_margin_api(
            "get", "staking/position", signed=True, data=params
        )

    async def get_staking_purchase_history(self, **params):
        return await self._request_margin_api(
            "get", "staking/purchaseRecord", signed=True, data=params
        )

    async def set_auto_staking(self, **params):
        return await self._request_margin_api(
            "post", "staking/setAutoStaking", signed=True, data=params
        )

    async def get_personal_left_quota(self, **params):
        return await self._request_margin_api(
            "get", "staking/personalLeftQuota", signed=True, data=params
        )

    # US Staking Endpoints

    async def get_staking_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("get", "staking/asset", True, data=params)

    get_staking_asset_us.__doc__ = Client.get_staking_asset_us.__doc__

    async def stake_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "post", "staking/stake", True, data=params
        )

    stake_asset_us.__doc__ = Client.stake_asset_us.__doc__

    async def unstake_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "post", "staking/unstake", True, data=params
        )

    unstake_asset_us.__doc__ = Client.unstake_asset_us.__doc__

    async def get_staking_balance_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "get", "staking/stakingBalance", True, data=params
        )

    get_staking_balance_us.__doc__ = Client.get_staking_balance_us.__doc__

    async def get_staking_history_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "get", "staking/history", True, data=params
        )

    get_staking_history_us.__doc__ = Client.get_staking_history_us.__doc__

    async def get_staking_rewards_history_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api(
            "get", "staking/stakingRewardsHistory", True, data=params
        )

    get_staking_rewards_history_us.__doc__ = (
        Client.get_staking_rewards_history_us.__doc__
    )

    # Sub Accounts

    async def get_sub_account_list(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/list", True, data=params
        )

    async def get_sub_account_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/sub/transfer/history", True, data=params
        )

    async def get_sub_account_futures_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/internalTransfer", True, data=params
        )

    async def create_sub_account_futures_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/futures/internalTransfer", True, data=params
        )

    async def get_sub_account_assets(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/assets", True, data=params, version=4
        )

    async def query_subaccount_spot_summary(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/spotSummary", True, data=params
        )

    async def get_subaccount_deposit_address(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/subAddress", True, data=params
        )

    async def get_subaccount_deposit_history(self, **params):
        return await self._request_margin_api(
            "get", "capital/deposit/subHisrec", True, data=params
        )

    async def get_subaccount_futures_margin_status(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/status", True, data=params
        )

    async def enable_subaccount_margin(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/margin/enable", True, data=params
        )

    async def get_subaccount_margin_details(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/margin/account", True, data=params
        )

    async def get_subaccount_margin_summary(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/margin/accountSummary", True, data=params
        )

    async def enable_subaccount_futures(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/futures/enable", True, data=params
        )

    async def get_subaccount_futures_details(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/account", True, data=params, version=2
        )

    async def get_subaccount_futures_summary(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/accountSummary", True, data=params, version=2
        )

    async def get_subaccount_futures_positionrisk(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/futures/positionRisk", True, data=params, version=2
        )

    async def make_subaccount_futures_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/futures/transfer", True, data=params
        )

    async def make_subaccount_margin_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/margin/transfer", True, data=params
        )

    async def make_subaccount_to_subaccount_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/transfer/subToSub", True, data=params
        )

    async def make_subaccount_to_master_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/transfer/subToMaster", True, data=params
        )

    async def get_subaccount_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/transfer/subUserHistory", True, data=params
        )

    async def make_subaccount_universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "sub-account/universalTransfer", True, data=params
        )

    async def get_universal_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "sub-account/universalTransfer", True, data=params
        )

    # Futures API

    async def futures_ping(self):
        return await self._request_futures_api("get", "ping")

    async def futures_time(self):
        return await self._request_futures_api("get", "time")

    async def futures_exchange_info(self):
        return await self._request_futures_api("get", "exchangeInfo")

    async def futures_order_book(self, **params):
        return await self._request_futures_api("get", "depth", data=params)

    async def futures_recent_trades(self, **params):
        return await self._request_futures_api("get", "trades", data=params)

    async def futures_historical_trades(self, **params):
        return await self._request_futures_api("get", "historicalTrades", data=params)

    async def futures_aggregate_trades(self, **params):
        return await self._request_futures_api("get", "aggTrades", data=params)

    async def futures_klines(self, **params):
        return await self._request_futures_api("get", "klines", data=params)

    async def futures_mark_price_klines(self, **params):
        return await self._request_futures_api("get", "markPriceKlines", data=params)

    futures_mark_price_klines.__doc__ = Client.futures_mark_price_klines.__doc__

    async def futures_index_price_klines(self, **params):
        return await self._request_futures_api("get", "indexPriceKlines", data=params)

    futures_index_price_klines.__doc__ = Client.futures_index_price_klines.__doc__

    async def futures_premium_index_klines(self, **params):
        return await self._request_futures_api("get", "premiumIndexKlines", data=params)

    futures_premium_index_klines.__doc__ = Client.futures_index_price_klines.__doc__

    async def futures_continous_klines(self, **params):
        return await self._request_futures_api("get", "continuousKlines", data=params)

    async def futures_historical_klines(
        self, symbol, interval, start_str, end_str=None, limit=500
    ):
        return await self._historical_klines(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            limit=limit,
            klines_type=HistoricalKlinesType.FUTURES,
        )

    async def futures_historical_klines_generator(
        self, symbol, interval, start_str, end_str=None
    ):
        return self._historical_klines_generator(
            symbol,
            interval,
            start_str,
            end_str=end_str,
            klines_type=HistoricalKlinesType.FUTURES,
        )

    async def futures_mark_price(self, **params):
        return await self._request_futures_api("get", "premiumIndex", data=params)

    async def futures_funding_rate(self, **params):
        return await self._request_futures_api("get", "fundingRate", data=params)

    async def futures_top_longshort_account_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "topLongShortAccountRatio", data=params
        )

    async def futures_top_longshort_position_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "topLongShortPositionRatio", data=params
        )

    async def futures_global_longshort_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "globalLongShortAccountRatio", data=params
        )
        
    async def futures_taker_longshort_ratio(self, **params):
        return await self._request_futures_data_api(
            "get", "takerlongshortRatio", data=params
        )

    async def futures_ticker(self, **params):
        return await self._request_futures_api("get", "ticker/24hr", data=params)

    async def futures_symbol_ticker(self, **params):
        return await self._request_futures_api("get", "ticker/price", data=params)

    async def futures_orderbook_ticker(self, **params):
        return await self._request_futures_api("get", "ticker/bookTicker", data=params)

    async def futures_index_price_constituents(self, **params):
        return await self._request_futures_api("get", "constituents", data=params)

    futures_index_price_constituents.__doc__ = (
        Client.futures_index_price_constituents.__doc__
    )

    async def futures_liquidation_orders(self, **params):
        return await self._request_futures_api(
            "get", "forceOrders", signed=True, data=params
        )

    async def futures_api_trading_status(self, **params):
        return await self._request_futures_api(
            "get", "apiTradingStatus", signed=True, data=params
        )

    async def futures_commission_rate(self, **params):
        return await self._request_futures_api(
            "get", "commissionRate", signed=True, data=params
        )

    async def futures_adl_quantile_estimate(self, **params):
        return await self._request_futures_api(
            "get", "adlQuantile", signed=True, data=params
        )

    async def futures_open_interest(self, **params):
        return await self._request_futures_api("get", "openInterest", data=params)

    async def futures_index_info(self, **params):
        return await self._request_futures_api("get", "indexInfo", data=params)

    async def futures_open_interest_hist(self, **params):
        return await self._request_futures_data_api(
            "get", "openInterestHist", data=params
        )

    async def futures_leverage_bracket(self, **params):
        return await self._request_futures_api(
            "get", "leverageBracket", True, data=params
        )

    async def futures_account_transfer(self, **params):
        return await self._request_margin_api(
            "post", "futures/transfer", True, data=params
        )

    async def transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/transfer", True, data=params
        )

    async def futures_loan_borrow_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/borrow/history", True, data=params
        )

    async def futures_loan_repay_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/repay/history", True, data=params
        )

    async def futures_loan_wallet(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/wallet", True, data=params, version=2
        )

    async def futures_cross_collateral_adjust_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/adjustCollateral/history", True, data=params
        )

    async def futures_cross_collateral_liquidation_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/liquidationHistory", True, data=params
        )

    async def futures_loan_interest_history(self, **params):
        return await self._request_margin_api(
            "get", "futures/loan/interestHistory", True, data=params
        )

    async def futures_create_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_futures_api("post", "order", True, data=params)

    async def futures_modify_order(self, **params):
        """Modify an existing order. Currently only LIMIT order modification is supported.

        https://binance-docs.github.io/apidocs/futures/en/#modify-order-trade

        """
        return await self._request_futures_api("put", "order", True, data=params)

    async def futures_create_test_order(self, **params):
        return await self._request_futures_api("post", "order/test", True, data=params)

    async def futures_place_batch_order(self, **params):
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
                order = self._order_params(order)
        query_string = urlencode(params).replace("%40", "@").replace("%27", "%22")
        params["batchOrders"] = query_string[12:]

        return await self._request_futures_api(
            "post", "batchOrders", True, data=params, force_params=True
        )

    async def futures_get_order(self, **params):
        return await self._request_futures_api("get", "order", True, data=params)

    async def futures_get_open_orders(self, **params):
        return await self._request_futures_api("get", "openOrders", True, data=params)

    async def futures_get_all_orders(self, **params):
        return await self._request_futures_api("get", "allOrders", True, data=params)

    async def futures_cancel_order(self, **params):
        return await self._request_futures_api("delete", "order", True, data=params)

    async def futures_cancel_all_open_orders(self, **params):
        return await self._request_futures_api(
            "delete", "allOpenOrders", True, data=params
        )

    async def futures_cancel_orders(self, **params):
        if params.get("orderidlist"):
            params["orderidlist"] = quote(
                convert_list_to_json_array(params["orderidlist"])
            )
        if params.get("origclientorderidlist"):
            params["origclientorderidlist"] = quote(
                convert_list_to_json_array(params["origclientorderidlist"])
            )
        return await self._request_futures_api(
            "delete", "batchOrders", True, data=params, force_params=True
        )

    async def futures_countdown_cancel_all(self, **params):
        return await self._request_futures_api(
            "post", "countdownCancelAll", True, data=params
        )

    async def futures_account_balance(self, **params):
        return await self._request_futures_api(
            "get", "balance", True, version=3, data=params
        )

    async def futures_account(self, **params):
        return await self._request_futures_api(
            "get", "account", True, version=2, data=params
        )

    async def futures_change_leverage(self, **params):
        return await self._request_futures_api("post", "leverage", True, data=params)

    async def futures_change_margin_type(self, **params):
        return await self._request_futures_api("post", "marginType", True, data=params)

    async def futures_change_position_margin(self, **params):
        return await self._request_futures_api(
            "post", "positionMargin", True, data=params
        )

    async def futures_position_margin_history(self, **params):
        return await self._request_futures_api(
            "get", "positionMargin/history", True, data=params
        )

    async def futures_position_information(self, **params):
        return await self._request_futures_api(
            "get", "positionRisk", True, version=3, data=params
        )

    async def futures_account_trades(self, **params):
        return await self._request_futures_api("get", "userTrades", True, data=params)

    async def futures_income_history(self, **params):
        return await self._request_futures_api("get", "income", True, data=params)

    async def futures_change_position_mode(self, **params):
        return await self._request_futures_api(
            "post", "positionSide/dual", True, data=params
        )

    async def futures_get_position_mode(self, **params):
        return await self._request_futures_api(
            "get", "positionSide/dual", True, data=params
        )

    async def futures_change_multi_assets_mode(self, multiAssetsMargin: bool):
        params = {"multiAssetsMargin": "true" if multiAssetsMargin else "false"}
        return await self._request_futures_api(
            "post", "multiAssetsMargin", True, data=params
        )

    async def futures_get_multi_assets_mode(self):
        return await self._request_futures_api(
            "get", "multiAssetsMargin", True, data={}
        )

    async def futures_stream_get_listen_key(self):
        res = await self._request_futures_api(
            "post", "listenKey", signed=False, data={}
        )
        return res["listenKey"]

    async def futures_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_api(
            "put", "listenKey", signed=False, data=params
        )

    async def futures_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_api(
            "delete", "listenKey", signed=False, data=params
        )

    # new methods
    async def futures_account_config(self, **params):
        return await self._request_futures_api(
            "get", "accountConfig", signed=True, version=1, data=params
        )

    async def futures_symbol_config(self, **params):
        return await self._request_futures_api(
            "get", "symbolConfig", signed=True, version=1, data=params
        )

    # COIN Futures API

    async def futures_coin_ping(self):
        return await self._request_futures_coin_api("get", "ping")

    async def futures_coin_time(self):
        return await self._request_futures_coin_api("get", "time")

    async def futures_coin_exchange_info(self):
        return await self._request_futures_coin_api("get", "exchangeInfo")

    async def futures_coin_order_book(self, **params):
        return await self._request_futures_coin_api("get", "depth", data=params)

    async def futures_coin_recent_trades(self, **params):
        return await self._request_futures_coin_api("get", "trades", data=params)

    async def futures_coin_historical_trades(self, **params):
        return await self._request_futures_coin_api(
            "get", "historicalTrades", data=params
        )

    async def futures_coin_aggregate_trades(self, **params):
        return await self._request_futures_coin_api("get", "aggTrades", data=params)

    async def futures_coin_klines(self, **params):
        return await self._request_futures_coin_api("get", "klines", data=params)

    async def futures_coin_continous_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "continuousKlines", data=params
        )

    async def futures_coin_index_price_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "indexPriceKlines", data=params
        )

    async def futures_coin_mark_price_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "markPriceKlines", data=params
        )

    futures_coin_mark_price_klines.__doc__ = Client.futures_mark_price_klines.__doc__

    async def futures_coin_premium_index_klines(self, **params):
        return await self._request_futures_coin_api(
            "get", "premiumIndexKlines", data=params
        )

    futures_coin_premium_index_klines.__doc__ = (
        Client.futures_premium_index_klines.__doc__
    )

    async def futures_coin_mark_price(self, **params):
        return await self._request_futures_coin_api("get", "premiumIndex", data=params)

    async def futures_coin_funding_rate(self, **params):
        return await self._request_futures_coin_api("get", "fundingRate", data=params)

    async def futures_coin_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/24hr", data=params)

    async def futures_coin_symbol_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/price", data=params)

    async def futures_coin_orderbook_ticker(self, **params):
        return await self._request_futures_coin_api(
            "get", "ticker/bookTicker", data=params
        )

    async def futures_coin_index_price_constituents(self, **params):
        return await self._request_futures_coin_api("get", "constituents", data=params)

    futures_coin_index_price_constituents.__doc__ = (
        Client.futures_coin_index_price_constituents.__doc__
    )

    async def futures_coin_liquidation_orders(self, **params):
        return await self._request_futures_coin_api(
            "get", "forceOrders", signed=True, data=params
        )

    async def futures_coin_open_interest(self, **params):
        return await self._request_futures_coin_api("get", "openInterest", data=params)

    async def futures_coin_open_interest_hist(self, **params):
        return await self._request_futures_coin_data_api(
            "get", "openInterestHist", data=params
        )

    async def futures_coin_leverage_bracket(self, **params):
        return await self._request_futures_coin_api(
            "get", "leverageBracket", version=2, signed=True, data=params
        )

    async def new_transfer_history(self, **params):
        return await self._request_margin_api(
            "get", "asset/transfer", True, data=params
        )

    async def funding_wallet(self, **params):
        return await self._request_margin_api(
            "post", "asset/get-funding-asset", True, data=params
        )

    async def get_user_asset(self, **params):
        return await self._request_margin_api(
            "post", "asset/getUserAsset", True, data=params, version=3
        )

    async def universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    async def futures_coin_create_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_futures_coin_api("post", "order", True, data=params)

    async def futures_coin_place_batch_order(self, **params):
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        query_string = urlencode(params)
        query_string = query_string.replace("%27", "%22")
        params["batchOrders"] = query_string[12:]

        return await self._request_futures_coin_api(
            "post", "batchOrders", True, data=params
        )

    async def futures_coin_get_order(self, **params):
        return await self._request_futures_coin_api("get", "order", True, data=params)

    async def futures_coin_get_open_orders(self, **params):
        return await self._request_futures_coin_api(
            "get", "openOrders", True, data=params
        )

    async def futures_coin_get_all_orders(self, **params):
        return await self._request_futures_coin_api(
            "get", "allOrders", signed=True, data=params
        )

    async def futures_coin_cancel_order(self, **params):
        return await self._request_futures_coin_api(
            "delete", "order", signed=True, data=params
        )

    async def futures_coin_cancel_all_open_orders(self, **params):
        return await self._request_futures_coin_api(
            "delete", "allOpenOrders", signed=True, data=params, force_params=True
        )

    async def futures_coin_cancel_orders(self, **params):
        if params.get("orderidlist"):
            params["orderidlist"] = quote(
                convert_list_to_json_array(params["orderidlist"])
            )
        if params.get("origclientorderidlist"):
            params["origclientorderidlist"] = quote(
                convert_list_to_json_array(params["origclientorderidlist"])
            )
        return await self._request_futures_coin_api(
            "delete", "batchOrders", True, data=params
        )

    async def futures_coin_account_balance(self, **params):
        return await self._request_futures_coin_api(
            "get", "balance", signed=True, data=params
        )

    async def futures_coin_account(self, **params):
        return await self._request_futures_coin_api(
            "get", "account", signed=True, data=params
        )

    async def futures_coin_change_leverage(self, **params):
        return await self._request_futures_coin_api(
            "post", "leverage", signed=True, data=params
        )

    async def futures_coin_change_margin_type(self, **params):
        return await self._request_futures_coin_api(
            "post", "marginType", signed=True, data=params
        )

    async def futures_coin_change_position_margin(self, **params):
        return await self._request_futures_coin_api(
            "post", "positionMargin", True, data=params
        )

    async def futures_coin_position_margin_history(self, **params):
        return await self._request_futures_coin_api(
            "get", "positionMargin/history", True, data=params
        )

    async def futures_coin_position_information(self, **params):
        return await self._request_futures_coin_api(
            "get", "positionRisk", True, data=params
        )

    async def futures_coin_account_trades(self, **params):
        return await self._request_futures_coin_api(
            "get", "userTrades", True, data=params
        )

    async def futures_coin_income_history(self, **params):
        return await self._request_futures_coin_api("get", "income", True, data=params)

    async def futures_coin_change_position_mode(self, **params):
        return await self._request_futures_coin_api(
            "post", "positionSide/dual", True, data=params
        )

    async def futures_coin_get_position_mode(self, **params):
        return await self._request_futures_coin_api(
            "get", "positionSide/dual", True, data=params
        )

    async def futures_coin_stream_get_listen_key(self):
        res = await self._request_futures_coin_api(
            "post", "listenKey", signed=False, data={}
        )
        return res["listenKey"]

    async def futures_coin_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_coin_api(
            "put", "listenKey", signed=False, data=params
        )

    async def futures_coin_account_order_history_download(self, **params):
        return await self._request_futures_coin_api(
            "get", "order/asyn", True, data=params
        )

    futures_coin_account_order_history_download.__doc__ = (
        Client.futures_coin_account_order_history_download.__doc__
    )

    async def futures_coin_account_order_history_download_link(self, **params):
        return await self._request_futures_coin_api(
            "get", "order/asyn/id", True, data=params
        )

    futures_coin_account_order_history_download_link.__doc__ = (
        Client.futures_coin_accout_order_history_download_link.__doc__
    )

    async def futures_coin_account_trade_history_download(self, **params):
        return await self._request_futures_coin_api(
            "get", "trade/asyn", True, data=params
        )

    futures_coin_account_trade_history_download.__doc__ = (
        Client.futures_coin_account_trade_history_download.__doc__
    )

    async def futures_coin_account_trade_history_download_link(self, **params):
        return await self._request_futures_coin_api(
            "get", "trade/asyn/id", True, data=params
        )

    futures_coin_account_trade_history_download_link.__doc__ = (
        Client.futures_coin_account_trade_history_download_link.__doc__
    )

    async def futures_coin_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_futures_coin_api(
            "delete", "listenKey", signed=False, data=params
        )

    async def get_all_coins_info(self, **params):
        return await self._request_margin_api(
            "get", "capital/config/getall", True, data=params
        )

    async def get_account_snapshot(self, **params):
        return await self._request_margin_api(
            "get", "accountSnapshot", True, data=params
        )

    async def disable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api(
            "post", "disableFastWithdrawSwitch", True, data=params
        )

    async def enable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api(
            "post", "enableFastWithdrawSwitch", True, data=params
        )

    """
    ====================================================================================================================
    Options API
    ====================================================================================================================
    """

    # Quoting interface endpoints

    async def options_ping(self):
        return await self._request_options_api("get", "ping")

    async def options_time(self):
        return await self._request_options_api("get", "time")

    async def options_info(self):
        return await self._request_options_api("get", "optionInfo")

    async def options_exchange_info(self):
        return await self._request_options_api("get", "exchangeInfo")

    async def options_index_price(self, **params):
        return await self._request_options_api("get", "index", data=params)

    async def options_price(self, **params):
        return await self._request_options_api("get", "ticker", data=params)

    async def options_mark_price(self, **params):
        return await self._request_options_api("get", "mark", data=params)

    async def options_order_book(self, **params):
        return await self._request_options_api("get", "depth", data=params)

    async def options_klines(self, **params):
        return await self._request_options_api("get", "klines", data=params)

    async def options_recent_trades(self, **params):
        return await self._request_options_api("get", "trades", data=params)

    async def options_historical_trades(self, **params):
        return await self._request_options_api("get", "historicalTrades", data=params)

    # Account and trading interface endpoints

    async def options_account_info(self, **params):
        return await self._request_options_api(
            "get", "account", signed=True, data=params
        )

    async def options_funds_transfer(self, **params):
        return await self._request_options_api(
            "post", "transfer", signed=True, data=params
        )

    async def options_positions(self, **params):
        return await self._request_options_api(
            "get", "position", signed=True, data=params
        )

    async def options_bill(self, **params):
        return await self._request_options_api("post", "bill", signed=True, data=params)

    async def options_place_order(self, **params):
        if "clientOrderId" not in params:
            params["clientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_options_api(
            "post", "order", signed=True, data=params
        )

    async def options_place_batch_order(self, **params):
        for order in params["batchOrders"]:
            if "newClientOrderId" not in order:
                order["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_options_api(
            "post", "batchOrders", signed=True, data=params
        )

    async def options_cancel_order(self, **params):
        return await self._request_options_api(
            "delete", "order", signed=True, data=params
        )

    async def options_cancel_batch_order(self, **params):
        return await self._request_options_api(
            "delete", "batchOrders", signed=True, data=params
        )

    async def options_cancel_all_orders(self, **params):
        return await self._request_options_api(
            "delete", "allOpenOrders", signed=True, data=params
        )

    async def options_query_order(self, **params):
        return await self._request_options_api("get", "order", signed=True, data=params)

    async def options_query_pending_orders(self, **params):
        return await self._request_options_api(
            "get", "openOrders", signed=True, data=params
        )

    async def options_query_order_history(self, **params):
        return await self._request_options_api(
            "get", "historyOrders", signed=True, data=params
        )

    async def options_user_trades(self, **params):
        return await self._request_options_api(
            "get", "userTrades", signed=True, data=params
        )

    # Fiat Endpoints

    async def get_fiat_deposit_withdraw_history(self, **params):
        return await self._request_margin_api(
            "get", "fiat/orders", signed=True, data=params
        )

    async def get_fiat_payments_history(self, **params):
        return await self._request_margin_api(
            "get", "fiat/payments", signed=True, data=params
        )

    # C2C Endpoints

    async def get_c2c_trade_history(self, **params):
        return await self._request_margin_api(
            "get", "c2c/orderMatch/listUserOrderHistory", signed=True, data=params
        )

    # Pay Endpoints

    async def get_pay_trade_history(self, **params):
        return await self._request_margin_api(
            "get", "pay/transactions", signed=True, data=params
        )

    get_pay_trade_history.__doc__ = Client.get_pay_trade_history.__doc__

    # Convert Endpoints

    async def get_convert_trade_history(self, **params):
        return await self._request_margin_api(
            "get", "convert/tradeFlow", signed=True, data=params
        )

    get_convert_trade_history.__doc__ = Client.get_convert_trade_history.__doc__

    async def convert_request_quote(self, **params):
        return await self._request_margin_api(
            "post", "convert/getQuote", signed=True, data=params
        )

    convert_request_quote.__doc__ = Client.convert_request_quote.__doc__

    async def convert_accept_quote(self, **params):
        return await self._request_margin_api(
            "post", "convert/acceptQuote", signed=True, data=params
        )

    convert_accept_quote.__doc__ = Client.convert_accept_quote.__doc__

    """
    ====================================================================================================================
    PortfolioMargin API
    ====================================================================================================================
    """

    async def papi_stream_get_listen_key(self):
        res = await self._request_papi_api("post", "listenKey", signed=False, data={})
        return res["listenKey"]

    papi_stream_get_listen_key.__doc__ = Client.papi_stream_get_listen_key.__doc__

    async def papi_stream_keepalive(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_papi_api(
            "put", "listenKey", signed=False, data=params
        )

    papi_stream_keepalive.__doc__ = Client.papi_stream_keepalive.__doc__

    async def papi_stream_close(self, listenKey):
        params = {"listenKey": listenKey}
        return await self._request_papi_api(
            "delete", "listenKey", signed=False, data=params
        )

    papi_stream_close.__doc__ = Client.papi_stream_close.__doc__

    async def papi_get_balance(self, **params):
        return await self._request_papi_api("get", "balance", signed=True, data=params)
    papi_get_balance.__doc__ = Client.papi_get_balance.__doc__

    async def papi_get_rate_limit(self, **params):
        return await self._request_papi_api("get", "rateLimit/order", signed=True, data=params)
    papi_get_rate_limit.__doc__ = Client.papi_get_rate_limit.__doc__

    async def papi_get_account(self, **params):
        return await self._request_papi_api("get", "account", signed=True, data=params)

    async def papi_get_margin_max_borrowable(self, **params):
        return await self._request_papi_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )

    async def papi_get_margin_max_withdraw(self, **params):
        return await self._request_papi_api(
            "get", "margin/maxWithdraw", signed=True, data=params
        )

    async def papi_get_um_position_risk(self, **params):
        return await self._request_papi_api(
            "get", "um/positionRisk", signed=True, data=params
        )

    async def papi_get_cm_position_risk(self, **params):
        return await self._request_papi_api(
            "get", "cm/positionRisk", signed=True, data=params
        )

    async def papi_set_um_leverage(self, **params):
        return await self._request_papi_api(
            "post", "um/leverage", signed=True, data=params
        )

    async def papi_set_cm_leverage(self, **params):
        return await self._request_papi_api(
            "post", "cm/leverage", signed=True, data=params
        )

    async def papi_change_um_position_side_dual(self, **params):
        return await self._request_papi_api(
            "post", "um/positionSide/dual", signed=True, data=params
        )

    async def papi_get_um_position_side_dual(self, **params):
        return await self._request_papi_api(
            "get", "um/positionSide/dual", signed=True, data=params
        )

    async def papi_get_cm_position_side_dual(self, **params):
        return await self._request_papi_api(
            "get", "cm/positionSide/dual", signed=True, data=params
        )

    async def papi_get_um_leverage_bracket(self, **params):
        return await self._request_papi_api(
            "get", "um/leverageBracket", signed=True, data=params
        )

    async def papi_get_cm_leverage_bracket(self, **params):
        return await self._request_papi_api(
            "get", "cm/leverageBracket", signed=True, data=params
        )

    async def papi_get_um_api_trading_status(self, **params):
        return await self._request_papi_api(
            "get", "um/apiTradingStatus", signed=True, data=params
        )

    async def papi_get_um_comission_rate(self, **params):
        return await self._request_papi_api(
            "get", "um/commissionRate", signed=True, data=params
        )

    async def papi_get_cm_comission_rate(self, **params):
        return await self._request_papi_api(
            "get", "cm/commissionRate", signed=True, data=params
        )

    async def papi_get_margin_margin_loan(self, **params):
        return await self._request_papi_api(
            "get", "margin/marginLoan", signed=True, data=params
        )

    async def papi_get_margin_repay_loan(self, **params):
        return await self._request_papi_api(
            "get", "margin/repayLoan", signed=True, data=params
        )

    async def papi_get_repay_futures_switch(self, **params):
        return await self._request_papi_api(
            "get", "repay-futures-switch", signed=True, data=params
        )

    async def papi_repay_futures_switch(self, **params):
        return await self._request_papi_api(
            "post", "repay-futures-switch", signed=True, data=params
        )

    async def papi_get_margin_interest_history(self, **params):
        return await self._request_papi_api(
            "get", "margin/marginInterestHistory", signed=True, data=params
        )

    async def papi_repay_futures_negative_balance(self, **params):
        return await self._request_papi_api(
            "post", "repay-futures-negative-balance", signed=True, data=params
        )

    async def papi_get_portfolio_interest_history(self, **params):
        return await self._request_papi_api(
            "get", "portfolio/interest-history", signed=True, data=params
        )


    async def papi_get_portfolio_negative_balance_exchange_record(self, **params):
        return await self._request_papi_api(
            "get", "portfolio/negative-balance-exchange-record", signed=True, data=params
        )
    papi_get_portfolio_negative_balance_exchange_record.__doc__ = Client.papi_get_portfolio_negative_balance_exchange_record.__doc__

    async def papi_fund_auto_collection(self, **params):
        return await self._request_papi_api(
            "post", "auto-collection", signed=True, data=params
        )

    async def papi_fund_asset_collection(self, **params):
        return await self._request_papi_api(
            "post", "asset-collection", signed=True, data=params
        )

    async def papi_bnb_transfer(self, **params):
        return await self._request_papi_api(
            "post", "bnb-transfer", signed=True, data=params
        )

    async def papi_get_um_income_history(self, **params):
        return await self._request_papi_api(
            "get", "um/income", signed=True, data=params
        )

    async def papi_get_cm_income_history(self, **params):
        return await self._request_papi_api(
            "get", "cm/income", signed=True, data=params
        )

    async def papi_get_um_account(self, **params):
        return await self._request_papi_api(
            "get", "um/account", signed=True, data=params
        )

    async def papi_get_um_account_v2(self, **params):
        return await self._request_papi_api(
            "get", "um/account", version=2, signed=True, data=params
        )

    async def papi_get_cm_account(self, **params):
        return await self._request_papi_api(
            "get", "cm/account", signed=True, data=params
        )

    async def papi_get_um_account_config(self, **params):
        return await self._request_papi_api(
            "get", "um/accountConfig", signed=True, data=params
        )

    async def papi_get_um_symbol_config(self, **params):
        return await self._request_papi_api(
            "get", "um/symbolConfig", signed=True, data=params
        )

    async def papi_get_um_trade_asyn(self, **params):
        return await self._request_papi_api(
            "get", "um/trade/asyn", signed=True, data=params
        )

    async def papi_get_um_trade_asyn_id(self, **params):
        return await self._request_papi_api(
            "get", "um/trade/asyn/id", signed=True, data=params
        )

    async def papi_get_um_order_asyn(self, **params):
        return await self._request_papi_api(
            "get", "um/order/asyn", signed=True, data=params
        )

    async def papi_get_um_order_asyn_id(self, **params):
        return await self._request_papi_api(
            "get", "um/order/asyn/id", signed=True, data=params
        )

    async def papi_get_um_income_asyn(self, **params):
        return await self._request_papi_api(
            "get", "um/income/asyn", signed=True, data=params
        )

    async def papi_get_um_income_asyn_id(self, **params):
        return await self._request_papi_api(
            "get", "um/income/asyn/id", signed=True, data=params
        )

    async def papi_ping(self, **params):
        return await self._request_papi_api("get", "ping", signed=False, data=params)

    # papi trading endpoints

    async def papi_create_um_order(self, **params):
        """Place new UM order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "um/order", signed=True, data=params
        )

    async def papi_create_um_conditional_order(self, **params):
        """Place new UM Conditional order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-UM-Conditional-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "um/conditional/order", signed=True, data=params
        )

    async def papi_create_cm_order(self, **params):
        """Place new CM order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "cm/order", signed=True, data=params
        )

    async def papi_create_cm_conditional_order(self, **params):
        """Place new CM Conditional order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-CM-Conditional-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "cm/conditional/order", signed=True, data=params
        )

    async def papi_create_margin_order(self, **params):
        """New Margin Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/New-Margin-Order

        :returns: API response

        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._request_papi_api(
            "post", "margin/order", signed=True, data=params
        )

    async def papi_margin_loan(self, **params):
        """Apply for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Borrow

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "marginLoan", signed=True, data=params
        )

    async def papi_repay_loan(self, **params):
        """Repay for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Repay

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "repayLoan", signed=True, data=params
        )

    async def papi_margin_order_oco(self, **params):
        """Send in a new OCO for a margin account.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-New-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "margin/order/oco", signed=True, data=params
        )

    async def papi_cancel_um_order(self, **params):
        """Cancel an active UM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/order", signed=True, data=params
        )

    async def papi_cancel_um_all_open_orders(self, **params):
        """Cancel an active UM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/allOpenOrders", signed=True, data=params
        )

    async def papi_cancel_um_conditional_order(self, **params):
        """Cancel UM Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-UM-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/conditional/order", signed=True, data=params
        )

    async def papi_cancel_um_conditional_all_open_orders(self, **params):
        """Cancel All UM Open Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-UM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "um/conditional/allOpenOrders", signed=True, data=params
        )

    async def papi_cancel_cm_order(self, **params):
        """Cancel an active CM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/order", signed=True, data=params
        )

    async def papi_cancel_cm_all_open_orders(self, **params):
        """Cancel an active CM LIMIT order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/allOpenOrders", signed=True, data=params
        )

    async def papi_cancel_cm_conditional_order(self, **params):
        """Cancel CM Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-CM-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/conditional/order", signed=True, data=params
        )

    async def papi_cancel_cm_conditional_all_open_orders(self, **params):
        """Cancel All CM Open Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-All-CM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "cm/conditional/allOpenOrders", signed=True, data=params
        )

    async def papi_cancel_margin_order(self, **params):
        """Cancel Margin Account Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "margin/order", signed=True, data=params
        )

    async def papi_cancel_margin_order_list(self, **params):
        """Cancel Margin Account OCO Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-OCO-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "margin/orderList", signed=True, data=params
        )

    async def papi_cancel_margin_all_open_orders(self, **params):
        """Cancel Margin Account All Open Orders on a Symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Cancel-Margin-Account-All-Open-Orders-on-a-Symbol

        :returns: API response

        """
        return await self._request_papi_api(
            "delete", "margin/allOpenOrders", signed=True, data=params
        )

    async def papi_modify_um_order(self, **params):
        """Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-UM-Order

        :returns: API response

        """
        return await self._request_papi_api("put", "um/order", signed=True, data=params)

    async def papi_modify_cm_order(self, **params):
        """Order modify function, currently only LIMIT order modification is supported, modified orders will be reordered in the match queue.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Modify-CM-Order

        :returns: API response

        """
        return await self._request_papi_api("put", "cm/order", signed=True, data=params)

    async def papi_get_um_order(self, **params):
        """Check an UM order's status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Order

        :returns: API response

        """
        return await self._request_papi_api("get", "um/order", signed=True, data=params)

    async def papi_get_um_all_orders(self, **params):
        """Get all account UM orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/allOrders", signed=True, data=params
        )

    async def papi_get_um_open_order(self, **params):
        """Query current UM open order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/openOrder", signed=True, data=params
        )

    async def papi_get_um_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/openOrders", signed=True, data=params
        )

    async def papi_get_um_conditional_all_orders(self, **params):
        """Query All UM Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-UM-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/allOrders", signed=True, data=params
        )

    async def papi_get_um_conditional_open_orders(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-UM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/openOrders", signed=True, data=params
        )

    async def papi_get_um_conditional_open_order(self, **params):
        """Query Current UM Open Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-UM-Open-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/openOrder", signed=True, data=params
        )

    async def papi_get_um_conditional_order_history(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Conditional-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/conditional/orderHistory", signed=True, data=params
        )

    async def papi_get_cm_order(self, **params):
        """Check an CM order's status.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Order

        :returns: API response

        """
        return await self._request_papi_api("get", "cm/order", signed=True, data=params)

    async def papi_get_cm_all_orders(self, **params):
        """Get all account CM orders; active, canceled, or filled.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/allOrders", signed=True, data=params
        )

    async def papi_get_cm_open_order(self, **params):
        """Query current CM open order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/openOrder", signed=True, data=params
        )

    async def papi_get_cm_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/openOrders", signed=True, data=params
        )

    async def papi_get_cm_conditional_all_orders(self, **params):
        """Query All CM Conditional Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-CM-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/allOrders", signed=True, data=params
        )

    async def papi_get_cm_conditional_open_orders(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Current-CM-Open-Conditional-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/openOrders", signed=True, data=params
        )

    async def papi_get_cm_conditional_open_order(self, **params):
        """Query Current UM Open Conditional Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Current-CM-Open-Conditional-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/openOrder", signed=True, data=params
        )

    async def papi_get_cm_conditional_order_history(self, **params):
        """Get all open conditional orders on a symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Conditional-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/conditional/orderHistory", signed=True, data=params
        )

    async def papi_get_um_force_orders(self, **params):
        """Query User's UM Force Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-UM-Force-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/forceOrders", signed=True, data=params
        )

    async def papi_get_cm_force_orders(self, **params):
        """Query User's CM Force Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-CM-Force-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/forceOrders", signed=True, data=params
        )

    async def papi_get_um_order_amendment(self, **params):
        """Get order modification history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-UM-Modify-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/orderAmendment", signed=True, data=params
        )

    async def papi_get_cm_order_amendment(self, **params):
        """Get order modification history.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-CM-Modify-Order-History

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/orderAmendment", signed=True, data=params
        )

    async def papi_get_margin_force_orders(self, **params):
        """Query user's margin force orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Users-Margin-Force-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/forceOrders", signed=True, data=params
        )

    async def papi_get_um_user_trades(self, **params):
        """Get trades for a specific account and UM symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/userTrades", signed=True, data=params
        )

    async def papi_get_cm_user_trades(self, **params):
        """Get trades for a specific account and CM symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/userTrades", signed=True, data=params
        )

    async def papi_get_um_adl_quantile(self, **params):
        """Query UM Position ADL Quantile Estimation.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/UM-Position-ADL-Quantile-Estimation

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/adlQuantile", signed=True, data=params
        )

    async def papi_get_cm_adl_quantile(self, **params):
        """Query CM Position ADL Quantile Estimation.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/CM-Position-ADL-Quantile-Estimation

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "cm/adlQuantile", signed=True, data=params
        )

    async def papi_set_um_fee_burn(self, **params):
        """Change user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off ) on EVERY symbol.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Toggle-BNB-Burn-On-UM-Futures-Trade

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "um/feeBurn", signed=True, data=params
        )

    async def papi_get_um_fee_burn(self, **params):
        """Get user's BNB Fee Discount for UM Futures (Fee Discount On or Fee Discount Off).

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Get-UM-Futures-BNB-Burn-Status

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "um/feeBurn", signed=True, data=params
        )

    async def papi_get_margin_order(self, **params):
        """Query Margin Account Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/order", signed=True, data=params
        )

    async def papi_get_margin_open_orders(self, **params):
        """Query Current Margin Open Order.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Order

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/openOrders", signed=True, data=params
        )

    async def papi_get_margin_all_orders(self, **params):
        """Query All Margin Account Orders.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-All-Margin-Account-Orders

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/allOrders", signed=True, data=params
        )

    async def papi_get_margin_order_list(self, **params):
        """Retrieves a specific OCO based on provided optional parameters.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/orderList", signed=True, data=params
        )

    async def papi_get_margin_all_order_list(self, **params):
        """Query all OCO for a specific margin account based on provided optional parameters.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-all-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/allOrderList", signed=True, data=params
        )

    async def papi_get_margin_open_order_list(self, **params):
        """Query Margin Account's Open OCO.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Query-Margin-Account-Open-OCO

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/openOrderList", signed=True, data=params
        )

    async def papi_get_margin_my_trades(self, **params):
        """Margin Account Trade List.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "get", "margin/myTrades", signed=True, data=params
        )

    async def papi_get_margin_repay_debt(self, **params):
        """Repay debt for a margin loan.

        https://developers.binance.com/docs/derivatives/portfolio-margin/trade/Margin-Account-Trade-List

        :returns: API response

        """
        return await self._request_papi_api(
            "post", "margin/repay-debt", signed=True, data=params
        )

    async def create_oco_order(self, **params):
        if "listClientOrderId" not in params:
            params["listClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._post("orderList/oco", True, data=params)

    ############################################################
    # WebSocket API methods
    ############################################################

    async def ws_create_test_order(self, **params):
        """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.
        https://binance-docs.github.io/apidocs/websocket_api/en/#test-new-order-trade
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param timeInForce: required if limit order
        :type timeInForce: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: The number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        .. code-block:: python
            {}
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()

        return await self._ws_api_request("order.test", True, params)

    async def ws_create_order(self, **params):
        """Create an order via WebSocket.
        https://binance-docs.github.io/apidocs/websocket_api/en/#place-new-order-trade
        :param id: The request ID to be used. By default uuid22() is used.
        :param symbol: The symbol to create an order for
        :param side: BUY or SELL
        :param type: Order type (e.g., LIMIT, MARKET)
        :param quantity: The amount to buy or sell
        :param kwargs: Additional order parameters
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()

        return await self._ws_api_request("order.place", True, params)

    async def ws_order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
        """Send in a new limit order
        Any order with an icebergQty MUST have timeInForce set to GTC.
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({
            "type": self.ORDER_TYPE_LIMIT,
            "timeInForce": timeInForce,
        })
        return await self.ws_create_order(**params)

    async def ws_order_limit_buy(
        self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params
    ):
        """Send in a new limit buy order
        Any order with an icebergQty MUST have timeInForce set to GTC.
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({
            "side": self.SIDE_BUY,
        })
        return await self.ws_order_limit(timeInForce=timeInForce, **params)

    async def ws_order_limit_sell(
        self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params
    ):
        """Send in a new limit sell order
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param timeInForce: default Good till cancelled
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param stopPrice: Used with stop orders
        :type stopPrice: decimal
        :param icebergQty: Used with iceberg orders
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_SELL})
        return await self.ws_order_limit(timeInForce=timeInForce, **params)

    async def ws_order_market(self, **params):
        """Send in a new market order
        :param symbol: required
        :type symbol: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"type": self.ORDER_TYPE_MARKET})
        return await self.ws_create_order(**params)

    async def ws_order_market_buy(self, **params):
        """Send in a new market buy order
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to spend of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_BUY})
        return await self.ws_order_market(**params)

    async def ws_order_market_sell(self, **params):
        """Send in a new market sell order
        :param symbol: required
        :type symbol: str
        :param quantity: required
        :type quantity: decimal
        :param quoteOrderQty: the amount the user wants to receive of the quote asset
        :type quoteOrderQty: decimal
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: WS response
        See order endpoint for full response options
        """
        params.update({"side": self.SIDE_SELL})
        return await self.ws_order_market(**params)

    async def ws_get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.
        https://binance-docs.github.io/apidocs/websocket_api/en/#query-order-user_data
        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        """

        return await self._ws_api_request("order.status", True, params)

    async def ws_cancel_order(self, **params):
        return await self._ws_api_request("order.cancel", True, params)

    ws_cancel_order.__doc__ = Client.ws_cancel_order.__doc__

    async def cancel_all_open_orders(self, **params):
        return await self._delete("openOrders", True, data=params)

    async def cancel_replace_order(self, **params):
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.SPOT_ORDER_PREFIX + self.uuid22()
        return await self._post("order/cancelReplace", signed=True, data=params)

    cancel_replace_order.__doc__ = Client.cancel_replace_order.__doc__

    async def ws_cancel_and_replace_order(self, **params):
        return await self._ws_api_request("order.cancelReplace", True, params)

    ws_cancel_and_replace_order.__doc__ = Client.ws_cancel_and_replace_order.__doc__

    async def ws_get_open_orders(self, **params):
        return await self._ws_api_request("openOrders.status", True, params)

    ws_get_open_orders.__doc__ = Client.ws_get_open_orders.__doc__

    async def ws_cancel_all_open_orders(self, **params):
        return await self._ws_api_request("openOrders.cancelAll", True, params)

    ws_cancel_all_open_orders.__doc__ = Client.ws_cancel_all_open_orders.__doc__

    async def ws_create_oco_order(self, **params):
        return await self._ws_api_request("orderList.place.oco", True, params)

    ws_create_oco_order.__doc__ = Client.ws_create_oco_order.__doc__

    async def ws_create_oto_order(self, **params):
        return await self._ws_api_request("orderList.place.oto", True, params)

    ws_create_oto_order.__doc__ = Client.ws_create_oto_order.__doc__

    async def ws_create_otoco_order(self, **params):
        return await self._ws_api_request("orderList.place.otoco", True, params)

    ws_create_otoco_order.__doc__ = Client.ws_create_otoco_order.__doc__

    async def ws_get_oco_order(self, **params):
        return await self._ws_api_request("orderList.status", True, params)

    ws_get_oco_order.__doc__ = Client.ws_get_oco_order.__doc__

    async def ws_cancel_oco_order(self, **params):
        return await self._ws_api_request("orderList.cancel", True, params)

    ws_cancel_oco_order.__doc__ = Client.ws_cancel_oco_order.__doc__

    async def ws_get_oco_open_orders(self, **params):
        return await self._ws_api_request("openOrderLists.status", True, params)

    ws_get_oco_open_orders.__doc__ = Client.ws_get_oco_open_orders.__doc__

    async def ws_create_sor_order(self, **params):
        return await self._ws_api_request("sor.order.place", True, params)

    ws_create_sor_order.__doc__ = Client.ws_create_sor_order.__doc__

    async def ws_create_test_sor_order(self, **params):
        return await self._ws_api_request("sor.order.test", True, params)

    ws_create_test_sor_order.__doc__ = Client.ws_create_test_sor_order.__doc__

    async def ws_get_account(self, **params):
        return await self._ws_api_request("account.status", True, params)

    ws_get_account.__doc__ = Client.ws_get_account.__doc__

    async def ws_get_account_rate_limits_orders(self, **params):
        return await self._ws_api_request("account.rateLimits.orders", True, params)

    ws_get_account_rate_limits_orders.__doc__ = Client.ws_get_account_rate_limits_orders.__doc__

    async def ws_get_all_orders(self, **params):
        return await self._ws_api_request("allOrders", True, params)

    ws_get_all_orders.__doc__ = Client.ws_get_all_orders.__doc__

    async def ws_get_my_trades(self, **params):
        return await self._ws_api_request("myTrades", True, params)

    ws_get_my_trades.__doc__ = Client.ws_get_my_trades.__doc__

    async def ws_get_prevented_matches(self, **params):
        return await self._ws_api_request("myPreventedMatches", True, params)

    ws_get_prevented_matches.__doc__ = Client.ws_get_prevented_matches.__doc__

    async def ws_get_allocations(self, **params):
        return await self._ws_api_request("myAllocations", True, params)

    ws_get_allocations.__doc__ = Client.ws_get_allocations.__doc__

    async def ws_get_commission_rates(self, **params):
        return await self._ws_api_request("account.commission", True, params)

    ws_get_commission_rates.__doc__ = Client.ws_get_commission_rates.__doc__

    async def ws_get_order_book(self, **params):
        return await self._ws_api_request("depth", False, params)

    ws_get_order_book.__doc__ = Client.ws_get_order_book.__doc__

    async def ws_get_recent_trades(self, **params):
        return await self._ws_api_request("trades.recent", False, params)

    ws_get_recent_trades.__doc__ = Client.ws_get_recent_trades.__doc__

    async def ws_get_historical_trades(self, **params):
        return await self._ws_api_request("trades.historical", False, params)

    ws_get_historical_trades.__doc__ = Client.ws_get_historical_trades.__doc__

    async def ws_get_aggregate_trades(self, **params):
        return await self._ws_api_request("trades.aggregate", False, params)

    ws_get_aggregate_trades.__doc__ = Client.ws_get_aggregate_trades.__doc__

    async def ws_get_klines(self, **params):
        return await self._ws_api_request("klines", False, params)

    ws_get_klines.__doc__ = Client.ws_get_klines.__doc__

    async def ws_get_uiKlines(self, **params):
        return await self._ws_api_request("uiKlines", False, params)

    ws_get_uiKlines.__doc__ = Client.ws_get_uiKlines.__doc__

    async def ws_get_avg_price(self, **params):
        return await self._ws_api_request("avgPrice", False, params)

    ws_get_avg_price.__doc__ = Client.ws_get_avg_price.__doc__

    async def ws_get_ticker(self, **params):
        return await self._ws_api_request("ticker.24hr", False, params)

    ws_get_ticker.__doc__ = Client.ws_get_ticker.__doc__

    async def ws_get_trading_day_ticker(self, **params):
        return await self._ws_api_request("ticker.tradingDay", False, params)

    ws_get_trading_day_ticker.__doc__ = Client.ws_get_trading_day_ticker.__doc__

    async def ws_get_symbol_ticker_window(self, **params):
        return await self._ws_api_request("ticker", False, params)

    ws_get_symbol_ticker_window.__doc__ = Client.ws_get_symbol_ticker_window.__doc__

    async def ws_get_symbol_ticker(self, **params):
        return await self._ws_api_request("ticker.price", False, params)

    ws_get_symbol_ticker.__doc__ = Client.ws_get_symbol_ticker.__doc__

    async def ws_get_orderbook_ticker(self, **params):
        return await self._ws_api_request("ticker.book", False, params)

    ws_get_orderbook_ticker.__doc__ = Client.ws_get_orderbook_ticker.__doc__

    async def ws_ping(self, **params):
        return await self._ws_api_request("ping", False, params)

    ws_ping.__doc__ = Client.ws_ping.__doc__

    async def ws_get_time(self, **params):
        return await self._ws_api_request("time", False, params)

    ws_get_time.__doc__ = Client.ws_get_time.__doc__

    async def ws_get_exchange_info(self, **params):
        return await self._ws_api_request("exchangeInfo", False, params)

    ws_get_exchange_info.__doc__ = Client.ws_get_exchange_info.__doc__

    ####################################################
    # FUTURES WS API Endpoints
    ####################################################
    async def ws_futures_get_order_book(self, **params):
        """
        Get the order book for a symbol
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api
        """
        return await self._ws_futures_api_request("depth", False, params)

    async def ws_futures_get_all_tickers(self, **params):
        """
        Latest price for a symbol or symbols
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api/Symbol-Price-Ticker
        """
        return await self._ws_futures_api_request("ticker.price", False, params)

    async def ws_futures_get_order_book_ticker(self, **params):
        """
        Best price/qty on the order book for a symbol or symbols.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/websocket-api/Symbol-Order-Book-Ticker
        """
        return await self._ws_futures_api_request("ticker.book", False, params)

    async def ws_futures_create_order(self, **params):
        """
        Send in a new order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api
        """
        if "newClientOrderId" not in params:
            params["newClientOrderId"] = self.CONTRACT_ORDER_PREFIX + self.uuid22()
        return await self._ws_futures_api_request("order.place", True, params)

    async def ws_futures_edit_order(self, **params):
        """
        Edit an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Modify-Order
        """
        return await self._ws_futures_api_request("order.modify", True, params)

    async def ws_futures_cancel_order(self, **params):
        """
        cancel an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Cancel-Order
        """
        return await self._ws_futures_api_request("order.cancel", True, params)

    async def ws_futures_get_order(self, **params):
        """
        Get an order
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Query-Order
        """
        return await self._ws_futures_api_request("order.status", True, params)

    async def ws_futures_v2_account_position(self, **params):
        """
        Get current position information(only symbol that has position or open orders will be return awaited).
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Position-Info-V2
        """
        return await self._ws_futures_api_request("v2/account.position", True, params)

    async def ws_futures_account_position(self, **params):
        """
        Get current position information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/websocket-api/Position-Information
        """
        return await self._ws_futures_api_request("account.position", True, params)

    async def ws_futures_v2_account_balance(self, **params):
        """
        Get current account information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api#api-description
        """
        return await self._ws_futures_api_request("v2/account.balance", True, params)

    async def ws_futures_account_balance(self, **params):
        """
        Get current account information.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Futures-Account-Balance
        """
        return await self._ws_futures_api_request("account.balance", True, params)

    async def ws_futures_v2_account_status(self, **params):
        """
        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Account-Information-V2
        """
        return await self._ws_futures_api_request("v2/account.status", True, params)

    async def ws_futures_account_status(self, **params):
        """
        Get current account information. User in single-asset/ multi-assets mode will see different value, see comments in response section for detail.
        https://developers.binance.com/docs/derivatives/usds-margined-futures/account/websocket-api/Account-Information
        """
        return await self._ws_futures_api_request("account.status", True, params)

    ####################################################
    # Gift Card API Endpoints
    ####################################################

    async def gift_card_fetch_token_limit(self, **params):
        return await self._request_margin_api(
            "get", "giftcard/buyCode/token-limit", signed=True, data=params
        )

    gift_card_fetch_token_limit.__doc__ = Client.gift_card_fetch_token_limit.__doc__

    async def gift_card_fetch_rsa_public_key(self, **params):
        return await self._request_margin_api(
            "get", "giftcard/cryptography/rsa-public-key", signed=True, data=params
        )

    gift_card_fetch_rsa_public_key.__doc__ = (
        Client.gift_card_fetch_rsa_public_key.__doc__
    )

    async def gift_card_verify(self, **params):
        return await self._request_margin_api(
            "get", "giftcard/verify", signed=True, data=params
        )

    gift_card_verify.__doc__ = Client.gift_card_verify.__doc__

    async def gift_card_redeem(self, **params):
        return await self._request_margin_api(
            "post", "giftcard/redeemCode", signed=True, data=params
        )

    gift_card_redeem.__doc__ = Client.gift_card_redeem.__doc__

    async def gift_card_create(self, **params):
        return await self._request_margin_api(
            "post", "giftcard/createCode", signed=True, data=params
        )

    gift_card_create.__doc__ = Client.gift_card_create.__doc__

    async def gift_card_create_dual_token(self, **params):
        return await self._request_margin_api(
            "post", "giftcard/buyCode", signed=True, data=params
        )

    gift_card_create_dual_token.__doc__ = Client.gift_card_create_dual_token.__doc__

    ####################################################
    # Options - Market Maker Block Trade
    ####################################################

    async def options_create_block_trade_order(self, **params):
        return await self._request_options_api(
            "post", "block/order/create", signed=True, data=params
        )

    options_create_block_trade_order.__doc__ = (
        Client.options_create_block_trade_order.__doc__
    )

    async def options_cancel_block_trade_order(self, **params):
        return await self._request_options_api(
            "delete", "block/order/create", signed=True, data=params
        )

    options_cancel_block_trade_order.__doc__ = (
        Client.options_cancel_block_trade_order.__doc__
    )

    async def options_extend_block_trade_order(self, **params):
        return await self._request_options_api(
            "put", "block/order/create", signed=True, data=params
        )

    options_extend_block_trade_order.__doc__ = (
        Client.options_extend_block_trade_order.__doc__
    )

    async def options_get_block_trade_orders(self, **params):
        return await self._request_options_api(
            "get", "block/order/orders", signed=True, data=params
        )

    options_get_block_trade_orders.__doc__ = (
        Client.options_get_block_trade_orders.__doc__
    )

    async def options_accept_block_trade_order(self, **params):
        return await self._request_options_api(
            "post", "block/order/execute", signed=True, data=params
        )

    options_accept_block_trade_order.__doc__ = (
        Client.options_accept_block_trade_order.__doc__
    )

    async def options_get_block_trade_order(self, **params):
        return await self._request_options_api(
            "get", "block/order/execute", signed=True, data=params
        )

    options_get_block_trade_order.__doc__ = Client.options_get_block_trade_order.__doc__

    async def options_account_get_block_trades(self, **params):
        return await self._request_options_api(
            "get", "block/user-trades", signed=True, data=params
        )

    options_account_get_block_trades.__doc__ = (
        Client.options_account_get_block_trades.__doc__
    )

    async def margin_next_hourly_interest_rate(self, **params):
        return await self._request_margin_api(
            "get", "margin/next-hourly-interest-rate", signed=True, data=params
        )

    margin_next_hourly_interest_rate.__doc__ = (
        Client.margin_next_hourly_interest_rate.__doc__
    )

    async def margin_interest_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/interestHistory", signed=True, data=params
        )

    margin_interest_history.__doc__ = Client.margin_interest_history.__doc__

    async def margin_borrow_repay(self, **params):
        return await self._request_margin_api(
            "post", "margin/borrow-repay", signed=True, data=params
        )

    margin_borrow_repay.__doc__ = Client.margin_borrow_repay.__doc__

    async def margin_get_borrow_repay_records(self, **params):
        return await self._request_margin_api(
            "get", "margin/borrow-repay", signed=True, data=params
        )

    margin_get_borrow_repay_records.__doc__ = (
        Client.margin_get_borrow_repay_records.__doc__
    )

    async def margin_interest_rate_history(self, **params):
        return await self._request_margin_api(
            "get", "margin/interestRateHistory", signed=True, data=params
        )

    margin_interest_rate_history.__doc__ = Client.margin_interest_rate_history.__doc__

    async def margin_max_borrowable(self, **params):
        return await self._request_margin_api(
            "get", "margin/maxBorrowable", signed=True, data=params
        )

    margin_max_borrowable.__doc__ = Client.margin_max_borrowable.__doc__

    ####################################################
    # Futures Data
    ####################################################

    async def futures_historical_data_link(self, **params):
        return await self._request_margin_api("get", "futures/data/histDataLink", signed=True, data=params)

    futures_historical_data_link.__doc__ = Client.futures_historical_data_link.__doc__

    async def margin_v1_get_loan_vip_ongoing_orders(self, **params):
        return await self._request_margin_api("get", "loan/vip/ongoing/orders", signed=True, data=params, version=1)
        
    margin_v1_get_loan_vip_ongoing_orders.__doc__ = Client.margin_v1_get_loan_vip_ongoing_orders.__doc__
            
    async def margin_v1_get_mining_payment_other(self, **params):
        return await self._request_margin_api("get", "mining/payment/other", signed=True, data=params, version=1)
        
    margin_v1_get_mining_payment_other.__doc__ = Client.margin_v1_get_mining_payment_other.__doc__
            
    async def futures_coin_v1_get_income_asyn_id(self, **params):
        return await self._request_futures_coin_api("get", "income/asyn/id", signed=True, data=params, version=1)
        
    futures_coin_v1_get_income_asyn_id.__doc__ = Client.futures_coin_v1_get_income_asyn_id.__doc__
            
    async def margin_v1_get_simple_earn_flexible_history_subscription_record(self, **params):
        return await self._request_margin_api("get", "simple-earn/flexible/history/subscriptionRecord", signed=True, data=params, version=1)
        
    margin_v1_get_simple_earn_flexible_history_subscription_record.__doc__ = Client.margin_v1_get_simple_earn_flexible_history_subscription_record.__doc__
            
    async def margin_v1_post_lending_auto_invest_one_off(self, **params):
        return await self._request_margin_api("post", "lending/auto-invest/one-off", signed=True, data=params, version=1)
        
    margin_v1_post_lending_auto_invest_one_off.__doc__ = Client.margin_v1_post_lending_auto_invest_one_off.__doc__
            
    async def margin_v1_post_broker_sub_account_api_commission_coin_futures(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/commission/coinFutures", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_commission_coin_futures.__doc__ = Client.margin_v1_post_broker_sub_account_api_commission_coin_futures.__doc__
            
    async def v3_post_order_list_otoco(self, **params):
        return await self._request_api("post", "orderList/otoco", signed=True, data=params, version="v3")
        
    v3_post_order_list_otoco.__doc__ = Client.v3_post_order_list_otoco.__doc__
            
    async def futures_v1_get_order_asyn(self, **params):
        return await self._request_futures_api("get", "order/asyn", signed=True, data=params, version=1)
        
    futures_v1_get_order_asyn.__doc__ = Client.futures_v1_get_order_asyn.__doc__
            
    async def margin_v1_get_asset_custody_transfer_history(self, **params):
        return await self._request_margin_api("get", "asset/custody/transfer-history", signed=True, data=params, version=1)
        
    margin_v1_get_asset_custody_transfer_history.__doc__ = Client.margin_v1_get_asset_custody_transfer_history.__doc__
            
    async def margin_v1_post_broker_sub_account_blvt(self, **params):
        return await self._request_margin_api("post", "broker/subAccount/blvt", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_blvt.__doc__ = Client.margin_v1_post_broker_sub_account_blvt.__doc__
            
    async def margin_v1_post_sol_staking_sol_redeem(self, **params):
        return await self._request_margin_api("post", "sol-staking/sol/redeem", signed=True, data=params, version=1)
        
    margin_v1_post_sol_staking_sol_redeem.__doc__ = Client.margin_v1_post_sol_staking_sol_redeem.__doc__
            
    async def options_v1_get_countdown_cancel_all(self, **params):
        return await self._request_options_api("get", "countdownCancelAll", signed=True, data=params)
        
    options_v1_get_countdown_cancel_all.__doc__ = Client.options_v1_get_countdown_cancel_all.__doc__
            
    async def margin_v1_get_margin_trade_coeff(self, **params):
        return await self._request_margin_api("get", "margin/tradeCoeff", signed=True, data=params, version=1)
        
    margin_v1_get_margin_trade_coeff.__doc__ = Client.margin_v1_get_margin_trade_coeff.__doc__
            
    async def futures_coin_v1_get_order_amendment(self, **params):
        return await self._request_futures_coin_api("get", "orderAmendment", signed=True, data=params, version=1)
        
    futures_coin_v1_get_order_amendment.__doc__ = Client.futures_coin_v1_get_order_amendment.__doc__
            
    async def margin_v1_get_margin_available_inventory(self, **params):
        return await self._request_margin_api("get", "margin/available-inventory", signed=True, data=params, version=1)
        
    margin_v1_get_margin_available_inventory.__doc__ = Client.margin_v1_get_margin_available_inventory.__doc__
            
    async def margin_v1_post_account_api_restrictions_ip_restriction_ip_list(self, **params):
        return await self._request_margin_api("post", "account/apiRestrictions/ipRestriction/ipList", signed=True, data=params, version=1)
        
    margin_v1_post_account_api_restrictions_ip_restriction_ip_list.__doc__ = Client.margin_v1_post_account_api_restrictions_ip_restriction_ip_list.__doc__
            
    async def margin_v2_get_eth_staking_account(self, **params):
        return await self._request_margin_api("get", "eth-staking/account", signed=True, data=params, version=2)
        
    margin_v2_get_eth_staking_account.__doc__ = Client.margin_v2_get_eth_staking_account.__doc__
            
    async def margin_v1_get_loan_income(self, **params):
        return await self._request_margin_api("get", "loan/income", signed=True, data=params, version=1)
        
    margin_v1_get_loan_income.__doc__ = Client.margin_v1_get_loan_income.__doc__
            
    async def futures_coin_v1_get_pm_account_info(self, **params):
        return await self._request_futures_coin_api("get", "pmAccountInfo", signed=True, data=params, version=1)
        
    futures_coin_v1_get_pm_account_info.__doc__ = Client.futures_coin_v1_get_pm_account_info.__doc__
            
    async def margin_v1_get_managed_subaccount_query_trans_log_for_investor(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/queryTransLogForInvestor", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_query_trans_log_for_investor.__doc__ = Client.margin_v1_get_managed_subaccount_query_trans_log_for_investor.__doc__
            
    async def margin_v1_post_dci_product_auto_compound_edit_status(self, **params):
        return await self._request_margin_api("post", "dci/product/auto_compound/edit-status", signed=True, data=params, version=1)
        
    margin_v1_post_dci_product_auto_compound_edit_status.__doc__ = Client.margin_v1_post_dci_product_auto_compound_edit_status.__doc__
            
    async def futures_v1_get_trade_asyn(self, **params):
        return await self._request_futures_api("get", "trade/asyn", signed=True, data=params, version=1)
        
    futures_v1_get_trade_asyn.__doc__ = Client.futures_v1_get_trade_asyn.__doc__
            
    async def margin_v1_get_loan_vip_request_interest_rate(self, **params):
        return await self._request_margin_api("get", "loan/vip/request/interestRate", signed=True, data=params, version=1)
        
    margin_v1_get_loan_vip_request_interest_rate.__doc__ = Client.margin_v1_get_loan_vip_request_interest_rate.__doc__
            
    async def futures_v1_get_funding_info(self, **params):
        return await self._request_futures_api("get", "fundingInfo", signed=False, data=params, version=1)
        
    futures_v1_get_funding_info.__doc__ = Client.futures_v1_get_funding_info.__doc__
            
    async def v3_get_all_orders(self, **params):
        return await self._request_api("get", "allOrders", signed=True, data=params, version="v3")
        
    async def margin_v2_get_loan_flexible_repay_rate(self, **params):
        return await self._request_margin_api("get", "loan/flexible/repay/rate", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_repay_rate.__doc__ = Client.margin_v2_get_loan_flexible_repay_rate.__doc__
            
    async def margin_v1_get_lending_auto_invest_plan_id(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/plan/id", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_plan_id.__doc__ = Client.margin_v1_get_lending_auto_invest_plan_id.__doc__
            
    async def margin_v1_post_loan_adjust_ltv(self, **params):
        return await self._request_margin_api("post", "loan/adjust/ltv", signed=True, data=params, version=1)
        
    margin_v1_post_loan_adjust_ltv.__doc__ = Client.margin_v1_post_loan_adjust_ltv.__doc__
            
    async def margin_v1_get_mining_statistics_user_status(self, **params):
        return await self._request_margin_api("get", "mining/statistics/user/status", signed=True, data=params, version=1)
        
    margin_v1_get_mining_statistics_user_status.__doc__ = Client.margin_v1_get_mining_statistics_user_status.__doc__
            
    async def margin_v1_get_broker_transfer_futures(self, **params):
        return await self._request_margin_api("get", "broker/transfer/futures", signed=True, data=params, version=1)
        
    margin_v1_get_broker_transfer_futures.__doc__ = Client.margin_v1_get_broker_transfer_futures.__doc__
            
    async def margin_v1_post_algo_spot_new_order_twap(self, **params):
        return await self._request_margin_api("post", "algo/spot/newOrderTwap", signed=True, data=params, version=1)
        
    margin_v1_post_algo_spot_new_order_twap.__doc__ = Client.margin_v1_post_algo_spot_new_order_twap.__doc__
            
    async def margin_v1_get_lending_auto_invest_target_asset_list(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/target-asset/list", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_target_asset_list.__doc__ = Client.margin_v1_get_lending_auto_invest_target_asset_list.__doc__
            
    async def margin_v1_get_capital_deposit_address_list(self, **params):
        return await self._request_margin_api("get", "capital/deposit/address/list", signed=True, data=params, version=1)
        
    margin_v1_get_capital_deposit_address_list.__doc__ = Client.margin_v1_get_capital_deposit_address_list.__doc__
            
    async def margin_v1_post_broker_sub_account_bnb_burn_margin_interest(self, **params):
        return await self._request_margin_api("post", "broker/subAccount/bnbBurn/marginInterest", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_bnb_burn_margin_interest.__doc__ = Client.margin_v1_post_broker_sub_account_bnb_burn_margin_interest.__doc__
            
    async def margin_v2_post_loan_flexible_repay(self, **params):
        return await self._request_margin_api("post", "loan/flexible/repay", signed=True, data=params, version=2)
        
    margin_v2_post_loan_flexible_repay.__doc__ = Client.margin_v2_post_loan_flexible_repay.__doc__
            
    async def margin_v2_get_loan_flexible_loanable_data(self, **params):
        return await self._request_margin_api("get", "loan/flexible/loanable/data", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_loanable_data.__doc__ = Client.margin_v2_get_loan_flexible_loanable_data.__doc__
            
    async def margin_v1_post_broker_sub_account_api_permission(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/permission", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_permission.__doc__ = Client.margin_v1_post_broker_sub_account_api_permission.__doc__
            
    async def margin_v1_post_broker_sub_account_api(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api.__doc__ = Client.margin_v1_post_broker_sub_account_api.__doc__
            
    async def margin_v1_get_dci_product_positions(self, **params):
        return await self._request_margin_api("get", "dci/product/positions", signed=True, data=params, version=1)
        
    margin_v1_get_dci_product_positions.__doc__ = Client.margin_v1_get_dci_product_positions.__doc__
            
    async def margin_v1_post_convert_limit_cancel_order(self, **params):
        return await self._request_margin_api("post", "convert/limit/cancelOrder", signed=True, data=params, version=1)
        
    margin_v1_post_convert_limit_cancel_order.__doc__ = Client.margin_v1_post_convert_limit_cancel_order.__doc__
            
    async def v3_post_order_list_oto(self, **params):
        return await self._request_api("post", "orderList/oto", signed=True, data=params, version="v3")
        
    v3_post_order_list_oto.__doc__ = Client.v3_post_order_list_oto.__doc__
            
    async def margin_v1_get_mining_hash_transfer_config_details_list(self, **params):
        return await self._request_margin_api("get", "mining/hash-transfer/config/details/list", signed=True, data=params, version=1)
        
    margin_v1_get_mining_hash_transfer_config_details_list.__doc__ = Client.margin_v1_get_mining_hash_transfer_config_details_list.__doc__
            
    async def margin_v1_get_mining_hash_transfer_profit_details(self, **params):
        return await self._request_margin_api("get", "mining/hash-transfer/profit/details", signed=True, data=params, version=1)
        
    margin_v1_get_mining_hash_transfer_profit_details.__doc__ = Client.margin_v1_get_mining_hash_transfer_profit_details.__doc__
            
    async def margin_v1_get_broker_sub_account(self, **params):
        return await self._request_margin_api("get", "broker/subAccount", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account.__doc__ = Client.margin_v1_get_broker_sub_account.__doc__
            
    async def margin_v1_get_portfolio_balance(self, **params):
        return await self._request_margin_api("get", "portfolio/balance", signed=True, data=params, version=1)
        
    margin_v1_get_portfolio_balance.__doc__ = Client.margin_v1_get_portfolio_balance.__doc__
            
    async def margin_v1_post_sub_account_eoptions_enable(self, **params):
        return await self._request_margin_api("post", "sub-account/eoptions/enable", signed=True, data=params, version=1)
        
    margin_v1_post_sub_account_eoptions_enable.__doc__ = Client.margin_v1_post_sub_account_eoptions_enable.__doc__
            
    async def papi_v1_post_ping(self, **params):
        return await self._request_papi_api("post", "ping", signed=True, data=params, version=1)
        
    papi_v1_post_ping.__doc__ = Client.papi_v1_post_ping.__doc__
            
    async def margin_v1_get_loan_loanable_data(self, **params):
        return await self._request_margin_api("get", "loan/loanable/data", signed=True, data=params, version=1)
        
    margin_v1_get_loan_loanable_data.__doc__ = Client.margin_v1_get_loan_loanable_data.__doc__
            
    async def margin_v1_post_eth_staking_wbeth_unwrap(self, **params):
        return await self._request_margin_api("post", "eth-staking/wbeth/unwrap", signed=True, data=params, version=1)
        
    margin_v1_post_eth_staking_wbeth_unwrap.__doc__ = Client.margin_v1_post_eth_staking_wbeth_unwrap.__doc__
            
    async def margin_v1_get_eth_staking_eth_history_staking_history(self, **params):
        return await self._request_margin_api("get", "eth-staking/eth/history/stakingHistory", signed=True, data=params, version=1)
        
    margin_v1_get_eth_staking_eth_history_staking_history.__doc__ = Client.margin_v1_get_eth_staking_eth_history_staking_history.__doc__
            
    async def margin_v1_get_staking_staking_record(self, **params):
        return await self._request_margin_api("get", "staking/stakingRecord", signed=True, data=params, version=1)
        
    margin_v1_get_staking_staking_record.__doc__ = Client.margin_v1_get_staking_staking_record.__doc__
            
    async def margin_v1_get_broker_rebate_recent_record(self, **params):
        return await self._request_margin_api("get", "broker/rebate/recentRecord", signed=True, data=params, version=1)
        
    margin_v1_get_broker_rebate_recent_record.__doc__ = Client.margin_v1_get_broker_rebate_recent_record.__doc__
            
    async def v3_delete_user_data_stream(self, **params):
        return await self._request_api("delete", "userDataStream", signed=True, data=params, version="v3")
        
    async def v3_get_open_order_list(self, **params):
        return await self._request_api("get", "openOrderList", signed=True, data=params, version="v3")
        
    async def margin_v1_get_loan_vip_collateral_account(self, **params):
        return await self._request_margin_api("get", "loan/vip/collateral/account", signed=True, data=params, version=1)
        
    margin_v1_get_loan_vip_collateral_account.__doc__ = Client.margin_v1_get_loan_vip_collateral_account.__doc__
            
    async def margin_v1_get_algo_spot_open_orders(self, **params):
        return await self._request_margin_api("get", "algo/spot/openOrders", signed=True, data=params, version=1)
        
    margin_v1_get_algo_spot_open_orders.__doc__ = Client.margin_v1_get_algo_spot_open_orders.__doc__
            
    async def margin_v1_post_loan_repay(self, **params):
        return await self._request_margin_api("post", "loan/repay", signed=True, data=params, version=1)
        
    margin_v1_post_loan_repay.__doc__ = Client.margin_v1_post_loan_repay.__doc__
            
    async def futures_coin_v1_get_funding_info(self, **params):
        return await self._request_futures_coin_api("get", "fundingInfo", signed=False, data=params, version=1)
        
    futures_coin_v1_get_funding_info.__doc__ = Client.futures_coin_v1_get_funding_info.__doc__
            
    async def margin_v1_get_margin_leverage_bracket(self, **params):
        return await self._request_margin_api("get", "margin/leverageBracket", signed=True, data=params, version=1)
        
    margin_v1_get_margin_leverage_bracket.__doc__ = Client.margin_v1_get_margin_leverage_bracket.__doc__
            
    async def margin_v2_get_portfolio_collateral_rate(self, **params):
        return await self._request_margin_api("get", "portfolio/collateralRate", signed=True, data=params, version=2)
        
    margin_v2_get_portfolio_collateral_rate.__doc__ = Client.margin_v2_get_portfolio_collateral_rate.__doc__
            
    async def margin_v2_post_loan_flexible_adjust_ltv(self, **params):
        return await self._request_margin_api("post", "loan/flexible/adjust/ltv", signed=True, data=params, version=2)
        
    margin_v2_post_loan_flexible_adjust_ltv.__doc__ = Client.margin_v2_post_loan_flexible_adjust_ltv.__doc__
            
    async def margin_v1_get_convert_order_status(self, **params):
        return await self._request_margin_api("get", "convert/orderStatus", signed=True, data=params, version=1)
        
    margin_v1_get_convert_order_status.__doc__ = Client.margin_v1_get_convert_order_status.__doc__
            
    async def margin_v1_get_broker_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api("get", "broker/subAccountApi/ipRestriction", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_api_ip_restriction.__doc__ = Client.margin_v1_get_broker_sub_account_api_ip_restriction.__doc__
            
    async def margin_v1_post_dci_product_subscribe(self, **params):
        return await self._request_margin_api("post", "dci/product/subscribe", signed=True, data=params, version=1)
        
    margin_v1_post_dci_product_subscribe.__doc__ = Client.margin_v1_post_dci_product_subscribe.__doc__
            
    async def futures_v1_get_income_asyn_id(self, **params):
        return await self._request_futures_api("get", "income/asyn/id", signed=True, data=params, version=1)
        
    futures_v1_get_income_asyn_id.__doc__ = Client.futures_v1_get_income_asyn_id.__doc__
            
    async def options_v1_post_countdown_cancel_all(self, **params):
        return await self._request_options_api("post", "countdownCancelAll", signed=True, data=params)
        
    options_v1_post_countdown_cancel_all.__doc__ = Client.options_v1_post_countdown_cancel_all.__doc__
            
    async def margin_v1_post_mining_hash_transfer_config_cancel(self, **params):
        return await self._request_margin_api("post", "mining/hash-transfer/config/cancel", signed=True, data=params, version=1)
        
    margin_v1_post_mining_hash_transfer_config_cancel.__doc__ = Client.margin_v1_post_mining_hash_transfer_config_cancel.__doc__
            
    async def margin_v1_get_broker_sub_account_deposit_hist(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/depositHist", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_deposit_hist.__doc__ = Client.margin_v1_get_broker_sub_account_deposit_hist.__doc__
            
    async def margin_v1_get_mining_payment_list(self, **params):
        return await self._request_margin_api("get", "mining/payment/list", signed=True, data=params, version=1)
        
    margin_v1_get_mining_payment_list.__doc__ = Client.margin_v1_get_mining_payment_list.__doc__
            
    async def futures_v1_get_pm_account_info(self, **params):
        return await self._request_futures_api("get", "pmAccountInfo", signed=True, data=params, version=1)
        
    futures_v1_get_pm_account_info.__doc__ = Client.futures_v1_get_pm_account_info.__doc__
            
    async def futures_coin_v1_get_adl_quantile(self, **params):
        return await self._request_futures_coin_api("get", "adlQuantile", signed=True, data=params, version=1)
        
    futures_coin_v1_get_adl_quantile.__doc__ = Client.futures_coin_v1_get_adl_quantile.__doc__
            
    async def options_v1_get_income_asyn_id(self, **params):
        return await self._request_options_api("get", "income/asyn/id", signed=True, data=params)
        
    options_v1_get_income_asyn_id.__doc__ = Client.options_v1_get_income_asyn_id.__doc__
            
    async def v3_post_cancel_replace(self, **params):
        return await self._request_api("post", "cancelReplace", signed=True, data=params, version="v3")
        
    v3_post_cancel_replace.__doc__ = Client.v3_post_cancel_replace.__doc__
            
    async def v3_post_order_test(self, **params):
        return await self._request_api("post", "order/test", signed=True, data=params, version="v3")
        
    async def margin_v1_post_account_enable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api("post", "account/enableFastWithdrawSwitch", signed=True, data=params, version=1)
        
    margin_v1_post_account_enable_fast_withdraw_switch.__doc__ = Client.margin_v1_post_account_enable_fast_withdraw_switch.__doc__
            
    async def margin_v1_post_broker_transfer_futures(self, **params):
        return await self._request_margin_api("post", "broker/transfer/futures", signed=True, data=params, version=1)
        
    margin_v1_post_broker_transfer_futures.__doc__ = Client.margin_v1_post_broker_transfer_futures.__doc__
            
    async def margin_v1_get_margin_isolated_transfer(self, **params):
        return await self._request_margin_api("get", "margin/isolated/transfer", signed=True, data=params, version=1)
        
    async def v3_post_order_cancel_replace(self, **params):
        return await self._request_api("post", "order/cancelReplace", signed=True, data=params, version="v3")
        
    async def margin_v1_post_sol_staking_sol_stake(self, **params):
        return await self._request_margin_api("post", "sol-staking/sol/stake", signed=True, data=params, version=1)
        
    margin_v1_post_sol_staking_sol_stake.__doc__ = Client.margin_v1_post_sol_staking_sol_stake.__doc__
            
    async def margin_v1_post_loan_borrow(self, **params):
        return await self._request_margin_api("post", "loan/borrow", signed=True, data=params, version=1)
        
    margin_v1_post_loan_borrow.__doc__ = Client.margin_v1_post_loan_borrow.__doc__
            
    async def margin_v1_get_managed_subaccount_info(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/info", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_info.__doc__ = Client.margin_v1_get_managed_subaccount_info.__doc__
            
    async def margin_v1_post_lending_auto_invest_plan_edit_status(self, **params):
        return await self._request_margin_api("post", "lending/auto-invest/plan/edit-status", signed=True, data=params, version=1)
        
    margin_v1_post_lending_auto_invest_plan_edit_status.__doc__ = Client.margin_v1_post_lending_auto_invest_plan_edit_status.__doc__
            
    async def margin_v1_get_sol_staking_sol_history_unclaimed_rewards(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/history/unclaimedRewards", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_history_unclaimed_rewards.__doc__ = Client.margin_v1_get_sol_staking_sol_history_unclaimed_rewards.__doc__
            
    async def margin_v1_post_asset_convert_transfer_query_by_page(self, **params):
        return await self._request_margin_api("post", "asset/convert-transfer/queryByPage", signed=True, data=params, version=1)
        
    margin_v1_post_asset_convert_transfer_query_by_page.__doc__ = Client.margin_v1_post_asset_convert_transfer_query_by_page.__doc__
            
    async def margin_v1_get_sol_staking_sol_history_boost_rewards_history(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/history/boostRewardsHistory", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_history_boost_rewards_history.__doc__ = Client.margin_v1_get_sol_staking_sol_history_boost_rewards_history.__doc__
            
    async def margin_v1_get_lending_auto_invest_one_off_status(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/one-off/status", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_one_off_status.__doc__ = Client.margin_v1_get_lending_auto_invest_one_off_status.__doc__
            
    async def margin_v1_post_broker_sub_account(self, **params):
        return await self._request_margin_api("post", "broker/subAccount", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account.__doc__ = Client.margin_v1_post_broker_sub_account.__doc__
            
    async def margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page(self, **params):
        return await self._request_margin_api("get", "asset/ledger-transfer/cloud-mining/queryByPage", signed=True, data=params, version=1)
        
    margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page.__doc__ = Client.margin_v1_get_asset_ledger_transfer_cloud_mining_query_by_page.__doc__
            
    async def margin_v1_get_mining_pub_coin_list(self, **params):
        return await self._request_margin_api("get", "mining/pub/coinList", signed=True, data=params, version=1)
        
    margin_v1_get_mining_pub_coin_list.__doc__ = Client.margin_v1_get_mining_pub_coin_list.__doc__
            
    async def margin_v2_get_loan_flexible_repay_history(self, **params):
        return await self._request_margin_api("get", "loan/flexible/repay/history", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_repay_history.__doc__ = Client.margin_v2_get_loan_flexible_repay_history.__doc__
            
    async def v3_post_sor_order(self, **params):
        return await self._request_api("post", "sor/order", signed=True, data=params, version="v3")
        
    v3_post_sor_order.__doc__ = Client.v3_post_sor_order.__doc__
            
    async def margin_v1_post_capital_deposit_credit_apply(self, **params):
        return await self._request_margin_api("post", "capital/deposit/credit-apply", signed=True, data=params, version=1)
        
    margin_v1_post_capital_deposit_credit_apply.__doc__ = Client.margin_v1_post_capital_deposit_credit_apply.__doc__
            
    async def futures_v1_put_batch_order(self, **params):
        return await self._request_futures_api("put", "batchOrder", signed=True, data=params, version=1)
        
    futures_v1_put_batch_order.__doc__ = Client.futures_v1_put_batch_order.__doc__
            
    async def v3_get_my_prevented_matches(self, **params):
        return await self._request_api("get", "myPreventedMatches", signed=True, data=params, version="v3")
        
    async def margin_v1_get_mining_statistics_user_list(self, **params):
        return await self._request_margin_api("get", "mining/statistics/user/list", signed=True, data=params, version=1)
        
    margin_v1_get_mining_statistics_user_list.__doc__ = Client.margin_v1_get_mining_statistics_user_list.__doc__
            
    async def futures_v1_post_batch_order(self, **params):
        return await self._request_futures_api("post", "batchOrder", signed=True, data=params, version=1)
        
    futures_v1_post_batch_order.__doc__ = Client.futures_v1_post_batch_order.__doc__
            
    async def v3_get_ticker_trading_day(self, **params):
        return await self._request_api("get", "ticker/tradingDay", signed=False, data=params, version="v3")
        
    v3_get_ticker_trading_day.__doc__ = Client.v3_get_ticker_trading_day.__doc__
            
    async def margin_v1_get_mining_worker_detail(self, **params):
        return await self._request_margin_api("get", "mining/worker/detail", signed=True, data=params, version=1)
        
    margin_v1_get_mining_worker_detail.__doc__ = Client.margin_v1_get_mining_worker_detail.__doc__
            
    async def margin_v1_get_managed_subaccount_fetch_future_asset(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/fetch-future-asset", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_fetch_future_asset.__doc__ = Client.margin_v1_get_managed_subaccount_fetch_future_asset.__doc__
            
    async def margin_v1_get_margin_rate_limit_order(self, **params):
        return await self._request_margin_api("get", "margin/rateLimit/order", signed=True, data=params, version=1)
        
    margin_v1_get_margin_rate_limit_order.__doc__ = Client.margin_v1_get_margin_rate_limit_order.__doc__
            
    async def margin_v1_get_localentity_vasp(self, **params):
        return await self._request_margin_api("get", "localentity/vasp", signed=True, data=params, version=1)
        
    margin_v1_get_localentity_vasp.__doc__ = Client.margin_v1_get_localentity_vasp.__doc__
            
    async def margin_v1_get_sol_staking_sol_history_rate_history(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/history/rateHistory", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_history_rate_history.__doc__ = Client.margin_v1_get_sol_staking_sol_history_rate_history.__doc__
            
    async def margin_v1_post_broker_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/ipRestriction", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_ip_restriction.__doc__ = Client.margin_v1_post_broker_sub_account_api_ip_restriction.__doc__
            
    async def margin_v1_get_broker_transfer(self, **params):
        return await self._request_margin_api("get", "broker/transfer", signed=True, data=params, version=1)
        
    margin_v1_get_broker_transfer.__doc__ = Client.margin_v1_get_broker_transfer.__doc__
            
    async def margin_v1_get_sol_staking_account(self, **params):
        return await self._request_margin_api("get", "sol-staking/account", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_account.__doc__ = Client.margin_v1_get_sol_staking_account.__doc__
            
    async def margin_v1_get_account_info(self, **params):
        return await self._request_margin_api("get", "account/info", signed=True, data=params, version=1)
        
    margin_v1_get_account_info.__doc__ = Client.margin_v1_get_account_info.__doc__
            
    async def margin_v1_post_portfolio_repay_futures_switch(self, **params):
        return await self._request_margin_api("post", "portfolio/repay-futures-switch", signed=True, data=params, version=1)
        
    margin_v1_post_portfolio_repay_futures_switch.__doc__ = Client.margin_v1_post_portfolio_repay_futures_switch.__doc__
            
    async def margin_v1_post_loan_vip_borrow(self, **params):
        return await self._request_margin_api("post", "loan/vip/borrow", signed=True, data=params, version=1)
        
    margin_v1_post_loan_vip_borrow.__doc__ = Client.margin_v1_post_loan_vip_borrow.__doc__
            
    async def margin_v2_get_loan_flexible_ltv_adjustment_history(self, **params):
        return await self._request_margin_api("get", "loan/flexible/ltv/adjustment/history", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_ltv_adjustment_history.__doc__ = Client.margin_v2_get_loan_flexible_ltv_adjustment_history.__doc__
            
    async def options_v1_delete_all_open_orders_by_underlying(self, **params):
        return await self._request_options_api("delete", "allOpenOrdersByUnderlying", signed=True, data=params)
        
    options_v1_delete_all_open_orders_by_underlying.__doc__ = Client.options_v1_delete_all_open_orders_by_underlying.__doc__
            
    async def margin_v1_get_broker_sub_account_futures_summary(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/futuresSummary", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_futures_summary.__doc__ = Client.margin_v1_get_broker_sub_account_futures_summary.__doc__
            
    async def margin_v1_get_broker_sub_account_spot_summary(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/spotSummary", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_spot_summary.__doc__ = Client.margin_v1_get_broker_sub_account_spot_summary.__doc__
            
    async def margin_v1_post_sub_account_blvt_enable(self, **params):
        return await self._request_margin_api("post", "sub-account/blvt/enable", signed=True, data=params, version=1)
        
    margin_v1_post_sub_account_blvt_enable.__doc__ = Client.margin_v1_post_sub_account_blvt_enable.__doc__
            
    async def margin_v1_get_algo_spot_historical_orders(self, **params):
        return await self._request_margin_api("get", "algo/spot/historicalOrders", signed=True, data=params, version=1)
        
    margin_v1_get_algo_spot_historical_orders.__doc__ = Client.margin_v1_get_algo_spot_historical_orders.__doc__
            
    async def margin_v1_get_loan_vip_repay_history(self, **params):
        return await self._request_margin_api("get", "loan/vip/repay/history", signed=True, data=params, version=1)
        
    margin_v1_get_loan_vip_repay_history.__doc__ = Client.margin_v1_get_loan_vip_repay_history.__doc__
            
    async def margin_v1_get_loan_borrow_history(self, **params):
        return await self._request_margin_api("get", "loan/borrow/history", signed=True, data=params, version=1)
        
    margin_v1_get_loan_borrow_history.__doc__ = Client.margin_v1_get_loan_borrow_history.__doc__
            
    async def margin_v1_post_lending_auto_invest_redeem(self, **params):
        return await self._request_margin_api("post", "lending/auto-invest/redeem", signed=True, data=params, version=1)
        
    margin_v1_post_lending_auto_invest_redeem.__doc__ = Client.margin_v1_post_lending_auto_invest_redeem.__doc__
            
    async def v3_get_account(self, **params):
        return await self._request_api("get", "account", signed=True, data=params, version="v3")
        
    async def v3_delete_order(self, **params):
        return await self._request_api("delete", "order", signed=True, data=params, version="v3")
        
    async def futures_coin_v1_get_income_asyn(self, **params):
        return await self._request_futures_coin_api("get", "income/asyn", signed=True, data=params, version=1)
        
    futures_coin_v1_get_income_asyn.__doc__ = Client.futures_coin_v1_get_income_asyn.__doc__
            
    async def margin_v1_post_managed_subaccount_deposit(self, **params):
        return await self._request_margin_api("post", "managed-subaccount/deposit", signed=True, data=params, version=1)
        
    margin_v1_post_managed_subaccount_deposit.__doc__ = Client.margin_v1_post_managed_subaccount_deposit.__doc__
            
    async def margin_v1_post_lending_daily_purchase(self, **params):
        return await self._request_margin_api("post", "lending/daily/purchase", signed=True, data=params, version=1)
        
    margin_v1_post_lending_daily_purchase.__doc__ = Client.margin_v1_post_lending_daily_purchase.__doc__
            
    async def futures_v1_get_trade_asyn_id(self, **params):
        return await self._request_futures_api("get", "trade/asyn/id", signed=True, data=params, version=1)
        
    futures_v1_get_trade_asyn_id.__doc__ = Client.futures_v1_get_trade_asyn_id.__doc__
            
    async def margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list(self, **params):
        return await self._request_margin_api("delete", "sub-account/subAccountApi/ipRestriction/ipList", signed=True, data=params, version=1)
        
    margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list.__doc__ = Client.margin_v1_delete_sub_account_sub_account_api_ip_restriction_ip_list.__doc__
            
    async def margin_v1_get_copy_trading_futures_user_status(self, **params):
        return await self._request_margin_api("get", "copyTrading/futures/userStatus", signed=True, data=params, version=1)
        
    margin_v1_get_copy_trading_futures_user_status.__doc__ = Client.margin_v1_get_copy_trading_futures_user_status.__doc__
            
    async def options_v1_get_margin_account(self, **params):
        return await self._request_options_api("get", "marginAccount", signed=True, data=params)
        
    options_v1_get_margin_account.__doc__ = Client.options_v1_get_margin_account.__doc__
            
    async def margin_v1_post_localentity_withdraw_apply(self, **params):
        return await self._request_margin_api("post", "localentity/withdraw/apply", signed=True, data=params, version=1)
        
    margin_v1_post_localentity_withdraw_apply.__doc__ = Client.margin_v1_post_localentity_withdraw_apply.__doc__
            
    async def v3_put_user_data_stream(self, **params):
        return await self._request_api("put", "userDataStream", signed=True, data=params, version="v3")
        
    async def margin_v1_get_asset_wallet_balance(self, **params):
        return await self._request_margin_api("get", "asset/wallet/balance", signed=True, data=params, version=1)
        
    margin_v1_get_asset_wallet_balance.__doc__ = Client.margin_v1_get_asset_wallet_balance.__doc__
            
    async def margin_v1_post_broker_transfer(self, **params):
        return await self._request_margin_api("post", "broker/transfer", signed=True, data=params, version=1)
        
    margin_v1_post_broker_transfer.__doc__ = Client.margin_v1_post_broker_transfer.__doc__
            
    async def margin_v1_post_lending_customized_fixed_purchase(self, **params):
        return await self._request_margin_api("post", "lending/customizedFixed/purchase", signed=True, data=params, version=1)
        
    margin_v1_post_lending_customized_fixed_purchase.__doc__ = Client.margin_v1_post_lending_customized_fixed_purchase.__doc__
            
    async def margin_v1_post_algo_futures_new_order_twap(self, **params):
        return await self._request_margin_api("post", "algo/futures/newOrderTwap", signed=True, data=params, version=1)
        
    margin_v1_post_algo_futures_new_order_twap.__doc__ = Client.margin_v1_post_algo_futures_new_order_twap.__doc__
            
    async def margin_v2_post_eth_staking_eth_stake(self, **params):
        return await self._request_margin_api("post", "eth-staking/eth/stake", signed=True, data=params, version=2)
        
    margin_v2_post_eth_staking_eth_stake.__doc__ = Client.margin_v2_post_eth_staking_eth_stake.__doc__
            
    async def margin_v1_post_loan_flexible_repay_history(self, **params):
        return await self._request_margin_api("post", "loan/flexible/repay/history", signed=True, data=params, version=1)
        
    margin_v1_post_loan_flexible_repay_history.__doc__ = Client.margin_v1_post_loan_flexible_repay_history.__doc__
            
    async def v3_post_user_data_stream(self, **params):
        return await self._request_api("post", "userDataStream", signed=True, data=params, version="v3")
        
    async def margin_v1_get_lending_auto_invest_index_info(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/index/info", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_index_info.__doc__ = Client.margin_v1_get_lending_auto_invest_index_info.__doc__
            
    async def margin_v1_get_sol_staking_sol_history_redemption_history(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/history/redemptionHistory", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_history_redemption_history.__doc__ = Client.margin_v1_get_sol_staking_sol_history_redemption_history.__doc__
            
    async def margin_v1_get_broker_rebate_futures_recent_record(self, **params):
        return await self._request_margin_api("get", "broker/rebate/futures/recentRecord", signed=True, data=params, version=1)
        
    margin_v1_get_broker_rebate_futures_recent_record.__doc__ = Client.margin_v1_get_broker_rebate_futures_recent_record.__doc__
            
    async def margin_v3_get_broker_sub_account_futures_summary(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/futuresSummary", signed=True, data=params, version=3)
        
    margin_v3_get_broker_sub_account_futures_summary.__doc__ = Client.margin_v3_get_broker_sub_account_futures_summary.__doc__
            
    async def margin_v1_post_margin_manual_liquidation(self, **params):
        return await self._request_margin_api("post", "margin/manual-liquidation", signed=True, data=params, version=1)
        
    async def margin_v1_get_lending_auto_invest_target_asset_roi_list(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/target-asset/roi/list", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_target_asset_roi_list.__doc__ = Client.margin_v1_get_lending_auto_invest_target_asset_roi_list.__doc__
            
    async def margin_v1_get_broker_universal_transfer(self, **params):
        return await self._request_margin_api("get", "broker/universalTransfer", signed=True, data=params, version=1)
        
    margin_v1_get_broker_universal_transfer.__doc__ = Client.margin_v1_get_broker_universal_transfer.__doc__
            
    async def futures_v1_put_batch_orders(self, **params):
        return await self._request_futures_api("put", "batchOrders", signed=True, data=params, version=1)
        
    futures_v1_put_batch_orders.__doc__ = Client.futures_v1_put_batch_orders.__doc__
            
    async def options_v1_post_countdown_cancel_all_heart_beat(self, **params):
        return await self._request_options_api("post", "countdownCancelAllHeartBeat", signed=True, data=params)
        
    options_v1_post_countdown_cancel_all_heart_beat.__doc__ = Client.options_v1_post_countdown_cancel_all_heart_beat.__doc__
            
    async def margin_v1_get_loan_collateral_data(self, **params):
        return await self._request_margin_api("get", "loan/collateral/data", signed=True, data=params, version=1)
        
    margin_v1_get_loan_collateral_data.__doc__ = Client.margin_v1_get_loan_collateral_data.__doc__
            
    async def margin_v1_get_loan_repay_history(self, **params):
        return await self._request_margin_api("get", "loan/repay/history", signed=True, data=params, version=1)
        
    margin_v1_get_loan_repay_history.__doc__ = Client.margin_v1_get_loan_repay_history.__doc__
            
    async def margin_v1_post_convert_limit_place_order(self, **params):
        return await self._request_margin_api("post", "convert/limit/placeOrder", signed=True, data=params, version=1)
        
    margin_v1_post_convert_limit_place_order.__doc__ = Client.margin_v1_post_convert_limit_place_order.__doc__
            
    async def futures_v1_get_convert_exchange_info(self, **params):
        return await self._request_futures_api("get", "convert/exchangeInfo", signed=False, data=params, version=1)
        
    futures_v1_get_convert_exchange_info.__doc__ = Client.futures_v1_get_convert_exchange_info.__doc__
            
    async def v3_get_all_order_list(self, **params):
        return await self._request_api("get", "allOrderList", signed=True, data=params, version="v3")
        
    v3_get_all_order_list.__doc__ = Client.v3_get_all_order_list.__doc__
            
    async def margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list(self, **params):
        return await self._request_margin_api("delete", "broker/subAccountApi/ipRestriction/ipList", signed=True, data=params, version=1)
        
    margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list.__doc__ = Client.margin_v1_delete_broker_sub_account_api_ip_restriction_ip_list.__doc__
            
    async def margin_v1_post_sub_account_virtual_sub_account(self, **params):
        return await self._request_margin_api("post", "sub-account/virtualSubAccount", signed=True, data=params, version=1)
        
    margin_v1_post_sub_account_virtual_sub_account.__doc__ = Client.margin_v1_post_sub_account_virtual_sub_account.__doc__
            
    async def margin_v1_put_localentity_deposit_provide_info(self, **params):
        return await self._request_margin_api("put", "localentity/deposit/provide-info", signed=True, data=params, version=1)
        
    margin_v1_put_localentity_deposit_provide_info.__doc__ = Client.margin_v1_put_localentity_deposit_provide_info.__doc__
            
    async def margin_v1_post_portfolio_mint(self, **params):
        return await self._request_margin_api("post", "portfolio/mint", signed=True, data=params, version=1)
        
    margin_v1_post_portfolio_mint.__doc__ = Client.margin_v1_post_portfolio_mint.__doc__
            
    async def futures_v1_get_order_amendment(self, **params):
        return await self._request_futures_api("get", "orderAmendment", signed=True, data=params, version=1)
        
    futures_v1_get_order_amendment.__doc__ = Client.futures_v1_get_order_amendment.__doc__
            
    async def margin_v1_post_sol_staking_sol_claim(self, **params):
        return await self._request_margin_api("post", "sol-staking/sol/claim", signed=True, data=params, version=1)
        
    margin_v1_post_sol_staking_sol_claim.__doc__ = Client.margin_v1_post_sol_staking_sol_claim.__doc__
            
    async def margin_v1_post_lending_daily_redeem(self, **params):
        return await self._request_margin_api("post", "lending/daily/redeem", signed=True, data=params, version=1)
        
    margin_v1_post_lending_daily_redeem.__doc__ = Client.margin_v1_post_lending_daily_redeem.__doc__
            
    async def margin_v1_post_mining_hash_transfer_config(self, **params):
        return await self._request_margin_api("post", "mining/hash-transfer/config", signed=True, data=params, version=1)
        
    margin_v1_post_mining_hash_transfer_config.__doc__ = Client.margin_v1_post_mining_hash_transfer_config.__doc__
            
    async def margin_v1_get_lending_auto_invest_rebalance_history(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/rebalance/history", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_rebalance_history.__doc__ = Client.margin_v1_get_lending_auto_invest_rebalance_history.__doc__
            
    async def margin_v1_get_loan_repay_collateral_rate(self, **params):
        return await self._request_margin_api("get", "loan/repay/collateral/rate", signed=True, data=params, version=1)
        
    margin_v1_get_loan_repay_collateral_rate.__doc__ = Client.margin_v1_get_loan_repay_collateral_rate.__doc__
            
    async def futures_v1_get_income_asyn(self, **params):
        return await self._request_futures_api("get", "income/asyn", signed=True, data=params, version=1)
        
    futures_v1_get_income_asyn.__doc__ = Client.futures_v1_get_income_asyn.__doc__
            
    async def margin_v1_get_mining_payment_uid(self, **params):
        return await self._request_margin_api("get", "mining/payment/uid", signed=True, data=params, version=1)
        
    margin_v1_get_mining_payment_uid.__doc__ = Client.margin_v1_get_mining_payment_uid.__doc__
            
    async def margin_v2_get_loan_flexible_borrow_history(self, **params):
        return await self._request_margin_api("get", "loan/flexible/borrow/history", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_borrow_history.__doc__ = Client.margin_v2_get_loan_flexible_borrow_history.__doc__
            
    async def v3_get_order(self, **params):
        return await self._request_api("get", "order", signed=True, data=params, version="v3")
        
    async def margin_v1_get_capital_contract_convertible_coins(self, **params):
        return await self._request_margin_api("get", "capital/contract/convertible-coins", signed=True, data=params, version=1)
        
    margin_v1_get_capital_contract_convertible_coins.__doc__ = Client.margin_v1_get_capital_contract_convertible_coins.__doc__
            
    async def margin_v1_post_broker_sub_account_api_permission_vanilla_options(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/permission/vanillaOptions", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_permission_vanilla_options.__doc__ = Client.margin_v1_post_broker_sub_account_api_permission_vanilla_options.__doc__
            
    async def margin_v1_get_lending_auto_invest_redeem_history(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/redeem/history", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_redeem_history.__doc__ = Client.margin_v1_get_lending_auto_invest_redeem_history.__doc__
            
    async def margin_v2_get_localentity_withdraw_history(self, **params):
        return await self._request_margin_api("get", "localentity/withdraw/history", signed=True, data=params, version=2)
        
    margin_v2_get_localentity_withdraw_history.__doc__ = Client.margin_v2_get_localentity_withdraw_history.__doc__
            
    async def margin_v1_get_eth_staking_eth_history_redemption_history(self, **params):
        return await self._request_margin_api("get", "eth-staking/eth/history/redemptionHistory", signed=True, data=params, version=1)
        
    margin_v1_get_eth_staking_eth_history_redemption_history.__doc__ = Client.margin_v1_get_eth_staking_eth_history_redemption_history.__doc__
            
    async def futures_v1_get_fee_burn(self, **params):
        return await self._request_futures_api("get", "feeBurn", signed=True, data=params, version=1)
        
    futures_v1_get_fee_burn.__doc__ = Client.futures_v1_get_fee_burn.__doc__
            
    async def margin_v1_get_lending_auto_invest_index_user_summary(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/index/user-summary", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_index_user_summary.__doc__ = Client.margin_v1_get_lending_auto_invest_index_user_summary.__doc__
            
    async def margin_v2_post_loan_flexible_borrow(self, **params):
        return await self._request_margin_api("post", "loan/flexible/borrow", signed=True, data=params, version=2)
        
    margin_v2_post_loan_flexible_borrow.__doc__ = Client.margin_v2_post_loan_flexible_borrow.__doc__
            
    async def margin_v1_post_loan_vip_repay(self, **params):
        return await self._request_margin_api("post", "loan/vip/repay", signed=True, data=params, version=1)
        
    margin_v1_post_loan_vip_repay.__doc__ = Client.margin_v1_post_loan_vip_repay.__doc__
            
    async def futures_coin_v1_get_commission_rate(self, **params):
        return await self._request_futures_coin_api("get", "commissionRate", signed=True, data=params, version=1)
        
    futures_coin_v1_get_commission_rate.__doc__ = Client.futures_coin_v1_get_commission_rate.__doc__
            
    async def margin_v1_get_convert_asset_info(self, **params):
        return await self._request_margin_api("get", "convert/assetInfo", signed=True, data=params, version=1)
        
    margin_v1_get_convert_asset_info.__doc__ = Client.margin_v1_get_convert_asset_info.__doc__
            
    async def v3_post_sor_order_test(self, **params):
        return await self._request_api("post", "sor/order/test", signed=True, data=params, version="v3")
        
    v3_post_sor_order_test.__doc__ = Client.v3_post_sor_order_test.__doc__
            
    async def margin_v1_post_broker_universal_transfer(self, **params):
        return await self._request_margin_api("post", "broker/universalTransfer", signed=True, data=params, version=1)
        
    margin_v1_post_broker_universal_transfer.__doc__ = Client.margin_v1_post_broker_universal_transfer.__doc__
            
    async def margin_v1_post_account_disable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api("post", "account/disableFastWithdrawSwitch", signed=True, data=params, version=1)
        
    margin_v1_post_account_disable_fast_withdraw_switch.__doc__ = Client.margin_v1_post_account_disable_fast_withdraw_switch.__doc__
            
    async def futures_v1_get_asset_index(self, **params):
        return await self._request_futures_api("get", "assetIndex", signed=False, data=params, version=1)
        
    futures_v1_get_asset_index.__doc__ = Client.futures_v1_get_asset_index.__doc__
            
    async def v3_get_rate_limit_order(self, **params):
        return await self._request_api("get", "rateLimit/order", signed=True, data=params, version="v3")
        
    async def margin_v1_get_account_api_restrictions_ip_restriction(self, **params):
        return await self._request_margin_api("get", "account/apiRestrictions/ipRestriction", signed=True, data=params, version=1)
        
    margin_v1_get_account_api_restrictions_ip_restriction.__doc__ = Client.margin_v1_get_account_api_restrictions_ip_restriction.__doc__
            
    async def margin_v1_post_broker_sub_account_bnb_burn_spot(self, **params):
        return await self._request_margin_api("post", "broker/subAccount/bnbBurn/spot", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_bnb_burn_spot.__doc__ = Client.margin_v1_post_broker_sub_account_bnb_burn_spot.__doc__
            
    async def futures_coin_v1_put_batch_orders(self, **params):
        return await self._request_futures_coin_api("put", "batchOrders", signed=True, data=params, version=1)
        
    futures_coin_v1_put_batch_orders.__doc__ = Client.futures_coin_v1_put_batch_orders.__doc__
            
    async def v3_delete_open_orders(self, **params):
        return await self._request_api("delete", "openOrders", signed=True, data=params, version="v3")
        
    async def margin_v1_post_broker_sub_account_api_permission_universal_transfer(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/permission/universalTransfer", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_permission_universal_transfer.__doc__ = Client.margin_v1_post_broker_sub_account_api_permission_universal_transfer.__doc__
            
    async def v3_get_my_allocations(self, **params):
        return await self._request_api("get", "myAllocations", signed=True, data=params, version="v3")
        
    async def margin_v1_get_loan_ltv_adjustment_history(self, **params):
        return await self._request_margin_api("get", "loan/ltv/adjustment/history", signed=True, data=params, version=1)
        
    margin_v1_get_loan_ltv_adjustment_history.__doc__ = Client.margin_v1_get_loan_ltv_adjustment_history.__doc__
            
    async def margin_v1_get_localentity_withdraw_history(self, **params):
        return await self._request_margin_api("get", "localentity/withdraw/history", signed=True, data=params, version=1)
        
    margin_v1_get_localentity_withdraw_history.__doc__ = Client.margin_v1_get_localentity_withdraw_history.__doc__
            
    async def margin_v2_post_sub_account_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api("post", "sub-account/subAccountApi/ipRestriction", signed=True, data=params, version=2)
        
    margin_v2_post_sub_account_sub_account_api_ip_restriction.__doc__ = Client.margin_v2_post_sub_account_sub_account_api_ip_restriction.__doc__
            
    async def futures_v1_get_rate_limit_order(self, **params):
        return await self._request_futures_api("get", "rateLimit/order", signed=True, data=params, version=1)
        
    futures_v1_get_rate_limit_order.__doc__ = Client.futures_v1_get_rate_limit_order.__doc__
            
    async def margin_v1_get_broker_sub_account_api_commission_futures(self, **params):
        return await self._request_margin_api("get", "broker/subAccountApi/commission/futures", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_api_commission_futures.__doc__ = Client.margin_v1_get_broker_sub_account_api_commission_futures.__doc__
            
    async def margin_v1_get_sol_staking_sol_history_staking_history(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/history/stakingHistory", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_history_staking_history.__doc__ = Client.margin_v1_get_sol_staking_sol_history_staking_history.__doc__
            
    async def futures_v1_get_open_order(self, **params):
        return await self._request_futures_api("get", "openOrder", signed=True, data=params, version=1)
        
    futures_v1_get_open_order.__doc__ = Client.futures_v1_get_open_order.__doc__
            
    async def margin_v1_delete_algo_spot_order(self, **params):
        return await self._request_margin_api("delete", "algo/spot/order", signed=True, data=params, version=1)
        
    margin_v1_delete_algo_spot_order.__doc__ = Client.margin_v1_delete_algo_spot_order.__doc__
            
    async def v3_post_order(self, **params):
        return await self._request_api("post", "order", signed=True, data=params, version="v3")
        
    async def margin_v1_delete_account_api_restrictions_ip_restriction_ip_list(self, **params):
        return await self._request_margin_api("delete", "account/apiRestrictions/ipRestriction/ipList", signed=True, data=params, version=1)
        
    margin_v1_delete_account_api_restrictions_ip_restriction_ip_list.__doc__ = Client.margin_v1_delete_account_api_restrictions_ip_restriction_ip_list.__doc__
            
    async def margin_v1_post_capital_contract_convertible_coins(self, **params):
        return await self._request_margin_api("post", "capital/contract/convertible-coins", signed=True, data=params, version=1)
        
    margin_v1_post_capital_contract_convertible_coins.__doc__ = Client.margin_v1_post_capital_contract_convertible_coins.__doc__
            
    async def margin_v1_get_managed_subaccount_margin_asset(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/marginAsset", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_margin_asset.__doc__ = Client.margin_v1_get_managed_subaccount_margin_asset.__doc__
            
    async def v3_delete_order_list(self, **params):
        return await self._request_api("delete", "orderList", signed=True, data=params, version="v3")
        
    v3_delete_order_list.__doc__ = Client.v3_delete_order_list.__doc__
            
    async def margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list(self, **params):
        return await self._request_margin_api("post", "sub-account/subAccountApi/ipRestriction/ipList", signed=True, data=params, version=1)
        
    margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list.__doc__ = Client.margin_v1_post_sub_account_sub_account_api_ip_restriction_ip_list.__doc__
            
    async def margin_v1_post_broker_sub_account_api_commission(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/commission", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_commission.__doc__ = Client.margin_v1_post_broker_sub_account_api_commission.__doc__
            
    async def futures_v1_post_fee_burn(self, **params):
        return await self._request_futures_api("post", "feeBurn", signed=True, data=params, version=1)
        
    futures_v1_post_fee_burn.__doc__ = Client.futures_v1_post_fee_burn.__doc__
            
    async def margin_v1_get_broker_sub_account_margin_summary(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/marginSummary", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_margin_summary.__doc__ = Client.margin_v1_get_broker_sub_account_margin_summary.__doc__
            
    async def margin_v1_get_lending_auto_invest_plan_list(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/plan/list", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_plan_list.__doc__ = Client.margin_v1_get_lending_auto_invest_plan_list.__doc__
            
    async def margin_v1_get_loan_vip_loanable_data(self, **params):
        return await self._request_margin_api("get", "loan/vip/loanable/data", signed=True, data=params, version=1)
        
    margin_v1_get_loan_vip_loanable_data.__doc__ = Client.margin_v1_get_loan_vip_loanable_data.__doc__
            
    async def margin_v2_get_loan_flexible_collateral_data(self, **params):
        return await self._request_margin_api("get", "loan/flexible/collateral/data", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_collateral_data.__doc__ = Client.margin_v2_get_loan_flexible_collateral_data.__doc__
            
    async def margin_v1_delete_broker_sub_account_api(self, **params):
        return await self._request_margin_api("delete", "broker/subAccountApi", signed=True, data=params, version=1)
        
    margin_v1_delete_broker_sub_account_api.__doc__ = Client.margin_v1_delete_broker_sub_account_api.__doc__
            
    async def margin_v1_get_sol_staking_sol_history_bnsol_rewards_history(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/history/bnsolRewardsHistory", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_history_bnsol_rewards_history.__doc__ = Client.margin_v1_get_sol_staking_sol_history_bnsol_rewards_history.__doc__
            
    async def margin_v1_get_convert_limit_query_open_orders(self, **params):
        return await self._request_margin_api("get", "convert/limit/queryOpenOrders", signed=True, data=params, version=1)
        
    margin_v1_get_convert_limit_query_open_orders.__doc__ = Client.margin_v1_get_convert_limit_query_open_orders.__doc__
            
    async def v3_get_account_commission(self, **params):
        return await self._request_api("get", "account/commission", signed=True, data=params, version="v3")
        
    v3_get_account_commission.__doc__ = Client.v3_get_account_commission.__doc__
            
    async def v3_post_order_list_oco(self, **params):
        return await self._request_api("post", "orderList/oco", signed=True, data=params, version="v3")
        
    async def margin_v1_get_managed_subaccount_query_trans_log(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/query-trans-log", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_query_trans_log.__doc__ = Client.margin_v1_get_managed_subaccount_query_trans_log.__doc__
            
    async def margin_v2_post_broker_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/ipRestriction", signed=True, data=params, version=2)
        
    margin_v2_post_broker_sub_account_api_ip_restriction.__doc__ = Client.margin_v2_post_broker_sub_account_api_ip_restriction.__doc__
            
    async def margin_v1_get_lending_auto_invest_all_asset(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/all/asset", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_all_asset.__doc__ = Client.margin_v1_get_lending_auto_invest_all_asset.__doc__
            
    async def futures_v1_post_convert_accept_quote(self, **params):
        return await self._request_futures_api("post", "convert/acceptQuote", signed=True, data=params, version=1)
        
    futures_v1_post_convert_accept_quote.__doc__ = Client.futures_v1_post_convert_accept_quote.__doc__
            
    async def margin_v1_get_spot_delist_schedule(self, **params):
        return await self._request_margin_api("get", "spot/delist-schedule", signed=True, data=params, version=1)
        
    margin_v1_get_spot_delist_schedule.__doc__ = Client.margin_v1_get_spot_delist_schedule.__doc__
            
    async def margin_v1_post_account_api_restrictions_ip_restriction(self, **params):
        return await self._request_margin_api("post", "account/apiRestrictions/ipRestriction", signed=True, data=params, version=1)
        
    margin_v1_post_account_api_restrictions_ip_restriction.__doc__ = Client.margin_v1_post_account_api_restrictions_ip_restriction.__doc__
            
    async def margin_v1_get_dci_product_accounts(self, **params):
        return await self._request_margin_api("get", "dci/product/accounts", signed=True, data=params, version=1)
        
    margin_v1_get_dci_product_accounts.__doc__ = Client.margin_v1_get_dci_product_accounts.__doc__
            
    async def margin_v1_get_sub_account_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api("get", "sub-account/subAccountApi/ipRestriction", signed=True, data=params, version=1)
        
    margin_v1_get_sub_account_sub_account_api_ip_restriction.__doc__ = Client.margin_v1_get_sub_account_sub_account_api_ip_restriction.__doc__
            
    async def margin_v1_get_sub_account_transaction_statistics(self, **params):
        return await self._request_margin_api("get", "sub-account/transaction-statistics", signed=True, data=params, version=1)
        
    margin_v1_get_sub_account_transaction_statistics.__doc__ = Client.margin_v1_get_sub_account_transaction_statistics.__doc__
            
    async def margin_v1_get_managed_subaccount_deposit_address(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/deposit/address", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_deposit_address.__doc__ = Client.margin_v1_get_managed_subaccount_deposit_address.__doc__
            
    async def margin_v2_get_portfolio_account(self, **params):
        return await self._request_margin_api("get", "portfolio/account", signed=True, data=params, version=2)
        
    margin_v2_get_portfolio_account.__doc__ = Client.margin_v2_get_portfolio_account.__doc__
            
    async def margin_v1_get_simple_earn_locked_history_redemption_record(self, **params):
        return await self._request_margin_api("get", "simple-earn/locked/history/redemptionRecord", signed=True, data=params, version=1)
        
    margin_v1_get_simple_earn_locked_history_redemption_record.__doc__ = Client.margin_v1_get_simple_earn_locked_history_redemption_record.__doc__
            
    async def futures_v1_get_order_asyn_id(self, **params):
        return await self._request_futures_api("get", "order/asyn/id", signed=True, data=params, version=1)
        
    futures_v1_get_order_asyn_id.__doc__ = Client.futures_v1_get_order_asyn_id.__doc__
            
    async def margin_v1_post_managed_subaccount_withdraw(self, **params):
        return await self._request_margin_api("post", "managed-subaccount/withdraw", signed=True, data=params, version=1)
        
    margin_v1_post_managed_subaccount_withdraw.__doc__ = Client.margin_v1_post_managed_subaccount_withdraw.__doc__
            
    async def margin_v1_get_localentity_deposit_history(self, **params):
        return await self._request_margin_api("get", "localentity/deposit/history", signed=True, data=params, version=1)
        
    margin_v1_get_localentity_deposit_history.__doc__ = Client.margin_v1_get_localentity_deposit_history.__doc__
            
    async def margin_v1_post_eth_staking_wbeth_wrap(self, **params):
        return await self._request_margin_api("post", "eth-staking/wbeth/wrap", signed=True, data=params, version=1)
        
    margin_v1_post_eth_staking_wbeth_wrap.__doc__ = Client.margin_v1_post_eth_staking_wbeth_wrap.__doc__
            
    async def margin_v1_post_simple_earn_locked_set_redeem_option(self, **params):
        return await self._request_margin_api("post", "simple-earn/locked/setRedeemOption", signed=True, data=params, version=1)
        
    margin_v1_post_simple_earn_locked_set_redeem_option.__doc__ = Client.margin_v1_post_simple_earn_locked_set_redeem_option.__doc__
            
    async def margin_v1_post_broker_sub_account_api_ip_restriction_ip_list(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/ipRestriction/ipList", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_ip_restriction_ip_list.__doc__ = Client.margin_v1_post_broker_sub_account_api_ip_restriction_ip_list.__doc__
            
    async def margin_v1_post_broker_sub_account_api_commission_futures(self, **params):
        return await self._request_margin_api("post", "broker/subAccountApi/commission/futures", signed=True, data=params, version=1)
        
    margin_v1_post_broker_sub_account_api_commission_futures.__doc__ = Client.margin_v1_post_broker_sub_account_api_commission_futures.__doc__
            
    async def v3_get_open_orders(self, **params):
        return await self._request_api("get", "openOrders", signed=True, data=params, version="v3")
        
    async def margin_v1_get_lending_auto_invest_history_list(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/history/list", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_history_list.__doc__ = Client.margin_v1_get_lending_auto_invest_history_list.__doc__
            
    async def margin_v1_post_loan_customize_margin_call(self, **params):
        return await self._request_margin_api("post", "loan/customize/margin_call", signed=True, data=params, version=1)
        
    margin_v1_post_loan_customize_margin_call.__doc__ = Client.margin_v1_post_loan_customize_margin_call.__doc__
            
    async def margin_v1_get_broker_sub_account_bnb_burn_status(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/bnbBurn/status", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_bnb_burn_status.__doc__ = Client.margin_v1_get_broker_sub_account_bnb_burn_status.__doc__
            
    async def margin_v1_get_managed_subaccount_account_snapshot(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/accountSnapshot", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_account_snapshot.__doc__ = Client.margin_v1_get_managed_subaccount_account_snapshot.__doc__
            
    async def margin_v1_post_asset_convert_transfer(self, **params):
        return await self._request_margin_api("post", "asset/convert-transfer", signed=True, data=params, version=1)
        
    margin_v1_post_asset_convert_transfer.__doc__ = Client.margin_v1_post_asset_convert_transfer.__doc__
            
    async def options_v1_get_income_asyn(self, **params):
        return await self._request_options_api("get", "income/asyn", signed=True, data=params)
        
    options_v1_get_income_asyn.__doc__ = Client.options_v1_get_income_asyn.__doc__
            
    async def margin_v1_get_broker_sub_account_api_commission_coin_futures(self, **params):
        return await self._request_margin_api("get", "broker/subAccountApi/commission/coinFutures", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_api_commission_coin_futures.__doc__ = Client.margin_v1_get_broker_sub_account_api_commission_coin_futures.__doc__
            
    async def margin_v2_get_broker_sub_account_futures_summary(self, **params):
        return await self._request_margin_api("get", "broker/subAccount/futuresSummary", signed=True, data=params, version=2)
        
    margin_v2_get_broker_sub_account_futures_summary.__doc__ = Client.margin_v2_get_broker_sub_account_futures_summary.__doc__
            
    async def margin_v1_get_loan_ongoing_orders(self, **params):
        return await self._request_margin_api("get", "loan/ongoing/orders", signed=True, data=params, version=1)
        
    margin_v1_get_loan_ongoing_orders.__doc__ = Client.margin_v1_get_loan_ongoing_orders.__doc__
            
    async def margin_v2_get_loan_flexible_ongoing_orders(self, **params):
        return await self._request_margin_api("get", "loan/flexible/ongoing/orders", signed=True, data=params, version=2)
        
    margin_v2_get_loan_flexible_ongoing_orders.__doc__ = Client.margin_v2_get_loan_flexible_ongoing_orders.__doc__
            
    async def margin_v1_post_algo_futures_new_order_vp(self, **params):
        return await self._request_margin_api("post", "algo/futures/newOrderVp", signed=True, data=params, version=1)
        
    margin_v1_post_algo_futures_new_order_vp.__doc__ = Client.margin_v1_post_algo_futures_new_order_vp.__doc__
            
    async def futures_v1_post_convert_get_quote(self, **params):
        return await self._request_futures_api("post", "convert/getQuote", signed=True, data=params, version=1)
        
    futures_v1_post_convert_get_quote.__doc__ = Client.futures_v1_post_convert_get_quote.__doc__
            
    async def margin_v1_get_algo_spot_sub_orders(self, **params):
        return await self._request_margin_api("get", "algo/spot/subOrders", signed=True, data=params, version=1)
        
    margin_v1_get_algo_spot_sub_orders.__doc__ = Client.margin_v1_get_algo_spot_sub_orders.__doc__
            
    async def margin_v1_post_portfolio_redeem(self, **params):
        return await self._request_margin_api("post", "portfolio/redeem", signed=True, data=params, version=1)
        
    margin_v1_post_portfolio_redeem.__doc__ = Client.margin_v1_post_portfolio_redeem.__doc__
            
    async def margin_v1_post_lending_auto_invest_plan_add(self, **params):
        return await self._request_margin_api("post", "lending/auto-invest/plan/add", signed=True, data=params, version=1)
        
    margin_v1_post_lending_auto_invest_plan_add.__doc__ = Client.margin_v1_post_lending_auto_invest_plan_add.__doc__
            
    async def v3_get_order_list(self, **params):
        return await self._request_api("get", "orderList", signed=True, data=params, version="v3")
        
    v3_get_order_list.__doc__ = Client.v3_get_order_list.__doc__
            
    async def v3_get_my_trades(self, **params):
        return await self._request_api("get", "myTrades", signed=True, data=params, version="v3")
        
    async def margin_v1_get_lending_auto_invest_source_asset_list(self, **params):
        return await self._request_margin_api("get", "lending/auto-invest/source-asset/list", signed=True, data=params, version=1)
        
    margin_v1_get_lending_auto_invest_source_asset_list.__doc__ = Client.margin_v1_get_lending_auto_invest_source_asset_list.__doc__
            
    async def margin_v1_get_margin_all_order_list(self, **params):
        return await self._request_margin_api("get", "margin/allOrderList", signed=True, data=params, version=1)
        
    margin_v1_get_margin_all_order_list.__doc__ = Client.margin_v1_get_margin_all_order_list.__doc__
            
    async def margin_v1_post_eth_staking_eth_redeem(self, **params):
        return await self._request_margin_api("post", "eth-staking/eth/redeem", signed=True, data=params, version=1)
        
    margin_v1_post_eth_staking_eth_redeem.__doc__ = Client.margin_v1_post_eth_staking_eth_redeem.__doc__
            
    async def margin_v1_get_broker_rebate_historical_record(self, **params):
        return await self._request_margin_api("get", "broker/rebate/historicalRecord", signed=True, data=params, version=1)
        
    margin_v1_get_broker_rebate_historical_record.__doc__ = Client.margin_v1_get_broker_rebate_historical_record.__doc__
            
    async def margin_v1_get_simple_earn_locked_history_subscription_record(self, **params):
        return await self._request_margin_api("get", "simple-earn/locked/history/subscriptionRecord", signed=True, data=params, version=1)
        
    margin_v1_get_simple_earn_locked_history_subscription_record.__doc__ = Client.margin_v1_get_simple_earn_locked_history_subscription_record.__doc__
            
    async def futures_coin_v1_put_order(self, **params):
        return await self._request_futures_coin_api("put", "order", signed=True, data=params, version=1)
        
    futures_coin_v1_put_order.__doc__ = Client.futures_coin_v1_put_order.__doc__
            
    async def margin_v1_get_managed_subaccount_asset(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/asset", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_asset.__doc__ = Client.margin_v1_get_managed_subaccount_asset.__doc__
            
    async def margin_v1_get_sol_staking_sol_quota(self, **params):
        return await self._request_margin_api("get", "sol-staking/sol/quota", signed=True, data=params, version=1)
        
    margin_v1_get_sol_staking_sol_quota.__doc__ = Client.margin_v1_get_sol_staking_sol_quota.__doc__
            
    async def margin_v1_post_loan_vip_renew(self, **params):
        return await self._request_margin_api("post", "loan/vip/renew", signed=True, data=params, version=1)
        
    margin_v1_post_loan_vip_renew.__doc__ = Client.margin_v1_post_loan_vip_renew.__doc__
            
    async def margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent(self, **params):
        return await self._request_margin_api("get", "managed-subaccount/queryTransLogForTradeParent", signed=True, data=params, version=1)
        
    margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent.__doc__ = Client.margin_v1_get_managed_subaccount_query_trans_log_for_trade_parent.__doc__
            
    async def margin_v1_post_sub_account_sub_account_api_ip_restriction(self, **params):
        return await self._request_margin_api("post", "sub-account/subAccountApi/ipRestriction", signed=True, data=params, version=1)
        
    margin_v1_post_sub_account_sub_account_api_ip_restriction.__doc__ = Client.margin_v1_post_sub_account_sub_account_api_ip_restriction.__doc__
            
    async def margin_v1_get_simple_earn_flexible_history_redemption_record(self, **params):
        return await self._request_margin_api("get", "simple-earn/flexible/history/redemptionRecord", signed=True, data=params, version=1)
        
    margin_v1_get_simple_earn_flexible_history_redemption_record.__doc__ = Client.margin_v1_get_simple_earn_flexible_history_redemption_record.__doc__
            
    async def margin_v1_get_broker_sub_account_api(self, **params):
        return await self._request_margin_api("get", "broker/subAccountApi", signed=True, data=params, version=1)
        
    margin_v1_get_broker_sub_account_api.__doc__ = Client.margin_v1_get_broker_sub_account_api.__doc__
            
    async def options_v1_get_exercise_history(self, **params):
        return await self._request_options_api("get", "exerciseHistory", signed=False, data=params)
        
    options_v1_get_exercise_history.__doc__ = Client.options_v1_get_exercise_history.__doc__
            
    async def margin_v1_get_convert_exchange_info(self, **params):
        return await self._request_margin_api("get", "convert/exchangeInfo", signed=False, data=params, version=1)
        
    margin_v1_get_convert_exchange_info.__doc__ = Client.margin_v1_get_convert_exchange_info.__doc__
            
    async def futures_v1_delete_batch_order(self, **params):
        return await self._request_futures_api("delete", "batchOrder", signed=True, data=params, version=1)
        
    futures_v1_delete_batch_order.__doc__ = Client.futures_v1_delete_batch_order.__doc__
            
    async def margin_v1_get_eth_staking_eth_history_wbeth_rewards_history(self, **params):
        return await self._request_margin_api("get", "eth-staking/eth/history/wbethRewardsHistory", signed=True, data=params, version=1)
        
    margin_v1_get_eth_staking_eth_history_wbeth_rewards_history.__doc__ = Client.margin_v1_get_eth_staking_eth_history_wbeth_rewards_history.__doc__
            
    async def margin_v1_get_mining_pub_algo_list(self, **params):
        return await self._request_margin_api("get", "mining/pub/algoList", signed=True, data=params, version=1)
        
    margin_v1_get_mining_pub_algo_list.__doc__ = Client.margin_v1_get_mining_pub_algo_list.__doc__
            
    async def options_v1_get_block_trades(self, **params):
        return await self._request_options_api("get", "blockTrades", signed=False, data=params)
        
    options_v1_get_block_trades.__doc__ = Client.options_v1_get_block_trades.__doc__
            
    async def margin_v1_get_copy_trading_futures_lead_symbol(self, **params):
        return await self._request_margin_api("get", "copyTrading/futures/leadSymbol", signed=True, data=params, version=1)
        
    margin_v1_get_copy_trading_futures_lead_symbol.__doc__ = Client.margin_v1_get_copy_trading_futures_lead_symbol.__doc__
            
    async def margin_v1_get_mining_worker_list(self, **params):
        return await self._request_margin_api("get", "mining/worker/list", signed=True, data=params, version=1)
        
    margin_v1_get_mining_worker_list.__doc__ = Client.margin_v1_get_mining_worker_list.__doc__
            
    async def margin_v1_get_dci_product_list(self, **params):
        return await self._request_margin_api("get", "dci/product/list", signed=True, data=params, version=1)
        
    margin_v1_get_dci_product_list.__doc__ = Client.margin_v1_get_dci_product_list.__doc__
            
    async def futures_v1_get_convert_order_status(self, **params):
        return await self._request_futures_api("get", "convert/orderStatus", signed=True, data=params, version=1)
        
    futures_v1_get_convert_order_status.__doc__ = Client.futures_v1_get_convert_order_status.__doc__
            
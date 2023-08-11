from base64 import b64encode
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Union, Any

import aiohttp
import asyncio
import hashlib
import hmac
import requests
import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from operator import itemgetter
from urllib.parse import urlencode

from .helpers import interval_to_milliseconds, convert_ts_str, get_loop
from .exceptions import BinanceAPIException, BinanceRequestException, NotImplementedException
from .enums import HistoricalKlinesType


class BaseClient:

    API_URL = 'https://api{}.binance.{}/api'
    API_TESTNET_URL = 'https://testnet.binance.vision/api'
    MARGIN_API_URL = 'https://api{}.binance.{}/sapi'
    WEBSITE_URL = 'https://www.binance.{}'
    FUTURES_URL = 'https://fapi.binance.{}/fapi'
    FUTURES_TESTNET_URL = 'https://testnet.binancefuture.com/fapi'
    FUTURES_DATA_URL = 'https://fapi.binance.{}/futures/data'
    FUTURES_DATA_TESTNET_URL = 'https://testnet.binancefuture.com/futures/data'
    FUTURES_COIN_URL = "https://dapi.binance.{}/dapi"
    FUTURES_COIN_TESTNET_URL = 'https://testnet.binancefuture.com/dapi'
    FUTURES_COIN_DATA_URL = "https://dapi.binance.{}/futures/data"
    FUTURES_COIN_DATA_TESTNET_URL = 'https://testnet.binancefuture.com/futures/data'
    OPTIONS_URL = 'https://eapi.binance.{}/eapi'
    OPTIONS_TESTNET_URL = 'https://testnet.binanceops.{}/eapi'
    PUBLIC_API_VERSION = 'v1'
    PRIVATE_API_VERSION = 'v3'
    MARGIN_API_VERSION = 'v1'
    MARGIN_API_VERSION2 = 'v2'
    MARGIN_API_VERSION3 = 'v3'
    MARGIN_API_VERSION4 = 'v4'
    FUTURES_API_VERSION = 'v1'
    FUTURES_API_VERSION2 = 'v2'
    OPTIONS_API_VERSION = 'v1'

    BASE_ENDPOINT_DEFAULT = ''
    BASE_ENDPOINT_1 = '1'
    BASE_ENDPOINT_2 = '2'
    BASE_ENDPOINT_3 = '3'
    BASE_ENDPOINT_4 = '4'

    REQUEST_TIMEOUT: float = 10

    SYMBOL_TYPE_SPOT = 'SPOT'

    ORDER_STATUS_NEW = 'NEW'
    ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    ORDER_STATUS_FILLED = 'FILLED'
    ORDER_STATUS_CANCELED = 'CANCELED'
    ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
    ORDER_STATUS_REJECTED = 'REJECTED'
    ORDER_STATUS_EXPIRED = 'EXPIRED'

    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'

    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    FUTURE_ORDER_TYPE_LIMIT = 'LIMIT'
    FUTURE_ORDER_TYPE_MARKET = 'MARKET'
    FUTURE_ORDER_TYPE_STOP = 'STOP'
    FUTURE_ORDER_TYPE_STOP_MARKET = 'STOP_MARKET'
    FUTURE_ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'
    FUTURE_ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    TIME_IN_FORCE_GTC = 'GTC'  # Good till cancelled
    TIME_IN_FORCE_IOC = 'IOC'  # Immediate or cancel
    TIME_IN_FORCE_FOK = 'FOK'  # Fill or kill

    ORDER_RESP_TYPE_ACK = 'ACK'
    ORDER_RESP_TYPE_RESULT = 'RESULT'
    ORDER_RESP_TYPE_FULL = 'FULL'

    # For accessing the data returned by Client.aggregate_trades().
    AGG_ID = 'a'
    AGG_PRICE = 'p'
    AGG_QUANTITY = 'q'
    AGG_FIRST_TRADE_ID = 'f'
    AGG_LAST_TRADE_ID = 'l'
    AGG_TIME = 'T'
    AGG_BUYER_MAKES = 'm'
    AGG_BEST_MATCH = 'M'

    # new asset transfer api enum
    SPOT_TO_FIAT = "MAIN_C2C"
    SPOT_TO_USDT_FUTURE = "MAIN_UMFUTURE"
    SPOT_TO_COIN_FUTURE = "MAIN_CMFUTURE"
    SPOT_TO_MARGIN_CROSS = "MAIN_MARGIN"
    SPOT_TO_MINING = "MAIN_MINING"
    FIAT_TO_SPOT = "C2C_MAIN"
    FIAT_TO_USDT_FUTURE = "C2C_UMFUTURE"
    FIAT_TO_MINING = "C2C_MINING"
    USDT_FUTURE_TO_SPOT = "UMFUTURE_MAIN"
    USDT_FUTURE_TO_FIAT = "UMFUTURE_C2C"
    USDT_FUTURE_TO_MARGIN_CROSS = "UMFUTURE_MARGIN"
    COIN_FUTURE_TO_SPOT = "CMFUTURE_MAIN"
    MARGIN_CROSS_TO_SPOT = "MARGIN_MAIN"
    MARGIN_CROSS_TO_USDT_FUTURE = "MARGIN_UMFUTURE"
    MINING_TO_SPOT = "MINING_MAIN"
    MINING_TO_USDT_FUTURE = "MINING_UMFUTURE"
    MINING_TO_FIAT = "MINING_C2C"

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com', base_endpoint: str = BASE_ENDPOINT_DEFAULT,
        testnet: bool = False, private_key: Optional[Union[str, Path]] = None, private_key_pass: Optional[str] = None
    ):
        """Binance API Client constructor

        :param api_key: Api Key
        :type api_key: str.
        :param api_secret: Api Secret
        :type api_secret: str.
        :param requests_params: optional - Dictionary of requests params to use for all calls
        :type requests_params: dict.
        :param testnet: Use testnet environment - only available for vanilla options at the moment
        :type testnet: bool
        :param private_key: Path to private key, or string of file contents
        :type private_key: optional - str or Path
        :param private_key_pass: Password of private key
        :type private_key_pass: optional - str

        """

        self.tld = tld
        self.API_URL = self.API_URL.format(base_endpoint, tld)
        self.MARGIN_API_URL = self.MARGIN_API_URL.format(base_endpoint, tld)
        self.WEBSITE_URL = self.WEBSITE_URL.format(tld)
        self.FUTURES_URL = self.FUTURES_URL.format(tld)
        self.FUTURES_DATA_URL = self.FUTURES_DATA_URL.format(tld)
        self.FUTURES_COIN_URL = self.FUTURES_COIN_URL.format(tld)
        self.FUTURES_COIN_DATA_URL = self.FUTURES_COIN_DATA_URL.format(tld)
        self.OPTIONS_URL = self.OPTIONS_URL.format(tld)
        self.OPTIONS_TESTNET_URL = self.OPTIONS_TESTNET_URL.format(tld)

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.PRIVATE_KEY = self._init_private_key(private_key, private_key_pass)
        self.session = self._init_session()
        self._requests_params = requests_params
        self.response = None
        self.testnet = testnet
        self.timestamp_offset = 0

    def _get_headers(self) -> Dict:
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',  # noqa
        }
        if self.API_KEY:
            assert self.API_KEY
            headers['X-MBX-APIKEY'] = self.API_KEY
        return headers

    def _init_session(self):
        raise NotImplementedError

    def _init_private_key(self, private_key: Optional[Union[str, Path]], private_key_pass: Optional[str] = None):
        if not private_key:
            return
        if isinstance(private_key, Path):
            with open(private_key, "r") as f:
                private_key = f.read()
        return RSA.import_key(private_key, passphrase=private_key_pass)

    def _create_api_uri(self, path: str, signed: bool = True, version: str = PUBLIC_API_VERSION) -> str:
        url = self.API_URL
        if self.testnet:
            url = self.API_TESTNET_URL
        v = self.PRIVATE_API_VERSION if signed else version
        return url + '/' + v + '/' + path

    def _create_margin_api_uri(self, path: str, version: int = 1) -> str:
        options = {
            1: self.MARGIN_API_VERSION,
            2: self.MARGIN_API_VERSION2,
            3: self.MARGIN_API_VERSION3,
            4: self.MARGIN_API_VERSION4,
        }
        return self.MARGIN_API_URL + '/' + options[version] + '/' + path

    def _create_website_uri(self, path: str) -> str:
        return self.WEBSITE_URL + '/' + path

    def _create_futures_api_uri(self, path: str, version: int = 1) -> str:
        url = self.FUTURES_URL
        if self.testnet:
            url = self.FUTURES_TESTNET_URL
        options = {1: self.FUTURES_API_VERSION, 2: self.FUTURES_API_VERSION2}
        return url + '/' + options[version] + '/' + path

    def _create_futures_data_api_uri(self, path: str) -> str:
        url = self.FUTURES_DATA_URL
        if self.testnet:
            url = self.FUTURES_DATA_TESTNET_URL
        return url + '/' + path

    def _create_futures_coin_api_url(self, path: str, version: int = 1) -> str:
        url = self.FUTURES_COIN_URL
        if self.testnet:
            url = self.FUTURES_COIN_TESTNET_URL
        options = {1: self.FUTURES_API_VERSION, 2: self.FUTURES_API_VERSION2}
        return url + "/" + options[version] + "/" + path

    def _create_futures_coin_data_api_url(self, path: str, version: int = 1) -> str:
        url = self.FUTURES_COIN_DATA_URL
        if self.testnet:
            url = self.FUTURES_COIN_DATA_TESTNET_URL
        return url + "/" + path

    def _create_options_api_uri(self, path: str) -> str:
        url = self.OPTIONS_URL
        if self.testnet:
            url = self.OPTIONS_TESTNET_URL
        return url + '/' + self.OPTIONS_API_VERSION + '/' + path

    def _rsa_signature(self, query_string: str):
        assert self.PRIVATE_KEY
        h = SHA256.new(query_string.encode("utf-8"))
        signature = pkcs1_15.new(self.PRIVATE_KEY).sign(h)
        return b64encode(signature).decode()

    def _hmac_signature(self, query_string: str) -> str:
        assert self.API_SECRET, "API Secret required for private endpoints"
        m = hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    def _generate_signature(self, data: Dict) -> str:
        sig_func = self._hmac_signature
        if self.PRIVATE_KEY:
            sig_func = self._rsa_signature
        query_string = '&'.join([f"{d[0]}={d[1]}" for d in self._order_params(data)])
        return sig_func(query_string)

    @staticmethod
    def _order_params(data: Dict) -> List[Tuple[str, str]]:
        """Convert params to list with signature as last element

        :param data:
        :return:

        """
        data = dict(filter(lambda el: el[1] is not None, data.items()))
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, str(value)))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def _get_request_kwargs(self, method, signed: bool, force_params: bool = False, **kwargs) -> Dict:

        # set default requests timeout
        kwargs['timeout'] = self.REQUEST_TIMEOUT

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get('data', None)
        if data and isinstance(data, dict):
            kwargs['data'] = data
            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del kwargs['data']['requests_params']

        if signed:
            # generate signature
            kwargs['data']['timestamp'] = int(time.time() * 1000 + self.timestamp_offset)
            kwargs['data']['signature'] = self._generate_signature(kwargs['data'])

        # sort get and post params to match signature order
        if data:
            # sort post params and remove any arguments with values of None
            kwargs['data'] = self._order_params(kwargs['data'])
            # Remove any arguments with values of None.
            null_args = [i for i, (key, value) in enumerate(kwargs['data']) if value is None]
            for i in reversed(null_args):
                del kwargs['data'][i]

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del kwargs['data']

        return kwargs


class Client(BaseClient):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com',
        base_endpoint: str = BaseClient.BASE_ENDPOINT_DEFAULT, testnet: bool = False,
        private_key: Optional[Union[str, Path]] = None, private_key_pass: Optional[str] = None
    ):

        super().__init__(api_key, api_secret, requests_params, tld, base_endpoint, testnet, private_key, private_key_pass)

        # init DNS and SSL cert
        self.ping()

    def _init_session(self) -> requests.Session:

        headers = self._get_headers()

        session = requests.session()
        session.headers.update(headers)
        return session

    def _request(self, method, uri: str, signed: bool, force_params: bool = False, **kwargs):

        kwargs = self._get_request_kwargs(method, signed, force_params, **kwargs)

        self.response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(self.response)

    @staticmethod
    def _handle_response(response: requests.Response):
        """Internal helper for handling API responses from the Binance server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not (200 <= response.status_code < 300):
            raise BinanceAPIException(response, response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            raise BinanceRequestException('Invalid Response: %s' % response.text)

    def _request_api(
        self, method, path: str, signed: bool = False, version=BaseClient.PUBLIC_API_VERSION, **kwargs
    ):
        uri = self._create_api_uri(path, signed, version)
        return self._request(method, uri, signed, **kwargs)

    def _request_futures_api(self, method, path, signed=False, version: int = 1, **kwargs) -> Dict:
        uri = self._create_futures_api_uri(path, version)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_futures_data_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_futures_data_api_uri(path)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_futures_coin_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_futures_coin_api_url(path, version=version)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_futures_coin_data_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_futures_coin_data_api_url(path, version=version)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_options_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_options_api_uri(path)

        return self._request(method, uri, signed, True, **kwargs)

    def _request_margin_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_margin_api_uri(path, version)

        return self._request(method, uri, signed, **kwargs)

    def _request_website(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_website_uri(path)
        return self._request(method, uri, signed, **kwargs)

    def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return self._request_api('get', path, signed, version, **kwargs)

    def _post(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request_api('post', path, signed, version, **kwargs)

    def _put(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request_api('put', path, signed, version, **kwargs)

    def _delete(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return self._request_api('delete', path, signed, version, **kwargs)

    # Exchange Endpoints

    def get_products(self) -> Dict:
        """Return list of products currently listed on Binance

        Use get_exchange_info() call instead

        :returns: list - List of product dictionaries

        :raises: BinanceRequestException, BinanceAPIException

        """
        products = self._request_website('get', 'exchange-api/v1/public/asset-service/product/get-products')
        return products

    def get_exchange_info(self) -> Dict:
        """Return rate limits and list of symbols

        :returns: list - List of product dictionaries

        .. code-block:: python

            {
                "timezone": "UTC",
                "serverTime": 1508631584636,
                "rateLimits": [
                    {
                        "rateLimitType": "REQUESTS",
                        "interval": "MINUTE",
                        "limit": 1200
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "SECOND",
                        "limit": 10
                    },
                    {
                        "rateLimitType": "ORDERS",
                        "interval": "DAY",
                        "limit": 100000
                    }
                ],
                "exchangeFilters": [],
                "symbols": [
                    {
                        "symbol": "ETHBTC",
                        "status": "TRADING",
                        "baseAsset": "ETH",
                        "baseAssetPrecision": 8,
                        "quoteAsset": "BTC",
                        "quotePrecision": 8,
                        "orderTypes": ["LIMIT", "MARKET"],
                        "icebergAllowed": false,
                        "filters": [
                            {
                                "filterType": "PRICE_FILTER",
                                "minPrice": "0.00000100",
                                "maxPrice": "100000.00000000",
                                "tickSize": "0.00000100"
                            }, {
                                "filterType": "LOT_SIZE",
                                "minQty": "0.00100000",
                                "maxQty": "100000.00000000",
                                "stepSize": "0.00100000"
                            }, {
                                "filterType": "MIN_NOTIONAL",
                                "minNotional": "0.00100000"
                            }
                        ]
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        return self._get('exchangeInfo', version=self.PRIVATE_API_VERSION)

    def get_symbol_info(self, symbol) -> Optional[Dict]:
        """Return information about a symbol

        :param symbol: required e.g. BNBBTC
        :type symbol: str

        :returns: Dict if found, None if not

        .. code-block:: python

            {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "orderTypes": ["LIMIT", "MARKET"],
                "icebergAllowed": false,
                "filters": [
                    {
                        "filterType": "PRICE_FILTER",
                        "minPrice": "0.00000100",
                        "maxPrice": "100000.00000000",
                        "tickSize": "0.00000100"
                    }, {
                        "filterType": "LOT_SIZE",
                        "minQty": "0.00100000",
                        "maxQty": "100000.00000000",
                        "stepSize": "0.00100000"
                    }, {
                        "filterType": "MIN_NOTIONAL",
                        "minNotional": "0.00100000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """

        res = self.get_exchange_info()

        for item in res['symbols']:
            if item['symbol'] == symbol.upper():
                return item

        return None

    # General Endpoints

    def ping(self) -> Dict:
        """Test connectivity to the Rest API.

        https://binance-docs.github.io/apidocs/spot/en/#test-connectivity

        :returns: Empty array

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ping', version=self.PRIVATE_API_VERSION)

    def get_server_time(self) -> Dict:
        """Test connectivity to the Rest API and get the current server time.

        https://binance-docs.github.io/apidocs/spot/en/#check-server-time

        :returns: Current server time

        .. code-block:: python

            {
                "serverTime": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('time', version=self.PRIVATE_API_VERSION)

    # Market Data Endpoints

    def get_all_tickers(self) -> List[Dict[str, str]]:
        """Latest price for all symbols.

        https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

        :returns: List of market tickers

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/price', version=self.PRIVATE_API_VERSION)

    def get_orderbook_tickers(self, **params) -> Dict:
        """Best price/qty on the order book for all symbols.

        https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker

        :param symbol: optional
        :type symbol: str
        :param symbols: optional accepted format  ["BTCUSDT","BNBUSDT"] or %5B%22BTCUSDT%22,%22BNBUSDT%22%5D
        :type symbols: str

        :returns: List of order book market entries

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        data = {}
        if "symbol" in params:
            data["symbol"] = params["symbol"]
        elif "symbols" in params:
            data["symbols"] = params["symbols"]
        return self._get('ticker/bookTicker', data=data, version=self.PRIVATE_API_VERSION)

    def get_order_book(self, **params) -> Dict:
        """Get the Order Book for the market

        https://binance-docs.github.io/apidocs/spot/en/#order-book

        :param symbol: required
        :type symbol: str
        :param limit:  Default 100; max 1000
        :type limit: int

        :returns: API response

        .. code-block:: python

            {
                "lastUpdateId": 1027024,
                "bids": [
                    [
                        "4.00000000",     # PRICE
                        "431.00000000",   # QTY
                        []                # Can be ignored
                    ]
                ],
                "asks": [
                    [
                        "4.00000200",
                        "12.00000000",
                        []
                    ]
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('depth', data=params, version=self.PRIVATE_API_VERSION)

    def get_recent_trades(self, **params) -> Dict:
        """Get recent trades (up to last 500).

        https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 1000.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('trades', data=params)

    def get_historical_trades(self, **params) -> Dict:
        """Get older trades.

        https://binance-docs.github.io/apidocs/spot/en/#old-trade-lookup

        :param symbol: required
        :type symbol: str
        :param limit:  Default 500; max 1000.
        :type limit: int
        :param fromId:  TradeId to fetch from. Default gets most recent trades.
        :type fromId: str

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "time": 1499865549590,
                    "isBuyerMaker": true,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('historicalTrades', data=params, version=self.PRIVATE_API_VERSION)

    def get_aggregate_trades(self, **params) -> Dict:
        """Get compressed, aggregate trades. Trades that fill at the time,
        from the same order, with the same price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

        :param symbol: required
        :type symbol: str
        :param fromId:  ID to get aggregate trades from INCLUSIVE.
        :type fromId: str
        :param startTime: Timestamp in ms to get aggregate trades from INCLUSIVE.
        :type startTime: int
        :param endTime: Timestamp in ms to get aggregate trades until INCLUSIVE.
        :type endTime: int
        :param limit:  Default 500; max 1000.
        :type limit: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "a": 26129,         # Aggregate tradeId
                    "p": "0.01633102",  # Price
                    "q": "4.70443515",  # Quantity
                    "f": 27781,         # First tradeId
                    "l": 27781,         # Last tradeId
                    "T": 1498793709153, # Timestamp
                    "m": true,          # Was the buyer the maker?
                    "M": true           # Was the trade the best price match?
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('aggTrades', data=params, version=self.PRIVATE_API_VERSION)

    def aggregate_trade_iter(self, symbol: str, start_str=None, last_id=None):
        """Iterate over aggregate trade data from (start_time or last_id) to
        the end of the history so far.

        If start_time is specified, start with the first trade after
        start_time. Meant to initialise a local cache of trade data.

        If last_id is specified, start with the trade after it. This is meant
        for updating a pre-existing local trade data cache.

        Only allows start_str or last_id—not both. Not guaranteed to work
        right if you're running more than one of these simultaneously. You
        will probably hit your rate limit.

        See dateparser docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Symbol string e.g. ETHBTC
        :type symbol: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds. The iterator will
        return the first trade occurring later than this time.
        :type start_str: str|int
        :param last_id: aggregate trade ID of the last known aggregate trade.
        Not a regular trade ID. See https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

        :returns: an iterator of JSON objects, one per trade. The format of
        each object is identical to Client.aggregate_trades().

        :type last_id: int
        """
        if start_str is not None and last_id is not None:
            raise ValueError(
                'start_time and last_id may not be simultaneously specified.')

        # If there's no last_id, get one.
        if last_id is None:
            # Without a last_id, we actually need the first trade.  Normally,
            # we'd get rid of it. See the next loop.
            if start_str is None:
                trades = self.get_aggregate_trades(symbol=symbol, fromId=0)
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
                    trades = self.get_aggregate_trades(
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
            trades = self.get_aggregate_trades(symbol=symbol, fromId=last_id)
            # fromId=n returns a set starting with id n, but we already have
            # that one. So get rid of the first item in the result set.
            trades = trades[1:]
            if len(trades) == 0:
                return
            for t in trades:
                yield t
            last_id = trades[-1][self.AGG_ID]

    def get_klines(self, **params) -> Dict:
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

        :param symbol: required
        :type symbol: str
        :param interval: -
        :type interval: str
        :param limit: - Default 500; max 1000.
        :type limit: int
        :param startTime:
        :type startTime: int
        :param endTime:
        :type endTime: int

        :returns: API response

        .. code-block:: python

            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('klines', data=params, version=self.PRIVATE_API_VERSION)

    def _klines(self, klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT, **params) -> Dict:
        """Get klines of spot (get_klines) or futures (futures_klines) endpoints.

        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: klines, see get_klines

        """
        if 'endTime' in params and not params['endTime']:
            del params['endTime']

        if HistoricalKlinesType.SPOT == klines_type:
            return self.get_klines(**params)
        elif HistoricalKlinesType.FUTURES == klines_type:
            return self.futures_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN == klines_type:
            return self.futures_coin_klines(**params)
        else:
            raise NotImplementedException(klines_type)

    def _get_earliest_valid_timestamp(self, symbol, interval, klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        """Get the earliest valid open timestamp from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: first valid timestamp

        """
        kline = self._klines(
            klines_type=klines_type,
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=int(time.time() * 1000)
        )
        return kline[0][0]

    def get_historical_klines(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                              klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        """Get Historical Klines from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 1000; max 1000.
        :type limit: int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """
        return self._historical_klines(
            symbol, interval, start_str=start_str, end_str=end_str, limit=limit, klines_type=klines_type
        )

    def _historical_klines(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                           klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        """Get Historical Klines from Binance (spot or futures)

        See dateparser docs for valid start and end string formats https://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: None|str|int
        :param limit: Default 1000; max 1000.
        :type limit: int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """
        # init our list
        output_data = []

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = self._get_earliest_valid_timestamp(symbol, interval, klines_type)
            start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)
        if end_ts and start_ts and end_ts <= start_ts:
            return output_data

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            temp_data = self._klines(
                klines_type=klines_type,
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
            )

            # append this loops data to our output data
            if temp_data:
                output_data += temp_data

            # handle the case where exactly the limit amount of data was returned last loop
            # check if we received less than the required limit and exit the loop
            if not len(temp_data) or len(temp_data) < limit:
                # exit the while loop
                break

            # increment next call by our timeframe
            start_ts = temp_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                time.sleep(1)

        return output_data

    def get_historical_klines_generator(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                                        klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        """Get Historical Klines generator from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: amount of candles to return per request (default 1000)
        :type limit: int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: generator of OHLCV values

        """

        return self._historical_klines_generator(symbol, interval, start_str, end_str, limit, klines_type=klines_type)

    def _historical_klines_generator(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                                     klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        """Get Historical Klines generator from Binance (spot or futures)

        See dateparser docs for valid start and end string formats https://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: optional - Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param klines_type: Historical klines type: SPOT or FUTURES
        :type klines_type: HistoricalKlinesType

        :return: generator of OHLCV values

        """

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = self._get_earliest_valid_timestamp(symbol, interval, klines_type)
            start_ts = max(start_ts, first_valid_ts)

        # if an end time was passed convert it
        end_ts = convert_ts_str(end_str)
        if end_ts and start_ts and end_ts <= start_ts:
            return

        idx = 0
        while True:
            # fetch the klines from start_ts up to max 500 entries or the end_ts if set
            output_data = self._klines(
                klines_type=klines_type,
                symbol=symbol,
                interval=interval,
                limit=limit,
                startTime=start_ts,
                endTime=end_ts
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

            # set our start timestamp using the last value in the array
            # increment next call by our timeframe
            start_ts = output_data[-1][0] + timeframe

            # exit loop if we reached end_ts before reaching <limit> klines
            if end_ts and start_ts >= end_ts:
                break

            # sleep after every 3rd call to be kind to the API
            idx += 1
            if idx % 3 == 0:
                time.sleep(1)

    def get_avg_price(self, **params):
        """Current average price for a symbol.

        https://binance-docs.github.io/apidocs/spot/en/#current-average-price

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "mins": 5,
                "price": "9.35751834"
            }
        """
        return self._get('avgPrice', data=params, version=self.PRIVATE_API_VERSION)

    def get_ticker(self, **params):
        """24 hour price change statistics.

        https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "fristId": 28385,   # First tradeId
                "lastId": 28460,    # Last tradeId
                "count": 76         # Trade count
            }

        OR

        .. code-block:: python

            [
                {
                    "priceChange": "-94.99999800",
                    "priceChangePercent": "-95.960",
                    "weightedAvgPrice": "0.29628482",
                    "prevClosePrice": "0.10002000",
                    "lastPrice": "4.00000200",
                    "bidPrice": "4.00000000",
                    "askPrice": "4.00000200",
                    "openPrice": "99.00000000",
                    "highPrice": "100.00000000",
                    "lowPrice": "0.10000000",
                    "volume": "8913.30000000",
                    "openTime": 1499783499040,
                    "closeTime": 1499869899040,
                    "fristId": 28385,   # First tradeId
                    "lastId": 28460,    # Last tradeId
                    "count": 76         # Trade count
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/24hr', data=params, version=self.PRIVATE_API_VERSION)

    def get_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "price": "4.00000200"
                },
                {
                    "symbol": "ETHBTC",
                    "price": "0.07946600"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/price', data=params, version=self.PRIVATE_API_VERSION)

    def get_orderbook_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker

        :param symbol:
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            }

        OR

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "bidPrice": "4.00000000",
                    "bidQty": "431.00000000",
                    "askPrice": "4.00000200",
                    "askQty": "9.00000000"
                },
                {
                    "symbol": "ETHBTC",
                    "bidPrice": "0.07946700",
                    "bidQty": "9.00000000",
                    "askPrice": "100000.00000000",
                    "askQty": "1000.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('ticker/bookTicker', data=params, version=self.PRIVATE_API_VERSION)

    # Account Endpoints

    def create_order(self, **params):
        """Send in a new order

        Any order with an icebergQty MUST have timeInForce set to GTC.

        https://binance-docs.github.io/apidocs/spot/en/#new-order-trade

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
        :param quoteOrderQty: amount the user wants to spend (when buying) or receive (when selling)
            of the quote asset, applicable to MARKET orders
        :type quoteOrderQty: decimal
        :param price: required
        :type price: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: decimal
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol":"LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1" # Will be newClientOrderId
                "transactTime": 1499827319559
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "0.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return self._post('order', True, data=params)

    def order_limit(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'type': self.ORDER_TYPE_LIMIT,
            'timeInForce': timeInForce
        })
        return self.create_order(**params)

    def order_limit_buy(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY,
        })
        return self.order_limit(timeInForce=timeInForce, **params)

    def order_limit_sell(self, timeInForce=BaseClient.TIME_IN_FORCE_GTC, **params):
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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_limit(timeInForce=timeInForce, **params)

    def order_market(self, **params):
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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'type': self.ORDER_TYPE_MARKET
        })
        return self.create_order(**params)

    def order_market_buy(self, **params):
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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY
        })
        return self.order_market(**params)

    def order_market_sell(self, **params):
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

        :returns: API response

        See order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.order_market(**params)

    def create_oco_order(self, **params):
        """Send in a new OCO order

        https://binance-docs.github.io/apidocs/spot/en/#new-oco-trade

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
            }

        Response RESULT:

        .. code-block:: python

            {
            }

        Response FULL:

        .. code-block:: python

            {
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        return self._post('order/oco', True, data=params)

    def order_oco_buy(self, **params):
        """Send in a new OCO buy order

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_BUY
        })
        return self.create_oco_order(**params)

    def order_oco_sell(self, **params):
        """Send in a new OCO sell order

        :param symbol: required
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique id for the stop order. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        See OCO order endpoint for full response options

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException

        """
        params.update({
            'side': self.SIDE_SELL
        })
        return self.create_oco_order(**params)

    def create_test_order(self, **params):
        """Test new order creation and signature/recvWindow long. Creates and validates a new order but does not send it into the matching engine.

        https://binance-docs.github.io/apidocs/spot/en/#test-new-order-trade

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

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException, BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException, BinanceOrderInactiveSymbolException


        """
        return self._post('order/test', True, data=params)

    def get_order(self, **params):
        """Check an order's status. Either orderId or origClientOrderId must be sent.

        https://binance-docs.github.io/apidocs/spot/en/#query-order-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('order', True, data=params)

    def get_all_orders(self, **params):
        """Get all account orders; active, canceled, or filled.

        https://binance-docs.github.io/apidocs/spot/en/#all-orders-user_data

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: Default 500; max 1000.
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('allOrders', True, data=params)

    def cancel_order(self, **params):
        """Cancel an active order. Either orderId or origClientOrderId must be sent.

        https://binance-docs.github.io/apidocs/spot/en/#cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param orderId: The unique order id
        :type orderId: int
        :param origClientOrderId: optional
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "symbol": "LTCBTC",
                "origClientOrderId": "myOrder1",
                "orderId": 1,
                "clientOrderId": "cancelMyOrder1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._delete('order', True, data=params)

    def get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://binance-docs.github.io/apidocs/spot/en/#current-open-orders-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "LTCBTC",
                    "orderId": 1,
                    "clientOrderId": "myOrder1",
                    "price": "0.1",
                    "origQty": "1.0",
                    "executedQty": "0.0",
                    "status": "NEW",
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.0",
                    "icebergQty": "0.0",
                    "time": 1499827319559
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('openOrders', True, data=params)

    def get_open_oco_orders(self, **params):
        """Get all open orders on a symbol.
        https://binance-docs.github.io/apidocs/spot/en/#query-open-oco-user_data
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: API response
        .. code-block:: python
            [
                {
                    "orderListId": 31,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "wuB13fmulKj3YjdqWEcsnp",
                    "transactionTime": 1565246080644,
                    "symbol": "LTCBTC",
                    "orders": [
                        {
                            "symbol": "LTCBTC",
                            "orderId": 4,
                            "clientOrderId": "r3EH2N76dHfLoSZWIUw1bT"
                        },
                        {
                            "symbol": "LTCBTC",
                            "orderId": 5,
                            "clientOrderId": "Cv1SnyPD3qhqpbjpYEHbd2"
                        }
                    ]
                }
            ]
        :raises: BinanceRequestException, BinanceAPIException
        """
        return self._get('openOrderList', True, data=params)

    # User Stream Endpoints
    def get_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/spot/en/#account-information-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "makerCommission": 15,
                "takerCommission": 15,
                "buyerCommission": 0,
                "sellerCommission": 0,
                "canTrade": true,
                "canWithdraw": true,
                "canDeposit": true,
                "balances": [
                    {
                        "asset": "BTC",
                        "free": "4723846.89208129",
                        "locked": "0.00000000"
                    },
                    {
                        "asset": "LTC",
                        "free": "4763368.68006011",
                        "locked": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('account', True, data=params)

    def get_asset_balance(self, asset, **params):
        """Get current asset balance.

        :param asset: required
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: dictionary or None if not found

        .. code-block:: python

            {
                "asset": "BTC",
                "free": "4723846.89208129",
                "locked": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self.get_account(**params)
        # find asset balance in list of balances
        if "balances" in res:
            for bal in res['balances']:
                if bal['asset'].lower() == asset.lower():
                    return bal
        return None

    def get_my_trades(self, **params):
        """Get trades for a specific symbol.

        https://binance-docs.github.io/apidocs/spot/en/#account-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: Default 500; max 1000.
        :type limit: int
        :param fromId: TradeId to fetch from. Default gets most recent trades.
        :type fromId: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "id": 28457,
                    "price": "4.00000100",
                    "qty": "12.00000000",
                    "commission": "10.10000000",
                    "commissionAsset": "BNB",
                    "time": 1499865549590,
                    "isBuyer": true,
                    "isMaker": false,
                    "isBestMatch": true
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._get('myTrades', True, data=params)

    def get_current_order_count(self):
        """Displays the user's current order count usage for all intervals.

        https://binance-docs.github.io/apidocs/spot/en/#query-current-order-count-usage-trade

        :returns: API response

        .. code-block:: python
            [

                {
                    "rateLimitType": "ORDERS",
                    "interval": "SECOND",
                    "intervalNum": 10,
                    "limit": 10000,
                    "count": 0
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "intervalNum": 1,
                    "limit": 20000,
                    "count": 0
                }
            ]

        """
        return self._get('rateLimit/order', True)

    def get_prevented_matches(self, **params):
        """Displays the list of orders that were expired because of STP.

        https://binance-docs.github.io/apidocs/spot/en/#query-prevented-matches-user_data

        :param symbol: required
        :type symbol: str
        :param preventedMatchId: optional
        :type preventedMatchId: int
        :param orderId: optional
        :type orderId: int
        :param fromPreventedMatchId: optional
        :type fromPreventedMatchId: int
        :param limit: optional, Default: 500; Max: 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "symbol": "BTCUSDT",
                    "preventedMatchId": 1,
                    "takerOrderId": 5,
                    "makerOrderId": 3,
                    "tradeGroupId": 1,
                    "selfTradePreventionMode": "EXPIRE_MAKER",
                    "price": "1.100000",
                    "makerPreventedQuantity": "1.300000",
                    "transactTime": 1669101687094
                }
            ]
        """
        return self._get('myPreventedMatches', True, data=params)

    def get_allocations(self, **params):
        """Retrieves allocations resulting from SOR order placement.

        https://binance-docs.github.io/apidocs/spot/en/#query-allocations-user_data

        :param symbol: required
        :type symbol: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param fromAllocationId: optional
        :type fromAllocationId: int
        :param orderId: optional
        :type orderId: int
        :param limit: optional, Default: 500; Max: 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python
            [
                {
                    "symbol": "BTCUSDT",
                    "allocationId": 0,
                    "allocationType": "SOR",
                    "orderId": 1,
                    "orderListId": -1,
                    "price": "1.00000000",
                    "qty": "5.00000000",
                    "quoteQty": "5.00000000",
                    "commission": "0.00000000",
                    "commissionAsset": "BTC",
                    "time": 1687506878118,
                    "isBuyer": true,
                    "isMaker": false,
                    "isAllocator": false
                }
            ]
        """
        return self._get('myAllocations', True, data=params)

    def get_system_status(self):
        """Get system status detail.

        https://binance-docs.github.io/apidocs/spot/en/#system-status-sapi-system

        :returns: API response

        .. code-block:: python

            {
                "status": 0,        # 0: normal，1：system maintenance
                "msg": "normal"     # normal or System maintenance.
            }

        :raises: BinanceAPIException

        """
        return self._request_margin_api('get', 'system/status')

    def get_account_status(self, **params):
        """Get account status detail.

        https://binance-docs.github.io/apidocs/spot/en/#account-status-sapi-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "data": "Normal"
            }

        """
        return self._request_margin_api('get', 'account/status', True, data=params)

    def get_account_api_trading_status(self, **params):
        """Fetch account api trading status detail.

        https://binance-docs.github.io/apidocs/spot/en/#account-api-trading-status-sapi-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "data": {          // API trading status detail
                    "isLocked": false,   // API trading function is locked or not
                    "plannedRecoverTime": 0,  // If API trading function is locked, this is the planned recover time
                    "triggerCondition": {
                            "GCR": 150,  // Number of GTC orders
                            "IFER": 150, // Number of FOK/IOC orders
                            "UFR": 300   // Number of orders
                    },
                    "indicators": {  // The indicators updated every 30 seconds
                         "BTCUSDT": [  // The symbol
                            {
                                "i": "UFR",  // Unfilled Ratio (UFR)
                                "c": 20,     // Count of all orders
                                "v": 0.05,   // Current UFR value
                                "t": 0.995   // Trigger UFR value
                            },
                            {
                                "i": "IFER", // IOC/FOK Expiration Ratio (IFER)
                                "c": 20,     // Count of FOK/IOC orders
                                "v": 0.99,   // Current IFER value
                                "t": 0.99    // Trigger IFER value
                            },
                            {
                                "i": "GCR",  // GTC Cancellation Ratio (GCR)
                                "c": 20,     // Count of GTC orders
                                "v": 0.99,   // Current GCR value
                                "t": 0.99    // Trigger GCR value
                            }
                        ],
                        "ETHUSDT": [
                            {
                                "i": "UFR",
                                "c": 20,
                                "v": 0.05,
                                "t": 0.995
                            },
                            {
                                "i": "IFER",
                                "c": 20,
                                "v": 0.99,
                                "t": 0.99
                            },
                            {
                                "i": "GCR",
                                "c": 20,
                                "v": 0.99,
                                "t": 0.99
                            }
                        ]
                    },
                    "updateTime": 1547630471725
                }
            }

        """
        return self._request_margin_api('get', 'account/apiTradingStatus', True, data=params)

    def get_account_api_permissions(self, **params):
        """Fetch api key permissions.

        https://binance-docs.github.io/apidocs/spot/en/#get-api-key-permission-user_data

        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "ipRestrict": false,
               "createTime": 1623840271000,
               "enableWithdrawals": false,   // This option allows you to withdraw via API. You must apply the IP Access Restriction filter in order to enable withdrawals
               "enableInternalTransfer": true,  // This option authorizes this key to transfer funds between your master account and your sub account instantly
               "permitsUniversalTransfer": true,  // Authorizes this key to be used for a dedicated universal transfer API to transfer multiple supported currencies. Each business's own transfer API rights are not affected by this authorization
               "enableVanillaOptions": false,  //  Authorizes this key to Vanilla options trading
               "enableReading": true,
               "enableFutures": false,  //  API Key created before your futures account opened does not support futures API service
               "enableMargin": false,   //  This option can be adjusted after the Cross Margin account transfer is completed
               "enableSpotAndMarginTrading": false, // Spot and margin trading
               "tradingAuthorityExpirationTime": 1628985600000  // Expiration time for spot and margin trading permission
            }

        """
        return self._request_margin_api('get', 'account/apiRestrictions', True, data=params)

    def get_dust_assets(self, **params):
        """Get assets that can be converted into BNB

        https://binance-docs.github.io/apidocs/spot/en/#get-assets-that-can-be-converted-into-bnb-user_data

        :returns: API response

        .. code-block:: python

            {
                "details": [
                    {
                        "asset": "ADA",
                        "assetFullName": "ADA",
                        "amountFree": "6.21",   //Convertible amount
                        "toBTC": "0.00016848",  //BTC amount
                        "toBNB": "0.01777302",  //BNB amount（Not deducted commission fee）
                        "toBNBOffExchange": "0.01741756", //BNB amount（Deducted commission fee）
                        "exchange": "0.00035546" //Commission fee
                    }
                ],
                "totalTransferBtc": "0.00016848",
                "totalTransferBNB": "0.01777302",
                "dribbletPercentage": "0.02"     //Commission fee
            }

        """
        return self._request_margin_api('post', 'asset/dust-btc', True, data=params)

    def get_dust_log(self, **params):
        """Get log of small amounts exchanged for BNB.

        https://binance-docs.github.io/apidocs/spot/en/#dustlog-sapi-user_data

        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "total": 8,   //Total counts of exchange
                "userAssetDribblets": [
                    {
                        "totalTransferedAmount": "0.00132256",   // Total transfered BNB amount for this exchange.
                        "totalServiceChargeAmount": "0.00002699",    //Total service charge amount for this exchange.
                        "transId": 45178372831,
                        "userAssetDribbletDetails": [           //Details of  this exchange.
                            {
                                "transId": 4359321,
                                "serviceChargeAmount": "0.000009",
                                "amount": "0.0009",
                                "operateTime": 1615985535000,
                                "transferedAmount": "0.000441",
                                "fromAsset": "USDT"
                            },
                            {
                                "transId": 4359321,
                                "serviceChargeAmount": "0.00001799",
                                "amount": "0.0009",
                                "operateTime": "2018-05-03 17:07:04",
                                "transferedAmount": "0.00088156",
                                "fromAsset": "ETH"
                            }
                        ]
                    },
                    {
                        "operateTime":1616203180000,
                        "totalTransferedAmount": "0.00058795",
                        "totalServiceChargeAmount": "0.000012",
                        "transId": 4357015,
                        "userAssetDribbletDetails": [
                            {
                                "transId": 4357015,
                                "serviceChargeAmount": "0.00001"
                                "amount": "0.001",
                                "operateTime": 1616203180000,
                                "transferedAmount": "0.00049",
                                "fromAsset": "USDT"
                            },
                            {
                                "transId": 4357015,
                                "serviceChargeAmount": "0.000002"
                                "amount": "0.0001",
                                "operateTime": 1616203180000,
                                "transferedAmount": "0.00009795",
                                "fromAsset": "ETH"
                            }
                        ]
                    }
                ]
            }

        """
        return self._request_margin_api('get', 'asset/dribblet', True, data=params)

    def transfer_dust(self, **params):
        """Convert dust assets to BNB.

        https://binance-docs.github.io/apidocs/spot/en/#dust-transfer-user_data

        :param asset: The asset being converted. e.g: 'ONE'
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            result = client.transfer_dust(asset='ONE')

        :returns: API response

        .. code-block:: python

            {
                "totalServiceCharge":"0.02102542",
                "totalTransfered":"1.05127099",
                "transferResult":[
                    {
                        "amount":"0.03000000",
                        "fromAsset":"ETH",
                        "operateTime":1563368549307,
                        "serviceChargeAmount":"0.00500000",
                        "tranId":2970932918,
                        "transferedAmount":"0.25000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'asset/dust', True, data=params)

    def get_asset_dividend_history(self, **params):
        """Query asset dividend record.

        https://binance-docs.github.io/apidocs/spot/en/#asset-dividend-record-user_data

        :param asset: optional
        :type asset: str
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            result = client.get_asset_dividend_history()

        :returns: API response

        .. code-block:: python

            {
                "rows":[
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189166000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    },
                    {
                        "amount":"10.00000000",
                        "asset":"BHFT",
                        "divTime":1563189165000,
                        "enInfo":"BHFT distribution",
                        "tranId":2968885920
                    }
                ],
                "total":2
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'asset/assetDividend', True, data=params)

    def make_universal_transfer(self, **params):
        """User Universal Transfer

        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer

        :param type: required
        :type type: str (ENUM)
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer_status = client.make_universal_transfer(params)

        :returns: API response

        .. code-block:: python

            {
                "tranId":13526853623
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'asset/transfer', signed=True, data=params)

    def query_universal_transfer_history(self, **params):
        """Query User Universal Transfer History

        https://binance-docs.github.io/apidocs/spot/en/#query-user-universal-transfer-history

        :param type: required
        :type type: str (ENUM)
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param current: optional - Default 1
        :type current: int
        :param size: required - Default 10, Max 100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer_status = client.query_universal_transfer_history(params)

        :returns: API response

        .. code-block:: python

            {
                "total":2,
                "rows":[
                    {
                        "asset":"USDT",
                        "amount":"1",
                        "type":"MAIN_UMFUTURE"
                        "status": "CONFIRMED",
                        "tranId": 11415955596,
                        "timestamp":1544433328000
                    },
                    {
                        "asset":"USDT",
                        "amount":"2",
                        "type":"MAIN_UMFUTURE",
                        "status": "CONFIRMED",
                        "tranId": 11366865406,
                        "timestamp":1544433328000
                    }
                ]
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'asset/transfer', signed=True, data=params)

    def get_trade_fee(self, **params):
        """Get trade fee.

        https://binance-docs.github.io/apidocs/spot/en/#trade-fee-sapi-user_data

        :param symbol: optional
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "symbol": "ADABNB",
                    "makerCommission": "0.001",
                    "takerCommission": "0.001"
                },
                {
                    "symbol": "BNBBTC",
                    "makerCommission": "0.001",
                    "takerCommission": "0.001"
                }
            ]

        """
        return self._request_margin_api('get', 'asset/tradeFee', True, data=params)

    def get_asset_details(self, **params):
        """Fetch details on assets.

        https://binance-docs.github.io/apidocs/spot/en/#asset-detail-sapi-user_data

        :param asset: optional
        :type asset: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                    "CTR": {
                        "minWithdrawAmount": "70.00000000", //min withdraw amount
                        "depositStatus": false,//deposit status (false if ALL of networks' are false)
                        "withdrawFee": 35, // withdraw fee
                        "withdrawStatus": true, //withdraw status (false if ALL of networks' are false)
                        "depositTip": "Delisted, Deposit Suspended" //reason
                    },
                    "SKY": {
                        "minWithdrawAmount": "0.02000000",
                        "depositStatus": true,
                        "withdrawFee": 0.01,
                        "withdrawStatus": true
                    }
            }

        """
        return self._request_margin_api('get', 'asset/assetDetail', True, data=params)

    # Withdraw Endpoints

    def withdraw(self, **params):
        """Submit a withdraw request.

        https://binance-docs.github.io/apidocs/spot/en/#withdraw-sapi

        Assumptions:

        - You must have Withdraw permissions enabled on your API key
        - You must have withdrawn to the address specified through the website and approved the transaction via email

        :param coin: required
        :type coin: str
        :param withdrawOrderId: optional - client id for withdraw
        :type withdrawOrderId: str
        :param network: optional
        :type network: str
        :param address: optional
        :type address: str
        :type addressTag: optional - Secondary address identifier for coins like XRP,XMR etc.
        :param amount: required
        :type amount: decimal
        :param transactionFeeFlag: required - When making internal transfer, true for returning the fee to the destination account; false for returning the fee back to the departure account. Default false.
        :type transactionFeeFlag: bool
        :param name: optional - Description of the address, default asset value passed will be used
        :type name: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "id":"7213fea8e94b4a5593d507237e5a555b"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        # force a name for the withdrawal if one not set
        if 'coin' in params and 'name' not in params:
            params['name'] = params['coin']
        return self._request_margin_api('post', 'capital/withdraw/apply', True, data=params)

    def get_deposit_history(self, **params):
        """Fetch deposit history.

        https://binance-docs.github.io/apidocs/spot/en/#deposit-history-supporting-network-user_data

        :param coin: optional
        :type coin: str
        :type status: optional - 0(0:pending,1:success) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param offset: optional - default:0
        :type offset: long
        :param limit: optional
        :type limit: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "amount":"0.00999800",
                    "coin":"PAXG",
                    "network":"ETH",
                    "status":1,
                    "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
                    "addressTag":"",
                    "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
                    "insertTime":1599621997000,
                    "transferType":0,
                    "confirmTimes":"12/12"
                },
                {
                    "amount":"0.50000000",
                    "coin":"IOTA",
                    "network":"IOTA",
                    "status":1,
                    "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
                    "addressTag":"",
                    "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
                    "insertTime":1599620082000,
                    "transferType":0,
                    "confirmTimes":"1/1"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/deposit/hisrec', True, data=params)

    def get_withdraw_history(self, **params):
        """Fetch withdraw history.

        https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-supporting-network-user_data

        :param coin: optional
        :type coin: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param offset: optional - default:0
        :type offset: int
        :param limit: optional
        :type limit: int
        :param startTime: optional - Default: 90 days from current timestamp
        :type startTime: int
        :param endTime: optional - Default: present timestamp
        :type endTime: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "address": "0x94df8b352de7f46f64b01d3666bf6e936e44ce60",
                    "amount": "8.91000000",
                    "applyTime": "2019-10-12 11:12:02",
                    "coin": "USDT",
                    "id": "b6ae22b3aa844210a7041aee7589627c",
                    "withdrawOrderId": "WITHDRAWtest123", // will not be returned if there's no withdrawOrderId for this withdraw.
                    "network": "ETH",
                    "transferType": 0,   // 1 for internal transfer, 0 for external transfer
                    "status": 6,
                    "txId": "0xb5ef8c13b968a406cc62a93a8bd80f9e9a906ef1b3fcf20a2e48573c17659268"
                },
                {
                    "address": "1FZdVHtiBqMrWdjPyRPULCUceZPJ2WLCsB",
                    "amount": "0.00150000",
                    "applyTime": "2019-09-24 12:43:45",
                    "coin": "BTC",
                    "id": "156ec387f49b41df8724fa744fa82719",
                    "network": "BTC",
                    "status": 6,
                    "txId": "60fd9007ebfddc753455f95fafa808c4302c836e4d1eebc5a132c36c1d8ac354"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/withdraw/history', True, data=params)

    def get_withdraw_history_id(self, withdraw_id, **params):
        """Fetch withdraw history.

        https://binance-docs.github.io/apidocs/spot/en/#withdraw-history-supporting-network-user_data

        :param withdraw_id: required
        :type withdraw_id: str
        :param asset: optional
        :type asset: str
        :type status: 0(0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed) optional
        :type status: int
        :param startTime: optional
        :type startTime: long
        :param endTime: optional
        :type endTime: long
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "id":"7213fea8e94b4a5593d507237e5a555b",
                "withdrawOrderId": None,
                "amount": 0.99,
                "transactionFee": 0.01,
                "address": "0x6915f16f8791d0a1cc2bf47c13a6b2a92000504b",
                "asset": "ETH",
                "txId": "0xdf33b22bdb2b28b1f75ccd201a4a4m6e7g83jy5fc5d5a9d1340961598cfcb0a1",
                "applyTime": 1508198532000,
                "status": 4
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        result = self.get_withdraw_history(**params)

        for entry in result:
            if 'id' in entry and entry['id'] == withdraw_id:
                return entry

        raise Exception("There is no entry with withdraw id", result)

    def get_deposit_address(self, coin: str, network: Optional[str] = None, **params):
        """Fetch a deposit address for a symbol

        https://binance-docs.github.io/apidocs/spot/en/#deposit-address-supporting-network-user_data

        :param coin: required
        :type coin: str
        :param network: optional
        :type network: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "address": "1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv",
                "coin": "BTC",
                "tag": "",
                "url": "https://btc.com/1HPn8Rx2y6nNSfagQBKy27GB99Vbzg89wv"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['coin'] = coin
        if network:
            params['network'] = network
        return self._request_margin_api('get', 'capital/deposit/address', True, data=params)

    # User Stream Endpoints

    def stream_get_listen_key(self):
        """Start a new user data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the user stream alive.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self._post('userDataStream', False, data={}, version=self.PRIVATE_API_VERSION)
        return res['listenKey']

    def stream_keepalive(self, listenKey):
        """PING a user data stream to prevent a time out.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._put('userDataStream', False, data=params, version=self.PRIVATE_API_VERSION)

    def stream_close(self, listenKey):
        """Close out a user data stream.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-spot

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._delete('userDataStream', False, data=params, version=self.PRIVATE_API_VERSION)

    # Margin Trading Endpoints

    def get_margin_account(self, **params):
        """Query cross-margin account details

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-account-details-user_data

        :returns: API response

        .. code-block:: python

            {
                "borrowEnabled": true,
                "marginLevel": "11.64405625",
                "totalAssetOfBtc": "6.82728457",
                "totalLiabilityOfBtc": "0.58633215",
                "totalNetAssetOfBtc": "6.24095242",
                "tradeEnabled": true,
                "transferEnabled": true,
                "userAssets": [
                    {
                        "asset": "BTC",
                        "borrowed": "0.00000000",
                        "free": "0.00499500",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00499500"
                    },
                    {
                        "asset": "BNB",
                        "borrowed": "201.66666672",
                        "free": "2346.50000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "2144.83333328"
                    },
                    {
                        "asset": "ETH",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    },
                    {
                        "asset": "USDT",
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/account', True, data=params)

    def get_isolated_margin_account(self, **params):
        """Query isolated margin account details

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-account-info-user_data

        :param symbols: optional up to 5 margin pairs as a comma separated string
        :type asset: str

        .. code:: python

            account_info = client.get_isolated_margin_account()
            account_info = client.get_isolated_margin_account(symbols="BTCUSDT,ETHUSDT")

        :returns: API response

        .. code-block:: python

            If "symbols" is not sent:

                {
                "assets":[
                    {
                        "baseAsset":
                        {
                        "asset": "BTC",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "quoteAsset":
                        {
                        "asset": "USDT",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "symbol": "BTCUSDT"
                        "isolatedCreated": true,
                        "marginLevel": "0.00000000",
                        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
                        "marginRatio": "0.00000000",
                        "indexPrice": "10000.00000000"
                        "liquidatePrice": "1000.00000000",
                        "liquidateRate": "1.00000000"
                        "tradeEnabled": true
                    }
                    ],
                    "totalAssetOfBtc": "0.00000000",
                    "totalLiabilityOfBtc": "0.00000000",
                    "totalNetAssetOfBtc": "0.00000000"
                }

            If "symbols" is sent:

                {
                "assets":[
                    {
                        "baseAsset":
                        {
                        "asset": "BTC",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "quoteAsset":
                        {
                        "asset": "USDT",
                        "borrowEnabled": true,
                        "borrowed": "0.00000000",
                        "free": "0.00000000",
                        "interest": "0.00000000",
                        "locked": "0.00000000",
                        "netAsset": "0.00000000",
                        "netAssetOfBtc": "0.00000000",
                        "repayEnabled": true,
                        "totalAsset": "0.00000000"
                        },
                        "symbol": "BTCUSDT"
                        "isolatedCreated": true,
                        "marginLevel": "0.00000000",
                        "marginLevelStatus": "EXCESSIVE", // "EXCESSIVE", "NORMAL", "MARGIN_CALL", "PRE_LIQUIDATION", "FORCE_LIQUIDATION"
                        "marginRatio": "0.00000000",
                        "indexPrice": "10000.00000000"
                        "liquidatePrice": "1000.00000000",
                        "liquidateRate": "1.00000000"
                        "tradeEnabled": true
                    }
                    ]
                }

        """
        return self._request_margin_api('get', 'margin/isolated/account', True, data=params)

    def enable_isolated_margin_account(self, **params):
        """Enable isolated margin account for a specific symbol.

        https://binance-docs.github.io/apidocs/spot/en/#enable-isolated-margin-account-trade

        :param symbol:
        :type asset: str

        :returns: API response

        .. code-block:: python

            {
              "success": true,
              "symbol": "BTCUSDT"
            }


        """
        return self._request_margin_api('post', 'margin/isolated/account', True, data=params)

    def disable_isolated_margin_account(self, **params):
        """Disable isolated margin account for a specific symbol. Each trading pair can only
        be deactivated once every 24 hours.

        https://binance-docs.github.io/apidocs/spot/en/#disable-isolated-margin-account-trade

        :param symbol:
        :type asset: str

        :returns: API response

        .. code-block:: python

            {
              "success": true,
              "symbol": "BTCUSDT"
            }


        """
        return self._request_margin_api('delete', 'margin/isolated/account', True, data=params)

    def get_margin_asset(self, **params):
        """Query cross-margin asset

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-asset-market_data

        :param asset: name of the asset
        :type asset: str

        .. code-block:: python

            asset_details = client.get_margin_asset(asset='BNB')

        :returns: API response

        .. code-block:: python

            {
                "assetFullName": "Binance Coin",
                "assetName": "BNB",
                "isBorrowable": false,
                "isMortgageable": true,
                "userMinBorrow": "0.00000000",
                "userMinRepay": "0.00000000"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/asset', data=params)

    def get_margin_symbol(self, **params):
        """Query cross-margin symbol info

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-pair-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "id":323355778339572400,
                "symbol":"BTCUSDT",
                "base":"BTC",
                "quote":"USDT",
                "isMarginTrade":true,
                "isBuyAllowed":true,
                "isSellAllowed":true
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/pair', data=params)

    def get_margin_all_assets(self, **params):
        """Get All Margin Assets (MARKET_DATA)

        https://binance-docs.github.io/apidocs/spot/en/#get-all-margin-assets-market_data

        .. code:: python

            margin_assets = client.get_margin_all_assets()

        :returns: API response

        .. code-block:: python

            [
                {
                    "assetFullName": "USD coin",
                    "assetName": "USDC",
                    "isBorrowable": true,
                    "isMortgageable": true,
                    "userMinBorrow": "0.00000000",
                    "userMinRepay": "0.00000000"
                },
                {
                    "assetFullName": "BNB-coin",
                    "assetName": "BNB",
                    "isBorrowable": true,
                    "isMortgageable": true,
                    "userMinBorrow": "1.00000000",
                    "userMinRepay": "0.00000000"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/allAssets', data=params)

    def get_margin_all_pairs(self, **params):
        """Get All Cross Margin Pairs (MARKET_DATA)

        https://binance-docs.github.io/apidocs/spot/en/#get-all-cross-margin-pairs-market_data

        .. code:: python

            margin_pairs = client.get_margin_all_pairs()

        :returns: API response

        .. code-block:: python

            [
                {
                    "base": "BNB",
                    "id": 351637150141315861,
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "BNBBTC"
                },
                {
                    "base": "TRX",
                    "id": 351637923235429141,
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "TRXBTC"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/allPairs', data=params)

    def create_isolated_margin_account(self, **params):
        """Create isolated margin account for symbol

        https://binance-docs.github.io/apidocs/spot/en/#create-isolated-margin-account-margin

        :param base: Base asset of symbol
        :type base: str
        :param quote: Quote asset of symbol
        :type quote: str

        .. code:: python

            pair_details = client.create_isolated_margin_account(base='USDT', quote='BTC')

        :returns: API response

        .. code-block:: python

            {
                "success": true,
                "symbol": "BTCUSDT"
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/isolated/create', signed=True, data=params)

    def get_isolated_margin_symbol(self, **params):
        """Query isolated margin symbol info

        https://binance-docs.github.io/apidocs/spot/en/#query-isolated-margin-symbol-user_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            pair_details = client.get_isolated_margin_symbol(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
            "symbol":"BTCUSDT",
            "base":"BTC",
            "quote":"USDT",
            "isMarginTrade":true,
            "isBuyAllowed":true,
            "isSellAllowed":true
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/isolated/pair', signed=True, data=params)

    def get_all_isolated_margin_symbols(self, **params):
        """Query isolated margin symbol info for all pairs

        https://binance-docs.github.io/apidocs/spot/en/#get-all-isolated-margin-symbol-user_data

        .. code:: python

            pair_details = client.get_all_isolated_margin_symbols()

        :returns: API response

        .. code-block:: python

            [
                {
                    "base": "BNB",
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "BNBBTC"
                },
                {
                    "base": "TRX",
                    "isBuyAllowed": true,
                    "isMarginTrade": true,
                    "isSellAllowed": true,
                    "quote": "BTC",
                    "symbol": "TRXBTC"
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/isolated/allPairs', signed=True, data=params)

    def toggle_bnb_burn_spot_margin(self, **params):
        """Toggle BNB Burn On Spot Trade And Margin Interest

        https://binance-docs.github.io/apidocs/spot/en/#toggle-bnb-burn-on-spot-trade-and-margin-interest-user_data

        :param spotBNBBurn: Determines whether to use BNB to pay for trading fees on SPOT
        :type spotBNBBurn: bool
        :param interestBNBBurn: Determines whether to use BNB to pay for margin loan's interest
        :type interestBNBBurn: bool

        .. code:: python

            response = client.toggle_bnb_burn_spot_margin()

        :returns: API response

        .. code-block:: python

            {
               "spotBNBBurn":true,
               "interestBNBBurn": false
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'bnbBurn', signed=True, data=params)

    def get_bnb_burn_spot_margin(self, **params):
        """Get BNB Burn Status

        https://binance-docs.github.io/apidocs/spot/en/#get-bnb-burn-status-user_data

        .. code:: python

            status = client.get_bnb_burn_spot_margin()

        :returns: API response

        .. code-block:: python

            {
               "spotBNBBurn":true,
               "interestBNBBurn": false
            }


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'bnbBurn', signed=True, data=params)

    def get_margin_price_index(self, **params):
        """Query margin priceIndex

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-priceindex-market_data

        :param symbol: name of the symbol pair
        :type symbol: str

        .. code:: python

            price_index_details = client.get_margin_price_index(symbol='BTCUSDT')

        :returns: API response

        .. code-block:: python

            {
                "calcTime": 1562046418000,
                "price": "0.00333930",
                "symbol": "BNBBTC"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/priceIndex', data=params)

    def transfer_margin_to_spot(self, **params):
        """Execute transfer between cross-margin account and spot account.

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_margin_to_spot(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['type'] = 2
        return self._request_margin_api('post', 'margin/transfer', signed=True, data=params)

    def transfer_spot_to_margin(self, **params):
        """Execute transfer between spot account and cross-margin account.

        https://binance-docs.github.io/apidocs/spot/en/#cross-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_spot_to_margin(asset='BTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['type'] = 1
        return self._request_margin_api('post', 'margin/transfer', signed=True, data=params)

    def transfer_isolated_margin_to_spot(self, **params):
        """Execute transfer between isolated margin account and spot account.

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair symbol
        :type symbol: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_isolated_margin_to_spot(asset='BTC',
                                                                symbol='ETHBTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['transFrom'] = "ISOLATED_MARGIN"
        params['transTo'] = "SPOT"
        return self._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)

    def transfer_spot_to_isolated_margin(self, **params):
        """Execute transfer between spot account and isolated margin account.

        https://binance-docs.github.io/apidocs/spot/en/#isolated-margin-account-transfer-margin

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair symbol
        :type symbol: str
        :param amount: amount to transfer
        :type amount: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_spot_to_isolated_margin(asset='BTC',
                                                                symbol='ETHBTC', amount='1.1')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params['transFrom'] = "SPOT"
        params['transTo'] = "ISOLATED_MARGIN"
        return self._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)

    def get_isolated_margin_tranfer_history(self, **params):
        """Get transfers to isolated margin account.

        https://binance-docs.github.io/apidocs/spot/en/#get-isolated-margin-transfer-history-user_data

        :param asset: name of the asset
        :type asset: str
        :param symbol: pair required
        :type symbol: str
        :param transFrom: optional SPOT, ISOLATED_MARGIN
        :param transFrom: str SPOT, ISOLATED_MARGIN
        :param transTo: optional
        :param transTo: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transfer = client.transfer_spot_to_isolated_margin(symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
              "rows": [
                {
                  "amount": "0.10000000",
                  "asset": "BNB",
                  "status": "CONFIRMED",
                  "timestamp": 1566898617000,
                  "txId": 5240372201,
                  "transFrom": "SPOT",
                  "transTo": "ISOLATED_MARGIN"
                },
                {
                  "amount": "5.00000000",
                  "asset": "USDT",
                  "status": "CONFIRMED",
                  "timestamp": 1566888436123,
                  "txId": 5239810406,
                  "transFrom": "ISOLATED_MARGIN",
                  "transTo": "SPOT"
                }
              ],
              "total": 2
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/isolated/transfer', signed=True, data=params)

    def create_margin_loan(self, **params):
        """Apply for a loan in cross-margin or isolated-margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-borrow-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param symbol: Isolated margin symbol (default blank for cross-margin)
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transaction = client.margin_create_loan(asset='BTC', amount='1.1')

            transaction = client.margin_create_loan(asset='BTC', amount='1.1',
                                                    isIsolated='TRUE', symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/loan', signed=True, data=params)

    def repay_margin_loan(self, **params):
        """Repay loan in cross-margin or isolated-margin account.

        If amount is more than the amount borrowed, the full loan will be repaid.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-repay-margin

        :param asset: name of the asset
        :type asset: str
        :param amount: amount to transfer
        :type amount: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param symbol: Isolated margin symbol (default blank for cross-margin)
        :type symbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        .. code-block:: python

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1')

            transaction = client.margin_repay_loan(asset='BTC', amount='1.1',
                                                    isIsolated='TRUE', symbol='ETHBTC')

        :returns: API response

        .. code-block:: python

            {
                "tranId": 100000001
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/repay', signed=True, data=params)

    def create_margin_order(self, **params):
        """Post a new order for margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-order-trade

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param side: required
        :type side: str
        :param type: required
        :type type: str
        :param quantity: required
        :type quantity: decimal
        :param price: required
        :type price: str
        :param stopPrice: Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
        :type stopPrice: str
        :param timeInForce: required if limit order GTC,IOC,FOK
        :type timeInForce: str
        :param newClientOrderId: A unique id for the order. Automatically generated if not sent.
        :type newClientOrderId: str
        :param icebergQty: Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
        :type icebergQty: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to
            FULL, all other orders default to ACK.
        :type newOrderRespType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        Response ACK:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595
            }

        Response RESULT:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL"
            }

        Response FULL:

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "orderId": 28,
                "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "10.00000000",
                "cummulativeQuoteQty": "10.00000000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "SELL",
                "fills": [
                    {
                        "price": "4000.00000000",
                        "qty": "1.00000000",
                        "commission": "4.00000000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3999.00000000",
                        "qty": "5.00000000",
                        "commission": "19.99500000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3998.00000000",
                        "qty": "2.00000000",
                        "commission": "7.99600000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3997.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99700000",
                        "commissionAsset": "USDT"
                    },
                    {
                        "price": "3995.00000000",
                        "qty": "1.00000000",
                        "commission": "3.99500000",
                        "commissionAsset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException

        """
        return self._request_margin_api('post', 'margin/order', signed=True, data=params)

    def cancel_margin_order(self, **params):
        """Cancel an active order for margin account.

        Either orderId or origClientOrderId must be sent.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-order-trade

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "symbol": "LTCBTC",
                "orderId": 28,
                "origClientOrderId": "myOrder1",
                "clientOrderId": "cancelMyOrder1",
                "transactTime": 1507725176595,
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "8.00000000",
                "cummulativeQuoteQty": "8.00000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "SELL"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('delete', 'margin/order', signed=True, data=params)

    def set_margin_max_leverage(self, **params):
        """Adjust cross margin max leverage

        https://binance-docs.github.io/apidocs/spot/en/#adjust-cross-margin-max-leverage-user_data

        :param maxLeverage: required Can only adjust 3 or 5，Example: maxLeverage=3
        :type maxLeverage: int

        :returns: API response

            {
                "success": true
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'margin/max-leverage', signed=True, data=params)

    def get_margin_transfer_history(self, **params):
        """Query margin transfer history

        https://binance-docs.github.io/apidocs/spot/en/#get-cross-margin-transfer-history-user_data

        :param asset: optional
        :type asset: str
        :param type: optional Transfer Type: ROLL_IN, ROLL_OUT
        :type type: str
        :param archived: optional Default: false. Set to true for archived data from 6 months ago
        :type archived: str
        :param startTime: earliest timestamp to filter transactions
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "amount": "0.10000000",
                        "asset": "BNB",
                        "status": "CONFIRMED",
                        "timestamp": 1566898617,
                        "txId": 5240372201,
                        "type": "ROLL_IN"
                    },
                    {
                        "amount": "5.00000000",
                        "asset": "USDT",
                        "status": "CONFIRMED",
                        "timestamp": 1566888436,
                        "txId": 5239810406,
                        "type": "ROLL_OUT"
                    },
                    {
                        "amount": "1.00000000",
                        "asset": "EOS",
                        "status": "CONFIRMED",
                        "timestamp": 1566888403,
                        "txId": 5239808703,
                        "type": "ROLL_IN"
                    }
                ],
                "total": 3
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/transfer', signed=True, data=params)

    def get_margin_loan_details(self, **params):
        """Query loan record

        txId or startTime must be sent. txId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#query-loan-record-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime: earliest timestamp to filter transactions
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "asset": "BNB",
                        "principal": "0.84624403",
                        "timestamp": 1555056425000,
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED"
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/loan', signed=True, data=params)

    def get_margin_repay_details(self, **params):
        """Query repay record

        txId or startTime must be sent. txId takes precedence.

        https://binance-docs.github.io/apidocs/spot/en/#query-repay-record-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param txId: the tranId in of the created loan
        :type txId: str
        :param startTime:
        :type startTime: str
        :param endTime: Used to uniquely identify this cancel. Automatically generated by default.
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        //Total amount repaid
                        "amount": "14.00000000",
                        "asset": "BNB",
                        //Interest repaid
                        "interest": "0.01866667",
                        //Principal repaid
                        "principal": "13.98133333",
                        //one of PENDING (pending to execution), CONFIRMED (successfully loaned), FAILED (execution failed, nothing happened to your account);
                        "status": "CONFIRMED",
                        "timestamp": 1563438204000,
                        "txId": 2970933056
                    }
                ],
                "total": 1
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/repay', signed=True, data=params)

    def get_cross_margin_data(self, **params):
        """Query Cross Margin Fee Data (USER_DATA)

        https://binance-docs.github.io/apidocs/spot/en/#query-cross-margin-fee-data-user_data
        :param vipLevel: User's current specific margin data will be returned if vipLevel is omitted
        :type vipLevel: int
        :param coin
        :type coin: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int
        :returns: API response (example):
            [
                {
                    "vipLevel": 0,
                    "coin": "BTC",
                    "transferIn": true,
                    "borrowable": true,
                    "dailyInterest": "0.00026125",
                    "yearlyInterest": "0.0953",
                    "borrowLimit": "180",
                    "marginablePairs": [
                        "BNBBTC",
                        "TRXBTC",
                        "ETHBTC",
                        "BTCUSDT"
                    ]
                }
            ]
        """
        return self._request_margin_api('get', 'margin/crossMarginData', signed=True, data=params)

    def get_margin_interest_history(self, **params):
        """Get Interest History (USER_DATA)

        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data

        :param asset:
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param startTime:
        :type startTime: str
        :param endTime:
        :type endTime: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param archived: Default: false. Set to true for archived data from 6 months ago
        :type archived: bool
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows":[
                    {
                        "isolatedSymbol": "BNBUSDT", // isolated symbol, will not be returned for crossed margin
                        "asset": "BNB",
                        "interest": "0.02414667",
                        "interestAccuredTime": 1566813600000,
                        "interestRate": "0.01600000",
                        "principal": "36.22000000",
                        "type": "ON_BORROW"
                    }
                ],
                "total": 1
            }


        """
        return self._request_margin_api('get', 'margin/interestHistory', signed=True, data=params)

    def get_margin_force_liquidation_rec(self, **params):
        """Get Force Liquidation Record (USER_DATA)

        https://binance-docs.github.io/apidocs/spot/en/#get-force-liquidation-record-user_data

        :param startTime:
        :type startTime: str
        :param endTime:
        :type endTime: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param current: Currently querying page. Start from 1. Default:1
        :type current: str
        :param size: Default:10 Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "rows": [
                    {
                        "avgPrice": "0.00388359",
                        "executedQty": "31.39000000",
                        "orderId": 180015097,
                        "price": "0.00388110",
                        "qty": "31.39000000",
                        "side": "SELL",
                        "symbol": "BNBBTC",
                        "timeInForce": "GTC",
                        "isIsolated": true,
                        "updatedTime": 1558941374745
                    }
                ],
                "total": 1
            }

        """
        return self._request_margin_api('get', 'margin/forceLiquidationRec', signed=True, data=params)

    def get_margin_order(self, **params):
        """Query margin accounts order

        Either orderId or origClientOrderId must be sent.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-order-user_data

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId:
        :type orderId: str
        :param origClientOrderId:
        :type origClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "clientOrderId": "ZwfQzuDIGpceVhKW5DvCmO",
                "cummulativeQuoteQty": "0.00000000",
                "executedQty": "0.00000000",
                "icebergQty": "0.00000000",
                "isWorking": true,
                "orderId": 213205622,
                "origQty": "0.30000000",
                "price": "0.00493630",
                "side": "SELL",
                "status": "NEW",
                "stopPrice": "0.00000000",
                "symbol": "BNBBTC",
                "time": 1562133008725,
                "timeInForce": "GTC",
                "type": "LIMIT",
                "updateTime": 1562133008725
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/order', signed=True, data=params)

    def get_open_margin_orders(self, **params):
        """Query margin accounts open orders

        If the symbol is not sent, orders for all symbols will be returned in an array (cross-margin only).

        If querying isolated margin orders, both the isIsolated='TRUE' and symbol=symbol_name must be set.

        When all symbols are returned, the number of requests counted against the rate limiter is equal to the number
        of symbols currently trading on the exchange.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-order-user_data

        :param symbol: optional
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "clientOrderId": "qhcZw71gAkCCTv0t0k8LUK",
                    "cummulativeQuoteQty": "0.00000000",
                    "executedQty": "0.00000000",
                    "icebergQty": "0.00000000",
                    "isWorking": true,
                    "orderId": 211842552,
                    "origQty": "0.30000000",
                    "price": "0.00475010",
                    "side": "SELL",
                    "status": "NEW",
                    "stopPrice": "0.00000000",
                    "symbol": "BNBBTC",
                    "time": 1562040170089,
                    "timeInForce": "GTC",
                    "type": "LIMIT",
                    "updateTime": 1562040170089
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/openOrders', signed=True, data=params)

    def get_all_margin_orders(self, **params):
        """Query all margin accounts orders

        If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.

        For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-all-order-user_data

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param orderId: optional
        :type orderId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "id": 43123876,
                    "price": "0.00395740",
                    "qty": "4.06000000",
                    "quoteQty": "0.01606704",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43123877,
                    "price": "0.00395740",
                    "qty": "0.77000000",
                    "quoteQty": "0.00304719",
                    "symbol": "BNBBTC",
                    "time": 1556089977693
                },
                {
                    "id": 43253549,
                    "price": "0.00428930",
                    "qty": "23.30000000",
                    "quoteQty": "0.09994069",
                    "symbol": "BNBBTC",
                    "time": 1556163963504
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/allOrders', signed=True, data=params)

    def get_margin_trades(self, **params):
        """Query margin accounts trades

        If fromId is set, it will get orders >= that fromId. Otherwise most recent orders are returned.

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-trade-list-user_data

        :param symbol: required
        :type symbol: str
        :param isIsolated: set to 'TRUE' for isolated margin (default 'FALSE')
        :type isIsolated: str
        :param fromId: optional
        :type fromId: str
        :param startTime: optional
        :type startTime: str
        :param endTime: optional
        :type endTime: str
        :param limit: Default 500; max 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "commission": "0.00006000",
                    "commissionAsset": "BTC",
                    "id": 34,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": false,
                    "orderId": 39324,
                    "price": "0.02000000",
                    "qty": "3.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561973357171
                }, {
                    "commission": "0.00002950",
                    "commissionAsset": "BTC",
                    "id": 32,
                    "isBestMatch": true,
                    "isBuyer": false,
                    "isMaker": true,
                    "orderId": 39319,
                    "price": "0.00590000",
                    "qty": "5.00000000",
                    "symbol": "BNBBTC",
                    "time": 1561964645345
                }
            ]


        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/myTrades', signed=True, data=params)

    def get_max_margin_loan(self, **params):
        """Query max borrow amount for an asset

        https://binance-docs.github.io/apidocs/spot/en/#query-max-borrow-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "1.69248805"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/maxBorrowable', signed=True, data=params)

    def get_max_margin_transfer(self, **params):
        """Query max transfer-out amount

        https://binance-docs.github.io/apidocs/spot/en/#query-max-transfer-out-amount-user_data

        :param asset: required
        :type asset: str
        :param isolatedSymbol: isolated symbol (if querying isolated margin)
        :type isolatedSymbol: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "amount": "3.59498107"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'margin/maxTransferable', signed=True, data=params)

    # Margin OCO

    def create_margin_oco_order(self, **params):
        """Post a new OCO trade for margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-new-oco-trade


        :param symbol: required
        :type symbol: str
        :param isIsolated: for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
        :type symbol: str
        :param listClientOrderId: A unique id for the list order. Automatically generated if not sent.
        :type listClientOrderId: str
        :param side: required
        :type side: str
        :param quantity: required
        :type quantity: decimal
        :param limitClientOrderId: A unique id for the limit order. Automatically generated if not sent.
        :type limitClientOrderId: str
        :param price: required
        :type price: str
        :param limitIcebergQty: Used to make the LIMIT_MAKER leg an iceberg order.
        :type limitIcebergQty: decimal
        :param stopClientOrderId: A unique Id for the stop loss/stop loss limit leg. Automatically generated if not sent.
        :type stopClientOrderId: str
        :param stopPrice: required
        :type stopPrice: str
        :param stopLimitPrice: If provided, stopLimitTimeInForce is required.
        :type stopLimitPrice: str
        :param stopIcebergQty: Used with STOP_LOSS_LIMIT leg to make an iceberg order.
        :type stopIcebergQty: decimal
        :param stopLimitTimeInForce: Valid values are GTC/FOK/IOC.
        :type stopLimitTimeInForce: str
        :param newOrderRespType: Set the response JSON. ACK, RESULT, or FULL; default: RESULT.
        :type newOrderRespType: str
        :param sideEffectType: NO_SIDE_EFFECT, MARGIN_BUY, AUTO_REPAY; default NO_SIDE_EFFECT.
        :type sideEffectType: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "orderListId": 0,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
                "transactionTime": 1563417480525,
                "symbol": "LTCBTC",
                "marginBuyBorrowAmount": "5",       // will not return if no margin trade happens
                "marginBuyBorrowAsset": "BTC",    // will not return if no margin trade happens
                "isIsolated": false,       // if isolated margin
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 2,
                        "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 3,
                        "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
                    }
                ],
                "orderReports": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 2,
                        "orderListId": 0,
                        "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
                        "transactTime": 1563417480525,
                        "price": "0.000000",
                        "origQty": "0.624363",
                        "executedQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS",
                        "side": "BUY",
                        "stopPrice": "0.960664"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 3,
                        "orderListId": 0,
                        "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
                        "transactTime": 1563417480525,
                        "price": "0.036435",
                        "origQty": "0.624363",
                        "executedQty": "0.000000",
                        "cummulativeQuoteQty": "0.000000",
                        "status": "NEW",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "BUY"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException, BinanceOrderException, BinanceOrderMinAmountException,
            BinanceOrderMinPriceException, BinanceOrderMinTotalException, BinanceOrderUnknownSymbolException,
            BinanceOrderInactiveSymbolException

        """
        return self._request_margin_api('post', 'margin/order/oco', signed=True, data=params)

    def cancel_margin_oco_order(self, **params):
        """Cancel an entire Order List for a margin account.

        https://binance-docs.github.io/apidocs/spot/en/#margin-account-cancel-oco-trade

        :param symbol: required
        :type symbol: str
        :param isIsolated: for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
        :type symbol: str
        :param orderListId: Either orderListId or listClientOrderId must be provided
        :type orderListId: int
        :param listClientOrderId: Either orderListId or listClientOrderId must be provided
        :type listClientOrderId: str
        :param newClientOrderId: Used to uniquely identify this cancel. Automatically generated by default.
        :type newClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "orderListId": 0,
                "contingencyType": "OCO",
                "listStatusType": "ALL_DONE",
                "listOrderStatus": "ALL_DONE",
                "listClientOrderId": "C3wyj4WVEktd7u9aVBRXcN",
                "transactionTime": 1574040868128,
                "symbol": "LTCBTC",
                "isIsolated": false,       // if isolated margin
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 2,
                        "clientOrderId": "pO9ufTiFGg3nw2fOdgeOXa"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 3,
                        "clientOrderId": "TXOvglzXuaubXAaENpaRCB"
                    }
                ],
                "orderReports": [
                    {
                        "symbol": "LTCBTC",
                        "origClientOrderId": "pO9ufTiFGg3nw2fOdgeOXa",
                        "orderId": 2,
                        "orderListId": 0,
                        "clientOrderId": "unfWT8ig8i0uj6lPuYLez6",
                        "price": "1.00000000",
                        "origQty": "10.00000000",
                        "executedQty": "0.00000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "CANCELED",
                        "timeInForce": "GTC",
                        "type": "STOP_LOSS_LIMIT",
                        "side": "SELL",
                        "stopPrice": "1.00000000"
                    },
                    {
                        "symbol": "LTCBTC",
                        "origClientOrderId": "TXOvglzXuaubXAaENpaRCB",
                        "orderId": 3,
                        "orderListId": 0,
                        "clientOrderId": "unfWT8ig8i0uj6lPuYLez6",
                        "price": "3.00000000",
                        "origQty": "10.00000000",
                        "executedQty": "0.00000000",
                        "cummulativeQuoteQty": "0.00000000",
                        "status": "CANCELED",
                        "timeInForce": "GTC",
                        "type": "LIMIT_MAKER",
                        "side": "SELL"
                    }
                ]
            }

    """
        return self._request_margin_api('delete', 'margin/orderList', signed=True, data=params)

    def get_margin_oco_order(self, **params):
        """Retrieves a specific OCO based on provided optional parameters

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-oco-user_data

        :param isIsolated: for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
        :type symbol: str
        :param symbol: mandatory for isolated margin, not supported for cross margin
        :type symbol: str
        :param orderListId: Either orderListId or listClientOrderId must be provided
        :type orderListId: int
        :param listClientOrderId: Either orderListId or listClientOrderId must be provided
        :type listClientOrderId: str
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            {
                "orderListId": 27,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "h2USkA5YQpaXHPIrkd96xE",
                "transactionTime": 1565245656253,
                "symbol": "LTCBTC",
                "isIsolated": false,       // if isolated margin
                "orders": [
                    {
                        "symbol": "LTCBTC",
                        "orderId": 4,
                        "clientOrderId": "qD1gy3kc3Gx0rihm9Y3xwS"
                    },
                    {
                        "symbol": "LTCBTC",
                        "orderId": 5,
                        "clientOrderId": "ARzZ9I00CPM8i3NhmU9Ega"
                    }
                ]
            }

    """
        return self._request_margin_api('get', 'margin/orderList', signed=True, data=params)

    def get_open_margin_oco_orders(self, **params):
        """Retrieves open OCO trades

        https://binance-docs.github.io/apidocs/spot/en/#query-margin-account-39-s-open-oco-user_data

        :param isIsolated: for isolated margin or not, "TRUE", "FALSE"，default "FALSE"
        :type symbol: str
        :param symbol: mandatory for isolated margin, not supported for cross margin
        :type symbol: str
        :param fromId: If supplied, neither startTime or endTime can be provided
        :type fromId: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional Default Value: 500; Max Value: 1000
        :type limit: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

            [
                {
                    "orderListId": 29,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "amEEAXryFzFwYF1FeRpUoZ",
                    "transactionTime": 1565245913483,
                    "symbol": "LTCBTC",
                    "isIsolated": true,       // if isolated margin
                    "orders": [
                        {
                            "symbol": "LTCBTC",
                            "orderId": 4,
                            "clientOrderId": "oD7aesZqjEGlZrbtRpy5zB"
                        },
                        {
                            "symbol": "LTCBTC",
                            "orderId": 5,
                            "clientOrderId": "Jr1h6xirOxgeJOUuYQS7V3"
                        }
                    ]
                },
                {
                    "orderListId": 28,
                    "contingencyType": "OCO",
                    "listStatusType": "EXEC_STARTED",
                    "listOrderStatus": "EXECUTING",
                    "listClientOrderId": "hG7hFNxJV6cZy3Ze4AUT4d",
                    "transactionTime": 1565245913407,
                    "symbol": "LTCBTC",
                    "orders": [
                        {
                            "symbol": "LTCBTC",
                            "orderId": 2,
                            "clientOrderId": "j6lFOfbmFMRjTYA7rRJ0LP"
                        },
                        {
                            "symbol": "LTCBTC",
                            "orderId": 3,
                            "clientOrderId": "z0KCjOdditiLS5ekAFtK81"
                        }
                    ]
                }
            ]

    """
        return self._request_margin_api('get', 'margin/allOrderList', signed=True, data=params)

    # Cross-margin

    def margin_stream_get_listen_key(self):
        """Start a new cross-margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the stream alive.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :returns: API response

        .. code-block:: python

            {
                "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        res = self._request_margin_api('post', 'userDataStream', signed=False, data={})
        return res['listenKey']

    def margin_stream_keepalive(self, listenKey):
        """PING a cross-margin data stream to prevent a time out.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._request_margin_api('put', 'userDataStream', signed=False, data=params)

    def margin_stream_close(self, listenKey):
        """Close out a cross-margin data stream.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-margin

        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'listenKey': listenKey
        }
        return self._request_margin_api('delete', 'userDataStream', signed=False, data=params)

    # Isolated margin

    def isolated_margin_stream_get_listen_key(self, symbol):
        """Start a new isolated margin data stream and return the listen key
        If a stream already exists it should return the same key.
        If the stream becomes invalid a new key is returned.

        Can be used to keep the stream alive.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "listenKey":  "T3ee22BIYuWqmvne0HNq2A2WsFlEtLhvWCtItw6ffhhdmjifQ2tRbuKkTHhr"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'symbol': symbol
        }
        res = self._request_margin_api('post', 'userDataStream/isolated', signed=False, data=params)
        return res['listenKey']

    def isolated_margin_stream_keepalive(self, symbol, listenKey):
        """PING an isolated margin data stream to prevent a time out.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'listenKey': listenKey
        }
        return self._request_margin_api('put', 'userDataStream/isolated', signed=False, data=params)

    def isolated_margin_stream_close(self, symbol, listenKey):
        """Close out an isolated margin data stream.

        https://binance-docs.github.io/apidocs/spot/en/#listen-key-isolated-margin

        :param symbol: required - symbol for the isolated margin account
        :type symbol: str
        :param listenKey: required
        :type listenKey: str

        :returns: API response

        .. code-block:: python

            {}

        :raises: BinanceRequestException, BinanceAPIException

        """
        params = {
            'symbol': symbol,
            'listenKey': listenKey
        }
        return self._request_margin_api('delete', 'userDataStream/isolated', signed=False, data=params)

    # Lending Endpoints

    def get_lending_product_list(self, **params):
        """Get Lending Product List

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-list-user_data

        """
        return self._request_margin_api('get', 'lending/daily/product/list', signed=True, data=params)

    def get_lending_daily_quota_left(self, **params):
        """Get Left Daily Purchase Quota of Flexible Product.

        https://binance-docs.github.io/apidocs/spot/en/#get-left-daily-purchase-quota-of-flexible-product-user_data

        """
        return self._request_margin_api('get', 'lending/daily/userLeftQuota', signed=True, data=params)

    def purchase_lending_product(self, **params):
        """Purchase Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#purchase-flexible-product-user_data

        """
        return self._request_margin_api('post', 'lending/daily/purchase', signed=True, data=params)

    def get_lending_daily_redemption_quota(self, **params):
        """Get Left Daily Redemption Quota of Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#get-left-daily-redemption-quota-of-flexible-product-user_data

        """
        return self._request_margin_api('get', 'lending/daily/userRedemptionQuota', signed=True, data=params)

    def redeem_lending_product(self, **params):
        """Redeem Flexible Product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-flexible-product-user_data

        """
        return self._request_margin_api('post', 'lending/daily/redeem', signed=True, data=params)

    def get_lending_position(self, **params):
        """Get Flexible Product Position

        https://binance-docs.github.io/apidocs/spot/en/#get-flexible-product-position-user_data

        """
        return self._request_margin_api('get', 'lending/daily/token/position', signed=True, data=params)

    def get_fixed_activity_project_list(self, **params):
        """Get Fixed and Activity Project List

        https://binance-docs.github.io/apidocs/spot/en/#get-fixed-and-activity-project-list-user_data

        :param asset: optional
        :type asset: str
        :param type: required - "ACTIVITY", "CUSTOMIZED_FIXED"
        :type type: str
        :param status: optional - "ALL", "SUBSCRIBABLE", "UNSUBSCRIBABLE"; default "ALL"
        :type status: str
        :param sortBy: optional - "START_TIME", "LOT_SIZE", "INTEREST_RATE", "DURATION"; default "START_TIME"
        :type sortBy: str
        :param current: optional - Currently querying page. Start from 1. Default:1
        :type current: int
        :param size: optional - Default:10, Max:100
        :type size: int
        :param recvWindow: the number of milliseconds the request is valid for
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "asset": "USDT",
                    "displayPriority": 1,
                    "duration": 90,
                    "interestPerLot": "1.35810000",
                    "interestRate": "0.05510000",
                    "lotSize": "100.00000000",
                    "lotsLowLimit": 1,
                    "lotsPurchased": 74155,
                    "lotsUpLimit": 80000,
                    "maxLotsPerUser": 2000,
                    "needKyc": False,
                    "projectId": "CUSDT90DAYSS001",
                    "projectName": "USDT",
                    "status": "PURCHASING",
                    "type": "CUSTOMIZED_FIXED",
                    "withAreaLimitation": False
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'lending/project/list', signed=True, data=params)

    def get_lending_account(self, **params):
        """Get Lending Account Details

        https://binance-docs.github.io/apidocs/spot/en/#lending-account-user_data

        """
        return self._request_margin_api('get', 'lending/union/account', signed=True, data=params)

    def get_lending_purchase_history(self, **params):
        """Get Lending Purchase History

        https://binance-docs.github.io/apidocs/spot/en/#get-purchase-record-user_data

        """
        return self._request_margin_api('get', 'lending/union/purchaseRecord', signed=True, data=params)

    def get_lending_redemption_history(self, **params):
        """Get Lending Redemption History

        https://binance-docs.github.io/apidocs/spot/en/#get-redemption-record-user_data

        """
        return self._request_margin_api('get', 'lending/union/redemptionRecord', signed=True, data=params)

    def get_lending_interest_history(self, **params):
        """Get Lending Interest History

        https://binance-docs.github.io/apidocs/spot/en/#get-interest-history-user_data-2

        """
        return self._request_margin_api('get', 'lending/union/interestHistory', signed=True, data=params)

    def change_fixed_activity_to_daily_position(self, **params):
        """Change Fixed/Activity Position to Daily Position

        https://binance-docs.github.io/apidocs/spot/en/#change-fixed-activity-position-to-daily-position-user_data

        """
        return self._request_margin_api('post', 'lending/positionChanged', signed=True, data=params)

    # Staking Endpoints

    def get_staking_product_list(self, **params):
        """Get Staking Product List

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-product-list-user_data

        """
        return self._request_margin_api('get', 'staking/productList', signed=True, data=params)

    def purchase_staking_product(self, **params):
        """Purchase Staking Product

        https://binance-docs.github.io/apidocs/spot/en/#purchase-staking-product-user_data

        """
        return self._request_margin_api('post', 'staking/purchase', signed=True, data=params)

    def redeem_staking_product(self, **params):
        """Redeem Staking Product

        https://binance-docs.github.io/apidocs/spot/en/#redeem-staking-product-user_data

        """
        return self._request_margin_api('post', 'staking/redeem', signed=True, data=params)

    def get_staking_position(self, **params):
        """Get Staking Product Position

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-product-position-user_data

        """
        return self._request_margin_api('get', 'staking/position', signed=True, data=params)

    def get_staking_purchase_history(self, **params):
        """Get Staking Purchase History

        https://binance-docs.github.io/apidocs/spot/en/#get-staking-history-user_data

        """
        return self._request_margin_api('get', 'staking/purchaseRecord', signed=True, data=params)

    def set_auto_staking(self, **params):
        """Set Auto Staking on Locked Staking or Locked DeFi Staking

        https://binance-docs.github.io/apidocs/spot/en/#set-auto-staking-user_data

        """
        return self._request_margin_api('post', 'staking/setAutoStaking', signed=True, data=params)

    def get_personal_left_quota(self, **params):
        """Get Personal Left Quota of Staking Product

        https://binance-docs.github.io/apidocs/spot/en/#get-personal-left-quota-of-staking-product-user_data

        """
        return self._request_margin_api('get', 'staking/personalLeftQuota', signed=True, data=params)

    # US Staking Endpoints

    def get_staking_asset_us(self, **params):
        """Get staking information for a supported asset (or assets)

        https://docs.binance.us/#get-staking-asset-information

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("get", "staking/asset", True, data=params)

    def stake_asset_us(self, **params):
        """Stake a supported asset.

        https://docs.binance.us/#stake-asset

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("post", "staking/stake", True, data=params)

    def unstake_asset_us(self, **params):
        """Unstake a staked asset

        https://docs.binance.us/#unstake-asset

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("post", "staking/unstake", True, data=params)

    def get_staking_balance_us(self, **params):
        """Get staking balance

        https://docs.binance.us/#get-staking-balance

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("get", "staking/stakingBalance", True, data=params)

    def get_staking_history_us(self, **params):
        """Get staking history

        https://docs.binance.us/#get-staking-history

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("get", "staking/history", True, data=params)

    def get_staking_rewards_history_us(self, **params):
        """Get staking rewards history for an asset(or assets) within a given time range.

        https://docs.binance.us/#get-staking-rewards-history

        """
        assert self.tld == "us", "Endpoint only available on binance.us"
        return self._request_margin_api("get", "staking/stakingRewardsHistory", True, data=params)

    # Sub Accounts

    def get_sub_account_list(self, **params):
        """Query Sub-account List.

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-list-sapi-for-master-account

        :param email: optional - Sub-account email
        :type email: str
        :param isFreeze: optional
        :type isFreeze: str
        :param page: optional - Default value: 1
        :type page: int
        :param limit: optional - Default value: 1, Max value: 200
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "subAccounts":[
                    {
                        "email":"testsub@gmail.com",
                        "isFreeze":false,
                        "createTime":1544433328000
                    },
                    {
                        "email":"virtual@oxebmvfonoemail.com",
                        "isFreeze":false,
                        "createTime":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/list', True, data=params)

    def get_sub_account_transfer_history(self, **params):
        """Query Sub-account Transfer History.

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-asset-transfer-history-sapi-for-master-account

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional - Default value: 1
        :type page: int
        :param limit: optional - Default value: 500
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "from":"aaa@test.com",
                    "to":"bbb@test.com",
                    "asset":"BTC",
                    "qty":"10",
                    "status": "SUCCESS",
                    "tranId": 6489943656,
                    "time":1544433328000
                },
                {
                    "from":"bbb@test.com",
                    "to":"ccc@test.com",
                    "asset":"ETH",
                    "qty":"2",
                    "status": "SUCCESS",
                    "tranId": 6489938713,
                    "time":1544433328000
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/sub/transfer/history', True, data=params)

    def get_sub_account_futures_transfer_history(self, **params):
        """Query Sub-account Futures Transfer History.

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-futures-asset-transfer-history-for-master-account

        :param email: required
        :type email: str
        :param futuresType: required
        :type futuresType: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "success":true,
                "futuresType": 2,
                "transfers":[
                    {
                        "from":"aaa@test.com",
                        "to":"bbb@test.com",
                        "asset":"BTC",
                        "qty":"1",
                        "time":1544433328000
                    },
                    {
                        "from":"bbb@test.com",
                        "to":"ccc@test.com",
                        "asset":"ETH",
                        "qty":"2",
                        "time":1544433328000
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/internalTransfer', True, data=params)

    def create_sub_account_futures_transfer(self, **params):
        """Execute sub-account Futures transfer

        https://github.com/binance-exchange/binance-official-api-docs/blob/9dbe0e961b80557bb19708a707c7fad08842b28e/wapi-api.md#sub-account-transferfor-master-account

        :param fromEmail: required - Sender email
        :type fromEmail: str
        :param toEmail: required - Recipient email
        :type toEmail: str
        :param futuresType: required
        :type futuresType: int
        :param asset: required
        :type asset: str
        :param amount: required
        :type amount: decimal
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "success":true,
                "txnId":"2934662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/futures/internalTransfer', True, data=params)

    def get_sub_account_assets(self, **params):
        """Fetch sub-account assets

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-assets-sapi-for-master-account

        :param email: required
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "balances":[
                    {
                        "asset":"ADA",
                        "free":10000,
                        "locked":0
                    },
                    {
                        "asset":"BNB",
                        "free":10003,
                        "locked":0
                    },
                    {
                        "asset":"BTC",
                        "free":11467.6399,
                        "locked":0
                    },
                    {
                        "asset":"ETH",
                        "free":10004.995,
                        "locked":0
                    },
                    {
                        "asset":"USDT",
                        "free":11652.14213,
                        "locked":0
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/assets', True, data=params, version=4)

    def query_subaccount_spot_summary(self, **params):
        """Query Sub-account Spot Assets Summary (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-sub-account-spot-assets-summary-for-master-account

        :param email: optional - Sub account email
        :type email: str
        :param page: optional - default 1
        :type page: int
        :param size: optional - default 10, max 20
        :type size: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "totalCount":2,
                "masterAccountTotalAsset": "0.23231201",
                "spotSubUserAssetBtcVoList":[
                    {
                        "email":"sub123@test.com",
                        "totalAsset":"9999.00000000"
                    },
                    {
                        "email":"test456@test.com",
                        "totalAsset":"0.00000000"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/spotSummary', True, data=params)

    def get_subaccount_deposit_address(self, **params):
        """Get Sub-account Deposit Address (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-deposit-address-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param coin: required
        :type coin: str
        :param network: optional
        :type network: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {
                "address":"TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV",
                "coin":"USDT",
                "tag":"",
                "url":"https://tronscan.org/#/address/TDunhSa7jkTNuKrusUTU1MUHtqXoBPKETV"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/deposit/subAddress', True, data=params)

    def get_subaccount_deposit_history(self, **params):
        """Get Sub-account Deposit History (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-deposit-address-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param coin: optional
        :type coin: str
        :param status: optional - (0:pending,6: credited but cannot withdraw, 1:success)
        :type status: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param offset: optional - default:0
        :type offset: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           [
                {
                    "amount":"0.00999800",
                    "coin":"PAXG",
                    "network":"ETH",
                    "status":1,
                    "address":"0x788cabe9236ce061e5a892e1a59395a81fc8d62c",
                    "addressTag":"",
                    "txId":"0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3",
                    "insertTime":1599621997000,
                    "transferType":0,
                    "confirmTimes":"12/12"
                },
                {
                    "amount":"0.50000000",
                    "coin":"IOTA",
                    "network":"IOTA",
                    "status":1,
                    "address":"SIZ9VLMHWATXKV99LH99CIGFJFUMLEHGWVZVNNZXRJJVWBPHYWPPBOSDORZ9EQSHCZAMPVAPGFYQAUUV9DROOXJLNW",
                    "addressTag":"",
                    "txId":"ESBFVQUTPIWQNJSPXFNHNYHSQNTGKRVKPRABQWTAXCDWOAKDKYWPTVG9BGXNVNKTLEJGESAVXIKIZ9999",
                    "insertTime":1599620082000,
                    "transferType":0,
                    "confirmTimes":"1/1"
                }
           ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/deposit/subHisrec', True, data=params)

    def get_subaccount_futures_margin_status(self, **params):
        """Get Sub-account's Status on Margin/Futures (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-sub-account-39-s-status-on-margin-futures-for-master-account

        :param email: optional - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           [
                {
                    "email":"123@test.com",      // user email
                    "isSubUserEnabled": true,    // true or false
                    "isUserActive": true,        // true or false
                    "insertTime": 1570791523523  // sub account create time
                    "isMarginEnabled": true,     // true or false for margin
                    "isFutureEnabled": true      // true or false for futures.
                    "mobile": 1570791523523      // user mobile number
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/status', True, data=params)

    def enable_subaccount_margin(self, **params):
        """Enable Margin for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#enable-margin-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

           {

                "email":"123@test.com",

                "isMarginEnabled": true

            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/margin/enable', True, data=params)

    def get_subaccount_margin_details(self, **params):
        """Get Detail on Sub-account's Margin Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-margin-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                  "email":"123@test.com",
                  "marginLevel": "11.64405625",
                  "totalAssetOfBtc": "6.82728457",
                  "totalLiabilityOfBtc": "0.58633215",
                  "totalNetAssetOfBtc": "6.24095242",
                  "marginTradeCoeffVo":
                        {
                            "forceLiquidationBar": "1.10000000",  // Liquidation margin ratio
                            "marginCallBar": "1.50000000",        // Margin call margin ratio
                            "normalBar": "2.00000000"             // Initial margin ratio
                        },
                  "marginUserAssetVoList": [
                      {
                          "asset": "BTC",
                          "borrowed": "0.00000000",
                          "free": "0.00499500",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00499500"
                      },
                      {
                          "asset": "BNB",
                          "borrowed": "201.66666672",
                          "free": "2346.50000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "2144.83333328"
                      },
                      {
                          "asset": "ETH",
                          "borrowed": "0.00000000",
                          "free": "0.00000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00000000"
                      },
                      {
                          "asset": "USDT",
                          "borrowed": "0.00000000",
                          "free": "0.00000000",
                          "interest": "0.00000000",
                          "locked": "0.00000000",
                          "netAsset": "0.00000000"
                      }
                  ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/margin/account', True, data=params)

    def get_subaccount_margin_summary(self, **params):
        """Get Summary of Sub-account's Margin Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-summary-of-sub-account-39-s-margin-account-for-master-account

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "totalAssetOfBtc": "4.33333333",
                "totalLiabilityOfBtc": "2.11111112",
                "totalNetAssetOfBtc": "2.22222221",
                "subAccountList":[
                    {
                        "email":"123@test.com",
                        "totalAssetOfBtc": "2.11111111",
                        "totalLiabilityOfBtc": "1.11111111",
                        "totalNetAssetOfBtc": "1.00000000"
                    },
                    {
                        "email":"345@test.com",
                        "totalAssetOfBtc": "2.22222222",
                        "totalLiabilityOfBtc": "1.00000001",
                        "totalNetAssetOfBtc": "1.22222221"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/margin/accountSummary', True, data=params)

    def enable_subaccount_futures(self, **params):
        """Enable Futures for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#enable-futures-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {

                "email":"123@test.com",

                "isFuturesEnabled": true  // true or false

            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/futures/enable', True, data=params)

    def get_subaccount_futures_details(self, **params):
        """Get Detail on Sub-account's Futures Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-detail-on-sub-account-39-s-futures-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "email": "abc@test.com",
                "asset": "USDT",
                "assets":[
                    {
                        "asset": "USDT",
                        "initialMargin": "0.00000000",
                        "maintenanceMargin": "0.00000000",
                        "marginBalance": "0.88308000",
                        "maxWithdrawAmount": "0.88308000",
                        "openOrderInitialMargin": "0.00000000",
                        "positionInitialMargin": "0.00000000",
                        "unrealizedProfit": "0.00000000",
                        "walletBalance": "0.88308000"
                     }
                ],
                "canDeposit": true,
                "canTrade": true,
                "canWithdraw": true,
                "feeTier": 2,
                "maxWithdrawAmount": "0.88308000",
                "totalInitialMargin": "0.00000000",
                "totalMaintenanceMargin": "0.00000000",
                "totalMarginBalance": "0.88308000",
                "totalOpenOrderInitialMargin": "0.00000000",
                "totalPositionInitialMargin": "0.00000000",
                "totalUnrealizedProfit": "0.00000000",
                "totalWalletBalance": "0.88308000",
                "updateTime": 1576756674610
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/account', True, data=params, version=2)

    def get_subaccount_futures_summary(self, **params):
        """Get Summary of Sub-account's Futures Account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-summary-of-sub-account-39-s-futures-account-for-master-account

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "totalInitialMargin": "9.83137400",
                "totalMaintenanceMargin": "0.41568700",
                "totalMarginBalance": "23.03235621",
                "totalOpenOrderInitialMargin": "9.00000000",
                "totalPositionInitialMargin": "0.83137400",
                "totalUnrealizedProfit": "0.03219710",
                "totalWalletBalance": "22.15879444",
                "asset": "USDT",
                "subAccountList":[
                    {
                        "email": "123@test.com",
                        "totalInitialMargin": "9.00000000",
                        "totalMaintenanceMargin": "0.00000000",
                        "totalMarginBalance": "22.12659734",
                        "totalOpenOrderInitialMargin": "9.00000000",
                        "totalPositionInitialMargin": "0.00000000",
                        "totalUnrealizedProfit": "0.00000000",
                        "totalWalletBalance": "22.12659734",
                        "asset": "USDT"
                    },
                    {
                        "email": "345@test.com",
                        "totalInitialMargin": "0.83137400",
                        "totalMaintenanceMargin": "0.41568700",
                        "totalMarginBalance": "0.90575887",
                        "totalOpenOrderInitialMargin": "0.00000000",
                        "totalPositionInitialMargin": "0.83137400",
                        "totalUnrealizedProfit": "0.03219710",
                        "totalWalletBalance": "0.87356177",
                        "asset": "USDT"
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/accountSummary', True, data=params, version=2)

    def get_subaccount_futures_positionrisk(self, **params):
        """Get Futures Position-Risk of Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#get-futures-position-risk-of-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
                {
                    "entryPrice": "9975.12000",
                    "leverage": "50",              // current initial leverage
                    "maxNotional": "1000000",      // notional value limit of current initial leverage
                    "liquidationPrice": "7963.54",
                    "markPrice": "9973.50770517",
                    "positionAmount": "0.010",
                    "symbol": "BTCUSDT",
                    "unrealizedProfit": "-0.01612295"
                }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/futures/positionRisk', True, data=params, version=2)

    def make_subaccount_futures_transfer(self, **params):
        """Futures Transfer for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#futures-transfer-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param type: required - 1: transfer from subaccount's spot account to its USDT-margined futures account
                                2: transfer from subaccount's USDT-margined futures account to its spot account
                                3: transfer from subaccount's spot account to its COIN-margined futures account
                                4: transfer from subaccount's COIN-margined futures account to its spot account
        :type type: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/futures/transfer', True, data=params)

    def make_subaccount_margin_transfer(self, **params):
        """Margin Transfer for Sub-account (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#margin-transfer-for-sub-account-for-master-account

        :param email: required - Sub account email
        :type email: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param type: required - 1: transfer from subaccount's spot account to margin account
                                2: transfer from subaccount's margin account to its spot account
        :type type: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/margin/transfer', True, data=params)

    def make_subaccount_to_subaccount_transfer(self, **params):
        """Transfer to Sub-account of Same Master (For Sub-account)

        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-sub-account-of-same-master-for-sub-account

        :param toEmail: required - Sub account email
        :type toEmail: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/transfer/subToSub', True, data=params)

    def make_subaccount_to_master_transfer(self, **params):
        """Transfer to Master (For Sub-account)

        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-master-for-sub-account

        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required - The amount to be transferred
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "txnId":"2966662589"
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/transfer/subToMaster', True, data=params)

    def get_subaccount_transfer_history(self, **params):
        """Sub-account Transfer History (For Sub-account)

        https://binance-docs.github.io/apidocs/spot/en/#transfer-to-master-for-sub-account

        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param type: optional - 1: transfer in, 2: transfer out
        :type type: int
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional - Default 500
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
              {
                "counterParty":"master",
                "email":"master@test.com",
                "type":1,  // 1 for transfer in, 2 for transfer out
                "asset":"BTC",
                "qty":"1",
                "status":"SUCCESS",
                "tranId":11798835829,
                "time":1544433325000
              },
              {
                "counterParty":"subAccount",
                "email":"sub2@test.com",
                "type":2,
                "asset":"ETH",
                "qty":"2",
                "status":"SUCCESS",
                "tranId":11798829519,
                "time":1544433326000
              }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/transfer/subUserHistory', True, data=params)

    def make_subaccount_universal_transfer(self, **params):
        """Universal Transfer (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#universal-transfer-for-master-account

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param fromAccountType: required - "SPOT","USDT_FUTURE","COIN_FUTURE"
        :type fromAccountType: str
        :param toAccountType: required - "SPOT","USDT_FUTURE","COIN_FUTURE"
        :type toAccountType: str
        :param asset: required - The asset being transferred, e.g., USDT
        :type asset: str
        :param amount: required
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "tranId":11945860693
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'sub-account/universalTransfer', True, data=params)

    def get_universal_transfer_history(self, **params):
        """Universal Transfer (For Master Account)

        https://binance-docs.github.io/apidocs/spot/en/#query-universal-transfer-history

        :param fromEmail: optional
        :type fromEmail: str
        :param toEmail: optional
        :type toEmail: str
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional
        :type page: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            [
              {
                "tranId":11945860693,
                "fromEmail":"master@test.com",
                "toEmail":"subaccount1@test.com",
                "asset":"BTC",
                "amount":"0.1",
                "fromAccountType":"SPOT",
                "toAccountType":"COIN_FUTURE",
                "status":"SUCCESS",
                "createTimeStamp":1544433325000
              },
              {
                "tranId":11945857955,
                "fromEmail":"master@test.com",
                "toEmail":"subaccount2@test.com",
                "asset":"ETH",
                "amount":"0.2",
                "fromAccountType":"SPOT",
                "toAccountType":"USDT_FUTURE",
                "status":"SUCCESS",
                "createTimeStamp":1544433326000
              }
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'sub-account/universalTransfer', True, data=params)

    # Futures API

    def futures_ping(self):
        """Test connectivity to the Rest API

        https://binance-docs.github.io/apidocs/futures/en/#test-connectivity

        """
        return self._request_futures_api('get', 'ping')

    def futures_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://binance-docs.github.io/apidocs/futures/en/#check-server-time

        """
        return self._request_futures_api('get', 'time')

    def futures_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://binance-docs.github.io/apidocs/futures/en/#exchange-information-market_data

        """
        return self._request_futures_api('get', 'exchangeInfo')

    def futures_order_book(self, **params):
        """Get the Order Book for the market

        https://binance-docs.github.io/apidocs/futures/en/#order-book-market_data

        """
        return self._request_futures_api('get', 'depth', data=params)

    def futures_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://binance-docs.github.io/apidocs/futures/en/#recent-trades-list-market_data

        """
        return self._request_futures_api('get', 'trades', data=params)

    def futures_historical_trades(self, **params):
        """Get older market historical trades.

        https://binance-docs.github.io/apidocs/futures/en/#old-trades-lookup-market_data

        """
        return self._request_futures_api('get', 'historicalTrades', data=params)

    def futures_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/futures/en/#compressed-aggregate-trades-list-market_data

        """
        return self._request_futures_api('get', 'aggTrades', data=params)

    def futures_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data-market_data

        """
        return self._request_futures_api('get', 'klines', data=params)

    def futures_continous_klines(self, **params):
        """Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-data

        """
        return self._request_futures_api('get', 'continuousKlines', data=params)

    def futures_historical_klines(self, symbol, interval, start_str, end_str=None, limit=500):
        """Get historical futures klines from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int
        :param limit: Default 500; max 1000.
        :type limit: int

        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)

        """
        return self._historical_klines(symbol, interval, start_str, end_str=end_str, limit=limit, klines_type=HistoricalKlinesType.FUTURES)

    def futures_historical_klines_generator(self, symbol, interval, start_str, end_str=None):
        """Get historical futures klines generator from Binance

        :param symbol: Name of symbol pair e.g. BNBBTC
        :type symbol: str
        :param interval: Binance Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format or timestamp in milliseconds
        :type start_str: str|int
        :param end_str: optional - end date string in UTC format or timestamp in milliseconds (default will fetch everything up to now)
        :type end_str: str|int

        :return: generator of OHLCV values

        """

        return self._historical_klines_generator(symbol, interval, start_str, end_str=end_str, klines_type=HistoricalKlinesType.FUTURES)

    def futures_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://binance-docs.github.io/apidocs/futures/en/#mark-price-market_data

        """
        return self._request_futures_api('get', 'premiumIndex', data=params)

    def futures_funding_rate(self, **params):
        """Get funding rate history

        https://binance-docs.github.io/apidocs/futures/en/#get-funding-rate-history-market_data

        """
        return self._request_futures_api('get', 'fundingRate', data=params)

    def futures_top_longshort_account_ratio(self, **params):
        """Get present long to short ratio for top accounts of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#top-trader-long-short-ratio-accounts-market_data
        """
        return self._request_futures_data_api('get', 'topLongShortAccountRatio', data=params)

    def futures_top_longshort_position_ratio(self, **params):
        """Get present long to short ratio for top positions of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#top-trader-long-short-ratio-positions
        """
        return self._request_futures_data_api('get', 'topLongShortPositionRatio', data=params)

    def futures_global_longshort_ratio(self, **params):
        """Get present global long to short ratio of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#long-short-ratio
        """
        return self._request_futures_data_api('get', 'globalLongShortAccountRatio', data=params)

    def futures_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://binance-docs.github.io/apidocs/futures/en/#24hr-ticker-price-change-statistics-market_data

        """
        return self._request_futures_api('get', 'ticker/24hr', data=params)

    def futures_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-price-ticker-market_data

        """
        return self._request_futures_api('get', 'ticker/price', data=params)

    def futures_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker-market_data

        """
        return self._request_futures_api('get', 'ticker/bookTicker', data=params)

    def futures_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://binance-docs.github.io/apidocs/futures/en/#get-all-liquidation-orders-market_data

        """
        return self._request_futures_api('get', 'forceOrders', signed=True, data=params)

    def futures_api_trading_status(self, **params):
        """Get Position ADL Quantile Estimate

        https://binance-docs.github.io/apidocs/futures/en/#futures-trading-quantitative-rules-indicators-user_data

        :param symbol: optional
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "indicators": { // indicator: quantitative rules indicators, value: user's indicators value, triggerValue: trigger indicator value threshold of quantitative rules.
                    "BTCUSDT": [
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "UFR",  // Unfilled Ratio (UFR)
                            "value": 0.05,  // Current value
                            "triggerValue": 0.995  // Trigger value
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "IFER",  // IOC/FOK Expiration Ratio (IFER)
                            "value": 0.99,  // Current value
                            "triggerValue": 0.99  // Trigger value
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "GCR",  // GTC Cancellation Ratio (GCR)
                            "value": 0.99,  // Current value
                            "triggerValue": 0.99  // Trigger value
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "DR",  // Dust Ratio (DR)
                            "value": 0.99,  // Current value
                            "triggerValue": 0.99  // Trigger value
                        }
                    ],
                    "ETHUSDT": [
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "UFR",
                            "value": 0.05,
                            "triggerValue": 0.995
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "IFER",
                            "value": 0.99,
                            "triggerValue": 0.99
                        },
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "GCR",
                            "value": 0.99,
                            "triggerValue": 0.99
                        }
                        {
                            "isLocked": true,
                            "plannedRecoverTime": 1545741270000,
                            "indicator": "DR",
                            "value": 0.99,
                            "triggerValue": 0.99
                        }
                    ]
                },
                "updateTime": 1545741270000
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_api('get', 'apiTradingStatus', signed=True, data=params)

    def futures_comission_rate(self, **params):
        """Get Futures commission rate

        https://binance-docs.github.io/apidocs/futures/en/#user-commission-rate-user_data

        :param symbol: required
        :type symbol: str

        :returns: API response

        .. code-block:: python

            {
                "symbol": "BTCUSDT",
                "makerCommissionRate": "0.0002",  // 0.02%
                "takerCommissionRate": "0.0004"   // 0.04%
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_futures_api('get', 'commissionRate', signed=True, data=params)

    def futures_adl_quantile_estimate(self, **params):
        """Get Position ADL Quantile Estimate

        https://binance-docs.github.io/apidocs/futures/en/#position-adl-quantile-estimation-user_data

        """
        return self._request_futures_api('get', 'adlQuantile', signed=True, data=params)

    def futures_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#open-interest

        """
        return self._request_futures_api('get', 'openInterest', data=params)

    def futures_index_info(self, **params):
        """Get index_info

        https://binance-docs.github.io/apidocs/futures/en/#indexInfo

        """
        return self._request_futures_api('get', 'indexInfo', data=params)

    def futures_open_interest_hist(self, **params):
        """Get open interest statistics of a specific symbol.

        https://binance-docs.github.io/apidocs/futures/en/#open-interest-statistics

        """
        return self._request_futures_data_api('get', 'openInterestHist', data=params)

    def futures_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://binance-docs.github.io/apidocs/futures/en/#notional-and-leverage-brackets-market_data

        """
        return self._request_futures_api('get', 'leverageBracket', True, data=params)

    def futures_account_transfer(self, **params):
        """Execute transfer between spot account and futures account.

        https://binance-docs.github.io/apidocs/futures/en/#new-future-account-transfer

        """
        return self._request_margin_api('post', 'futures/transfer', True, data=params)

    def transfer_history(self, **params):
        """Get future account transaction history list

        https://binance-docs.github.io/apidocs/futures/en/#get-future-account-transaction-history-list-user_data

        """
        return self._request_margin_api('get', 'futures/transfer', True, data=params)

    def futures_loan_borrow_history(self, **params):
        return self._request_margin_api('get', 'futures/loan/borrow/history', True, data=params)

    def futures_loan_repay_history(self, **params):
        return self._request_margin_api('get', 'futures/loan/repay/history', True, data=params)

    def futures_loan_wallet(self, **params):
        return self._request_margin_api('get', 'futures/loan/wallet', True, data=params, version=2)

    def futures_cross_collateral_adjust_history(self, **params):
        return self._request_margin_api('get', 'futures/loan/adjustCollateral/history', True, data=params)

    def futures_cross_collateral_liquidation_history(self, **params):
        return self._request_margin_api('get', 'futures/loan/liquidationHistory', True, data=params)

    def futures_loan_interest_history(self, **params):
        return self._request_margin_api('get', 'futures/loan/interestHistory', True, data=params)

    def futures_create_order(self, **params):
        """Send in a new order.

        https://binance-docs.github.io/apidocs/futures/en/#new-order-trade

        """
        return self._request_futures_api('post', 'order', True, data=params)

    def futures_place_batch_order(self, **params):
        """Send in new orders.

        https://binance-docs.github.io/apidocs/futures/en/#place-multiple-orders-trade

        To avoid modifying the existing signature generation and parameter order logic,
        the url encoding is done on the special query param, batchOrders, in the early stage.

        """
        query_string = urlencode(params)
        query_string = query_string.replace('%27', '%22')
        params['batchOrders'] = query_string[12:]
        return self._request_futures_api('post', 'batchOrders', True, data=params)

    def futures_get_order(self, **params):
        """Check an order's status.

        https://binance-docs.github.io/apidocs/futures/en/#query-order-user_data

        """
        return self._request_futures_api('get', 'order', True, data=params)

    def futures_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://binance-docs.github.io/apidocs/futures/en/#current-open-orders-user_data

        """
        return self._request_futures_api('get', 'openOrders', True, data=params)

    def futures_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://binance-docs.github.io/apidocs/futures/en/#all-orders-user_data

        """
        return self._request_futures_api('get', 'allOrders', True, data=params)

    def futures_cancel_order(self, **params):
        """Cancel an active futures order.

        https://binance-docs.github.io/apidocs/futures/en/#cancel-order-trade

        """
        return self._request_futures_api('delete', 'order', True, data=params)

    def futures_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://binance-docs.github.io/apidocs/futures/en/#cancel-all-open-orders-trade

        """
        return self._request_futures_api('delete', 'allOpenOrders', True, data=params)

    def futures_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://binance-docs.github.io/apidocs/futures/en/#cancel-multiple-orders-trade

        """
        return self._request_futures_api('delete', 'batchOrders', True, data=params)

    def futures_account_balance(self, **params):
        """Get futures account balance

        https://binance-docs.github.io/apidocs/futures/en/#future-account-balance-user_data

        """
        return self._request_futures_api('get', 'balance', True, 2, data=params)

    def futures_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/futures/en/#account-information-user_data

        """
        return self._request_futures_api('get', 'account', True, 2, data=params)

    def futures_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://binance-docs.github.io/apidocs/futures/en/#change-initial-leverage-trade

        """
        return self._request_futures_api('post', 'leverage', True, data=params)

    def futures_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://binance-docs.github.io/apidocs/futures/en/#change-margin-type-trade

        """
        return self._request_futures_api('post', 'marginType', True, data=params)

    def futures_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://binance-docs.github.io/apidocs/futures/en/#modify-isolated-position-margin-trade

        """
        return self._request_futures_api('post', 'positionMargin', True, data=params)

    def futures_position_margin_history(self, **params):
        """Get position margin change history

        https://binance-docs.github.io/apidocs/futures/en/#get-postion-margin-change-history-trade

        """
        return self._request_futures_api('get', 'positionMargin/history', True, data=params)

    def futures_position_information(self, **params):
        """Get position information

        https://binance-docs.github.io/apidocs/futures/en/#position-information-user_data

        """
        return self._request_futures_api('get', 'positionRisk', True, 2, data=params)

    def futures_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data

        """
        return self._request_futures_api('get', 'userTrades', True, data=params)

    def futures_income_history(self, **params):
        """Get income history for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#get-income-history-user_data

        """
        return self._request_futures_api('get', 'income', True, data=params)

    def futures_change_position_mode(self, **params):
        """Change position mode for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade

        """
        return self._request_futures_api('post', 'positionSide/dual', True, data=params)

    def futures_get_position_mode(self, **params):
        """Get position mode for authenticated account

        https://binance-docs.github.io/apidocs/futures/en/#get-current-position-mode-user_data

        """
        return self._request_futures_api('get', 'positionSide/dual', True, data=params)

    def futures_change_multi_assets_mode(self, multiAssetsMargin: bool):
        """Change user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol

        https://binance-docs.github.io/apidocs/futures/en/#change-multi-assets-mode-trade

        """
        params = {
            'multiAssetsMargin': 'true' if multiAssetsMargin else 'false'
        }
        return self._request_futures_api('post', 'multiAssetsMargin', True, data=params)

    def futures_get_multi_assets_mode(self):
        """Get user's Multi-Assets mode (Multi-Assets Mode or Single-Asset Mode) on Every symbol

        https://binance-docs.github.io/apidocs/futures/en/#get-current-multi-assets-mode-user_data

        """
        return self._request_futures_api('get', 'multiAssetsMargin', True, data={})

    def futures_stream_get_listen_key(self):
        res = self._request_futures_api('post', 'listenKey', signed=False, data={})
        return res['listenKey']

    def futures_stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return self._request_futures_api('put', 'listenKey', signed=False, data=params)

    def futures_stream_close(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return self._request_futures_api('delete', 'listenKey', signed=False, data=params)

    # COIN Futures API
    def futures_coin_ping(self):
        """Test connectivity to the Rest API

        https://binance-docs.github.io/apidocs/delivery/en/#test-connectivity

        """
        return self._request_futures_coin_api("get", "ping")

    def futures_coin_time(self):
        """Test connectivity to the Rest API and get the current server time.

        https://binance-docs.github.io/apidocs/delivery/en/#check-server-time

        """
        return self._request_futures_coin_api("get", "time")

    def futures_coin_exchange_info(self):
        """Current exchange trading rules and symbol information

        https://binance-docs.github.io/apidocs/delivery/en/#exchange-information

        """
        return self._request_futures_coin_api("get", "exchangeInfo")

    def futures_coin_order_book(self, **params):
        """Get the Order Book for the market

        https://binance-docs.github.io/apidocs/delivery/en/#order-book

        """
        return self._request_futures_coin_api("get", "depth", data=params)

    def futures_coin_recent_trades(self, **params):
        """Get recent trades (up to last 500).

        https://binance-docs.github.io/apidocs/delivery/en/#recent-trades-list

        """
        return self._request_futures_coin_api("get", "trades", data=params)

    def futures_coin_historical_trades(self, **params):
        """Get older market historical trades.

        https://binance-docs.github.io/apidocs/delivery/en/#old-trades-lookup-market_data

        """
        return self._request_futures_coin_api("get", "historicalTrades", data=params)

    def futures_coin_aggregate_trades(self, **params):
        """Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same
        price will have the quantity aggregated.

        https://binance-docs.github.io/apidocs/delivery/en/#compressed-aggregate-trades-list

        """
        return self._request_futures_coin_api("get", "aggTrades", data=params)

    def futures_coin_klines(self, **params):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/delivery/en/#kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "klines", data=params)

    def futures_coin_continous_klines(self, **params):
        """Kline/candlestick bars for a specific contract type. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/delivery/en/#continuous-contract-kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "continuousKlines", data=params)

    def futures_coin_index_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://binance-docs.github.io/apidocs/delivery/en/#index-price-kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "indexPriceKlines", data=params)

    def futures_coin_mark_price_klines(self, **params):
        """Kline/candlestick bars for the index price of a pair..

        https://binance-docs.github.io/apidocs/delivery/en/#mark-price-kline-candlestick-data

        """
        return self._request_futures_coin_api("get", "markPriceKlines", data=params)

    def futures_coin_mark_price(self, **params):
        """Get Mark Price and Funding Rate

        https://binance-docs.github.io/apidocs/delivery/en/#index-price-and-mark-price

        """
        return self._request_futures_coin_api("get", "premiumIndex", data=params)

    def futures_coin_funding_rate(self, **params):
        """Get funding rate history

        https://binance-docs.github.io/apidocs/delivery/en/#get-funding-rate-history-of-perpetual-futures

        """
        return self._request_futures_coin_api("get", "fundingRate", data=params)

    def futures_coin_ticker(self, **params):
        """24 hour rolling window price change statistics.

        https://binance-docs.github.io/apidocs/delivery/en/#24hr-ticker-price-change-statistics

        """
        return self._request_futures_coin_api("get", "ticker/24hr", data=params)

    def futures_coin_symbol_ticker(self, **params):
        """Latest price for a symbol or symbols.

        https://binance-docs.github.io/apidocs/delivery/en/#symbol-price-ticker

        """
        return self._request_futures_coin_api("get", "ticker/price", data=params)

    def futures_coin_orderbook_ticker(self, **params):
        """Best price/qty on the order book for a symbol or symbols.

        https://binance-docs.github.io/apidocs/delivery/en/#symbol-order-book-ticker

        """
        return self._request_futures_coin_api("get", "ticker/bookTicker", data=params)

    def futures_coin_liquidation_orders(self, **params):
        """Get all liquidation orders

        https://binance-docs.github.io/apidocs/delivery/en/#user-39-s-force-orders-user_data

        """
        return self._request_futures_coin_api("get", "forceOrders", signed=True, data=params)

    def futures_coin_open_interest(self, **params):
        """Get present open interest of a specific symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#open-interest

        """
        return self._request_futures_coin_api("get", "openInterest", data=params)

    def futures_coin_open_interest_hist(self, **params):
        """Get open interest statistics of a specific symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#open-interest-statistics-market-data

        """
        return self._request_futures_coin_data_api("get", "openInterestHist", data=params)

    def futures_coin_leverage_bracket(self, **params):
        """Notional and Leverage Brackets

        https://binance-docs.github.io/apidocs/delivery/en/#notional-bracket-for-pair-user_data

        """
        return self._request_futures_coin_api(
            "get", "leverageBracket", version=2, signed=True, data=params
        )

    def new_transfer_history(self, **params):
        """Get future account transaction history list

        https://binance-docs.github.io/apidocs/delivery/en/#new-future-account-transfer

        """
        return self._request_margin_api("get", "asset/transfer", True, data=params)

    def funding_wallet(self, **params):
        return self._request_margin_api("post", "asset/get-funding-asset", True, data=params)

    def get_user_asset(self, **params):
        return self._request_margin_api("post", "asset/getUserAsset", True, data=params, version=3)

    def universal_transfer(self, **params):
        """Unviversal transfer api accross different binance account types

        https://binance-docs.github.io/apidocs/spot/en/#user-universal-transfer
        """
        return self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    def futures_coin_create_order(self, **params):
        """Send in a new order.

        https://binance-docs.github.io/apidocs/delivery/en/#new-order-trade

        """
        return self._request_futures_coin_api("post", "order", True, data=params)

    def futures_coin_place_batch_order(self, **params):
        """Send in new orders.

        https://binance-docs.github.io/apidocs/delivery/en/#place-multiple-orders-trade

        To avoid modifying the existing signature generation and parameter order logic,
        the url encoding is done on the special query param, batchOrders, in the early stage.

        """
        query_string = urlencode(params)
        query_string = query_string.replace('%27', '%22')
        params['batchOrders'] = query_string[12:]

        return self._request_futures_coin_api('post', 'batchOrders', True, data=params)

    def futures_coin_get_order(self, **params):
        """Check an order's status.

        https://binance-docs.github.io/apidocs/delivery/en/#query-order-user_data

        """
        return self._request_futures_coin_api("get", "order", True, data=params)

    def futures_coin_get_open_orders(self, **params):
        """Get all open orders on a symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#current-all-open-orders-user_data

        """
        return self._request_futures_coin_api("get", "openOrders", True, data=params)

    def futures_coin_get_all_orders(self, **params):
        """Get all futures account orders; active, canceled, or filled.

        https://binance-docs.github.io/apidocs/delivery/en/#all-orders-user_data

        """
        return self._request_futures_coin_api(
            "get", "allOrders", signed=True, data=params
        )

    def futures_coin_cancel_order(self, **params):
        """Cancel an active futures order.

        https://binance-docs.github.io/apidocs/delivery/en/#cancel-order-trade

        """
        return self._request_futures_coin_api(
            "delete", "order", signed=True, data=params
        )

    def futures_coin_cancel_all_open_orders(self, **params):
        """Cancel all open futures orders

        https://binance-docs.github.io/apidocs/delivery/en/#cancel-all-open-orders-trade

        """
        return self._request_futures_coin_api(
            "delete", "allOpenOrders", signed=True, data=params
        )

    def futures_coin_cancel_orders(self, **params):
        """Cancel multiple futures orders

        https://binance-docs.github.io/apidocs/delivery/en/#cancel-multiple-orders-trade

        """
        return self._request_futures_coin_api(
            "delete", "batchOrders", True, data=params
        )

    def futures_coin_account_balance(self, **params):
        """Get futures account balance

        https://binance-docs.github.io/apidocs/delivery/en/#futures-account-balance-user_data

        """
        return self._request_futures_coin_api(
            "get", "balance", signed=True, data=params
        )

    def futures_coin_account(self, **params):
        """Get current account information.

        https://binance-docs.github.io/apidocs/delivery/en/#account-information-user_data

        """
        return self._request_futures_coin_api(
            "get", "account", signed=True, data=params
        )

    def futures_coin_change_leverage(self, **params):
        """Change user's initial leverage of specific symbol market

        https://binance-docs.github.io/apidocs/delivery/en/#change-initial-leverage-trade

        """
        return self._request_futures_coin_api(
            "post", "leverage", signed=True, data=params
        )

    def futures_coin_change_margin_type(self, **params):
        """Change the margin type for a symbol

        https://binance-docs.github.io/apidocs/delivery/en/#change-margin-type-trade

        """
        return self._request_futures_coin_api(
            "post", "marginType", signed=True, data=params
        )

    def futures_coin_change_position_margin(self, **params):
        """Change the position margin for a symbol

        https://binance-docs.github.io/apidocs/delivery/en/#modify-isolated-position-margin-trade

        """
        return self._request_futures_coin_api(
            "post", "positionMargin", True, data=params
        )

    def futures_coin_position_margin_history(self, **params):
        """Get position margin change history

        https://binance-docs.github.io/apidocs/delivery/en/#get-position-margin-change-history-trade

        """
        return self._request_futures_coin_api(
            "get", "positionMargin/history", True, data=params
        )

    def futures_coin_position_information(self, **params):
        """Get position information

        https://binance-docs.github.io/apidocs/delivery/en/#position-information-user_data

        """
        return self._request_futures_coin_api("get", "positionRisk", True, data=params)

    def futures_coin_account_trades(self, **params):
        """Get trades for the authenticated account and symbol.

        https://binance-docs.github.io/apidocs/delivery/en/#account-trade-list-user_data

        """
        return self._request_futures_coin_api("get", "userTrades", True, data=params)

    def futures_coin_income_history(self, **params):
        """Get income history for authenticated account

        https://binance-docs.github.io/apidocs/delivery/en/#get-income-history-user_data

        """
        return self._request_futures_coin_api("get", "income", True, data=params)

    def futures_coin_change_position_mode(self, **params):
        """Change user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://binance-docs.github.io/apidocs/delivery/en/#change-position-mode-trade
        """
        return self._request_futures_coin_api("post", "positionSide/dual", True, data=params)

    def futures_coin_get_position_mode(self, **params):
        """Get user's position mode (Hedge Mode or One-way Mode ) on EVERY symbol

        https://binance-docs.github.io/apidocs/delivery/en/#get-current-position-mode-user_data

        """
        return self._request_futures_coin_api("get", "positionSide/dual", True, data=params)

    def futures_coin_stream_get_listen_key(self):
        res = self._request_futures_coin_api('post', 'listenKey', signed=False, data={})
        return res['listenKey']

    def futures_coin_stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return self._request_futures_coin_api('put', 'listenKey', signed=False, data=params)

    def futures_coin_stream_close(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return self._request_futures_coin_api('delete', 'listenKey', signed=False, data=params)

    def get_all_coins_info(self, **params):
        """Get information of coins (available for deposit and withdraw) for user.

        https://binance-docs.github.io/apidocs/spot/en/#all-coins-39-information-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
                "coin": "BTC",
                "depositAllEnable": true,
                "withdrawAllEnable": true,
                "name": "Bitcoin",
                "free": "0",
                "locked": "0",
                "freeze": "0",
                "withdrawing": "0",
                "ipoing": "0",
                "ipoable": "0",
                "storage": "0",
                "isLegalMoney": false,
                "trading": true,
                "networkList": [
                    {
                        "network": "BNB",
                        "coin": "BTC",
                        "withdrawIntegerMultiple": "0.00000001",
                        "isDefault": false,
                        "depositEnable": true,
                        "withdrawEnable": true,
                        "depositDesc": "",
                        "withdrawDesc": "",
                        "specialTips": "Both a MEMO and an Address are required to successfully deposit your BEP2-BTCB tokens to Binance.",
                        "name": "BEP2",
                        "resetAddressStatus": false,
                        "addressRegex": "^(bnb1)[0-9a-z]{38}$",
                        "memoRegex": "^[0-9A-Za-z-_]{1,120}$",
                        "withdrawFee": "0.0000026",
                        "withdrawMin": "0.0000052",
                        "withdrawMax": "0",
                        "minConfirm": 1,
                        "unLockConfirm": 0
                    },
                    {
                        "network": "BTC",
                        "coin": "BTC",
                        "withdrawIntegerMultiple": "0.00000001",
                        "isDefault": true,
                        "depositEnable": true,
                        "withdrawEnable": true,
                        "depositDesc": "",
                        "withdrawDesc": "",
                        "specialTips": "",
                        "name": "BTC",
                        "resetAddressStatus": false,
                        "addressRegex": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^(bc1)[0-9A-Za-z]{39,59}$",
                        "memoRegex": "",
                        "withdrawFee": "0.0005",
                        "withdrawMin": "0.001",
                        "withdrawMax": "0",
                        "minConfirm": 1,
                        "unLockConfirm": 2
                    }
                ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'capital/config/getall', True, data=params)

    def get_account_snapshot(self, **params):
        """Get daily account snapshot of specific type.

        https://binance-docs.github.io/apidocs/spot/en/#daily-account-snapshot-user_data

        :param type: required. Valid values are SPOT/MARGIN/FUTURES.
        :type type: string
        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "balances":[
                           {
                              "asset":"BTC",
                              "free":"0.09905021",
                              "locked":"0.00000000"
                           },
                           {
                              "asset":"USDT",
                              "free":"1.89109409",
                              "locked":"0.00000000"
                           }
                        ],
                        "totalAssetOfBtc":"0.09942700"
                     },
                     "type":"spot",
                     "updateTime":1576281599000
                  }
               ]
            }

        OR

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "marginLevel":"2748.02909813",
                        "totalAssetOfBtc":"0.00274803",
                        "totalLiabilityOfBtc":"0.00000100",
                        "totalNetAssetOfBtc":"0.00274750",
                        "userAssets":[
                           {
                              "asset":"XRP",
                              "borrowed":"0.00000000",
                              "free":"1.00000000",
                              "interest":"0.00000000",
                              "locked":"0.00000000",
                              "netAsset":"1.00000000"
                           }
                        ]
                     },
                     "type":"margin",
                     "updateTime":1576281599000
                  }
               ]
            }

        OR

        .. code-block:: python

            {
               "code":200, // 200 for success; others are error codes
               "msg":"", // error message
               "snapshotVos":[
                  {
                     "data":{
                        "assets":[
                           {
                              "asset":"USDT",
                              "marginBalance":"118.99782335",
                              "walletBalance":"120.23811389"
                           }
                        ],
                        "position":[
                           {
                              "entryPrice":"7130.41000000",
                              "markPrice":"7257.66239673",
                              "positionAmt":"0.01000000",
                              "symbol":"BTCUSDT",
                              "unRealizedProfit":"1.24029054"
                           }
                        ]
                     },
                     "type":"futures",
                     "updateTime":1576281599000
                  }
               ]
            }

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('get', 'accountSnapshot', True, data=params)

    def disable_fast_withdraw_switch(self, **params):
        """Disable Fast Withdraw Switch

        https://binance-docs.github.io/apidocs/spot/en/#disable-fast-withdraw-switch-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'disableFastWithdrawSwitch', True, data=params)

    def enable_fast_withdraw_switch(self, **params):
        """Enable Fast Withdraw Switch

        https://binance-docs.github.io/apidocs/spot/en/#enable-fast-withdraw-switch-user_data

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        :raises: BinanceRequestException, BinanceAPIException

        """
        return self._request_margin_api('post', 'enableFastWithdrawSwitch', True, data=params)

    """
    ====================================================================================================================
    Options API
    ====================================================================================================================
    """
    # Quoting interface endpoints

    def options_ping(self):
        """Test connectivity

        https://binance-docs.github.io/apidocs/voptions/en/#test-connectivity

        """
        return self._request_options_api('get', 'ping')

    def options_time(self):
        """Get server time

        https://binance-docs.github.io/apidocs/voptions/en/#get-server-time

        """
        return self._request_options_api('get', 'time')

    def options_info(self):
        """Get current trading pair info

        https://binance-docs.github.io/apidocs/voptions/en/#get-current-trading-pair-info

        """
        return self._request_options_api('get', 'optionInfo')

    def options_exchange_info(self):
        """Get current limit info and trading pair info

        https://binance-docs.github.io/apidocs/voptions/en/#get-current-limit-info-and-trading-pair-info

        """
        return self._request_options_api('get', 'exchangeInfo')

    def options_index_price(self, **params):
        """Get the spot index price

        https://binance-docs.github.io/apidocs/voptions/en/#get-the-spot-index-price

        :param underlying: required - Spot pair（Option contract underlying asset）- BTCUSDT
        :type underlying: str

        """
        return self._request_options_api('get', 'index', data=params)

    def options_price(self, **params):
        """Get the latest price

        https://binance-docs.github.io/apidocs/voptions/en/#get-the-latest-price

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str

        """
        return self._request_options_api('get', 'ticker', data=params)

    def options_mark_price(self, **params):
        """Get the latest mark price

        https://binance-docs.github.io/apidocs/voptions/en/#get-the-latest-mark-price

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str

        """
        return self._request_options_api('get', 'mark', data=params)

    def options_order_book(self, **params):
        """Depth information

        https://binance-docs.github.io/apidocs/voptions/en/#depth-information

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param limit: optional - Default:100 Max:1000.Optional value:[10, 20, 50, 100, 500, 1000] - 100
        :type limit: int

        """
        return self._request_options_api('get', 'depth', data=params)

    def options_klines(self, **params):
        """Candle data

        https://binance-docs.github.io/apidocs/voptions/en/#candle-data

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param interval: required - Time interval - 5m
        :type interval: str
        :param startTime: optional - Start Time - 1592317127349
        :type startTime: int
        :param endTime: optional - End Time - 1592317127349
        :type endTime: int
        :param limit: optional - Number of records Default:500 Max:1500 - 500
        :type limit: int

        """
        return self._request_options_api('get', 'klines', data=params)

    def options_recent_trades(self, **params):
        """Recently completed Option trades

        https://binance-docs.github.io/apidocs/voptions/en/#recently-completed-option-trades

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param limit: optional - Number of records Default:100 Max:500 - 100
        :type limit: int

        """
        return self._request_options_api('get', 'trades', data=params)

    def options_historical_trades(self, **params):
        """Query trade history

        https://binance-docs.github.io/apidocs/voptions/en/#query-trade-history

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param fromId: optional - The deal ID from which to return. The latest deal record is returned by default - 1592317127349
        :type fromId: int
        :param limit: optional - Number of records Default:100 Max:500 - 100
        :type limit: int

        """
        return self._request_options_api('get', 'historicalTrades', data=params)

    # Account and trading interface endpoints

    def options_account_info(self, **params):
        """Account asset info (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#account-asset-info-user_data

        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'account', signed=True, data=params)

    def options_funds_transfer(self, **params):
        """Funds transfer (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#funds-transfer-user_data

        :param currency: required - Asset type - USDT
        :type currency: str
        :param type: required - IN: Transfer from spot account to option account OUT: Transfer from option account to spot account - IN
        :type type: str (ENUM)
        :param amount: required - Amount - 10000
        :type amount: float
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'transfer', signed=True, data=params)

    def options_positions(self, **params):
        """Option holdings info (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#option-holdings-info-user_data

        :param symbol: optional - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'position', signed=True, data=params)

    def options_bill(self, **params):
        """Account funding flow (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#account-funding-flow-user_data

        :param currency: required - Asset type - USDT
        :type currency: str
        :param recordId: optional - Return the recordId and subsequent data, the latest data is returned by default - 100000
        :type recordId: int
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'bill', signed=True, data=params)

    def options_place_order(self, **params):
        """Option order (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#option-order-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param side: required - Buy/sell direction: SELL, BUY - BUY
        :type side: str (ENUM)
        :param type: required - Order Type: LIMIT, MARKET - LIMIT
        :type type: str (ENUM)
        :param quantity: required - Order Quantity - 3
        :type quantity: float
        :param price: optional - Order Price - 1000
        :type price: float
        :param timeInForce: optional - Time in force method（Default GTC) - GTC
        :type timeInForce: str (ENUM)
        :param reduceOnly: optional - Reduce Only (Default false) - false
        :type reduceOnly: bool
        :param postOnly: optional - Post Only (Default false) - false
        :type postOnly: bool
        :param newOrderRespType: optional - "ACK", "RESULT", Default "ACK" - ACK
        :type newOrderRespType: str (ENUM)
        :param clientOrderId: optional - User-defined order ID cannot be repeated in pending orders - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'order', signed=True, data=params)

    def options_place_batch_order(self, **params):
        """Place Multiple Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#place-multiple-option-orders-trade

        :param orders: required - order list. Max 5 orders - [{"symbol":"BTC-210115-35000-C","price":"100","quantity":"0.0001","side":"BUY","type":"LIMIT"}]
        :type orders: list
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('post', 'batchOrders', signed=True, data=params)

    def options_cancel_order(self, **params):
        """Cancel Option order (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#cancel-option-order-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Order ID - 4611875134427365377
        :type orderId: str
        :param clientOrderId: optional - User-defined order ID - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('delete', 'order', signed=True, data=params)

    def options_cancel_batch_order(self, **params):
        """Cancel Multiple Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#cancel-multiple-option-orders-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderIds: optional - Order ID - [4611875134427365377,4611875134427365378]
        :type orderId: list
        :param clientOrderIds: optional - User-defined order ID - ["my_id_1","my_id_2"]
        :type clientOrderIds: list
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('delete', 'batchOrders', signed=True, data=params)

    def options_cancel_all_orders(self, **params):
        """Cancel all Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#cancel-all-option-orders-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('delete', 'allOpenOrders', signed=True, data=params)

    def options_query_order(self, **params):
        """Query Option order (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#query-option-order-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Order ID - 4611875134427365377
        :type orderId: str
        :param clientOrderId: optional - User-defined order ID - 10000
        :type clientOrderId: str
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'order', signed=True, data=params)

    def options_query_pending_orders(self, **params):
        """Query current pending Option orders (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#query-current-pending-option-orders-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Returns the orderId and subsequent orders, the most recent order is returned by default - 100000
        :type orderId: str
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'openOrders', signed=True, data=params)

    def options_query_order_history(self, **params):
        """Query Option order history (TRADE)

        https://binance-docs.github.io/apidocs/voptions/en/#query-option-order-history-trade

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param orderId: optional - Returns the orderId and subsequent orders, the most recent order is returned by default - 100000
        :type orderId: str
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'historyOrders', signed=True, data=params)

    def options_user_trades(self, **params):
        """Option Trade List (USER_DATA)

        https://binance-docs.github.io/apidocs/voptions/en/#option-trade-list-user_data

        :param symbol: required - Option trading pair - BTC-200730-9000-C
        :type symbol: str
        :param fromId: optional - Trade id to fetch from. Default gets most recent trades. - 4611875134427365376
        :type fromId: int
        :param startTime: optional - Start Time - 1593511200000
        :type startTime: int
        :param endTime: optional - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - Number of result sets returned Default:100 Max:1000 - 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_options_api('get', 'userTrades', signed=True, data=params)

    # Fiat Endpoints

    def get_fiat_deposit_withdraw_history(self, **params):
        """Get Fiat Deposit/Withdraw History

        https://binance-docs.github.io/apidocs/spot/en/#get-fiat-deposit-withdraw-history-user_data

        :param transactionType: required - 0-deposit,1-withdraw
        :type transactionType: str
        :param beginTime: optional
        :type beginTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional - default 1
        :type page: int
        :param rows: optional - default 100, max 500
        :type rows: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_margin_api('get', 'fiat/orders', signed=True, data=params)

    def get_fiat_payments_history(self, **params):
        """Get Fiat Payments History

        https://binance-docs.github.io/apidocs/spot/en/#get-fiat-payments-history-user_data

        :param transactionType: required - 0-buy,1-sell
        :type transactionType: str
        :param beginTime: optional
        :type beginTime: int
        :param endTime: optional
        :type endTime: int
        :param page: optional - default 1
        :type page: int
        :param rows: optional - default 100, max 500
        :type rows: int
        :param recvWindow: optional
        :type recvWindow: int

        """
        return self._request_margin_api('get', 'fiat/payments', signed=True, data=params)

    # C2C Endpoints

    def get_c2c_trade_history(self, **params):
        """Get C2C Trade History

        https://binance-docs.github.io/apidocs/spot/en/#get-c2c-trade-history-user_data

        :param tradeType: required - BUY, SELL
        :type tradeType: str
        :param startTimestamp: optional
        :type startTime: int
        :param endTimestamp: optional
        :type endTimestamp: int
        :param page: optional - default 1
        :type page: int
        :param rows: optional - default 100, max 100
        :type rows: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

            {
                "code": "000000",
                "message": "success",
                "data": [
                    {
                        "orderNumber":"20219644646554779648",
                        "advNo": "11218246497340923904",
                        "tradeType": "SELL",
                        "asset": "BUSD",
                        "fiat": "CNY",
                        "fiatSymbol": "￥",
                        "amount": "5000.00000000",  // Quantity (in Crypto)
                        "totalPrice": "33400.00000000",
                        "unitPrice": "6.68", // Unit Price (in Fiat)
                        "orderStatus": "COMPLETED",  // PENDING, TRADING, BUYER_PAYED, DISTRIBUTING, COMPLETED, IN_APPEAL, CANCELLED, CANCELLED_BY_SYSTEM
                        "createTime": 1619361369000,
                        "commission": "0",   // Transaction Fee (in Crypto)
                        "counterPartNickName": "ab***",
                        "advertisementRole": "TAKER"
                    }
                ],
                "total": 1,
                "success": true
            }

        """
        return self._request_margin_api('get', 'c2c/orderMatch/listUserOrderHistory', signed=True, data=params)

    # Pay Endpoints

    def get_pay_trade_history(self, **params):
        """Get C2C Trade History

        https://binance-docs.github.io/apidocs/spot/en/#pay-endpoints

        :param startTime: optional
        :type startTime: int
        :param endTime: optional
        :type endTime: int
        :param limit: optional - default 100, max 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_margin_api('get', 'pay/transactions', signed=True, data=params)

    # Convert Endpoints

    def get_convert_trade_history(self, **params):
        """Get C2C Trade History

        https://binance-docs.github.io/apidocs/spot/en/#pay-endpoints

        :param startTime: required - Start Time - 1593511200000
        :type startTime: int
        :param endTime: required - End Time - 1593511200000
        :type endTime: int
        :param limit: optional - default 100, max 100
        :type limit: int
        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_margin_api('get', 'convert/tradeFlow', signed=True, data=params)

    def convert_request_quote(self, **params):
        """Request a quote for the requested token pairs

        https://binance-docs.github.io/apidocs/spot/en/#send-quote-request-user_data

        :param fromAsset: required - Asset to convert from - BUSD
        :type fromAsset: str
        :param toAsset: required - Asset to convert to - BTC
        :type toAsset: str
        :param fromAmount: EITHER - When specified, it is the amount you will be debited after the conversion
        :type fromAmount: decimal
        :param toAmount: EITHER - When specified, it is the amount you will be credited after the conversion
        :type toAmount: decimal

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_margin_api('post', 'convert/getQuote', signed=True, data=params)

    def convert_accept_quote(self, **params):
        """Accept the offered quote by quote ID.

        https://binance-docs.github.io/apidocs/spot/en/#accept-quote-trade

        :param quoteId: required - 457235734584567
        :type quoteId: str

        :param recvWindow: optional
        :type recvWindow: int

        :returns: API response

        """
        return self._request_margin_api('post', 'convert/acceptQuote', signed=True, data=params)

    def close_connection(self):
        if self.session:
            self.session.close()

    def __del__(self):
        self.close_connection()


class AsyncClient(BaseClient):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com',
        base_endpoint: str = BaseClient.BASE_ENDPOINT_DEFAULT,
        testnet: bool = False, loop=None, session_params: Optional[Dict[str, Any]] = None,
        private_key: Optional[Union[str, Path]] = None, private_key_pass: Optional[str] = None,
    ):

        self.loop = loop or get_loop()
        self._session_params: Dict[str, Any] = session_params or {}
        super().__init__(api_key, api_secret, requests_params, tld, base_endpoint, testnet, private_key, private_key_pass)

    @classmethod
    async def create(
        cls, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com',
        base_endpoint: str = BaseClient.BASE_ENDPOINT_DEFAULT,
        testnet: bool = False, loop=None, session_params: Optional[Dict[str, Any]] = None
    ):

        self = cls(api_key, api_secret, requests_params, tld, base_endpoint, testnet, loop, session_params)

        try:
            await self.ping()

            # calculate timestamp offset between local and binance server
            res = await self.get_server_time()
            self.timestamp_offset = res['serverTime'] - int(time.time() * 1000)

            return self
        except Exception:
            # If ping throw an exception, the current self must be cleaned
            # else, we can receive a "asyncio:Unclosed client session"
            await self.close_connection()
            raise

    def _init_session(self) -> aiohttp.ClientSession:

        session = aiohttp.ClientSession(
            loop=self.loop,
            headers=self._get_headers(),
            **self._session_params
        )
        return session

    async def close_connection(self):
        if self.session:
            assert self.session
            await self.session.close()

    async def _request(self, method, uri: str, signed: bool, force_params: bool = False, **kwargs):

        kwargs = self._get_request_kwargs(method, signed, force_params, **kwargs)

        async with getattr(self.session, method)(uri, **kwargs) as response:
            self.response = response
            return await self._handle_response(response)

    async def _handle_response(self, response: aiohttp.ClientResponse):
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
            raise BinanceRequestException(f'Invalid Response: {txt}')

    async def _request_api(self, method, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        uri = self._create_api_uri(path, signed, version)
        return await self._request(method, uri, signed, **kwargs)

    async def _request_futures_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_futures_api_uri(path, version=version)

        return await self._request(method, uri, signed, True, **kwargs)

    async def _request_futures_data_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_futures_data_api_uri(path)

        return await self._request(method, uri, signed, True, **kwargs)

    async def _request_futures_coin_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_futures_coin_api_url(path, version=version)

        return await self._request(method, uri, signed, True, **kwargs)

    async def _request_futures_coin_data_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_futures_coin_data_api_url(path, version=version)

        return await self._request(method, uri, signed, True, **kwargs)

    async def _request_options_api(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_options_api_uri(path)

        return await self._request(method, uri, signed, True, **kwargs)

    async def _request_margin_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_margin_api_uri(path, version)

        return await self._request(method, uri, signed, **kwargs)

    async def _request_website(self, method, path, signed=False, **kwargs) -> Dict:
        uri = self._create_website_uri(path)
        return await self._request(method, uri, signed, **kwargs)

    async def _get(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs):
        return await self._request_api('get', path, signed, version, **kwargs)

    async def _post(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return await self._request_api('post', path, signed, version, **kwargs)

    async def _put(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return await self._request_api('put', path, signed, version, **kwargs)

    async def _delete(self, path, signed=False, version=BaseClient.PUBLIC_API_VERSION, **kwargs) -> Dict:
        return await self._request_api('delete', path, signed, version, **kwargs)

    # Exchange Endpoints

    async def get_products(self) -> Dict:
        products = await self._request_website('get', 'exchange-api/v1/public/asset-service/product/get-products')
        return products
    get_products.__doc__ = Client.get_products.__doc__

    async def get_exchange_info(self) -> Dict:
        return await self._get('exchangeInfo', version=self.PRIVATE_API_VERSION)
    get_exchange_info.__doc__ = Client.get_exchange_info.__doc__

    async def get_symbol_info(self, symbol) -> Optional[Dict]:
        res = await self.get_exchange_info()

        for item in res['symbols']:
            if item['symbol'] == symbol.upper():
                return item

        return None
    get_symbol_info.__doc__ = Client.get_symbol_info.__doc__

    # General Endpoints

    async def ping(self) -> Dict:
        return await self._get('ping', version=self.PRIVATE_API_VERSION)
    ping.__doc__ = Client.ping.__doc__

    async def get_server_time(self) -> Dict:
        return await self._get('time', version=self.PRIVATE_API_VERSION)
    get_server_time.__doc__ = Client.get_server_time.__doc__

    # Market Data Endpoints

    async def get_all_tickers(self, symbol: Optional[str] = None) -> List[Dict[str, str]]:
        params = {}
        if symbol:
            params['symbol'] = symbol
        return await self._get('ticker/price', version=self.PRIVATE_API_VERSION, data=params)
    get_all_tickers.__doc__ = Client.get_all_tickers.__doc__

    async def get_orderbook_tickers(self, **params) -> Dict:
        data = {}
        if "symbol" in params:
            data["symbol"] = params["symbol"]
        elif "symbols" in params:
            data["symbols"] = params["symbols"]
        return await self._get('ticker/bookTicker', data=data, version=self.PRIVATE_API_VERSION)
    get_orderbook_tickers.__doc__ = Client.get_orderbook_tickers.__doc__

    async def get_order_book(self, **params) -> Dict:
        return await self._get('depth', data=params, version=self.PRIVATE_API_VERSION)
    get_order_book.__doc__ = Client.get_order_book.__doc__

    async def get_recent_trades(self, **params) -> Dict:
        return await self._get('trades', data=params)
    get_recent_trades.__doc__ = Client.get_recent_trades.__doc__

    async def get_historical_trades(self, **params) -> Dict:
        return await self._get('historicalTrades', data=params, version=self.PRIVATE_API_VERSION)
    get_historical_trades.__doc__ = Client.get_historical_trades.__doc__

    async def get_aggregate_trades(self, **params) -> Dict:
        return await self._get('aggTrades', data=params, version=self.PRIVATE_API_VERSION)
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

    async def get_klines(self, **params) -> Dict:
        return await self._get('klines', data=params, version=self.PRIVATE_API_VERSION)
    get_klines.__doc__ = Client.get_klines.__doc__

    async def _klines(self, klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT, **params) -> Dict:
        if 'endTime' in params and not params['endTime']:
            del params['endTime']
        if HistoricalKlinesType.SPOT == klines_type:
            return await self.get_klines(**params)
        elif HistoricalKlinesType.FUTURES == klines_type:
            return await self.futures_klines(**params)
        elif HistoricalKlinesType.FUTURES_COIN == klines_type:
            return await self.futures_coin_klines(**params)
        else:
            raise NotImplementedException(klines_type)
    _klines.__doc__ = Client._klines.__doc__

    async def _get_earliest_valid_timestamp(self, symbol, interval,
                                            klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        kline = await self._klines(
            klines_type=klines_type,
            symbol=symbol,
            interval=interval,
            limit=1,
            startTime=0,
            endTime=int(time.time() * 1000)
        )
        return kline[0][0]
    _get_earliest_valid_timestamp.__doc__ = Client._get_earliest_valid_timestamp.__doc__

    async def get_historical_klines(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                                    klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        return await self._historical_klines(symbol, interval, start_str, end_str=end_str, limit=limit, klines_type=klines_type)
    get_historical_klines.__doc__ = Client.get_historical_klines.__doc__

    async def _historical_klines(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                                 klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):

        # init our list
        output_data = []

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # establish first available start timestamp
        start_ts = convert_ts_str(start_str)
        if start_ts is not None:
            first_valid_ts = await self._get_earliest_valid_timestamp(symbol, interval, klines_type)
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
                endTime=end_ts
            )

            # append this loops data to our output data
            if temp_data:
                output_data += temp_data

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

    async def get_historical_klines_generator(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                                              klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):
        return self._historical_klines_generator(
            symbol, interval, start_str, end_str=end_str, limit=limit, klines_type=klines_type
        )
    get_historical_klines_generator.__doc__ = Client.get_historical_klines_generator.__doc__

    async def _historical_klines_generator(self, symbol, interval, start_str=None, end_str=None, limit=1000,
                                           klines_type: HistoricalKlinesType = HistoricalKlinesType.SPOT):

        # convert interval to useful value in seconds
        timeframe = interval_to_milliseconds(interval)

        # if a start time was passed convert it
        start_ts = convert_ts_str(start_str)

        # establish first available start timestamp
        if start_ts is not None:
            first_valid_ts = await self._get_earliest_valid_timestamp(symbol, interval, klines_type)
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
                endTime=end_ts
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
        return await self._get('avgPrice', data=params, version=self.PRIVATE_API_VERSION)
    get_avg_price.__doc__ = Client.get_avg_price.__doc__

    async def get_ticker(self, **params):
        return await self._get('ticker/24hr', data=params, version=self.PRIVATE_API_VERSION)
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

    async def create_oco_order(self, **params):
        return await self._post('order/oco', True, data=params)
    create_oco_order.__doc__ = Client.create_oco_order.__doc__

    async def order_oco_buy(self, **params):
        params.update({
            'side': self.SIDE_BUY
        })
        return await self.create_oco_order(**params)
    order_oco_buy.__doc__ = Client.order_oco_buy.__doc__

    async def order_oco_sell(self, **params):
        params.update({
            'side': self.SIDE_SELL
        })
        return await self.create_oco_order(**params)
    order_oco_sell.__doc__ = Client.order_oco_sell.__doc__

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

    async def get_open_oco_orders(self, **params):
        return await self._get('openOrderList', True, data=params)
    get_open_oco_orders.__doc__ = Client.get_open_oco_orders.__doc__

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

    async def get_current_order_count(self):
        return await self._get('rateLimit/order', True)
    get_current_order_count.__doc__ = Client.get_current_order_count.__doc__

    async def get_prevented_matches(self, **params):
        return await self._get('myPreventedMatches', True, data=params)
    get_prevented_matches.__doc__ = Client.get_prevented_matches.__doc__

    async def get_allocations(self, **params):
        return await self._get('myAllocations', True, data=params)
    get_allocations.__doc__ = Client.get_allocations.__doc__

    async def get_system_status(self):
        return await self._request_margin_api('get', 'system/status')
    get_system_status.__doc__ = Client.get_system_status.__doc__

    async def get_account_status(self, **params):
        return await self._request_margin_api('get', 'account/status', True, data=params)
    get_account_status.__doc__ = Client.get_account_status.__doc__

    async def get_account_api_trading_status(self, **params):
        return await self._request_margin_api('get', 'account/apiTradingStatus', True, data=params)
    get_account_api_trading_status.__doc__ = Client.get_account_api_trading_status.__doc__

    async def get_account_api_permissions(self, **params):
        return await self._request_margin_api('get', 'account/apiRestrictions', True, data=params)
    get_account_api_permissions.__doc__ = Client.get_account_api_permissions.__doc__

    async def get_dust_assets(self, **params):
        return await self._request_margin_api('post', 'asset/dust-btc', True, data=params)
    get_dust_assets.__doc__ = Client.get_dust_assets.__doc__

    async def get_dust_log(self, **params):
        return await self._request_margin_api('get', 'asset/dribblet', True, data=params)
    get_dust_log.__doc__ = Client.get_dust_log.__doc__

    async def transfer_dust(self, **params):
        return await self._request_margin_api('post', 'asset/dust', True, data=params)
    transfer_dust.__doc__ = Client.transfer_dust.__doc__

    async def get_asset_dividend_history(self, **params):
        return await self._request_margin_api('get', 'asset/assetDividend', True, data=params)
    get_asset_dividend_history.__doc__ = Client.get_asset_dividend_history.__doc__

    async def make_universal_transfer(self, **params):
        return await self._request_margin_api('post', 'asset/transfer', signed=True, data=params)
    make_universal_transfer.__doc__ = Client.make_universal_transfer.__doc__

    async def query_universal_transfer_history(self, **params):
        return await self._request_margin_api('get', 'asset/transfer', signed=True, data=params)
    query_universal_transfer_history.__doc__ = Client.query_universal_transfer_history.__doc__

    async def get_trade_fee(self, **params):
        return await self._request_margin_api('get', 'asset/tradeFee', True, data=params)
    get_trade_fee.__doc__ = Client.get_trade_fee.__doc__

    async def get_asset_details(self, **params):
        return await self._request_margin_api('get', 'asset/assetDetail', True, data=params)
    get_asset_details.__doc__ = Client.get_asset_details.__doc__

    # Withdraw Endpoints

    async def withdraw(self, **params):
        # force a name for the withdrawal if one not set
        if 'coin' in params and 'name' not in params:
            params['name'] = params['coin']
        return await self._request_margin_api('post', 'capital/withdraw/apply', True, data=params)
    withdraw.__doc__ = Client.withdraw.__doc__

    async def get_deposit_history(self, **params):
        return await self._request_margin_api('get', 'capital/deposit/hisrec', True, data=params)
    get_deposit_history.__doc__ = Client.get_deposit_history.__doc__

    async def get_withdraw_history(self, **params):
        return await self._request_margin_api('get', 'capital/withdraw/history', True, data=params)
    get_withdraw_history.__doc__ = Client.get_withdraw_history.__doc__

    async def get_withdraw_history_id(self, withdraw_id, **params):
        result = await self.get_withdraw_history(**params)

        for entry in result:
            if 'id' in entry and entry['id'] == withdraw_id:
                return entry

        raise Exception("There is no entry with withdraw id", result)
    get_withdraw_history_id.__doc__ = Client.get_withdraw_history_id.__doc__

    async def get_deposit_address(self, coin: str, network: Optional[str] = None, **params):
        params['coin'] = coin
        if network:
            params['network'] = network
        return await self._request_margin_api('get', 'capital/deposit/address', True, data=params)
    get_deposit_address.__doc__ = Client.get_deposit_address.__doc__

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

    # Margin Trading Endpoints
    async def get_margin_account(self, **params):
        return await self._request_margin_api('get', 'margin/account', True, data=params)
    get_margin_account.__doc__ = Client.get_margin_account.__doc__

    async def get_isolated_margin_account(self, **params):
        return await self._request_margin_api('get', 'margin/isolated/account', True, data=params)
    get_isolated_margin_account.__doc__ = Client.get_isolated_margin_account.__doc__

    async def enable_isolated_margin_account(self, **params):
        return await self._request_margin_api('post', 'margin/isolated/account', True, data=params)
    enable_isolated_margin_account.__doc__ = Client.enable_isolated_margin_account.__doc__

    async def disable_isolated_margin_account(self, **params):
        return await self._request_margin_api('delete', 'margin/isolated/account', True, data=params)
    disable_isolated_margin_account.__doc__ = Client.disable_isolated_margin_account.__doc__

    async def get_margin_asset(self, **params):
        return await self._request_margin_api('get', 'margin/asset', data=params)
    get_margin_asset.__doc__ = Client.get_margin_asset.__doc__

    async def get_margin_symbol(self, **params):
        return await self._request_margin_api('get', 'margin/pair', data=params)
    get_margin_symbol.__doc__ = Client.get_margin_symbol.__doc__

    async def get_margin_all_assets(self, **params):
        return await self._request_margin_api('get', 'margin/allAssets', data=params)
    get_margin_all_assets.__doc__ = Client.get_margin_all_assets.__doc__

    async def get_margin_all_pairs(self, **params):
        return await self._request_margin_api('get', 'margin/allPairs', data=params)
    get_margin_all_pairs.__doc__ = Client.get_margin_all_pairs.__doc__

    async def create_isolated_margin_account(self, **params):
        return await self._request_margin_api('post', 'margin/isolated/create', signed=True, data=params)
    create_isolated_margin_account.__doc__ = Client.create_isolated_margin_account.__doc__

    async def get_isolated_margin_symbol(self, **params):
        return await self._request_margin_api('get', 'margin/isolated/pair', signed=True, data=params)
    get_isolated_margin_symbol.__doc__ = Client.get_isolated_margin_symbol.__doc__

    async def get_all_isolated_margin_symbols(self, **params):
        return await self._request_margin_api('get', 'margin/isolated/allPairs', signed=True, data=params)
    get_all_isolated_margin_symbols.__doc__ = Client.get_all_isolated_margin_symbols.__doc__

    async def toggle_bnb_burn_spot_margin(self, **params):
        return await self._request_margin_api('post', 'bnbBurn', signed=True, data=params)
    toggle_bnb_burn_spot_margin.__doc__ = Client.toggle_bnb_burn_spot_margin.__doc__

    async def get_bnb_burn_spot_margin(self, **params):
        return await self._request_margin_api('get', 'bnbBurn', signed=True, data=params)
    get_bnb_burn_spot_margin.__doc__ = Client.get_bnb_burn_spot_margin.__doc__

    async def get_margin_price_index(self, **params):
        return await self._request_margin_api('get', 'margin/priceIndex', data=params)
    get_margin_price_index.__doc__ = Client.get_margin_price_index.__doc__

    async def transfer_margin_to_spot(self, **params):
        params['type'] = 2
        return await self._request_margin_api('post', 'margin/transfer', signed=True, data=params)
    transfer_margin_to_spot.__doc__ = Client.transfer_margin_to_spot.__doc__

    async def transfer_spot_to_margin(self, **params):
        params['type'] = 1
        return await self._request_margin_api('post', 'margin/transfer', signed=True, data=params)
    transfer_spot_to_margin.__doc__ = Client.transfer_spot_to_margin.__doc__

    async def transfer_isolated_margin_to_spot(self, **params):
        params['transFrom'] = "ISOLATED_MARGIN"
        params['transTo'] = "SPOT"
        return await self._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)
    transfer_isolated_margin_to_spot.__doc__ = Client.transfer_isolated_margin_to_spot.__doc__

    async def transfer_spot_to_isolated_margin(self, **params):
        params['transFrom'] = "SPOT"
        params['transTo'] = "ISOLATED_MARGIN"
        return await self._request_margin_api('post', 'margin/isolated/transfer', signed=True, data=params)
    transfer_spot_to_isolated_margin.__doc__ = Client.transfer_spot_to_isolated_margin.__doc__

    async def create_margin_loan(self, **params):
        return await self._request_margin_api('post', 'margin/loan', signed=True, data=params)
    create_margin_loan.__doc__ = Client.create_margin_loan.__doc__

    async def repay_margin_loan(self, **params):
        return await self._request_margin_api('post', 'margin/repay', signed=True, data=params)
    repay_margin_loan.__doc__ = Client.repay_margin_loan.__doc__

    async def create_margin_order(self, **params):
        return await self._request_margin_api('post', 'margin/order', signed=True, data=params)
    create_margin_order.__doc__ = Client.create_margin_order.__doc__

    async def cancel_margin_order(self, **params):
        return await self._request_margin_api('delete', 'margin/order', signed=True, data=params)
    cancel_margin_order.__doc__ = Client.cancel_margin_order.__doc__

    async def set_margin_max_leverage(self, **params):
        return await self._request_margin_api('post', 'margin/max-leverage', signed=True, data=params)
    set_margin_max_leverage.__doc__ = Client.set_margin_max_leverage.__doc__

    async def get_margin_transfer_history(self, **params):
        return await self._request_margin_api('get', 'margin/transfer', signed=True, data=params)
    get_margin_transfer_history.__doc__ = Client.get_margin_transfer_history.__doc__

    async def get_margin_loan_details(self, **params):
        return await self._request_margin_api('get', 'margin/loan', signed=True, data=params)
    get_margin_loan_details.__doc__ = Client.get_margin_loan_details.__doc__

    async def get_margin_repay_details(self, **params):
        return await self._request_margin_api('get', 'margin/repay', signed=True, data=params)

    async def get_cross_margin_data(self, **params):
        return await self._request_margin_api('get', 'margin/crossMarginData', signed=True, data=params)

    async def get_margin_interest_history(self, **params):
        return await self._request_margin_api('get', 'margin/interestHistory', signed=True, data=params)

    async def get_margin_force_liquidation_rec(self, **params):
        return await self._request_margin_api('get', 'margin/forceLiquidationRec', signed=True, data=params)

    async def get_margin_order(self, **params):
        return await self._request_margin_api('get', 'margin/order', signed=True, data=params)

    async def get_open_margin_orders(self, **params):
        return await self._request_margin_api('get', 'margin/openOrders', signed=True, data=params)

    async def get_all_margin_orders(self, **params):
        return await self._request_margin_api('get', 'margin/allOrders', signed=True, data=params)

    async def get_margin_trades(self, **params):
        return await self._request_margin_api('get', 'margin/myTrades', signed=True, data=params)

    async def get_max_margin_loan(self, **params):
        return await self._request_margin_api('get', 'margin/maxBorrowable', signed=True, data=params)

    async def get_max_margin_transfer(self, **params):
        return await self._request_margin_api('get', 'margin/maxTransferable', signed=True, data=params)

    # Margin OCO

    async def create_margin_oco_order(self, **params):
        return await self._request_margin_api('post', 'margin/order/oco', signed=True, data=params)

    async def cancel_margin_oco_order(self, **params):
        return await self._request_margin_api('delete', 'margin/orderList', signed=True, data=params)

    async def get_margin_oco_order(self, **params):
        return await self._request_margin_api('get', 'margin/orderList', signed=True, data=params)

    async def get_open_margin_oco_orders(self, **params):
        return await self._request_margin_api('get', 'margin/allOrderList', signed=True, data=params)

    # Cross-margin

    async def margin_stream_get_listen_key(self):
        res = await self._request_margin_api('post', 'userDataStream', signed=False, data={})
        return res['listenKey']

    async def margin_stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._request_margin_api('put', 'userDataStream', signed=False, data=params)

    async def margin_stream_close(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._request_margin_api('delete', 'userDataStream', signed=False, data=params)

        # Isolated margin

    async def isolated_margin_stream_get_listen_key(self, symbol):
        params = {
            'symbol': symbol
        }
        res = await self._request_margin_api('post', 'userDataStream/isolated', signed=False, data=params)
        return res['listenKey']

    async def isolated_margin_stream_keepalive(self, symbol, listenKey):
        params = {
            'symbol': symbol,
            'listenKey': listenKey
        }
        return await self._request_margin_api('put', 'userDataStream/isolated', signed=False, data=params)

    async def isolated_margin_stream_close(self, symbol, listenKey):
        params = {
            'symbol': symbol,
            'listenKey': listenKey
        }
        return await self._request_margin_api('delete', 'userDataStream/isolated', signed=False, data=params)

    # Lending Endpoints

    async def get_lending_product_list(self, **params):
        return await self._request_margin_api('get', 'lending/daily/product/list', signed=True, data=params)

    async def get_lending_daily_quota_left(self, **params):
        return await self._request_margin_api('get', 'lending/daily/userLeftQuota', signed=True, data=params)

    async def purchase_lending_product(self, **params):
        return await self._request_margin_api('post', 'lending/daily/purchase', signed=True, data=params)

    async def get_lending_daily_redemption_quota(self, **params):
        return await self._request_margin_api('get', 'lending/daily/userRedemptionQuota', signed=True, data=params)

    async def redeem_lending_product(self, **params):
        return await self._request_margin_api('post', 'lending/daily/redeem', signed=True, data=params)

    async def get_lending_position(self, **params):
        return await self._request_margin_api('get', 'lending/daily/token/position', signed=True, data=params)

    async def get_fixed_activity_project_list(self, **params):
        return await self._request_margin_api('get', 'lending/project/list', signed=True, data=params)

    async def get_lending_account(self, **params):
        return await self._request_margin_api('get', 'lending/union/account', signed=True, data=params)

    async def get_lending_purchase_history(self, **params):
        return await self._request_margin_api('get', 'lending/union/purchaseRecord', signed=True, data=params)

    async def get_lending_redemption_history(self, **params):
        return await self._request_margin_api('get', 'lending/union/redemptionRecord', signed=True, data=params)

    async def get_lending_interest_history(self, **params):
        return await self._request_margin_api('get', 'lending/union/interestHistory', signed=True, data=params)

    async def change_fixed_activity_to_daily_position(self, **params):
        return await self._request_margin_api('post', 'lending/positionChanged', signed=True, data=params)

    # Staking Endpoints

    async def get_staking_product_list(self, **params):
        return await self._request_margin_api('get', 'staking/productList', signed=True, data=params)

    async def purchase_staking_product(self, **params):
        return await self._request_margin_api('post', 'staking/purchase', signed=True, data=params)

    async def redeem_staking_product(self, **params):
        return await self._request_margin_api('post', 'staking/redeem', signed=True, data=params)

    async def get_staking_position(self, **params):
        return await self._request_margin_api('get', 'staking/position', signed=True, data=params)

    async def get_staking_purchase_history(self, **params):
        return await self._request_margin_api('get', 'staking/purchaseRecord', signed=True, data=params)

    async def set_auto_staking(self, **params):
        return await self._request_margin_api('post', 'staking/setAutoStaking', signed=True, data=params)

    async def get_personal_left_quota(self, **params):
        return await self._request_margin_api('get', 'staking/personalLeftQuota', signed=True, data=params)

    # US Staking Endpoints

    async def get_staking_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("get", "staking/asset", True, data=params)
    get_staking_asset_us.__doc__ = Client.get_staking_asset_us.__doc__

    async def stake_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("post", "staking/stake", True, data=params)
    stake_asset_us.__doc__ = Client.stake_asset_us.__doc__

    async def unstake_asset_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("post", "staking/unstake", True, data=params)
    unstake_asset_us.__doc__ = Client.unstake_asset_us.__doc__

    async def get_staking_balance_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("get", "staking/stakingBalance", True, data=params)
    get_staking_balance_us.__doc__ = Client.get_staking_balance_us.__doc__

    async def get_staking_history_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("get", "staking/history", True, data=params)
    get_staking_history_us.__doc__ = Client.get_staking_history_us.__doc__

    async def get_staking_rewards_history_us(self, **params):
        assert self.tld == "us", "Endpoint only available on binance.us"
        return await self._request_margin_api("get", "staking/stakingRewardsHistory", True, data=params)
    get_staking_rewards_history_us.__doc__ = Client.get_staking_rewards_history_us.__doc__

    # Sub Accounts

    async def get_sub_account_list(self, **params):
        return await self._request_margin_api('get', 'sub-account/list', True, data=params)

    async def get_sub_account_transfer_history(self, **params):
        return await self._request_margin_api('get', 'sub-account/sub/transfer/history', True, data=params)

    async def get_sub_account_futures_transfer_history(self, **params):
        return await self._request_margin_api('get', 'sub-account/futures/internalTransfer', True, data=params)

    async def create_sub_account_futures_transfer(self, **params):
        return await self._request_margin_api('post', 'sub-account/futures/internalTransfer', True, data=params)

    async def get_sub_account_assets(self, **params):
        return await self._request_margin_api('get', 'sub-account/assets', True, data=params, version=4)

    async def query_subaccount_spot_summary(self, **params):
        return await self._request_margin_api('get', 'sub-account/spotSummary', True, data=params)

    async def get_subaccount_deposit_address(self, **params):
        return await self._request_margin_api('get', 'capital/deposit/subAddress', True, data=params)

    async def get_subaccount_deposit_history(self, **params):
        return await self._request_margin_api('get', 'capital/deposit/subHisrec', True, data=params)

    async def get_subaccount_futures_margin_status(self, **params):
        return await self._request_margin_api('get', 'sub-account/status', True, data=params)

    async def enable_subaccount_margin(self, **params):
        return await self._request_margin_api('post', 'sub-account/margin/enable', True, data=params)

    async def get_subaccount_margin_details(self, **params):
        return await self._request_margin_api('get', 'sub-account/margin/account', True, data=params)

    async def get_subaccount_margin_summary(self, **params):
        return await self._request_margin_api('get', 'sub-account/margin/accountSummary', True, data=params)

    async def enable_subaccount_futures(self, **params):
        return await self._request_margin_api('post', 'sub-account/futures/enable', True, data=params)

    async def get_subaccount_futures_details(self, **params):
        return await self._request_margin_api('get', 'sub-account/futures/account', True, data=params, version=2)

    async def get_subaccount_futures_summary(self, **params):
        return await self._request_margin_api('get', 'sub-account/futures/accountSummary', True, data=params, version=2)

    async def get_subaccount_futures_positionrisk(self, **params):
        return await self._request_margin_api('get', 'sub-account/futures/positionRisk', True, data=params, version=2)

    async def make_subaccount_futures_transfer(self, **params):
        return await self._request_margin_api('post', 'sub-account/futures/transfer', True, data=params)

    async def make_subaccount_margin_transfer(self, **params):
        return await self._request_margin_api('post', 'sub-account/margin/transfer', True, data=params)

    async def make_subaccount_to_subaccount_transfer(self, **params):
        return await self._request_margin_api('post', 'sub-account/transfer/subToSub', True, data=params)

    async def make_subaccount_to_master_transfer(self, **params):
        return await self._request_margin_api('post', 'sub-account/transfer/subToMaster', True, data=params)

    async def get_subaccount_transfer_history(self, **params):
        return await self._request_margin_api('get', 'sub-account/transfer/subUserHistory', True, data=params)

    async def make_subaccount_universal_transfer(self, **params):
        return await self._request_margin_api('post', 'sub-account/universalTransfer', True, data=params)

    async def get_universal_transfer_history(self, **params):
        return await self._request_margin_api('get', 'sub-account/universalTransfer', True, data=params)

    # Futures API

    async def futures_ping(self):
        return await self._request_futures_api('get', 'ping')

    async def futures_time(self):
        return await self._request_futures_api('get', 'time')

    async def futures_exchange_info(self):
        return await self._request_futures_api('get', 'exchangeInfo')

    async def futures_order_book(self, **params):
        return await self._request_futures_api('get', 'depth', data=params)

    async def futures_recent_trades(self, **params):
        return await self._request_futures_api('get', 'trades', data=params)

    async def futures_historical_trades(self, **params):
        return await self._request_futures_api('get', 'historicalTrades', data=params)

    async def futures_aggregate_trades(self, **params):
        return await self._request_futures_api('get', 'aggTrades', data=params)

    async def futures_klines(self, **params):
        return await self._request_futures_api('get', 'klines', data=params)

    async def futures_continous_klines(self, **params):
        return await self._request_futures_api('get', 'continuousKlines', data=params)

    async def futures_historical_klines(self, symbol, interval, start_str, end_str=None, limit=500):
        return await self._historical_klines(symbol, interval, start_str, end_str=end_str, limit=limit, klines_type=HistoricalKlinesType.FUTURES)

    async def futures_historical_klines_generator(self, symbol, interval, start_str, end_str=None):
        return self._historical_klines_generator(symbol, interval, start_str, end_str=end_str, klines_type=HistoricalKlinesType.FUTURES)

    async def futures_mark_price(self, **params):
        return await self._request_futures_api('get', 'premiumIndex', data=params)

    async def futures_funding_rate(self, **params):
        return await self._request_futures_api('get', 'fundingRate', data=params)

    async def futures_top_longshort_account_ratio(self, **params):
        return await self._request_futures_data_api('get', 'topLongShortAccountRatio', data=params)

    async def futures_top_longshort_position_ratio(self, **params):
        return await self._request_futures_data_api('get', 'topLongShortPositionRatio', data=params)

    async def futures_global_longshort_ratio(self, **params):
        return await self._request_futures_data_api('get', 'globalLongShortAccountRatio', data=params)

    async def futures_ticker(self, **params):
        return await self._request_futures_api('get', 'ticker/24hr', data=params)

    async def futures_symbol_ticker(self, **params):
        return await self._request_futures_api('get', 'ticker/price', data=params)

    async def futures_orderbook_ticker(self, **params):
        return await self._request_futures_api('get', 'ticker/bookTicker', data=params)

    async def futures_liquidation_orders(self, **params):
        return await self._request_futures_api('get', 'forceOrders', signed=True, data=params)

    async def futures_api_trading_status(self, **params):
        return await self._request_futures_api('get', 'apiTradingStatus', signed=True, data=params)

    async def futures_comission_rate(self, **params):
        return await self._request_futures_api('get', 'commissionRate', signed=True, data=params)

    async def futures_adl_quantile_estimate(self, **params):
        return await self._request_futures_api('get', 'adlQuantile', signed=True, data=params)

    async def futures_open_interest(self, **params):
        return await self._request_futures_api('get', 'openInterest', data=params)

    async def futures_index_info(self, **params):
        return await self._request_futures_api('get', 'indexInfo', data=params)

    async def futures_open_interest_hist(self, **params):
        return await self._request_futures_data_api('get', 'openInterestHist', data=params)

    async def futures_leverage_bracket(self, **params):
        return await self._request_futures_api('get', 'leverageBracket', True, data=params)

    async def futures_account_transfer(self, **params):
        return await self._request_margin_api('post', 'futures/transfer', True, data=params)

    async def transfer_history(self, **params):
        return await self._request_margin_api('get', 'futures/transfer', True, data=params)

    async def futures_loan_borrow_history(self, **params):
        return await self._request_margin_api('get', 'futures/loan/borrow/history', True, data=params)

    async def futures_loan_repay_history(self, **params):
        return await self._request_margin_api('get', 'futures/loan/repay/history', True, data=params)

    async def futures_loan_wallet(self, **params):
        return await self._request_margin_api('get', 'futures/loan/wallet', True, data=params, version=2)

    async def futures_cross_collateral_adjust_history(self, **params):
        return await self._request_margin_api('get', 'futures/loan/adjustCollateral/history', True, data=params)

    async def futures_cross_collateral_liquidation_history(self, **params):
        return await self._request_margin_api('get', 'futures/loan/liquidationHistory', True, data=params)

    async def futures_loan_interest_history(self, **params):
        return await self._request_margin_api('get', 'futures/loan/interestHistory', True, data=params)

    async def futures_create_order(self, **params):
        return await self._request_futures_api('post', 'order', True, data=params)

    async def futures_place_batch_order(self, **params):
        query_string = urlencode(params)
        query_string = query_string.replace('%27', '%22')
        params['batchOrders'] = query_string[12:]
        return await self._request_futures_api('post', 'batchOrders', True, data=params)

    async def futures_get_order(self, **params):
        return await self._request_futures_api('get', 'order', True, data=params)

    async def futures_get_open_orders(self, **params):
        return await self._request_futures_api('get', 'openOrders', True, data=params)

    async def futures_get_all_orders(self, **params):
        return await self._request_futures_api('get', 'allOrders', True, data=params)

    async def futures_cancel_order(self, **params):
        return await self._request_futures_api('delete', 'order', True, data=params)

    async def futures_cancel_all_open_orders(self, **params):
        return await self._request_futures_api('delete', 'allOpenOrders', True, data=params)

    async def futures_cancel_orders(self, **params):
        return await self._request_futures_api('delete', 'batchOrders', True, data=params)

    async def futures_account_balance(self, **params):
        return await self._request_futures_api('get', 'balance', True, version=2, data=params)

    async def futures_account(self, **params):
        return await self._request_futures_api('get', 'account', True, version=2, data=params)

    async def futures_change_leverage(self, **params):
        return await self._request_futures_api('post', 'leverage', True, data=params)

    async def futures_change_margin_type(self, **params):
        return await self._request_futures_api('post', 'marginType', True, data=params)

    async def futures_change_position_margin(self, **params):
        return await self._request_futures_api('post', 'positionMargin', True, data=params)

    async def futures_position_margin_history(self, **params):
        return await self._request_futures_api('get', 'positionMargin/history', True, data=params)

    async def futures_position_information(self, **params):
        return await self._request_futures_api('get', 'positionRisk', True, version=2, data=params)

    async def futures_account_trades(self, **params):
        return await self._request_futures_api('get', 'userTrades', True, data=params)

    async def futures_income_history(self, **params):
        return await self._request_futures_api('get', 'income', True, data=params)

    async def futures_change_position_mode(self, **params):
        return await self._request_futures_api('post', 'positionSide/dual', True, data=params)

    async def futures_get_position_mode(self, **params):
        return await self._request_futures_api('get', 'positionSide/dual', True, data=params)

    async def futures_change_multi_assets_mode(self, multiAssetsMargin: bool):
        params = {
            'multiAssetsMargin': 'true' if multiAssetsMargin else 'false'
        }
        return await self._request_futures_api('post', 'multiAssetsMargin', True, data=params)

    async def futures_get_multi_assets_mode(self):
        return await self._request_futures_api('get', 'multiAssetsMargin', True, data={})

    async def futures_stream_get_listen_key(self):
        res = await self._request_futures_api('post', 'listenKey', signed=False, data={})
        return res['listenKey']

    async def futures_stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._request_futures_api('put', 'listenKey', signed=False, data=params)

    async def futures_stream_close(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._request_futures_api('delete', 'listenKey', signed=False, data=params)

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
        return await self._request_futures_coin_api("get", "historicalTrades", data=params)

    async def futures_coin_aggregate_trades(self, **params):
        return await self._request_futures_coin_api("get", "aggTrades", data=params)

    async def futures_coin_klines(self, **params):
        return await self._request_futures_coin_api("get", "klines", data=params)

    async def futures_coin_continous_klines(self, **params):
        return await self._request_futures_coin_api("get", "continuousKlines", data=params)

    async def futures_coin_index_price_klines(self, **params):
        return await self._request_futures_coin_api("get", "indexPriceKlines", data=params)

    async def futures_coin_mark_price_klines(self, **params):
        return await self._request_futures_coin_api("get", "markPriceKlines", data=params)

    async def futures_coin_mark_price(self, **params):
        return await self._request_futures_coin_api("get", "premiumIndex", data=params)

    async def futures_coin_funding_rate(self, **params):
        return await self._request_futures_coin_api("get", "fundingRate", data=params)

    async def futures_coin_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/24hr", data=params)

    async def futures_coin_symbol_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/price", data=params)

    async def futures_coin_orderbook_ticker(self, **params):
        return await self._request_futures_coin_api("get", "ticker/bookTicker", data=params)

    async def futures_coin_liquidation_orders(self, **params):
        return await self._request_futures_coin_api("get", "forceOrders", signed=True, data=params)

    async def futures_coin_open_interest(self, **params):
        return await self._request_futures_coin_api("get", "openInterest", data=params)

    async def futures_coin_open_interest_hist(self, **params):
        return await self._request_futures_coin_data_api("get", "openInterestHist", data=params)

    async def futures_coin_leverage_bracket(self, **params):
        return await self._request_futures_coin_api(
            "get", "leverageBracket", version=2, signed=True, data=params
        )

    async def new_transfer_history(self, **params):
        return await self._request_margin_api("get", "asset/transfer", True, data=params)

    async def funding_wallet(self, **params):
        return await self._request_margin_api("post", "asset/get-funding-asset", True, data=params)

    async def get_user_asset(self, **params):
        return await self._request_margin_api("post", "asset/getUserAsset", True, data=params, version=3)

    async def universal_transfer(self, **params):
        return await self._request_margin_api(
            "post", "asset/transfer", signed=True, data=params
        )

    async def futures_coin_create_order(self, **params):
        return await self._request_futures_coin_api("post", "order", True, data=params)

    async def futures_coin_place_batch_order(self, **params):
        query_string = urlencode(params)
        query_string = query_string.replace('%27', '%22')
        params['batchOrders'] = query_string[12:]

        return await self._request_futures_coin_api('post', 'batchOrders', True, data=params)

    async def futures_coin_get_order(self, **params):
        return await self._request_futures_coin_api("get", "order", True, data=params)

    async def futures_coin_get_open_orders(self, **params):
        return await self._request_futures_coin_api("get", "openOrders", True, data=params)

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
            "delete", "allOpenOrders", signed=True, data=params
        )

    async def futures_coin_cancel_orders(self, **params):
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
        return await self._request_futures_coin_api("get", "positionRisk", True, data=params)

    async def futures_coin_account_trades(self, **params):
        return await self._request_futures_coin_api("get", "userTrades", True, data=params)

    async def futures_coin_income_history(self, **params):
        return await self._request_futures_coin_api("get", "income", True, data=params)

    async def futures_coin_change_position_mode(self, **params):
        return await self._request_futures_coin_api("post", "positionSide/dual", True, data=params)

    async def futures_coin_get_position_mode(self, **params):
        return await self._request_futures_coin_api("get", "positionSide/dual", True, data=params)

    async def futures_coin_stream_get_listen_key(self):
        res = await self._request_futures_coin_api('post', 'listenKey', signed=False, data={})
        return res['listenKey']

    async def futures_coin_stream_keepalive(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._request_futures_coin_api('put', 'listenKey', signed=False, data=params)

    async def futures_coin_stream_close(self, listenKey):
        params = {
            'listenKey': listenKey
        }
        return await self._request_futures_coin_api('delete', 'listenKey', signed=False, data=params)

    async def get_all_coins_info(self, **params):
        return await self._request_margin_api('get', 'capital/config/getall', True, data=params)

    async def get_account_snapshot(self, **params):
        return await self._request_margin_api('get', 'accountSnapshot', True, data=params)

    async def disable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api('post', 'disableFastWithdrawSwitch', True, data=params)

    async def enable_fast_withdraw_switch(self, **params):
        return await self._request_margin_api('post', 'enableFastWithdrawSwitch', True, data=params)

    """
    ====================================================================================================================
    Options API
    ====================================================================================================================
    """

    # Quoting interface endpoints

    async def options_ping(self):
        return await self._request_options_api('get', 'ping')

    async def options_time(self):
        return await self._request_options_api('get', 'time')

    async def options_info(self):
        return await self._request_options_api('get', 'optionInfo')

    async def options_exchange_info(self):
        return await self._request_options_api('get', 'exchangeInfo')

    async def options_index_price(self, **params):
        return await self._request_options_api('get', 'index', data=params)

    async def options_price(self, **params):
        return await self._request_options_api('get', 'ticker', data=params)

    async def options_mark_price(self, **params):
        return await self._request_options_api('get', 'mark', data=params)

    async def options_order_book(self, **params):
        return await self._request_options_api('get', 'depth', data=params)

    async def options_klines(self, **params):
        return await self._request_options_api('get', 'klines', data=params)

    async def options_recent_trades(self, **params):
        return await self._request_options_api('get', 'trades', data=params)

    async def options_historical_trades(self, **params):
        return await self._request_options_api('get', 'historicalTrades', data=params)

    # Account and trading interface endpoints

    async def options_account_info(self, **params):
        return await self._request_options_api('get', 'account', signed=True, data=params)

    async def options_funds_transfer(self, **params):
        return await self._request_options_api('post', 'transfer', signed=True, data=params)

    async def options_positions(self, **params):
        return await self._request_options_api('get', 'position', signed=True, data=params)

    async def options_bill(self, **params):
        return await self._request_options_api('post', 'bill', signed=True, data=params)

    async def options_place_order(self, **params):
        return await self._request_options_api('post', 'order', signed=True, data=params)

    async def options_place_batch_order(self, **params):
        return await self._request_options_api('post', 'batchOrders', signed=True, data=params)

    async def options_cancel_order(self, **params):
        return await self._request_options_api('delete', 'order', signed=True, data=params)

    async def options_cancel_batch_order(self, **params):
        return await self._request_options_api('delete', 'batchOrders', signed=True, data=params)

    async def options_cancel_all_orders(self, **params):
        return await self._request_options_api('delete', 'allOpenOrders', signed=True, data=params)

    async def options_query_order(self, **params):
        return await self._request_options_api('get', 'order', signed=True, data=params)

    async def options_query_pending_orders(self, **params):
        return await self._request_options_api('get', 'openOrders', signed=True, data=params)

    async def options_query_order_history(self, **params):
        return await self._request_options_api('get', 'historyOrders', signed=True, data=params)

    async def options_user_trades(self, **params):
        return await self._request_options_api('get', 'userTrades', signed=True, data=params)

    # Fiat Endpoints

    async def get_fiat_deposit_withdraw_history(self, **params):
        return await self._request_margin_api('get', 'fiat/orders', signed=True, data=params)

    async def get_fiat_payments_history(self, **params):
        return await self._request_margin_api('get', 'fiat/payments', signed=True, data=params)

    # C2C Endpoints

    async def get_c2c_trade_history(self, **params):
        return await self._request_margin_api('get', 'c2c/orderMatch/listUserOrderHistory', signed=True, data=params)

    # Pay Endpoints

    async def get_pay_trade_history(self, **params):
        return await self._request_margin_api('get', 'pay/transactions', signed=True, data=params)
    get_pay_trade_history.__doc__ = Client.get_pay_trade_history.__doc__

    # Convert Endpoints

    async def get_convert_trade_history(self, **params):
        return await self._request_margin_api('get', 'convert/tradeFlow', signed=True, data=params)
    get_convert_trade_history.__doc__ = Client.get_convert_trade_history.__doc__

    async def convert_request_quote(self, **params):
        return await self._request_margin_api('post', 'convert/getQuote', signed=True, data=params)
    convert_request_quote.__doc__ = Client.convert_request_quote.__doc__

    async def convert_accept_quote(self, **params):
        return await self._request_margin_api('post', 'convert/acceptQuote', signed=True, data=params)
    convert_accept_quote.__doc__ = Client.convert_accept_quote.__doc__

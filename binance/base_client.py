from base64 import b64encode
from pathlib import Path
import random
from typing import Dict, Optional, List, Tuple, Union, Any

import asyncio
import hashlib
import hmac
import time
from Crypto.PublicKey import RSA, ECC
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15, eddsa
import urllib.parse as _urlencode
from operator import itemgetter
from urllib.parse import urlencode

from binance.ws.websocket_api import WebsocketAPI

from .helpers import get_loop


class BaseClient:
    API_URL = "https://api{}.binance.{}/api"
    API_TESTNET_URL = "https://testnet.binance.vision/api"
    MARGIN_API_URL = "https://api{}.binance.{}/sapi"
    WEBSITE_URL = "https://www.binance.{}"
    FUTURES_URL = "https://fapi.binance.{}/fapi"
    FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"
    FUTURES_DATA_URL = "https://fapi.binance.{}/futures/data"
    FUTURES_DATA_TESTNET_URL = "https://testnet.binancefuture.com/futures/data"
    FUTURES_COIN_URL = "https://dapi.binance.{}/dapi"
    FUTURES_COIN_TESTNET_URL = "https://testnet.binancefuture.com/dapi"
    FUTURES_COIN_DATA_URL = "https://dapi.binance.{}/futures/data"
    FUTURES_COIN_DATA_TESTNET_URL = "https://testnet.binancefuture.com/futures/data"
    OPTIONS_URL = "https://eapi.binance.{}/eapi"
    OPTIONS_TESTNET_URL = "https://testnet.binanceops.{}/eapi"
    PAPI_URL = "https://papi.binance.{}/papi"
    WS_API_URL = "wss://ws-api.binance.{}/ws-api/v3"
    WS_API_TESTNET_URL = "wss://testnet.binance.vision/ws-api/v3"
    WS_FUTURES_URL = "wss://ws-fapi.binance.{}/ws-fapi/v1"
    WS_FUTURES_TESTNET_URL = "wss://testnet.binancefuture.com/ws-fapi/v1"
    PUBLIC_API_VERSION = "v1"
    PRIVATE_API_VERSION = "v3"
    MARGIN_API_VERSION = "v1"
    MARGIN_API_VERSION2 = "v2"
    MARGIN_API_VERSION3 = "v3"
    MARGIN_API_VERSION4 = "v4"
    FUTURES_API_VERSION = "v1"
    FUTURES_API_VERSION2 = "v2"
    FUTURES_API_VERSION3 = "v3"
    OPTIONS_API_VERSION = "v1"
    PORTFOLIO_API_VERSION = "v1"
    PORTFOLIO_API_VERSION2 = "v2"

    BASE_ENDPOINT_DEFAULT = ""
    BASE_ENDPOINT_1 = "1"
    BASE_ENDPOINT_2 = "2"
    BASE_ENDPOINT_3 = "3"
    BASE_ENDPOINT_4 = "4"

    REQUEST_TIMEOUT: float = 10

    REQUEST_RECVWINDOW: int = 10000  # 10 seconds

    SYMBOL_TYPE_SPOT = "SPOT"

    ORDER_STATUS_NEW = "NEW"
    ORDER_STATUS_PARTIALLY_FILLED = "PARTIALLY_FILLED"
    ORDER_STATUS_FILLED = "FILLED"
    ORDER_STATUS_CANCELED = "CANCELED"
    ORDER_STATUS_PENDING_CANCEL = "PENDING_CANCEL"
    ORDER_STATUS_REJECTED = "REJECTED"
    ORDER_STATUS_EXPIRED = "EXPIRED"

    KLINE_INTERVAL_1SECOND = "1s"
    KLINE_INTERVAL_1MINUTE = "1m"
    KLINE_INTERVAL_3MINUTE = "3m"
    KLINE_INTERVAL_5MINUTE = "5m"
    KLINE_INTERVAL_15MINUTE = "15m"
    KLINE_INTERVAL_30MINUTE = "30m"
    KLINE_INTERVAL_1HOUR = "1h"
    KLINE_INTERVAL_2HOUR = "2h"
    KLINE_INTERVAL_4HOUR = "4h"
    KLINE_INTERVAL_6HOUR = "6h"
    KLINE_INTERVAL_8HOUR = "8h"
    KLINE_INTERVAL_12HOUR = "12h"
    KLINE_INTERVAL_1DAY = "1d"
    KLINE_INTERVAL_3DAY = "3d"
    KLINE_INTERVAL_1WEEK = "1w"
    KLINE_INTERVAL_1MONTH = "1M"

    SIDE_BUY = "BUY"
    SIDE_SELL = "SELL"

    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_STOP_LOSS = "STOP_LOSS"
    ORDER_TYPE_STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    ORDER_TYPE_TAKE_PROFIT = "TAKE_PROFIT"
    ORDER_TYPE_TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    ORDER_TYPE_LIMIT_MAKER = "LIMIT_MAKER"

    FUTURE_ORDER_TYPE_LIMIT = "LIMIT"
    FUTURE_ORDER_TYPE_MARKET = "MARKET"
    FUTURE_ORDER_TYPE_STOP = "STOP"
    FUTURE_ORDER_TYPE_STOP_MARKET = "STOP_MARKET"
    FUTURE_ORDER_TYPE_TAKE_PROFIT = "TAKE_PROFIT"
    FUTURE_ORDER_TYPE_TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"
    FUTURE_ORDER_TYPE_LIMIT_MAKER = "LIMIT_MAKER"

    TIME_IN_FORCE_GTC = "GTC"  # Good till cancelled
    TIME_IN_FORCE_IOC = "IOC"  # Immediate or cancel
    TIME_IN_FORCE_FOK = "FOK"  # Fill or kill

    ORDER_RESP_TYPE_ACK = "ACK"
    ORDER_RESP_TYPE_RESULT = "RESULT"
    ORDER_RESP_TYPE_FULL = "FULL"

    # For accessing the data returned by Client.aggregate_trades().
    AGG_ID = "a"
    AGG_PRICE = "p"
    AGG_QUANTITY = "q"
    AGG_FIRST_TRADE_ID = "f"
    AGG_LAST_TRADE_ID = "l"
    AGG_TIME = "T"
    AGG_BUYER_MAKES = "m"
    AGG_BEST_MATCH = "M"

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

    ## order ids
    SPOT_ORDER_PREFIX = "x-HNA2TXFJ"
    CONTRACT_ORDER_PREFIX = "x-Cb7ytekJ"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None,
        tld: str = "com",
        base_endpoint: str = BASE_ENDPOINT_DEFAULT,
        testnet: bool = False,
        private_key: Optional[Union[str, Path]] = None,
        private_key_pass: Optional[str] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        time_unit: Optional[str] = None,
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
        :param time_unit: Time unit to use for requests. Supported values: "MILLISECOND", "MICROSECOND"
        :type time_unit: optional - str

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
        self.TIME_UNIT = time_unit
        self._is_rsa = False
        self.PRIVATE_KEY: Any = self._init_private_key(private_key, private_key_pass)
        self.session = self._init_session()
        self._requests_params = requests_params
        self.response = None
        self.testnet = testnet
        self.timestamp_offset = 0
        ws_api_url = self.WS_API_TESTNET_URL if testnet else self.WS_API_URL.format(tld)
        if self.TIME_UNIT:
            ws_api_url += f"?timeUnit={self.TIME_UNIT}"
        self.ws_api = WebsocketAPI(url=ws_api_url, tld=tld)
        ws_future_url = (
            self.WS_FUTURES_TESTNET_URL if testnet else self.WS_FUTURES_URL.format(tld)
        )
        self.ws_future = WebsocketAPI(url=ws_future_url, tld=tld)
        self.loop = loop or get_loop()

    def _get_headers(self) -> Dict:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",  # noqa
        }
        if self.API_KEY:
            assert self.API_KEY
            headers["X-MBX-APIKEY"] = self.API_KEY
        if self.TIME_UNIT:
            assert self.TIME_UNIT
            headers["X-MBX-TIME-UNIT"] = self.TIME_UNIT
        return headers

    def _init_session(self):
        raise NotImplementedError

    def _init_private_key(
        self,
        private_key: Optional[Union[str, Path]],
        private_key_pass: Optional[str] = None,
    ):
        if not private_key:
            return
        if isinstance(private_key, Path):
            with open(private_key, "r") as f:
                private_key = f.read()
        if len(private_key) > 120:
            self._is_rsa = True
            return RSA.import_key(private_key, passphrase=private_key_pass)
        return ECC.import_key(private_key)

    def _create_api_uri(
        self, path: str, signed: bool = True, version: str = PUBLIC_API_VERSION
    ) -> str:
        url = self.API_URL
        if self.testnet:
            url = self.API_TESTNET_URL
        v = self.PRIVATE_API_VERSION if signed else version
        return url + "/" + v + "/" + path

    def _create_margin_api_uri(self, path: str, version: int = 1) -> str:
        options = {
            1: self.MARGIN_API_VERSION,
            2: self.MARGIN_API_VERSION2,
            3: self.MARGIN_API_VERSION3,
            4: self.MARGIN_API_VERSION4,
        }
        return self.MARGIN_API_URL + "/" + options[version] + "/" + path

    def _create_papi_api_uri(self, path: str, version: int = 1) -> str:
        options = {1: self.PORTFOLIO_API_VERSION, 2: self.PORTFOLIO_API_VERSION2}
        return self.PAPI_URL.format(self.tld) + "/" + options[version] + "/" + path

    def _create_website_uri(self, path: str) -> str:
        return self.WEBSITE_URL + "/" + path

    def _create_futures_api_uri(self, path: str, version: int = 1) -> str:
        url = self.FUTURES_URL
        if self.testnet:
            url = self.FUTURES_TESTNET_URL
        options = {
            1: self.FUTURES_API_VERSION,
            2: self.FUTURES_API_VERSION2,
            3: self.FUTURES_API_VERSION3,
        }
        return url + "/" + options[version] + "/" + path

    def _create_futures_data_api_uri(self, path: str) -> str:
        url = self.FUTURES_DATA_URL
        if self.testnet:
            url = self.FUTURES_DATA_TESTNET_URL
        return url + "/" + path

    def _create_futures_coin_api_url(self, path: str, version: int = 1) -> str:
        url = self.FUTURES_COIN_URL
        if self.testnet:
            url = self.FUTURES_COIN_TESTNET_URL
        options = {
            1: self.FUTURES_API_VERSION,
            2: self.FUTURES_API_VERSION2,
            3: self.FUTURES_API_VERSION3,
        }
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
        return url + "/" + self.OPTIONS_API_VERSION + "/" + path

    def _rsa_signature(self, query_string: str):
        assert self.PRIVATE_KEY
        h = SHA256.new(query_string.encode("utf-8"))
        signature = pkcs1_15.new(self.PRIVATE_KEY).sign(h)  # type: ignore
        res = b64encode(signature).decode()
        # return self.encode_uri_component(res)
        return res

    @staticmethod
    def encode_uri_component(uri, safe="~()*!.'"):
        return _urlencode.quote(uri, safe=safe)

    @staticmethod
    def convert_to_dict(list_tuples):
        dictionary = dict((key, value) for key, value in list_tuples)
        return dictionary

    def _ed25519_signature(self, query_string: str):
        assert self.PRIVATE_KEY
        res = b64encode(
            eddsa.new(self.PRIVATE_KEY, "rfc8032").sign(query_string.encode())
        ).decode()  # type: ignore
        # return self.encode_uri_component(res)
        return res

    def _hmac_signature(self, query_string: str) -> str:
        assert self.API_SECRET, "API Secret required for private endpoints"
        m = hmac.new(
            self.API_SECRET.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        )
        return m.hexdigest()

    def _generate_signature(self, data: Dict, uri_encode=True) -> str:
        sig_func = self._hmac_signature
        if self.PRIVATE_KEY:
            if self._is_rsa:
                sig_func = self._rsa_signature
            else:
                sig_func = self._ed25519_signature
        query_string = "&".join([f"{d[0]}={d[1]}" for d in self._order_params(data)])
        res = sig_func(query_string)
        return self.encode_uri_component(res) if uri_encode else res

    def _sign_ws_params(self, params, signature_func):
        if "signature" in params:
            return params
        params.setdefault("apiKey", self.API_KEY)
        params.setdefault("timestamp", int(time.time() * 1000 + self.timestamp_offset))
        params = dict(sorted(params.items()))
        return {**params, "signature": signature_func(params)}

    def _generate_ws_api_signature(self, data: Dict) -> str:
        sig_func = self._hmac_signature
        if self.PRIVATE_KEY:
            if self._is_rsa:
                sig_func = self._rsa_signature
            else:
                sig_func = self._ed25519_signature
        query_string = urlencode(data)
        return sig_func(query_string)

    async def _ws_futures_api_request(self, method: str, signed: bool, params: dict):
        """Send request and wait for response"""
        id = params.pop("id", self.uuid22())
        payload = {
            "id": id,
            "method": method,
            "params": params,
        }
        if signed:
            payload["params"] = self._sign_ws_params(params, self._generate_signature)
        return await self.ws_future.request(id, payload)

    def _ws_futures_api_request_sync(self, method: str, signed: bool, params: dict):
        self.loop = get_loop()
        return self.loop.run_until_complete(
            self._ws_futures_api_request(method, signed, params)
        )

    async def _make_sync(self, method):
        return asyncio.run(method)

    async def _ws_api_request(self, method: str, signed: bool, params: dict):
        """Send request and wait for response"""
        id = params.pop("id", self.uuid22())
        payload = {
            "id": id,
            "method": method,
            "params": params,
        }
        if signed:
            payload["params"] = self._sign_ws_params(
                params, self._generate_ws_api_signature
            )
        return await self.ws_api.request(id, payload)

    def _ws_api_request_sync(self, method: str, signed: bool, params: dict):
        """Send request to WS API and wait for response"""
        self.loop = get_loop()
        return self.loop.run_until_complete(
            self._ws_api_request(method, signed, params)
        )

    @staticmethod
    def _get_version(version: int, **kwargs) -> int:
        if "data" in kwargs and "version" in kwargs["data"]:
            version_override = kwargs["data"].get("version")
            del kwargs["data"]["version"]
            return version_override
        return version

    @staticmethod
    def uuid22(length=22):
        return format(random.getrandbits(length * 4), "x")

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
            if key == "signature":
                has_signature = True
            else:
                params.append((key, str(value)))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(("signature", data["signature"]))
        return params

    def _get_request_kwargs(
        self, method, signed: bool, force_params: bool = False, **kwargs
    ) -> Dict:
        # set default requests timeout
        kwargs["timeout"] = self.REQUEST_TIMEOUT

        # add our global requests params
        if self._requests_params:
            kwargs.update(self._requests_params)

        data = kwargs.get("data", None)
        if data and isinstance(data, dict):
            kwargs["data"] = data
            # find any requests params passed and apply them
            if "requests_params" in kwargs["data"]:
                # merge requests params into kwargs
                kwargs.update(kwargs["data"]["requests_params"])
                del kwargs["data"]["requests_params"]

        if signed:
            # generate signature
            kwargs["data"]["timestamp"] = int(
                time.time() * 1000 + self.timestamp_offset
            )
            if self.REQUEST_RECVWINDOW:
                kwargs["data"]["recvWindow"] = self.REQUEST_RECVWINDOW
            kwargs["data"]["signature"] = self._generate_signature(kwargs["data"])

        # sort get and post params to match signature order
        if data:
            # sort post params and remove any arguments with values of None
            kwargs["data"] = self._order_params(kwargs["data"])
            # Remove any arguments with values of None.
            null_args = [
                i for i, (key, value) in enumerate(kwargs["data"]) if value is None
            ]
            for i in reversed(null_args):
                del kwargs["data"][i]

        # if get request assign data array to params value for requests lib
        if data and (method == "get" or force_params):
            kwargs["params"] = "&".join(
                "%s=%s" % (data[0], data[1]) for data in kwargs["data"]
            )
            del kwargs["data"]

        # Temporary fix for Signature issue while using batchOrders in AsyncClient
        if "params" in kwargs.keys():
            if (
                "batchOrders" in kwargs["params"]
                or "orderidlist" in kwargs["params"]
                or "origclientorderidlist" in kwargs["params"]
            ):
                kwargs["data"] = kwargs["params"]
                del kwargs["params"]

        return kwargs

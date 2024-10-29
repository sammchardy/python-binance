import requests_mock
import json
from binance.client import Client
import re

client = Client(api_key="api_key", api_secret="api_secret", ping=False)


def test_futures_position_information():
    with requests_mock.mock() as m:
        url_matcher = re.compile(
            r"https:\/\/fapi.binance.com\/fapi\/v3\/positionRisk\?.+"
        )
        response = [
            {
                "symbol": "LTCUSDT",
                "positionSide": "LONG",
                "positionAmt": "0.700",
                "entryPrice": "75.6",
                "breakEvenPrice": "75.63024",
                "markPrice": "73.18000000",
                "unRealizedProfit": "-1.69400000",
                "liquidationPrice": "0",
                "isolatedMargin": "0",
                "notional": "51.22600000",
                "marginAsset": "USDT",
                "isolatedWallet": "0",
                "initialMargin": "10.24520000",
                "maintMargin": "0.33296900",
                "positionInitialMargin": "10.24520000",
                "openOrderInitialMargin": "0",
                "adl": 0,
                "bidNotional": "0",
                "askNotional": "0",
                "updateTime": 1729436057076,
            }
        ]
        m.register_uri("GET", url_matcher, json=json.dumps(response), status_code=200)
        pos = client.futures_position_information(symbol="LTCUSDT")
        assert m.last_request.qs["symbol"][0] == "LTCUSDT".lower()
        assert m.last_request.path == "/fapi/v3/positionrisk"


def test_futures_position_information_version_override():
    with requests_mock.mock() as m:
        url_matcher = re.compile(
            r"https:\/\/fapi.binance.com\/fapi\/v2\/positionRisk\?.+"
        )
        response = [
            {
                "symbol": "LTCUSDT",
                "positionSide": "LONG",
                "positionAmt": "0.700",
                "entryPrice": "75.6",
                "breakEvenPrice": "75.63024",
                "markPrice": "73.18000000",
                "unRealizedProfit": "-1.69400000",
                "liquidationPrice": "0",
                "isolatedMargin": "0",
                "notional": "51.22600000",
                "marginAsset": "USDT",
                "isolatedWallet": "0",
                "initialMargin": "10.24520000",
                "maintMargin": "0.33296900",
                "positionInitialMargin": "10.24520000",
                "openOrderInitialMargin": "0",
                "adl": 0,
                "bidNotional": "0",
                "askNotional": "0",
                "updateTime": 1729436057076,
            }
        ]
        m.register_uri("GET", url_matcher, json=json.dumps(response), status_code=200)
        pos = client.futures_position_information(symbol="LTCUSDT", version=2)
        assert m.last_request.qs["symbol"][0] == "LTCUSDT".lower()
        assert m.last_request.path == "/fapi/v2/positionrisk"


def test_futures_account_balance():
    with requests_mock.mock() as m:
        url_matcher = re.compile(r"https:\/\/fapi.binance.com\/fapi\/v3\/balance\?.+")
        m.register_uri("GET", url_matcher, json={}, status_code=200)
        client.futures_account_balance()
        assert m.last_request.path == "/fapi/v3/balance"


def test_futures_account_config():
    with requests_mock.mock() as m:
        url_matcher = re.compile(
            r"https:\/\/fapi.binance.com\/fapi\/v1\/accountConfig\?.+"
        )
        m.register_uri("GET", url_matcher, json={}, status_code=200)
        client.futures_account_config()
        assert m.last_request.path == "/fapi/v1/accountconfig"

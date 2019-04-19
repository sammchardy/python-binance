#!/usr/bin/env python
# coding=utf-8

from binance.client import Client
from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
    BinanceWithdrawException,
)
import pytest
import requests_mock

client = Client("api_key", "api_secret")


@pytest.mark.asyncio
async def test_invalid_json(client, get_session):
    """Test Invalid response Exception"""

    async def callback(request):
        assert "https://www.binance.com/exchange/public/product" == str(request.url)

    client.session = get_session(
        "https://www.binance.com/exchange/public/product", text="<head></html>"
    )
    with pytest.raises(BinanceRequestException):
        await client.get_products()


@pytest.mark.asyncio
async def test_api_exception(client, get_session):
    """Test API response Exception"""
    json_obj = {"code": 1002, "msg": "Invalid API call"}

    async def callback(request):
        assert "https://api.binance.com/api/v1/time" == str(request.url)

    client.session = get_session(
        "https://api.binance.com/api/v1/time",
        json=json_obj,
        status_code=400,
        callback=callback,
    )
    with pytest.raises(BinanceAPIException):
        await client.get_server_time()


@pytest.mark.asyncio
async def test_api_exception_invalid_json(client, get_session):
    """Test API response Exception"""
    not_json_str = "<html><body>Error</body></html>"

    async def callback(request):
        assert "https://api.binance.com/api/v1/time" == str(request.url)

    client.session = get_session(
        "https://api.binance.com/api/v1/time", text=not_json_str, status_code=400
    )
    with pytest.raises(BinanceAPIException):
        await client.get_server_time()


@pytest.mark.asyncio
async def test_withdraw_api_exception(client, get_session):
    """Test Withdraw API response Exception"""
    json_obj = {"success": False, "msg": "Insufficient funds"}

    client.session = get_session(requests_mock.ANY, json=json_obj, status_code=200)
    with pytest.raises(BinanceWithdrawException):
        await client.withdraw(asset="BTC", address="BTCADDRESS", amount=100)


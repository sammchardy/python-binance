import re

import pytest
import requests_mock
from aioresponses import aioresponses

from binance.client import Client
from binance.async_client import AsyncClient

EXPECTED = [
    {
        "delistTime": 1686161202000,
        "crossMarginAssets": ["BTC", "USDT"],
        "isolatedMarginSymbols": ["ADAUSDT", "BNBUSDT"],
    }
]

# Exactly one slash between the version and the path segment.
MARGIN_DELIST_URL = re.compile(
    r"^https://api\.binance\.com/sapi/v1/margin/delist-schedule(\?.*)?$"
)


def test_get_margin_delist_schedule_url():
    client = Client("api_key", "api_secret")
    with requests_mock.mock() as m:
        m.get(MARGIN_DELIST_URL, json=EXPECTED)
        response = client.get_margin_delist_schedule()

    assert response == EXPECTED
    assert m.call_count == 1
    assert "//margin" not in m.last_request.url


@pytest.mark.asyncio()
async def test_get_margin_delist_schedule_url_async():
    client = AsyncClient("api_key", "api_secret")
    try:
        with aioresponses() as m:
            m.get(MARGIN_DELIST_URL, payload=EXPECTED)
            response = await client.get_margin_delist_schedule()

        assert response == EXPECTED
        requested = [str(key[1]) for key in m.requests]
        assert len(requested) == 1
        assert "//margin" not in requested[0]
    finally:
        await client.close_connection()

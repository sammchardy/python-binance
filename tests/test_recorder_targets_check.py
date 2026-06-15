"""Check record_targets (monkeypatch-style) against the real binance Client.

No fixture seam: the client is constructed *inline*, and record_targets patches
binance.client.Client by import path so the inline construction is recorded/replayed.
"""

import binance.client as bc
from pytest_recorder import record_targets

from .conftest import api_key, api_secret, proxies, testnet


@record_targets("binance.client.Client")
def test_targets_inline_symbol_info():
    c = bc.Client(api_key, api_secret, {"proxies": proxies}, testnet=testnet)
    info = c.get_symbol_info("BTCUSDT")
    assert info["symbol"] == "BTCUSDT"

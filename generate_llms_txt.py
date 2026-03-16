#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the python-binance Client class.

Usage:
    python generate_llms_txt.py

Outputs:
    llms.txt       - Concise LLM overview (~4-6KB)
    llms-full.txt  - Compact method reference
"""

import inspect
import re
from collections import defaultdict


# Methods inherited from BaseClient that are not API endpoints
INTERNAL_METHODS = {
    "convert_to_dict",
}


def get_public_methods(cls):
    """Get all public methods from a class (non-underscore, non-internal)."""
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith("_") and name not in INTERNAL_METHODS:
            methods.append((name, method))
    return sorted(methods, key=lambda x: x[0])


def categorize_method(name):
    """Categorize a method by its prefix."""
    prefixes = [
        ("futures_coin_", "Futures Coin-M"),
        ("futures_", "Futures USD-M"),
        ("margin_", "Margin"),
        ("options_", "Options"),
        ("papi_", "Portfolio Margin"),
        ("ws_futures_", "WebSocket Futures"),
        ("ws_", "WebSocket API"),
        ("gift_card_", "Gift Card"),
        ("convert_", "Convert"),
    ]
    for prefix, category in prefixes:
        if name.startswith(prefix):
            return category
    return "Spot / General"


def get_signature_str(method):
    """Get a clean signature string for a method."""
    try:
        sig = inspect.signature(method)
        params = []
        for pname, param in sig.parameters.items():
            if pname == "self":
                continue
            if param.kind == param.VAR_KEYWORD:
                params.append("**params")
            elif param.kind == param.VAR_POSITIONAL:
                params.append(f"*{pname}")
            elif param.default is inspect.Parameter.empty:
                params.append(pname)
            else:
                default = param.default
                if isinstance(default, str):
                    params.append(f'{pname}="{default}"')
                else:
                    params.append(f"{pname}={default}")
        return ", ".join(params)
    except (ValueError, TypeError):
        return "**params"


def extract_docstring_info(method):
    """Extract description and params from a docstring."""
    doc = inspect.getdoc(method)
    if not doc:
        return "", [], ""

    lines = doc.strip().split("\n")

    # First non-empty line(s) before :param or https:// is the description
    desc_lines = []
    param_lines = []
    in_params = False
    in_rest = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(":param ") or stripped.startswith(":type "):
            in_params = True
            in_rest = False
        elif (
            stripped.startswith(":returns:")
            or stripped.startswith(":raises:")
            or stripped.startswith(".. code-block")
        ):
            in_params = False
            in_rest = True

        if in_rest:
            continue
        elif in_params:
            param_lines.append(line)
        elif stripped.startswith("https://"):
            continue  # skip doc links
        else:
            desc_lines.append(stripped)

    description = " ".join(d for d in desc_lines if d).strip()

    # Parse params
    params = []
    current_param = None
    for line in param_lines:
        stripped = line.strip()
        m = re.match(r":param (\w+):\s*(.*)", stripped)
        if m:
            current_param = {"name": m.group(1), "desc": m.group(2), "type": ""}
            params.append(current_param)
        elif current_param:
            tm = re.match(r":type \w+:\s*(.*)", stripped)
            if tm:
                current_param["type"] = tm.group(1)
            elif stripped and not stripped.startswith(":"):
                # Continuation line for multi-line param descriptions
                current_param["desc"] += " " + stripped

    return description, params, ""


def generate_llms_txt(methods_by_category, total_count):
    """Generate the concise llms.txt content."""
    # Count per category
    cat_summary = []
    for cat in [
        "Spot / General",
        "Futures USD-M",
        "Futures Coin-M",
        "Margin",
        "Options",
        "Portfolio Margin",
        "WebSocket API",
        "WebSocket Futures",
        "Gift Card",
        "Convert",
    ]:
        if cat in methods_by_category:
            cat_summary.append(f"- **{cat}**: {len(methods_by_category[cat])} methods")

    category_list = "\n".join(cat_summary)

    content = f"""\
# python-binance

> Unofficial Python SDK for the Binance cryptocurrency exchange. Covers Spot, Margin, Futures (USD-M & Coin-M), Options, Portfolio Margin, and WebSocket APIs with {total_count}+ methods across sync and async clients.

## Docs

- [Getting Started](https://python-binance.readthedocs.io/en/latest/overview.html): Installation, authentication, setup
- [Full Endpoint Reference](./Endpoints.md): All methods mapped to Binance API endpoints
- [Comprehensive LLM Reference](./llms-full.txt): Every method with signature, description, and parameters
- [Binance API Docs](https://developers.binance.com/docs/): Official Binance API documentation

## Installation & Auth

```bash
pip install python-binance
```

```python
from binance import Client, AsyncClient

# Basic setup
client = Client(api_key, api_secret)

# Async setup
async_client = await AsyncClient.create(api_key, api_secret)

# Testnet
client = Client(api_key, api_secret, testnet=True)

# Demo trading (paper trading)
client = Client(api_key, api_secret, demo=True)

# RSA key authentication
client = Client(api_key, private_key=open("private_key.pem").read())

# Other TLD (e.g. Binance US)
client = Client(api_key, api_secret, tld="us")
```

## Core Concepts

- **All methods return plain Python dicts** (not custom objects). Parse responses using standard dict access.
- **Extra parameters**: Most methods accept `**params` — pass any Binance API parameter as a keyword argument.
- **Sync/async parity**: `Client` and `AsyncClient` have identical method names. Async methods need `await`.
- **Enums**: Import constants from `binance.enums` or use string values directly.
- **Exceptions**: Catch `BinanceAPIException` (has `.code` and `.message` attributes).

## Method Categories

{category_list}

## Method Naming Conventions

| Prefix | Domain | Example |
|--------|--------|---------|
| `get_*` / `create_*` / `cancel_*` | Spot trading & account | `get_order_book()`, `create_order()` |
| `futures_*` | USD-M Futures | `futures_create_order()`, `futures_account()` |
| `futures_coin_*` | Coin-M Futures | `futures_coin_create_order()` |
| `margin_*` | Margin trading | `margin_borrow_repay()`, `margin_max_borrowable()` |
| `options_*` | Vanilla Options | `options_place_order()`, `options_account_info()` |
| `papi_*` | Portfolio Margin | `papi_create_um_order()`, `papi_get_balance()` |
| `ws_*` | WebSocket API (CRUD) | `ws_create_order()`, `ws_get_order()` |
| `ws_futures_*` | WebSocket Futures | `ws_futures_create_order()` |
| `gift_card_*` | Gift cards | `gift_card_create()`, `gift_card_redeem()` |
| `order_*` | Order helpers | `order_limit_buy()`, `order_market_sell()` |
| `stream_*` | User data stream | `stream_get_listen_key()`, `stream_keepalive()` |

## Key Enums

```python
from binance.enums import *

# Sides
SIDE_BUY = "BUY"
SIDE_SELL = "SELL"

# Order types (spot)
ORDER_TYPE_LIMIT = "LIMIT"
ORDER_TYPE_MARKET = "MARKET"
ORDER_TYPE_STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
ORDER_TYPE_TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"

# Time in force
TIME_IN_FORCE_GTC = "GTC"   # Good till cancelled
TIME_IN_FORCE_IOC = "IOC"   # Immediate or cancel
TIME_IN_FORCE_FOK = "FOK"   # Fill or kill

# Kline intervals
KLINE_INTERVAL_1MINUTE = "1m"
KLINE_INTERVAL_1HOUR = "1h"
KLINE_INTERVAL_1DAY = "1d"
KLINE_INTERVAL_1WEEK = "1w"

# Futures order types (also includes STOP, STOP_MARKET, TRAILING_STOP_MARKET)
FUTURE_ORDER_TYPE_LIMIT = "LIMIT"
FUTURE_ORDER_TYPE_MARKET = "MARKET"
```

## Common Tasks

### Get current price
```python
ticker = client.get_symbol_ticker(symbol="BTCUSDT")
print(ticker["price"])  # "50000.00000000"
```

### Get account balances
```python
account = client.get_account()
balances = [b for b in account["balances"] if float(b["free"]) > 0]
```

### Place a market buy order
```python
order = client.create_order(
    symbol="BTCUSDT",
    side=SIDE_BUY,
    type=ORDER_TYPE_MARKET,
    quoteOrderQty=100  # spend 100 USDT
)
```

### Place a limit sell order
```python
order = client.create_order(
    symbol="BTCUSDT",
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=0.001,
    price="60000"
)
```

### Get order status
```python
order = client.get_order(symbol="BTCUSDT", orderId=12345)
print(order["status"])  # "FILLED", "NEW", "CANCELED", etc.
```

### Cancel an order
```python
result = client.cancel_order(symbol="BTCUSDT", orderId=12345)
```

### Get historical klines (candlesticks)
```python
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
# Each kline: [open_time, open, high, low, close, volume, close_time, ...]
```

### Get order book
```python
depth = client.get_order_book(symbol="BTCUSDT")
print(depth["bids"][:5])  # Top 5 bids [[price, qty], ...]
print(depth["asks"][:5])  # Top 5 asks
```

### Futures: place an order
```python
order = client.futures_create_order(
    symbol="BTCUSDT",
    side=SIDE_BUY,
    type=FUTURE_ORDER_TYPE_MARKET,
    quantity=0.001
)
```

### Futures: get position info
```python
positions = client.futures_position_information(symbol="BTCUSDT")
```

### WebSocket: stream real-time trades
```python
from binance import ThreadedWebsocketManager

twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()

def handle_message(msg):
    print(msg)

twm.start_kline_socket(callback=handle_message, symbol="BTCUSDT")
twm.join()
```

### Async WebSocket example
```python
from binance import AsyncClient, BinanceSocketManager

async def main():
    client = await AsyncClient.create()
    bsm = BinanceSocketManager(client)
    async with bsm.trade_socket("BTCUSDT") as ts:
        for _ in range(10):
            msg = await ts.recv()
            print(msg)
    await client.close_connection()
```

## Error Handling

```python
from binance.exceptions import BinanceAPIException, BinanceOrderException

try:
    order = client.create_order(...)
except BinanceAPIException as e:
    print(e.code)       # e.g., -1013
    print(e.message)    # e.g., "Filter failure: LOT_SIZE"
    print(e.status_code)  # HTTP status code
except BinanceOrderException as e:
    print(e.code, e.message)
```

## WebSocket Managers

| Class | Use Case | Threading |
|-------|----------|-----------|
| `ThreadedWebsocketManager` | Simple threaded streaming | Thread-based |
| `BinanceSocketManager` | Async streaming | asyncio |
| `ThreadedDepthCacheManager` | Local order book cache (threaded) | Thread-based |
| `DepthCacheManager` | Local order book cache (async) | asyncio |

### Available socket types on BinanceSocketManager
`trade_socket`, `kline_socket`, `depth_socket`, `ticker_socket`, `symbol_ticker_socket`, `multiplex_socket`, `user_socket`, `futures_socket`, `coin_futures_socket`
"""
    return content


def generate_llms_full_txt(methods_by_category, total_count):
    """Generate a compact llms-full.txt method reference.

    Uses a dense format: one heading + description + param list per method,
    no response examples. Keeps the file small enough to fit in LLM context.
    """
    lines = []
    lines.append("# python-binance — Full Method Reference")
    lines.append("")
    lines.append(
        f"> Auto-generated reference for all {total_count} public methods in python-binance."
    )
    lines.append("> For a concise overview, see llms.txt.")
    lines.append("")

    # Table of contents
    lines.append("## Table of Contents")
    lines.append("")
    for cat in sorted(methods_by_category.keys()):
        anchor = cat.lower().replace(" ", "-").replace("/", "").replace("&", "and")
        count = len(methods_by_category[cat])
        lines.append(f"- [{cat}](#{anchor}) ({count} methods)")
    lines.append("")

    # Method details by category — compact format
    for cat in sorted(methods_by_category.keys()):
        lines.append(f"## {cat}")
        lines.append("")

        for name, method in methods_by_category[cat]:
            sig_str = get_signature_str(method)
            description, params, _ = extract_docstring_info(method)

            # Method heading with signature
            lines.append(f"### `client.{name}({sig_str})`")
            if description:
                lines.append(f"> {description}")

            if params:
                for p in params:
                    type_str = f": {p['type']}" if p["type"] else ""
                    # Truncate long descriptions to keep file compact
                    desc = p["desc"]
                    if len(desc) > 80:
                        desc = desc[:77] + "..."
                    desc_str = f" — {desc}" if desc else ""
                    lines.append(f"- `{p['name']}`{type_str}{desc_str}")

            lines.append("")

    return "\n".join(lines)


def main():
    # Import Client here so the script can be run from the repo root
    import sys

    sys.path.insert(0, ".")
    from binance.client import Client

    methods = get_public_methods(Client)
    total_count = len(methods)

    # Group by category
    methods_by_category = defaultdict(list)
    for name, method in methods:
        cat = categorize_method(name)
        methods_by_category[cat].append((name, method))

    # Generate llms.txt
    llms_txt = generate_llms_txt(methods_by_category, total_count)
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_txt)
    print(f"Generated llms.txt ({len(llms_txt):,} bytes)")

    # Generate llms-full.txt
    llms_full_txt = generate_llms_full_txt(methods_by_category, total_count)
    with open("llms-full.txt", "w", encoding="utf-8") as f:
        f.write(llms_full_txt)
    print(f"Generated llms-full.txt ({len(llms_full_txt):,} bytes)")

    # Print summary
    print(f"\nTotal methods: {total_count}")
    for cat in sorted(methods_by_category.keys()):
        print(f"  {cat}: {len(methods_by_category[cat])}")


if __name__ == "__main__":
    main()

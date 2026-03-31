---
name: python-binance
description: >
  Help developers use the python-binance library for trading on Binance.
  Use when code imports binance, references Client/AsyncClient, or asks
  about Binance API trading, market data, websockets, or account management.
---

# python-binance SDK

Unofficial Python SDK for the Binance cryptocurrency exchange. 797+ methods covering Spot, Margin, Futures, Options, Portfolio Margin, and WebSocket APIs.

## Setup

```python
from binance import Client, AsyncClient

# Sync client
client = Client(api_key, api_secret)

# Async client
client = await AsyncClient.create(api_key, api_secret)

# Testnet
client = Client(api_key, api_secret, testnet=True)

# Demo/paper trading
client = Client(api_key, api_secret, demo=True)

# RSA key auth
client = Client(api_key, private_key=open("key.pem").read())

# Other TLD (Binance US, Japan, etc.)
client = Client(api_key, api_secret, tld="us")
```

## Critical Patterns

1. **All methods return plain Python dicts** — not custom objects. Access fields with `response["key"]`.
2. **`**params` kwargs** — most methods accept extra Binance API parameters as keyword arguments.
3. **Sync/async parity** — `Client` and `AsyncClient` have identical method names. Use `await` for async.
4. **Enums** — import from `binance.enums` or use string values directly (`"BUY"`, `"LIMIT"`, etc.).

## Method Naming Convention

This is the most important pattern — it lets you infer method names:

| Prefix | Domain | Example |
|--------|--------|---------|
| `get_*` / `create_*` / `cancel_*` | Spot | `get_order_book()`, `create_order()` |
| `futures_*` | USD-M Futures | `futures_create_order()` |
| `futures_coin_*` | Coin-M Futures | `futures_coin_create_order()` |
| `margin_*` | Margin | `margin_borrow_repay()` |
| `options_*` | Vanilla Options | `options_place_order()` |
| `papi_*` | Portfolio Margin | `papi_create_um_order()` |
| `ws_*` | WebSocket CRUD | `ws_create_order()` |
| `order_*` | Order helpers | `order_limit_buy()` |
| `stream_*` | User data stream | `stream_get_listen_key()` |

## Key Enums

```python
from binance.enums import *

SIDE_BUY, SIDE_SELL = "BUY", "SELL"
ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET = "LIMIT", "MARKET"
ORDER_TYPE_STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
TIME_IN_FORCE_GTC = "GTC"  # Good till cancelled
TIME_IN_FORCE_IOC = "IOC"  # Immediate or cancel
KLINE_INTERVAL_1MINUTE = "1m"
KLINE_INTERVAL_1HOUR = "1h"
KLINE_INTERVAL_1DAY = "1d"
FUTURE_ORDER_TYPE_MARKET = "MARKET"
FUTURE_ORDER_TYPE_LIMIT = "LIMIT"
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
from binance.enums import *
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
print(order["status"])  # "FILLED", "NEW", "CANCELED"
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

### Get order book depth
```python
depth = client.get_order_book(symbol="BTCUSDT")
print(depth["bids"][:5])  # [[price, qty], ...]
```

### Futures: place an order
```python
order = client.futures_create_order(
    symbol="BTCUSDT", side="BUY", type="MARKET", quantity=0.001
)
```

### Futures: get position info
```python
positions = client.futures_position_information(symbol="BTCUSDT")
```

## WebSocket Streaming

```python
from binance import ThreadedWebsocketManager

twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()

def handle_message(msg):
    print(msg)

twm.start_kline_socket(callback=handle_message, symbol="BTCUSDT")
twm.join()
```

### Async WebSocket
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
from binance.exceptions import BinanceAPIException

try:
    order = client.create_order(...)
except BinanceAPIException as e:
    print(e.code)       # e.g., -1013
    print(e.message)    # e.g., "Filter failure: LOT_SIZE"
    print(e.status_code)
```

## Full Reference

For the complete method reference with all 797+ methods, signatures, and parameters, see:
- `llms-full.txt` in the repository root
- `Endpoints.md` for endpoint-to-method mapping

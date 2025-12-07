# Verbose Mode

The python-binance library supports verbose mode for debugging purposes. When enabled, verbose mode provides detailed logging of all HTTP requests and responses.

## Features

- Detailed request logging (method, URL, headers, body)
- Detailed response logging (status code, headers, body)
- Compatible with both `Client` and `AsyncClient`
- Standard Python logging framework integration
- Two ways to enable: `verbose` parameter or Python's logging module

## Usage

### Method 1: Using the `verbose` Parameter (Quick & Easy)

This is the quickest way to enable verbose logging, similar to libraries like ccxt.

#### Synchronous Client

```python
from binance.client import Client
import logging

# Configure logging to see output
logging.basicConfig(level=logging.DEBUG)

# Enable verbose mode
client = Client(api_key='your_api_key', api_secret='your_api_secret', verbose=True)

# All API calls will now log detailed information
server_time = client.get_server_time()
```

#### Async Client

```python
import asyncio
import logging
from binance.async_client import AsyncClient

logging.basicConfig(level=logging.DEBUG)

async def main():
    # Enable verbose mode
    client = await AsyncClient.create(
        api_key='your_api_key',
        api_secret='your_api_secret',
        verbose=True
    )

    # All API calls will now log detailed information
    server_time = await client.get_server_time()

    await client.close_connection()

asyncio.run(main())
```

### Method 2: Using Python's Logging Module (More Control)

For production environments or when you need fine-grained control over logging, use Python's standard logging module.

```python
import logging
from binance.client import Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set root level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Enable debug logging for binance only
logging.getLogger('binance.base_client').setLevel(logging.DEBUG)

# Create client (no verbose parameter needed)
client = Client(api_key='your_api_key', api_secret='your_api_secret')

# Detailed logs will be shown
server_time = client.get_server_time()
```

This approach is more Pythonic and integrates better with existing logging infrastructure.

## Log Output Format

When verbose mode is enabled, you'll see logs in the following format:

```
2025-11-30 22:01:26,957 - binance.base_client - DEBUG -
Request: GET https://api.binance.com/api/v3/time
RequestHeaders: {'Accept': 'application/json', 'Content-Type': 'application/json'}
RequestBody: None
Response: 200
ResponseHeaders: {'Content-Type': 'application/json;charset=UTF-8', ...}
ResponseBody: {"serverTime":1764536487218}
```

## Logging Configuration

The verbose mode uses Python's standard `logging` module. You can customize the logging behavior:

```python
import logging
from binance.client import Client

# Configure logging format and level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

client = Client(verbose=True)
```

## Use Cases

Verbose mode is particularly useful for:

1. **Debugging API issues**: See exactly what's being sent and received
2. **Development**: Understand the API behavior during development
3. **Troubleshooting**: Diagnose connection or authentication problems
4. **Learning**: Understand how the library interacts with the Binance API

## Performance Considerations

- Verbose mode logs can be large, especially for responses with lots of data
- Response bodies are truncated to 1000 characters in logs to prevent excessive output
- For production use, keep verbose mode disabled (default) to minimize overhead

## WebSocket Verbose Logging

WebSocket connections support verbose mode just like REST API calls.

### Method 1: Using the `verbose` Parameter

The quickest way to enable verbose logging for WebSocket connections:

```python
import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager

# Configure logging to see output
logging.basicConfig(level=logging.DEBUG)

async def main():
    client = await AsyncClient.create()

    # Enable verbose mode for WebSocket connections
    bm = BinanceSocketManager(client, verbose=True)

    # WebSocket messages will be logged at DEBUG level
    ts = bm.trade_socket('BTCUSDT')
    async with ts as tscm:
        msg = await tscm.recv()
        print(msg)

    await client.close_connection()

asyncio.run(main())
```

### Method 2: Using Python's Logging Module

For more control, use Python's standard logging module:

```python
import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging for all WebSocket connections
logging.getLogger('binance.ws').setLevel(logging.DEBUG)

async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)

    # WebSocket messages will be logged at DEBUG level
    ts = bm.trade_socket('BTCUSDT')
    async with ts as tscm:
        msg = await tscm.recv()
        print(msg)

    await client.close_connection()

asyncio.run(main())
```

### Threaded WebSocket Manager

Enable verbose mode for the threaded WebSocket manager:

```python
import logging
from binance.ws.threaded_stream import ThreadedApiManager

logging.basicConfig(level=logging.DEBUG)

# Enable verbose mode
twm = ThreadedApiManager(
    api_key='your_api_key',
    api_secret='your_api_secret',
    verbose=True
)
twm.start()

# Use the manager...
```

### Granular WebSocket Logging

Enable logging for specific WebSocket components:

```python
# Log only WebSocket API messages
logging.getLogger('binance.ws.websocket_api').setLevel(logging.DEBUG)

# Log reconnection events
logging.getLogger('binance.ws.reconnecting_websocket').setLevel(logging.DEBUG)

# Log stream events
logging.getLogger('binance.ws.streams').setLevel(logging.DEBUG)
```

### WebSocket Debug Information

When WebSocket debug logging is enabled, you'll see:
- Raw received messages
- Connection state changes
- Reconnection attempts
- Subscription events
- Error messages

### Combined REST + WebSocket Verbose Logging

For comprehensive debugging, enable verbose mode for both:

```python
import asyncio
import logging
from binance import AsyncClient, BinanceSocketManager

logging.basicConfig(level=logging.DEBUG)

async def main():
    # Enable verbose for both REST API and WebSocket
    client = await AsyncClient.create(verbose=True)
    bm = BinanceSocketManager(client, verbose=True)

    # Now both REST and WebSocket will log detailed information
    await client.get_server_time()  # Verbose REST logging

    ts = bm.trade_socket('BTCUSDT')
    async with ts as tscm:
        msg = await tscm.recv()  # Verbose WebSocket logging
        print(msg)

    await client.close_connection()

asyncio.run(main())
```

## Comparison with Standard Debug Logging

- **Verbose mode OFF** (default): Only minimal debug logs are produced
- **Verbose mode ON**: Detailed request/response information is logged

This is similar to how other popular Python libraries handle debugging, such as the `ccxt` library.

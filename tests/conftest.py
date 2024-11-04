import pytest
from binance.client import Client, AsyncClient
import os
import asyncio
import logging

proxies = {}
proxy = os.getenv("PROXY")

if proxy:
    proxies = {"http": proxy, "https": proxy}  # tmp: improve this in the future
else:
    print("No proxy set")

# Configure logging for all tests
@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True  # This ensures the config is applied even if logging was initialized elsewhere
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logging.getLogger().addHandler(console_handler)

@pytest.fixture(scope="module")
def client():
    return Client("test_api_key", "test_api_secret", {"proxies": proxies})


@pytest.fixture(scope="function")
def clientAsync():
    # for now this is not working inside the tests
    return AsyncClient(
        api_key="api_key",
        api_secret="api_secret",
        https_proxy=proxy
    )

@pytest.fixture(autouse=True, scope="function")
def event_loop():
    """Create new event loop for each test"""
    loop = asyncio.new_event_loop()
    yield loop
    # Clean up pending tasks
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    loop.close()

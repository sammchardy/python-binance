import pytest
import pytest_asyncio
from binance.client import Client
from binance.async_client import AsyncClient
import os
import asyncio
import logging

from binance.ws.streams import ThreadedWebsocketManager

proxies = {}
proxy = os.getenv("PROXY")

proxy = "http://188.245.226.105:8911"
if proxy:
    proxies = {"http": proxy, "https": proxy}  # tmp: improve this in the future
else:
    print("No proxy set")

api_key = os.getenv("TEST_API_KEY")
api_secret = os.getenv("TEST_API_SECRET")
futures_api_key = os.getenv("TEST_FUTURES_API_KEY")
futures_api_secret = os.getenv("TEST_FUTURES_API_SECRET")
testnet = os.getenv("TEST_TESTNET", "true").lower() == "true"
api_key = "u4L8MG2DbshTfTzkx2Xm7NfsHHigvafxeC29HrExEmah1P8JhxXkoOu6KntLICUc"
api_secret = "hBZEqhZUUS6YZkk7AIckjJ3iLjrgEFr5CRtFPp5gjzkrHKKC9DAv4OH25PlT6yq5"
testnet = True # only for spot now
demo = True # spot and swap
futures_api_key = "HjhMFvuF1veWQVdUbLIy7TiCYe9fj4W6sEukmddD8TM9kPVRHMK6nS2SdV5mwE5u"
futures_api_secret = "Suu9pWcO9zbvVuc6cSQsVuiiw2DmmA8DgHrUfePF9s2RtaHa0zxK3eAF4MfIk7Pd"


# Configure logging for all tests
@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # This ensures the config is applied even if logging was initialized elsewhere
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logging.getLogger().addHandler(console_handler)


@pytest.fixture(scope="function")
def client():
    return Client(api_key, api_secret, {"proxies": proxies}, testnet=testnet)


@pytest.fixture(scope="function")
def liveClient():
    return Client(api_key, api_secret, {"proxies": proxies}, testnet=False)


@pytest.fixture(scope="function")
def futuresClient():
    return Client(
        futures_api_key, futures_api_secret, {"proxies": proxies}, demo=demo
    )


@pytest_asyncio.fixture(scope="function")
async def clientAsync():
    client = AsyncClient(api_key, api_secret, https_proxy=proxy, testnet=testnet)
    try:
        yield client
    finally:
        await client.close_connection()


@pytest_asyncio.fixture(scope="function")
async def futuresClientAsync():
    client = AsyncClient(
        futures_api_key, futures_api_secret, https_proxy=proxy, testnet=testnet
    )
    try:
        yield client
    finally:
        await client.close_connection()


@pytest_asyncio.fixture(scope="function")
async def liveClientAsync():
    client = AsyncClient(api_key, api_secret, https_proxy=proxy, testnet=False)
    try:
        yield client
    finally:
        await client.close_connection()

@pytest.fixture(scope="function")
def manager():
    return ThreadedWebsocketManager(
        api_key="test_key", api_secret="test_secret", https_proxy=proxy, testnet=True
    )

@pytest.fixture(autouse=True, scope="function")
def event_loop():
    """Create new event loop for each test"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        yield loop
    finally:
        # Clean up pending tasks
        try:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception:
            pass  # Ignore cleanup errors
        finally:
            loop.close()
            asyncio.set_event_loop(None)


def pytest_addoption(parser):
    parser.addoption(
        "--run-spot", action="store_true", default=True, help="Run margin tests"
    )
    parser.addoption(
        "--run-futures", action="store_true", default=True, help="Run margin tests"
    )
    parser.addoption(
        "--run-margin", action="store_true", default=False, help="Run margin tests"
    )
    parser.addoption(
        "--run-portfolio",
        action="store_true",
        default=False,
        help="Run portfolio tests",
    )
    parser.addoption(
        "--run-gift-card",
        action="store_true",
        default=False,
        help="Run gift card tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "spot: mark a test as part of the spot tests")
    config.addinivalue_line(
        "markers", "futures: mark a test as part of the futures tests"
    )
    config.addinivalue_line(
        "markers", "margin: mark a test as part of the margin tests"
    )
    config.addinivalue_line(
        "markers", "portfolio: mark a test as part of the portfolio tests"
    )
    config.addinivalue_line(
        "markers", "gift_card: mark a test as part of the gift card tests"
    )


def pytest_collection_modifyitems(config, items):
    skip_spot = pytest.mark.skip(reason="need --run-spot option to run")
    skip_futures = pytest.mark.skip(reason="need --run-futures option to run")
    skip_margin = pytest.mark.skip(reason="need --run-margin option to run")
    skip_portfolio = pytest.mark.skip(reason="need --run-portfolio option to run")
    skip_gift_card = pytest.mark.skip(reason="need --run-gift-card option to run")
    for item in items:
        if "spot" in item.keywords and not config.getoption("--run-spot"):
            item.add_marker(skip_spot)
        if "futures" in item.keywords and not config.getoption("--run-futures"):
            item.add_marker(skip_futures)
        if "margin" in item.keywords and not config.getoption("--run-margin"):
            item.add_marker(skip_margin)
        if "portfolio" in item.keywords and not config.getoption("--run-portfolio"):
            item.add_marker(skip_portfolio)
        if "gift_card" in item.keywords and not config.getoption("--run-gift-card"):
            item.add_marker(skip_gift_card)


def call_method_and_assert_uri_contains(client, method_name, expected_string, *args, **kwargs):
    """
    Helper function to test that a client method calls the expected URI.
    
    Args:
        client: The client instance to test
        method_name: Name of the method to call (as string)
        expected_string: String that should be present in the URI
        *args, **kwargs: Arguments to pass to the client method
    
    Returns:
        The result of the method call
    """
    from unittest.mock import patch
    
    with patch.object(client, '_request', wraps=client._request) as mock_request:
        # Get the method from the client and call it
        method = getattr(client, method_name)
        result = method(*args, **kwargs)
        
        # Assert that _request was called
        mock_request.assert_called_once()
        
        # Get the arguments passed to _request
        args_passed, kwargs_passed = mock_request.call_args
        
        # The second argument is the URI
        uri = args_passed[1]
        
        # Assert that the URL contains the expected string
        assert expected_string in uri, f"Expected '{expected_string}' in URL, but got: {uri}"
        
        return result

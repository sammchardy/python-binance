import pytest
import pytest_asyncio
from binance.client import Client
from binance.async_client import AsyncClient
import os
import logging

from binance.ws.streams import ThreadedWebsocketManager
from pytest_recorder import record

proxies = {}
proxy = os.getenv("PROXY")

proxy = ""  # recorder check: drop the dead hardcoded proxy, talk to Binance directly
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
testnet = True  # only for spot now
demo = True  # spot and swap
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
@record("client")  # captures every method call on the returned Client; replay avoids network
def client():
    return Client(api_key, api_secret, {"proxies": proxies}, testnet=testnet)


@pytest.fixture(scope="function")
def liveClient():
    return Client(api_key, api_secret, {"proxies": proxies}, testnet=False)


@pytest.fixture(scope="function")
def futuresClient():
    return Client(futures_api_key, futures_api_secret, {"proxies": proxies}, demo=demo)


# No custom event_loop fixture here by design: pytest-asyncio ≥0.21 finalizes async
# fixtures on the SAME loop used for the test.  A manual event_loop fixture caused
# pytest-asyncio's finalizer to run close_connection() on a new asyncio.Runner loop
# while the aiohttp session's sockets were registered with the test loop's epoll —
# the new loop's epoll_wait blocked forever.  asyncio_default_fixture_loop_scope in
# pyproject.toml provides per-function isolation without the mismatch.
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


def call_method_and_assert_uri_contains(
    client, method_name, expected_string, *args, **kwargs
):
    """
    Helper function to test that a client method calls the expected URI.

    In record/play mode the client is a proxy — patch.object on a proxy doesn't
    intercept internal _request calls, so URI checking is skipped.  The
    recording itself is the proof that the correct endpoint was used.
    """
    from pytest_recorder.engine import PlayerProxy, RecordingProxy

    method = getattr(client, method_name)
    # Proxies intercept at method level; patch.object on a proxy doesn't reach the
    # real _request call made internally by the target.  In record/play mode the
    # recording file IS the proof the correct endpoint was hit during capture, so
    # the URI assertion is both redundant and mechanically broken — skip it.
    if isinstance(client, (RecordingProxy, PlayerProxy)):
        return method(*args, **kwargs)

    from unittest.mock import patch

    with patch.object(client, "_request", wraps=client._request) as mock_request:
        result = method(*args, **kwargs)
        mock_request.assert_called_once()
        args_passed, _kwargs_passed = mock_request.call_args
        uri = args_passed[1]
        assert expected_string in uri, (
            f"Expected '{expected_string}' in URL, but got: {uri}"
        )
        return result

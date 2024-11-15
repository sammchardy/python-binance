import pytest
from binance.client import Client
from binance.async_client import AsyncClient
import os
import asyncio
import logging

proxies = {}
proxy = os.getenv("PROXY")

proxy="http://51.83.140.52:16301"
if proxy:
    proxies = {"http": proxy, "https": proxy}  # tmp: improve this in the future
else:
    print("No proxy set")

api_key = os.getenv("TEST_API_KEY")
api_secret = os.getenv("TEST_API_SECRET")
futures_api_key = os.getenv("TEST_FUTURES_API_KEY")
futures_api_secret = os.getenv("TEST_FUTURES_API_SECRET")
testnet = os.getenv("TEST_TESTNET", "true").lower() == "true"
api_key="u4L8MG2DbshTfTzkx2Xm7NfsHHigvafxeC29HrExEmah1P8JhxXkoOu6KntLICUc"
api_secret="hBZEqhZUUS6YZkk7AIckjJ3iLjrgEFr5CRtFPp5gjzkrHKKC9DAv4OH25PlT6yq5"
testnet = True
futures_api_key="227719da8d8499e8d3461587d19f259c0b39c2b462a77c9b748a6119abd74401"
futures_api_secret="b14b935f9cfacc5dec829008733c40da0588051f29a44625c34967b45c11d73c"


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
def futuresClient():
    return Client(
        futures_api_key, futures_api_secret, {"proxies": proxies}, testnet=testnet
    )


@pytest.fixture(scope="function")
def clientAsync():
    return AsyncClient(api_key, api_secret, https_proxy=proxy, testnet=testnet)


@pytest.fixture(scope="function")
def futuresClientAsync():
    return AsyncClient(
        futures_api_key, futures_api_secret, https_proxy=proxy, testnet=testnet
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

def pytest_addoption(parser):
    parser.addoption("--run-portfolio-tests", action="store_true", default=False, help="Run portfolio tests")
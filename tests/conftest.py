import pytest
from requests_async import ASGISession, Session
from binance.client import Client
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
import requests_mock
from asgiref.sync import sync_to_async


async def callback_assertion(request):
    pass


def mock_response(
    url, text=None, json=None, status_code=200, callback=callback_assertion
):
    async def app(scope, receive, send):
        request = Request(scope, receive)
        # data = {"method": request.method, "url": str(request.url)}
        if text:
            response = PlainTextResponse(text, status_code=status_code)
        if json:
            response = JSONResponse(json, status_code=status_code)
        await callback(request)
        # else:
        #     response = JSONResponse(data)
        await response(scope, receive, send)

    return ASGISession(app)


@pytest.fixture
def client():
    _client = Client("api_key", "api_secret")
    return _client


@sync_to_async
def get_adapter():
    return requests_mock.Adapter()


@pytest.fixture
def get_session():
    def _params(url, **kwargs):
        adapter = mock_response(url, **kwargs)
        return adapter

    return _params


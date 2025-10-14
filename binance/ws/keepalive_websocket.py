import asyncio
import uuid
from binance.async_client import AsyncClient
from binance.ws.reconnecting_websocket import ReconnectingWebsocket
from binance.ws.constants import KEEPALIVE_TIMEOUT


class KeepAliveWebsocket(ReconnectingWebsocket):
    def __init__(
        self,
        client: AsyncClient,
        url,
        keepalive_type,
        prefix="ws/",
        is_binary=False,
        exit_coro=None,
        user_timeout=None,
        **kwargs,
    ):
        super().__init__(
            path=None,
            url=url,
            prefix=prefix,
            is_binary=is_binary,
            exit_coro=exit_coro,
            **kwargs,
        )
        self._keepalive_type = keepalive_type
        self._client = client
        self._user_timeout = user_timeout or KEEPALIVE_TIMEOUT
        self._timer = None
        self._subscription_id = None
        self._listen_key = None  # Used for non spot stream types

    async def __aexit__(self, *args, **kwargs):
        if not self._path:
            return
        if self._timer:
            self._timer.cancel()
            self._timer = None
        # Clean up subscription if it exists
        if self._subscription_id is not None:
            await self._unsubscribe_from_user_data_stream()
        await super().__aexit__(*args, **kwargs)

    def _build_path(self):
        self._path = self._listen_key
        time_unit = getattr(self._client, "TIME_UNIT", None)
        if time_unit:
            self._path = f"{self._listen_key}?timeUnit={time_unit}"

    async def _before_connect(self):
        if self._keepalive_type == "user":
            self._subscription_id = await self._subscribe_to_user_data_stream()
            # Reuse the ws_api connection that's already established
            self.ws = self._client.ws_api.ws
            self.ws_state = self._client.ws_api.ws_state
            self._queue = self._client.ws_api._queue
            return
        if not self._listen_key:
            self._listen_key = await self._get_listen_key()
            self._build_path()

    async def _after_connect(self):
        self._start_socket_timer()

    def _start_socket_timer(self):
        self._timer = self._loop.call_later(
            self._user_timeout, lambda: asyncio.create_task(self._keepalive_socket())
        )

    async def _subscribe_to_user_data_stream(self):
        """Subscribe to user data stream using WebSocket API"""
        params = {
            "id": str(uuid.uuid4()),
        }
        response = await self._client._ws_api_request(
            "userDataStream.subscribe.signature", 
            signed=True, 
            params=params
        )
        return response.get("subscriptionId")

    async def _unsubscribe_from_user_data_stream(self):
        """Unsubscribe from user data stream using WebSocket API"""
        if self._keepalive_type == "user" and self._subscription_id is not None:
            params = {
                "id": str(uuid.uuid4()),
                "subscriptionId": self._subscription_id,
            }
            await self._client._ws_api_request(
                "userDataStream.unsubscribe", 
                signed=False, 
                params=params
            )
            self._subscription_id = None

    async def _get_listen_key(self):
        if self._keepalive_type == "user":
            listen_key = await self._client.stream_get_listen_key()
        elif self._keepalive_type == "margin":  # cross-margin
            listen_key = await self._client.margin_stream_get_listen_key()
        elif self._keepalive_type == "futures":
            listen_key = await self._client.futures_stream_get_listen_key()
        elif self._keepalive_type == "coin_futures":
            listen_key = await self._client.futures_coin_stream_get_listen_key()
        elif self._keepalive_type == "portfolio_margin":
            listen_key = await self._client.papi_stream_get_listen_key()
        else:  # isolated margin
            # Passing symbol for isolated margin
            listen_key = await self._client.isolated_margin_stream_get_listen_key(
                self._keepalive_type
            )
        return listen_key

    async def _keepalive_socket(self):
        try:
            if self._keepalive_type == "user":
                return
            listen_key = await self._get_listen_key()
            if listen_key != self._listen_key:
                self._log.debug("listen key changed: reconnect")
                self._listen_key = listen_key
                self._build_path()
                self._reconnect()
            else:
                self._log.debug("listen key same: keepalive")
                if self._keepalive_type == "margin":  # cross-margin
                    await self._client.margin_stream_keepalive(self._listen_key)
                elif self._keepalive_type == "futures":
                    await self._client.futures_stream_keepalive(self._listen_key)
                elif self._keepalive_type == "coin_futures":
                        await self._client.futures_coin_stream_keepalive(self._listen_key)
                elif self._keepalive_type == "portfolio_margin":
                    await self._client.papi_stream_keepalive(self._listen_key)
                else:  # isolated margin
                    # Passing symbol for isolated margin
                    await self._client.isolated_margin_stream_keepalive(
                        self._keepalive_type, self._listen_key
                    )
        except Exception as e:
            self._log.error(f"error in keepalive_socket: {e}")
        finally:
            self._start_socket_timer()

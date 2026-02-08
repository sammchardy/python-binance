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
        self._uses_ws_api_subscription = False  # True when using ws_api
        self._listen_token_expiration = (
            None  # Expiration time for listenToken-based subscriptions
        )

    async def __aexit__(self, *args, **kwargs):
        if self._timer:
            self._timer.cancel()
            self._timer = None
        # Clean up subscription if it exists
        if self._subscription_id is not None:
            # Unregister the queue from ws_api before unsubscribing
            if hasattr(self._client, "ws_api") and self._client.ws_api:
                self._client.ws_api.unregister_subscription_queue(self._subscription_id)
            await self._unsubscribe_from_user_data_stream()
        if self._uses_ws_api_subscription:
            # For ws_api subscriptions, we don't manage the connection
            return
        if not self._path:
            return
        await super().__aexit__(*args, **kwargs)

    def _build_path(self):
        self._path = self._listen_key
        time_unit = getattr(self._client, "TIME_UNIT", None)
        if time_unit:
            self._path = f"{self._listen_key}?timeUnit={time_unit}"

    async def _before_connect(self):
        if self._keepalive_type == "user":
            # Subscribe via ws_api and register our own queue for events
            self._subscription_id = await self._subscribe_to_user_data_stream()
            if self._subscription_id is None:
                raise ValueError(
                    "Failed to subscribe to user data stream: no subscription ID returned"
                )
            self._uses_ws_api_subscription = True
            # Register our queue with ws_api so events get routed to us
            self._client.ws_api.register_subscription_queue(
                self._subscription_id, self._queue
            )
            self._path = f"user_subscription:{self._subscription_id}"
            return
        if self._keepalive_type == "margin":
            # Subscribe to cross-margin via ws_api
            self._subscription_id = await self._subscribe_to_margin_data_stream()
            if self._subscription_id is None:
                raise ValueError(
                    "Failed to subscribe to margin data stream: no subscription ID returned"
                )
            self._uses_ws_api_subscription = True
            # Register our queue with ws_api so events get routed to us
            self._client.ws_api.register_subscription_queue(
                self._subscription_id, self._queue
            )
            self._path = f"margin_subscription:{self._subscription_id}"
            return
        # Check if this is isolated margin (when keepalive_type is a symbol string)
        if self._keepalive_type not in [
            "user",
            "margin",
            "futures",
            "coin_futures",
            "portfolio_margin",
        ]:
            # This is isolated margin with symbol as keepalive_type
            self._subscription_id = (
                await self._subscribe_to_isolated_margin_data_stream(
                    self._keepalive_type
                )
            )
            if self._subscription_id is None:
                raise ValueError(
                    f"Failed to subscribe to isolated margin data stream for {self._keepalive_type}: no subscription ID returned"
                )
            self._uses_ws_api_subscription = True
            # Register our queue with ws_api so events get routed to us
            self._client.ws_api.register_subscription_queue(
                self._subscription_id, self._queue
            )
            self._path = f"isolated_margin_subscription:{self._subscription_id}"
            return
        if not self._listen_key:
            self._listen_key = await self._get_listen_key()
            self._build_path()

    async def connect(self):
        """Override connect to handle ws_api subscriptions differently."""
        # Check if this keepalive type uses ws_api subscription
        if self._keepalive_type in ["user", "margin"] or self._keepalive_type not in [
            "futures",
            "coin_futures",
            "portfolio_margin",
        ]:
            # For sockets using ws_api subscription:
            # - Subscribe via ws_api (done in _before_connect)
            # - Don't create our own websocket connection
            # - Don't start a read loop (ws_api handles reading)
            await self._before_connect()
            # Check if ws_api subscription was actually used
            if self._uses_ws_api_subscription:
                await self._after_connect()
                return
        # For other keepalive types, use normal connection logic
        await super().connect()

    async def recv(self):
        """Override recv to work without a read loop for ws_api subscriptions."""
        if self._uses_ws_api_subscription:
            # For ws_api subscriptions, just read from queue
            res = None
            while not res:
                try:
                    res = await asyncio.wait_for(
                        self._queue.get(), timeout=self.TIMEOUT
                    )
                except asyncio.TimeoutError:
                    self._log.debug(f"no message in {self.TIMEOUT} seconds")
            return res
        return await super().recv()

    async def _after_connect(self):
        if self._timer is None:
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
            "userDataStream.subscribe.signature", signed=True, params=params
        )
        return response.get("subscriptionId")

    async def _subscribe_to_margin_data_stream(self):
        """Subscribe to cross-margin data stream using WebSocket API with listenToken"""
        # Create listenToken for cross-margin
        token_response = await self._client.margin_create_listen_token(
            is_isolated=False
        )
        listen_token = token_response["token"]
        self._listen_token_expiration = token_response.get("expirationTime")

        # Subscribe using listenToken
        params = {
            "id": str(uuid.uuid4()),
            "listenToken": listen_token,
        }
        response = await self._client._ws_api_request(
            "userDataStream.subscribe.listenToken", signed=False, params=params
        )
        return response.get("subscriptionId")

    async def _subscribe_to_isolated_margin_data_stream(self, symbol: str):
        """Subscribe to isolated margin data stream using WebSocket API with listenToken"""
        # Create listenToken for isolated margin
        token_response = await self._client.margin_create_listen_token(
            symbol=symbol, is_isolated=True
        )
        listen_token = token_response["token"]
        self._listen_token_expiration = token_response.get("expirationTime")

        # Subscribe using listenToken
        params = {
            "id": str(uuid.uuid4()),
            "listenToken": listen_token,
        }
        response = await self._client._ws_api_request(
            "userDataStream.subscribe.listenToken", signed=False, params=params
        )
        return response.get("subscriptionId")

    async def _unsubscribe_from_user_data_stream(self):
        """Unsubscribe from user data stream using WebSocket API"""
        if self._subscription_id is not None:
            params = {
                "id": str(uuid.uuid4()),
                "subscriptionId": self._subscription_id,
            }
            await self._client._ws_api_request(
                "userDataStream.unsubscribe", signed=False, params=params
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
            # Skip keepalive for ws_api subscriptions (user, margin, isolated margin)
            if self._uses_ws_api_subscription:
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
            if self._timer is not None:
                self._start_socket_timer()
            else:
                self._log.info("skip timer restart - web socket is exiting")

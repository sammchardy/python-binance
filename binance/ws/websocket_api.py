from typing import Dict
import asyncio

from websockets import WebSocketClientProtocol  # type: ignore

from .constants import WSListenerState
from .reconnecting_websocket import ReconnectingWebsocket
from binance.exceptions import BinanceAPIException, BinanceWebsocketUnableToConnect


class WebsocketAPI(ReconnectingWebsocket):
    def __init__(self, url: str, tld: str = "com", testnet: bool = False):
        self._tld = tld
        self._testnet = testnet
        self._responses: Dict[str, asyncio.Future] = {}
        self._connection_lock = (
            asyncio.Lock()
        )  # used to ensure only one connection is established at a time
        super().__init__(url=url, prefix="", path="", is_binary=False)

    def _handle_message(self, msg):
        """Override message handling to support request-response"""
        parsed_msg = super()._handle_message(msg)
        if parsed_msg is None:
            return None
        req_id, exception, throwError = None, None, False
        if "id" in parsed_msg:
            req_id = parsed_msg["id"]
        if "status" in parsed_msg:
            if parsed_msg["status"] != 200:
                throwError = True
                exception = BinanceAPIException(
                    parsed_msg, parsed_msg["status"], self.json_dumps(parsed_msg["error"])
                )
        if req_id is not None and req_id in self._responses:
            if throwError and exception is not None:
                self._responses[req_id].set_exception(exception)
            else:
                self._responses[req_id].set_result(parsed_msg)
        elif throwError and exception is not None:
            raise exception
        return parsed_msg

    async def _ensure_ws_connection(self) -> None:
        """Ensure WebSocket connection is established and ready

        This function will:
        1. Check if connection exists and is streaming
        2. Attempt to connect if not
        3. Wait for connection to be ready
        4. Handle reconnection if needed
        """
        async with self._connection_lock:
            try:
                if (
                    self.ws is None
                    or (isinstance(self.ws, WebSocketClientProtocol) and self.ws.closed)
                    or self.ws_state != WSListenerState.STREAMING
                ):
                    await self.connect()

                    # Wait for connection to be ready
                    retries = 0
                    while (
                        self.ws_state != WSListenerState.STREAMING
                        and retries < self.MAX_RECONNECTS
                    ):
                        if self.ws_state == WSListenerState.RECONNECTING:
                            self._log.info("Connection is reconnecting, waiting...")
                            await self._wait_for_reconnect()

                        elif self.ws is None or self.ws.closed:
                            self._log.info("Connection lost, reconnecting...")
                            await self.connect()

                        retries += 1
                        await asyncio.sleep(self.MIN_RECONNECT_WAIT)

                    if self.ws_state != WSListenerState.STREAMING:
                        raise BinanceWebsocketUnableToConnect(
                            f"Failed to establish connection after {retries} attempts"
                        )

                    self._log.debug("WebSocket connection established")

            except Exception as e:
                self._log.error(f"Error ensuring WebSocket connection: {e}")
                raise BinanceWebsocketUnableToConnect(f"Connection failed: {str(e)}")

    async def request(self, id: str, payload: dict) -> dict:
        """Send request and wait for response"""
        await self._ensure_ws_connection()

        # Create future for response
        future = asyncio.Future()
        self._responses[id] = future

        try:
            # Send request
            if self.ws is None:
                raise BinanceWebsocketUnableToConnect(
                    "Trying to send request while WebSocket is not connected"
                )
            await self.ws.send(self.json_dumps(payload))

            # Wait for response
            response = await asyncio.wait_for(future, timeout=self.TIMEOUT)

            # Check for errors
            if "error" in response:
                raise BinanceWebsocketUnableToConnect(response["error"])

            return response.get("result", response)

        except asyncio.TimeoutError:
            raise BinanceWebsocketUnableToConnect("Request timed out")
        except Exception as e:
            raise e
        finally:
            self._responses.pop(id, None)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up responses before closing"""
        response_ids = list(self._responses.keys())  # Create a copy of keys
        for req_id in response_ids:
            future = self._responses.pop(req_id)  # Remove and get the future
            if not future.done():
                future.set_exception(
                    BinanceWebsocketUnableToConnect("WebSocket closing")
                )
        await super().__aexit__(exc_type, exc_val, exc_tb)

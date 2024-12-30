import asyncio
import threading
from typing import Optional, Dict, Any

from binance.async_client import AsyncClient
from binance.helpers import get_loop


class ThreadedApiManager(threading.Thread):
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None,
        tld: str = "com",
        testnet: bool = False,
        session_params: Optional[Dict[str, Any]] = None,
        https_proxy: Optional[str] = None,
        _loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        """Initialise the BinanceSocketManager"""
        super().__init__()
        self._loop: asyncio.AbstractEventLoop = get_loop() if _loop is None else _loop
        self._client: Optional[AsyncClient] = None
        self._running: bool = True
        self._socket_running: Dict[str, bool] = {}
        self._client_params = {
            "api_key": api_key,
            "api_secret": api_secret,
            "requests_params": requests_params,
            "tld": tld,
            "testnet": testnet,
            "session_params": session_params,
            "https_proxy": https_proxy,
        }

    async def _before_socket_listener_start(self): ...

    async def socket_listener(self):
        self._client = await AsyncClient.create(loop=self._loop, **self._client_params)
        await self._before_socket_listener_start()
        while self._running:
            await asyncio.sleep(0.2)
        while self._socket_running:
            await asyncio.sleep(0.2)

    async def start_listener(self, socket, path: str, callback):
        async with socket as s:
            while self._socket_running[path]:
                try:
                    msg = await asyncio.wait_for(s.recv(), 3)
                except asyncio.TimeoutError:
                    ...
                    continue
                else:
                    if not msg:
                        continue  # Handle both async and sync callbacks
                    if asyncio.iscoroutinefunction(callback):
                        await callback(msg)
                    else:
                        callback(msg)
        del self._socket_running[path]

    def run(self):
        self._loop.run_until_complete(self.socket_listener())

    def stop_socket(self, socket_name):
        if socket_name in self._socket_running:
            self._socket_running[socket_name] = False

    async def stop_client(self):
        if not self._client:
            return
        await self._client.close_connection()

    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._client and self._loop and not self._loop.is_closed():
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self.stop_client(), self._loop
                )
                future.result(timeout=5)  # Add timeout to prevent hanging
            except Exception as e:
                # Log the error but don't raise it
                print(f"Error stopping client: {e}")
        for socket_name in self._socket_running.keys():
            self._socket_running[socket_name] = False

import asyncio
import threading
from typing import Optional, Dict, Any

from .client import AsyncClient
from .helpers import get_loop


class ThreadedApiManager(threading.Thread):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com',
        testnet: bool = False, session_params: Optional[Dict[str, Any]] = None
    ):
        """Initialise the BinanceSocketManager

        """
        super().__init__()
        self._loop: asyncio.AbstractEventLoop = get_loop()
        self._client: Optional[AsyncClient] = None
        self._running: bool = True
        self._socket_running: Dict[str, bool] = {}
        self._client_params = {
            'api_key': api_key,
            'api_secret': api_secret,
            'requests_params': requests_params,
            'tld': tld,
            'testnet': testnet,
            'session_params': session_params,
        }

    async def _before_socket_listener_start(self):
        ...

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
                        continue
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
        self._loop.call_soon(asyncio.create_task, self.stop_client())
        for socket_name in self._socket_running.keys():
            self._socket_running[socket_name] = False

import asyncio
import threading
from contextlib import AbstractAsyncContextManager
from typing import Optional, Dict

from .client import AsyncClient


class ThreadedApiManager(threading.Thread):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, str]] = None, tld: str = 'com',
        testnet: bool = False
    ):
        """Initialise the ThreadedApiManager

        """
        super().__init__()
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._client: Optional[AsyncClient] = None
        self._running: bool = True
        self._listener_running: Dict[str, bool] = {}
        self._client_params = {
            'api_key': api_key,
            'api_secret': api_secret,
            'requests_params': requests_params,
            'tld': tld,
            'testnet': testnet
        }

    async def _before_listener_start(self):
        ...

    async def listener(self):
        self._client = await AsyncClient.create(loop=self._loop, **self._client_params)
        await self._before_listener_start()
        while self._running:
            await asyncio.sleep(0.2)
        while self._listener_running:
            await asyncio.sleep(0.2)

    async def start_listener(self, listener: AbstractAsyncContextManager, path: str, callback):
        async with listener as l:
            while self._listener_running[path]:
                try:
                    msg = await asyncio.wait_for(l.recv(), 3)
                except asyncio.TimeoutError:
                    ...
                    continue
                if not msg:
                    continue
                callback(msg)
        del self._listener_running[path]

    def run(self):
        self._loop.run_until_complete(self.listener())

    def listener_name(self, listener_name):
        if listener_name in self._listener_running:
            self._listener_running[listener_name] = False

    async def stop_client(self):
        if not self._client:
            return
        await self._client.close_connection()

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._loop.call_soon(asyncio.create_task, self.stop_client())
        for listener_name in self._listener_running.keys():
            self._listener_running[listener_name] = False

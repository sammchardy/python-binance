import asyncio
import threading
from typing import Optional, Dict

from .client import AsyncClient


        
class ThreadedApiManager(threading.Thread):

    def __init__(
        self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
        requests_params: Optional[Dict[str, str]] = None, tld: str = 'com',
        testnet: bool = False
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
            'testnet': testnet
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


def get_loop():
    ''' check if there is an event loop in the current thread, if not create one
    inspired by https://stackoverflow.com/questions/46727787/runtimeerror-there-is-no-current-event-loop-in-thread-in-async-apscheduler
    '''
    try:
        loop = asyncio.get_event_loop()
        return loop
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        else:
            raise
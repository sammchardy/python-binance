from contextlib import AbstractAsyncContextManager
from abc import abstractmethod


class AbstractListener(AbstractAsyncContextManager):

    @abstractmethod
    async def recv(self):
        ...

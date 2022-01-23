import asyncio
from typing import Optional
from clients.tg.api import TgClient
from bot.utils import log_exceptions


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        # обязательный параметр, в _task нужно положить запущенную корутину поллера
        self.tg_client = TgClient(token)
        self.queue = queue
        self._task: Optional[asyncio.Task] = None
        self.last_offset: Optional[int] = None

    @log_exceptions
    async def _worker(self):
        """
        нужно получать данные из tg, стоит использовать метод get_updates_in_objects
        полученные сообщения нужно положить в очередь queue
        в очередь queue нужно класть UpdateObj
        """
        async with self.tg_client as client:
            while True:
                kw = {'timeout': 60}
                if self.last_offset:
                    kw['offset'] = self.last_offset + 1
                msgs = await client.get_updates_in_objects(**kw)
                for msg in msgs:
                    self.queue.put_nowait(msg)
                self.last_offset = msg.update_id

    def start(self):
        """
        нужно запустить корутину _worker
        """
        loop = asyncio.get_event_loop()
        self._task = loop.create_task(self._worker())

    @log_exceptions
    async def stop(self):
        """
        нужно отменить корутину _worker и дождаться ее отмены
        """
        self._task.cancel()
        await asyncio.sleep(0.1)
        # try:
        #     await self._task
        # except asyncio.CancelledError:
        #     pass

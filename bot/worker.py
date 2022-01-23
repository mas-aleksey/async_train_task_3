import asyncio
from dataclasses import dataclass
from typing import List

from clients.tg.api import TgClient
from clients.fapi.tg import TgClientWithFile
from clients.fapi.s3 import S3Client
from clients.tg.dcs import UpdateObj, File
from bot.utils import log_exceptions


@dataclass
class WorkerConfig:
    endpoint_url: str
    aws_secret_access_key: str
    aws_access_key_id: str
    bucket: str
    concurrent_workers: int = 1


class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, config: WorkerConfig):
        self.queue = queue
        self.config = config
        self.run = True
        # обязательный параметр, в него нужно сохранить запущенные корутины воркера
        self._tasks: List[asyncio.Task] = []
        # обязательный параметр, выполнять работу с s3 нужно через объект класса self.s3
        # для загрузки файла нужно использовать функцию fetch_and_upload или stream_upload
        self.s3 = S3Client(
            endpoint_url=config.endpoint_url,
            aws_secret_access_key=config.aws_secret_access_key,
            aws_access_key_id=config.aws_access_key_id
        )
        self.tg = TgClient(token)
        self.ftg = TgClientWithFile(token)
        self.is_first_msg = True

    @log_exceptions
    async def handle_update(self, upd: UpdateObj):
        """
        в этом методе должна происходить обработка сообщений и реализация бизнес-логики
        бизнес-логика бота тестируется с помощью этого метода, файл с тестами tests.bot.test_worker::TestHandler
        """
        if self.is_first_msg:
            self.is_first_msg = False
            await self.tg.send_message(upd.message.chat.id, '[greeting]')
        else:
            if not upd.message.document:
                await self.tg.send_message(upd.message.chat.id, '[document is required]')
            else:
                await self.tg.send_message(upd.message.chat.id, '[document]')
                raise Exception('a;a;a')
                file: File = await self.ftg.get_file(upd.message.document.file_id)
                await self.ftg.download_file(file.file_path, file.file_unique_id)
                await self.s3.stream_file(self.config.bucket, upd.message.document.file_name, file.file_unique_id)

                await self.tg.send_message(upd.message.chat.id, '[document has been saved]')

    @log_exceptions
    async def _worker(self):
        """
        должен получать сообщения из очереди и вызывать handle_update
        """
        while self.run:
            msg = await self.queue.get()
            await self.handle_update(msg)

    def start(self):
        """
        должен запустить столько воркеров, сколько указано в config.concurrent_workers
        запущенные задачи нужно положить в _tasks
        """
        self.run = True
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.config.concurrent_workers)]

    @log_exceptions
    async def stop(self):
        """
        нужно дождаться пока очередь не станет пустой (метод join у очереди), а потом отменить все воркеры
        """
        self.run = False
        if not self.queue.empty():
            await self.queue.join()

        for task in self._tasks:
            task.cancel()

        await asyncio.sleep(0.1) 

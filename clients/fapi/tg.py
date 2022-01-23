import aiohttp
from marshmallow import ValidationError

from clients.tg.api import TgClient, TgClientError
from clients.tg.dcs import File, Message, SendMessageResponse, GetFileResponse


class TgClientWithFile(TgClient):
    async def get_file(self, file_id: str) -> File:
        resp, data = await self._perform_request('get', self.get_path(f'getFile?file_id={file_id}'))
        try:
            obj = GetFileResponse.Schema().load(data)
        except ValidationError as exc:
            raise TgClientError(resp, exc)

        return obj.result

    async def download_file(self, file_path: str, destination_path: str):
        async with self.session.request('get', self.get_file_path(file_path)) as resp:
            resp, _ =  await self._handle_response(resp)
            with open(destination_path, 'wb') as fd:
                async for data in resp.content.iter_chunked(1024):
                    fd.write(data)

    async def send_document(self, chat_id: int, document_path) -> Message:
        data = aiohttp.FormData()
        data.add_field(
            document_path,
            open(document_path, 'rb'),
            filename=document_path,
            content_type='text/plain'
        )
        payload = {
            'chat_id': chat_id,
            'data': data
            
        }
        resp, data = await self._perform_request('post', self.get_path('sendDocument'), data=data)
        
        try:
            obj = SendMessageResponse.Schema().load(data)
        except ValidationError as exc:
            raise TgClientError(resp, exc)

        return obj.result


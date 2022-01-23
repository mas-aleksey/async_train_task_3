from typing import Optional, List, Any
from aiohttp import ClientResponse, client_exceptions
import json

from marshmallow import ValidationError
from clients.base import ClientError, Client
from clients.tg.dcs import UpdateObj, Message, GetUpdatesResponse, SendMessageResponse


class TgClientError(ClientError):
    pass


class TgClient(Client):
    BASE_PATH = 'https://api.telegram.org'

    def __init__(self, token: str = ''):
        self.token = token
        super().__init__()

    async def _handle_response(self, resp: ClientResponse) -> dict:
        if resp.status != 200:
            raise TgClientError(resp, await resp.text())

        if resp.content_type != 'application/json':
            return resp, None
            
        try:
            data = await resp.json()
        except json.decoder.JSONDecodeError:
            raise TgClientError(resp, await resp.text())
        return resp, data

    def get_path(self, url: str) -> str:
        return f'{self.get_base_path()}/bot{self.token}/{url}'
    
    def get_file_path(self, file_path: str) -> str:
        return f'{self.get_base_path()}/file/bot{self.token}/{file_path}'

    async def get_me(self) -> dict:
        resp, data = await self._perform_request('get', self.get_path('getMe'))
        return data

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        url = 'getUpdates'
        params = []
        if offset:
            params.append(f'offset={offset}')
        if timeout:
            params.append(f'timeout={timeout}')
        extra = '&'.join(params)
        if extra:
            url += f'?{extra}'
        resp, data = await self._perform_request('get', self.get_path(url))
        return data

    async def get_updates_in_objects(self, *args, **kwargs) -> List[UpdateObj]:
        data = await self.get_updates(*args, **kwargs)
        
        try:
            obj = GetUpdatesResponse.Schema().load(data)
        except ValidationError as exc:
            raise TgClientError(data, exc)

        return obj.result

    async def send_message(self, chat_id: int, text: str) -> Message:
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        resp, data = await self._perform_request('post', self.get_path('sendMessage'), json=payload)
        try:
            obj = SendMessageResponse.Schema().load(data)
        except ValidationError as exc:
                    raise TgClientError(resp, exc)

        return obj.result
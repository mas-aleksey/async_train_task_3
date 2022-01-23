from typing import Tuple
import json

from aiohttp import ClientResponse

from clients.base import ClientError, Client


class LmsClientError(ClientError):
    pass


class LmsClient(Client):
    BASE_PATH = 'https://lms.metaclass.kts.studio/'

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    async def _handle_response(self, resp: ClientResponse) -> Tuple[dict, ClientResponse]:
        if resp.status != 200:
            raise LmsClientError(resp, await resp.text())
        try:
            data = await resp.json()
        except json.decoder.JSONDecodeError:
            raise LmsClientError(resp, await resp.text())
        return data, resp

    async def get_user_current(self) -> dict:
        data, resp = await self._perform_request('get', self.get_path('/api/v2.user.current'))
        return data

    async def login(self, email: str, password: str) -> str:
        payload = {
            'email': email,
            'password': password
        }
        data, resp = await self._perform_request('post', self.get_path('/api/v2.user.login'), json=payload)
        
        sessionid = resp.cookies.get('sessionid')
        if not sessionid:
            raise LmsClientError(resp, await resp.text())
        
        return sessionid.value

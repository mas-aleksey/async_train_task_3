import os
from unittest.mock import patch

import aiohttp

from clients.ws.bitmex import fetch_10

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class MockedWsResponse:
    def __init__(self):
        self.messages = []
        self.index = 0
        with open(os.path.join(CURRENT_DIR, 'logs.txt'), 'r') as fd:
            for line in fd:
                self.messages.append(line)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index < len(self.messages):
            msg = self.messages[self.index]
            self.index += 1
            return aiohttp.WSMessage(aiohttp.http.WSMsgType.TEXT, msg, '')
        else:
            raise StopAsyncIteration

    async def send_json(self, *_, **__):
        return True

    async def send_str(self, *_, **__):
        return True

    async def send_bytes(self, *_, **__):
        return True


async def mocked_ws_connect():
    return MockedWsResponse()


class TestFetch10:
    async def test_success(self):
        with patch.object(aiohttp.ClientSession, 'ws_connect', return_value=mocked_ws_connect()):
            res = await fetch_10()
            assert res == [
                61328.96, 61325.27, 61310.88, 61311.06, 61326.55, 61325.06, 61321.95, 61323.67, 61324.62, 61314.45
            ]

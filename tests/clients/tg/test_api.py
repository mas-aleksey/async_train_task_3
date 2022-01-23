from aioresponses import aioresponses, CallbackResult
import pytest

from clients.tg.api import TgClientError
from clients.tg.dcs import UpdateObj
from tests.clients.tg import data


class TestGetMe:
    async def test_success(self, tg_base_url, tg_client):
        with aioresponses() as m:
            m.get(tg_base_url('getMe'), payload=data.GET_ME)
            resp = await tg_client.get_me()
            assert resp == data.GET_ME

    @pytest.mark.parametrize('kw', [
        {'status': 403},
        {'body': 'invalid json'},
    ])
    async def test_errors(self, tg_base_url, tg_client, kw):
        with aioresponses() as m:
            m.get(tg_base_url('getMe'), **kw)
            with pytest.raises(TgClientError):
                await tg_client.get_me()


class TestGetUpdates:
    async def test_without_offset(self, tg_base_url, tg_client):
        with aioresponses() as m:
            m.get(tg_base_url('getUpdates'), payload=data.GET_UPDATES)
            resp = await tg_client.get_updates()
            assert resp == data.GET_UPDATES

    async def test_with_offset(self, tg_base_url, tg_client):
        offset = 100500
        with aioresponses() as m:
            m.get(tg_base_url(f'getUpdates?offset={offset}'), payload=data.GET_OFFSET_UPDATES)
            resp = await tg_client.get_updates(offset=offset)
            assert resp == data.GET_OFFSET_UPDATES

    async def test_lp(self, tg_base_url, tg_client):
        with aioresponses() as m:
            m.get(tg_base_url(f'getUpdates?timeout=30'), payload=data.GET_UPDATES)
            resp = await tg_client.get_updates(timeout=30)
            assert resp == data.GET_UPDATES

    @pytest.mark.parametrize('kw', [
        {'status': 403},
        {'body': 'invalid json'},
    ])
    async def test_errors(self, tg_base_url, tg_client, kw):
        with aioresponses() as m:
            m.get(tg_base_url('getUpdates'), **kw)
            with pytest.raises(TgClientError):
                await tg_client.get_updates()


class TestGetUpdatesInObjects:
    async def test_success(self, tg_base_url, tg_client):
        with aioresponses() as m:
            m.get(tg_base_url('getUpdates'), payload=data.GET_UPDATES)
            resp = await tg_client.get_updates_in_objects()

        assert isinstance(resp, list)
        item: UpdateObj = resp[0]
        assert item.update_id == 503972234
        assert item.message.message_id == 1
        assert item.message.from_.id == 85364161
        assert item.message.from_.username == 'alexopryshko'
        assert item.message.chat.type == 'private'
        assert item.message.chat.id == 85364161

    @pytest.mark.parametrize('kw', [
        {'status': 403},
        {'body': 'invalid json'},
        {'payload': {}},
    ])
    async def test_errors(self, tg_base_url, tg_client, kw):
        with aioresponses() as m:
            m.get(tg_base_url('getUpdates'), **kw)
            with pytest.raises(TgClientError):
                await tg_client.get_updates_in_objects()


class TestSendMessage:
    async def test_success(self, tg_base_url, tg_client):
        def callback(*_, json, **__):
            assert 'chat_id' in json
            assert 'text' in json
            return CallbackResult(payload=data.SEND_MESSAGE)

        with aioresponses() as m:
            m.post(tg_base_url('sendMessage'), callback=callback)
            resp = await tg_client.send_message(1, 'hello')

        assert resp.message_id
        assert resp.chat.id
        assert resp.from_.id

    @pytest.mark.parametrize('kw', [
        {'status': 403},
        {'body': 'invalid json'},
    ])
    async def test_errors(self, tg_base_url, tg_client, kw):
        with aioresponses() as m:
            m.post(tg_base_url(f'sendMessage'), **kw)
            with pytest.raises(TgClientError):
                await tg_client.send_message(1, 'hello')

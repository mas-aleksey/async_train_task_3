import aiohttp
from aioresponses import aioresponses, CallbackResult
import pytest

from clients.tg.api import TgClientError
from clients.tg.dcs import File
from tests.clients.fapi import data


class TestSendDocument:
    async def test_success(self, tg_base_url, file_tg_client):
        def callback(*_, **kwargs):
            form_data = kwargs['data']
            assert isinstance(form_data, aiohttp.FormData)
            assert form_data.is_multipart
            return CallbackResult(payload=data.SEND_DOCUMENT)

        with aioresponses() as m:
            m.post(tg_base_url('sendDocument'), callback=callback)
            resp = await file_tg_client.send_document(1, 'README.md')

        assert resp.message_id
        assert resp.chat.id
        assert resp.from_.id

    @pytest.mark.parametrize('kw', [
        {'status': 403},
        {'body': 'invalid json'},
    ])
    async def test_errors(self, tg_base_url, file_tg_client, kw):
        with aioresponses() as m:
            m.post(tg_base_url(f'sendDocument'), **kw)
            with pytest.raises(TgClientError):
                await file_tg_client.send_document(1, 'README.md')


class TestGetFile:
    async def test_success(self, tg_base_url, file_tg_client):
        file_id = '1_file_id_1'
        with aioresponses() as m:
            m.get(tg_base_url(f'getFile?file_id={file_id}'), payload=data.GET_FILE)
            resp: File = await file_tg_client.get_file(file_id)

        assert resp.file_id
        assert resp.file_size
        assert resp.file_path
        assert resp.file_unique_id

    @pytest.mark.parametrize('kw', [
        {'status': 403},
        {'body': 'invalid json'},
    ])
    async def test_errors(self, tg_base_url, file_tg_client, kw):
        file_id = '1_file_id_1'
        with aioresponses() as m:
            m.get(tg_base_url(f'getFile?file_id={file_id}'), **kw)
            with pytest.raises(TgClientError):
                await file_tg_client.get_file(file_id)


class TestDownloadFile:
    async def test_success(self, tg_api_url, file_tg_client, tg_token):
        file_path = 'file_0.pdf'
        body = 'test'
        with aioresponses() as m:
            m.get(f'{tg_api_url}/file/bot{tg_token}/{file_path}', content_type='text/plain', body=body)
            await file_tg_client.download_file(file_path, file_path)

        with open(file_path) as fd:
            content = fd.read()
        assert content == body

    async def test_errors(self, tg_api_url, file_tg_client, tg_token):
        file_path = 'file_0.pdf'
        with aioresponses() as m:
            m.get(f'{tg_api_url}/file/bot{tg_token}/{file_path}', status=403)
            with pytest.raises(TgClientError):
                await file_tg_client.download_file(file_path, file_path)

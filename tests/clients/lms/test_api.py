from aioresponses import aioresponses, CallbackResult
import pytest

from clients.lms.api import LmsClientError
from tests.clients.lms import data


class TestGetUserCurrent:
    async def test_success(self, lms_url, lms_client):
        with aioresponses() as m:
            m.get(lms_url('v2.user.current'), payload=data.USER_CURRENT)
            resp = await lms_client.get_user_current()
            assert resp == data.USER_CURRENT

    @pytest.mark.parametrize('kw', [
        {'body': 'invalid json'},
        {'status': 401},
    ])
    async def test_errors(self, lms_url, lms_client, kw):
        with aioresponses() as m:
            m.get(lms_url('v2.user.current'), **kw)
            with pytest.raises(LmsClientError):
                await lms_client.get_user_current()


class TestLogin:
    async def test_success(self, lms_url, lms_client):
        def callback(*_, json, **__):
            assert 'email' in json
            assert 'password' in json
            return CallbackResult(
                payload=data.USER_CURRENT,
                headers={
                    'set-cookie': (
                        'sessionid=token; expires=Sun, 23 Oct 2022 12:38:05 GMT; HttpOnly; Max-Age=31536000; '
                        'Path=/; SameSite=Strict; Secure'
                    )
                }
            )

        with aioresponses() as m:
            m.post(lms_url('v2.user.login'), callback=callback)
            resp = await lms_client.login('alex@ktsstudio.ru', 'pass')
            assert resp == 'token'

    @pytest.mark.parametrize('kw', [
        {'body': 'invalid json'},
        {'status': 401},
        {'payload': {}},
    ])
    async def test_errors(self, lms_url, lms_client, kw):
        with aioresponses() as m:
            m.post(lms_url('v2.user.login'), **kw)
            with pytest.raises(LmsClientError):
                await lms_client.login('alex@ktsstudio.ru', 'pass')

import pytest

from clients.lms.api import LmsClient


@pytest.fixture
def lms_token():
    return '123'


@pytest.fixture
def lms_api_url():
    return 'https://lms.metaclass.kts.studio/api'


@pytest.fixture
def lms_url(lms_api_url):
    def _builder(method):
        return f'{lms_api_url}/{method}'

    return _builder


@pytest.fixture
async def lms_client(lms_token):
    return LmsClient(lms_token)

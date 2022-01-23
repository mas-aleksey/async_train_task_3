import os

import pytest

from bot import WorkerConfig
from bot.worker import Worker
from clients.tg.dcs import GetUpdatesResponse
from tests.bot import data


@pytest.fixture
def worker_config():
    return WorkerConfig(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        bucket='telegram',
        concurrent_workers=2
    )


@pytest.fixture
def update_obj():
    r: GetUpdatesResponse = GetUpdatesResponse.Schema().load(data.GET_UPDATES)
    return r.result[0]


@pytest.fixture
async def tg_worker(tg_token, worker_config):
    return lambda q: Worker(tg_token, q, worker_config)


@pytest.fixture
def update_obj_with_document():
    r: GetUpdatesResponse = GetUpdatesResponse.Schema().load(data.GET_UPDATES_WITH_DOCUMENT)
    return r.result[0]

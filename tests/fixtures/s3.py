import os
import uuid

import pytest
from aiobotocore.session import get_session


@pytest.fixture
def s3_credentials():
    assert os.getenv("MINIO_SERVER_URL"), "env var MINIO_SERVER_URL is required"
    assert os.getenv("MINIO_ROOT_PASSWORD"), "env var MINIO_ROOT_PASSWORD is required"
    assert os.getenv("MINIO_ROOT_USER"), "env var MINIO_ROOT_USER is required"
    return dict(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER")
    )


@pytest.fixture
def s3_context_manager(s3_credentials):
    def cm():
        session = get_session()
        return session.create_client("s3", region_name="", **s3_credentials)
    return cm


@pytest.fixture
async def bucket(s3_context_manager):
    name = str(uuid.uuid4().hex)
    async with s3_context_manager() as cl:
        await cl.create_bucket(Bucket=name)
    return name

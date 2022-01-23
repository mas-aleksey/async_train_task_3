import uuid

from aioresponses import aioresponses

from clients.fapi.s3 import S3Client


class TestS3:
    async def test_upload_file(self, s3_context_manager, bucket, s3_credentials):
        client = S3Client(**s3_credentials)
        file_name = str(uuid.uuid4().hex)
        body = b"test"
        key = f'{file_name}.txt'
        await client.upload_file(bucket, key, body)

        async with s3_context_manager() as cl:
            response = await cl.get_object(Bucket=bucket, Key=key)
            async with response['Body'] as stream:
                assert await stream.read() == body

    async def test_fetch_and_upload(self, s3_context_manager, bucket, s3_credentials):
        client = S3Client(**s3_credentials)
        file_name = str(uuid.uuid4().hex)
        body = b"test"
        key = f'{file_name}.txt'
        with aioresponses(passthrough=[s3_credentials['endpoint_url']]) as m:
            url = 'https://some.ru/test.txt'
            m.get(url, body=body)
            await client.fetch_and_upload(bucket, key, url)

        async with s3_context_manager() as cl:
            response = await cl.get_object(Bucket=bucket, Key=key)
            async with response['Body'] as stream:
                assert await stream.read() == body

    async def test_stream_upload(self, s3_context_manager, bucket, s3_credentials):
        client = S3Client(**s3_credentials)
        file_name = str(uuid.uuid4().hex)
        body = b"test"
        key = f'{file_name}.txt'
        with aioresponses(passthrough=[s3_credentials['endpoint_url']]) as m:
            url = 'https://some.ru/test.txt'
            m.get(url, body=body)
            await client.stream_upload(bucket, key, url)

        async with s3_context_manager() as cl:
            response = await cl.get_object(Bucket=bucket, Key=key)
            async with response['Body'] as stream:
                assert await stream.read() == body

import asyncio
import os

from clients.fapi.s3 import S3Client
from clients.tg.api import TgClient
from clients.lms.api import LmsClient
from clients.ws.bitmex import fetch_10
from clients.fapi.tg import TgClientWithFile


BOT_TOKEN = '1455367170:AAGrC9nBxFusYIfwd8dLHqO2UW4HkewRJU4'

async def cli():
    async with TgClientWithFile(BOT_TOKEN) as tg_cli:
        res = await tg_cli.send_document(703432434, 'file_0.pdf')
        print(res)


async def ws():
    res = await fetch_10()
    print(res)


async def s3():
    cr = dict(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER")
    )
    s3cli = S3Client(**cr)
    await s3cli.stream_upload(
        'test_bucket',
        'bbabae8bcbce1.mov',
        'https://lms-metaclass-prod.hb.bizmrg.com/media/019c3374-9099-4c49-9037-bbabae8bcbce.mov'
    )


if __name__ == '__main__':
    asyncio.run(cli())

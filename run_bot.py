import asyncio
import os

from bot import Bot, BotConfig, WorkerConfig


def run():
    loop = asyncio.get_event_loop()

    worker_config = WorkerConfig(
        endpoint_url=os.getenv("MINIO_SERVER_URL"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
        bucket='telegram',
        concurrent_workers=2
    )
    bot_config = BotConfig(
        token=os.getenv("BOT_TOKEN") or '1455367170:AAGrC9nBxFusYIfwd8dLHqO2UW4HkewRJU4',
        worker=worker_config
    )
    tg_bot = Bot(bot_config)

    try:
        print('bot has been started')
        loop.create_task(tg_bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print('\nstopping bot')
        loop.run_until_complete(tg_bot.stop())


if __name__ == '__main__':
    run()

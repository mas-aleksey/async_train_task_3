from functools import wraps
import logging


def log_exceptions(func):
    @wraps(func)
    async def wrapped(*args):
        try:
            return await func(*args)
        except Exception as e:
            logging.exception(e)
    return wrapped

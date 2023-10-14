import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps
from logging import FileHandler, Handler, Logger

load_dotenv()
NAME_LOGGER = os.getenv('NAME_LOGGER', 'exc_logger')
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', logging.INFO)


def create_file_handler(file_name: str) -> Handler:
    handler = FileHandler(file_name)
    format_logging = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(format_logging)
    return handler


def create_logger(name_logger: str, handler: Handler, level: str | int = logging.INFO) -> Logger:
    logger = logging.getLogger(name_logger)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def exception(logger: Logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                issue = f"EXCEPTION in {func.__name__}\n"
                issue += "============================\n"
                logger.exception(issue)
                raise
        return wrapper
    return decorator


date = datetime.now().strftime("%Y-%m-%d")
file_handler = create_file_handler(
    os.path.join(os.getcwd(), f'logs/{date}-crawl.log'))
logger = create_logger(NAME_LOGGER, file_handler, LOGGING_LEVEL)

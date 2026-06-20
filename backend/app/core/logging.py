import logging
import sys
from app.core.config import settings


def setup_logging():
    logger = logging.getLogger(settings.APP_NAME)
    logger.setLevel(settings.LOG_LEVEL)

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter(settings.LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.propagate = False

    return logger


logger = setup_logging()

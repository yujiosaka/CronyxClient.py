import logging
import os

log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger("cronyx.client")
logger.setLevel(log_level)


def log(msg):
    logger.debug(msg)

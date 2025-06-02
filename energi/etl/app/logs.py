import logging
import os
from logging import StreamHandler

logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)

def get_logger(name: str):
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    return logger

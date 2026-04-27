import logging
import os
import sys

def get_logger(name: str):
    logger = logging.getLogger(name)

    # Read level from env; default to INFO so DEBUG doesn't leak into production
    log_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    logger.setLevel(log_level)

    # Console handler — prints to terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Format — how the log message looks
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
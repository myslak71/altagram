"""Logging module."""
import logging
import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

LOGGER = logging.getLogger("starships_logger")

sh = logging.StreamHandler()

level = os.environ.get("LOGGING_LEVEL", "INFO")

LOGGER.setLevel(getattr(logging, level, "20"))
LOGGER.addHandler(sh)

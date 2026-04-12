"""Logging configuration for Stampede."""

import logging
import sys


def setup_logging():
    """Configure root logger with file and console handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )

    file_handler = logging.FileHandler("stampede.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

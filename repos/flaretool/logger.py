#!/bin/python
# -*- coding: utf-8 -*-
import logging
import flaretool
from logging import Logger
import logging.handlers


def setup_logger(
    loglevel: int = logging.INFO,
    console: bool = False,
    file: bool = False,
    file_name: str = 'flaretool.log',
    rotating: bool = False,
    max_bytes: int = 1024000,
    backup_count: int = 5,
    extra: bool = False,
) -> Logger:
    if max_bytes < 0:
        raise ValueError("max_bytes must be a non-negative value")
    if backup_count < 0:
        raise ValueError("backup_count must be a non-negative value")

    logger = logging.getLogger(flaretool.__name__)
    logger.setLevel(loglevel)
    logger.handlers.clear()

    extra_string = ""

    if extra:
        extra_string = "- %(pathname)s:%(lineno)d - %(funcName)s "
    format_string = f"[%(asctime)s] %(levelname)s {extra_string}: %(message)s"
    formatter = logging.Formatter(format_string)

    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(loglevel)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(formatter)

    rotating_handler = logging.handlers.RotatingFileHandler(
        file_name,
        encoding='utf-8',
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    rotating_handler.setLevel(loglevel)
    rotating_handler.setFormatter(formatter)

    if file:
        logger.addHandler(rotating_handler if rotating else file_handler)

    if console:
        logger.addHandler(console_handler)

    return logger


def get_logger() -> Logger:
    return logging.getLogger(flaretool.__name__)

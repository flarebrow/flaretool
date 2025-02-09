#!/bin/python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from logging import Logger

import flaretool


def setup_logger(
    loglevel: int = logging.INFO,
    logger_name: str = flaretool.__name__,
    console: bool = True,
    file: bool = False,
    file_name: str = "flaretool.log",
    rotating: bool = False,
    max_bytes: int = 1024000,
    backup_count: int = 5,
    extra: bool = False,
    encoding: str = "utf-8",
) -> Logger:
    if max_bytes < 0:
        raise ValueError("max_bytes must be a non-negative value")
    if backup_count < 0:
        raise ValueError("backup_count must be a non-negative value")

    logger = logging.getLogger(logger_name)
    logger.setLevel(loglevel)
    logger.handlers.clear()

    extra_string = ""

    if extra:
        extra_string = "- %(pathname)s:%(lineno)d - %(funcName)s "
    format_string = (
        f"[%(asctime)s] - %(name)s - [%(levelname)s] {extra_string}: %(message)s"
    )
    formatter = logging.Formatter(format_string)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    console_handler.setFormatter(formatter)

    if file:
        if rotating:
            rotating_handler = logging.handlers.RotatingFileHandler(
                file_name,
                encoding=encoding,
                maxBytes=max_bytes,
                backupCount=backup_count,
            )
            rotating_handler.setLevel(loglevel)
            rotating_handler.setFormatter(formatter)
            logger.addHandler(rotating_handler)
        else:
            file_handler = logging.FileHandler(file_name)
            file_handler.setLevel(loglevel)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    if console:
        logger.addHandler(console_handler)

    return logger


def get_logger(logger_name: str = flaretool.__name__) -> Logger:
    return logging.getLogger(logger_name)

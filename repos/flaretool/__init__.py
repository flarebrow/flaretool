#!/bin/python
# -*- coding: utf-8 -*-
"""
flaretool python module
[Terms of service](https://main.flarebrow.com/terms)
"""
from flaretool.VERSION import VERSION
from flaretool import nettool
from flaretool.settings import get_settings
from flaretool import logger
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

settings = get_settings()
api_key: str = settings.api_key


def get_lib_version():
    return VERSION


__version__ = get_lib_version()
__all__ = [
    "api_key",
    # "nettool",
    "settings",
    "logger",
    # "errors",
]

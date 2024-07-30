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


def get_latest_version() -> str:
    try:
        from flaretool.common import requests
        return requests.get("https://pypi.org/pypi/flaretool/json", timeout=5).json()["info"]["version"]
    except:
        return VERSION


def check_version():
    current_ver = VERSION
    latest_ver = get_latest_version()
    from packaging.version import parse as StrictVersion
    import warnings
    if StrictVersion(current_ver) < StrictVersion(latest_ver):
        warnings.warn(
            f"flaretool a new version has been released. Please update to the latest version as it has been released."
        )


__version__ = get_lib_version()
__all__ = [
    "api_key",
    # "nettool",
    "settings",
    "logger",
    # "errors",
    "get_lib_version",
    "get_latest_version",
    "check_version",
]

check_version()

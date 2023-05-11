#!/bin/python
# -*- coding: utf-8 -*-
"""
flaretool python module
[Terms of service](https://main.flarebrow.com/terms)
"""
from flaretool.VERSION import VERSION
from flaretool import settings
from flaretool import nettool

api_key: str = None


def get_lib_version():
    return VERSION


__version__ = get_lib_version()
__all__ = [
    "api_key",
    "nettool",
    "settings",
    "error",
]

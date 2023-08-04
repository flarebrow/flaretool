#!/bin/python
# -*- coding: utf-8 -*-
import os
from typing import Union
# try:
from pydantic_settings import BaseSettings as bs
# except ImportError:
#     from pydantic import BaseSettings as bs

from dotenv import load_dotenv


class BaseSettings(bs):
    api_key: Union[str, None] = None

    class Config:
        env_prefix = ""

        @classmethod
        def _load_env_file(cls):
            load_dotenv()

        @classmethod
        def _get_environment_variable(cls, name, default):
            return os.getenv(name, default)

    @classmethod
    def get(cls):
        return cls()


def get_settings():
    return BaseSettings()

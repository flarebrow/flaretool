#!/bin/python
# -*- coding: utf-8 -*-
import os
from typing import Union
# try:
from pydantic_settings import BaseSettings as bs, SettingsConfigDict
# except ImportError:
#     from pydantic import BaseSettings as bs

from dotenv import load_dotenv


class BaseSettings(bs):
    api_key: Union[str, None] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

def get_settings():
    return BaseSettings()

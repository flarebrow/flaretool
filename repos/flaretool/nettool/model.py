#!/bin/python
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class BaseClass():
    pass


class BaseDataModel(BaseModel):
    pass


class IpInfo(BaseDataModel):
    ipaddr: str
    hostname: str
    country: str

#!/bin/python
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class BaseDataModel(BaseModel):
    pass


class IpInfo(BaseDataModel):
    ipaddr: str
    hostname: str
    country: str


class PunyDomainInfo(BaseDataModel):
    originalvalue: str
    encodevalue: str
    decodevalue: str

#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.basemodels import BaseDataModel


class IpInfo(BaseDataModel):
    ipaddr: str = None
    hostname: str = None
    country: str = None


class PunyDomainInfo(BaseDataModel):
    originalvalue: str
    encodevalue: str
    decodevalue: str

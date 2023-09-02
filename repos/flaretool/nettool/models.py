#!/bin/python
# -*- coding: utf-8 -*-
from typing import Union
from flaretool.basemodels import BaseDataModel


class IpInfo(BaseDataModel):
    ipaddr: Union[str, None] = None
    hostname: Union[str, None] = None
    country: Union[str, None] = None


class PunyDomainInfo(BaseDataModel):
    originalvalue: str
    encodevalue: str
    decodevalue: str

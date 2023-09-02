#!/bin/python
# -*- coding: utf-8 -*-
from typing import Union
from flaretool.basemodels import BaseDataModel


class DdnsInfo(BaseDataModel):
    """
    Represents the Dynamic DNS (DDNS) information.

    Attributes:
        result (int): The result code of the DDNS update.
        status (str): The status of the DDNS update.
        currentIp (str): The current IP address associated with the domain.
        updateIp (str): The IP address that was updated.
        domain (str): The domain associated with the DDNS update.
    """
    result: int
    status: str
    currentIp: Union[str, None] = None
    updateIp: str
    domain: str

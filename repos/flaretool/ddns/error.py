#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.error import FlareToolError


class DdnsError(FlareToolError):

    def __init__(self, result, status, currentIp, updateIp, domain):
        self.result = result
        self.status = status
        self.currentIp = currentIp
        self.updateIp = updateIp
        self.domain = domain
        super().__init__(self.status)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.status


class DdnsAuthenticationError(DdnsError):
    pass

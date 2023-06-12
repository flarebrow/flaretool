#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.errors import FlareToolError


class DdnsError(FlareToolError):

    def __init__(self, result, status, currentIp, updateIp, domain):
        self.result = result
        self.status = status
        self.currentIp = currentIp
        self.updateIp = updateIp
        self.domain = domain
        super().__init__(self.status)


class DdnsAuthenticationError(DdnsError):
    pass

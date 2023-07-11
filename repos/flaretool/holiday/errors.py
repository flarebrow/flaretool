#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.errors import FlareToolError


class JapaneseHolidaysError(FlareToolError):

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", "")
        super().__init__(self.message)

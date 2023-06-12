#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.errors import FlareToolError


class ShortUrlError(FlareToolError):

    def __init__(self, message, author=None, response=None, data=None):
        self.message = message
        self.author = author
        self.response = response
        self.data = data
        super().__init__(self.message)


class ShortUrlAuthenticationError(ShortUrlError):
    pass


class ShortUrlDataUpdateError(ShortUrlError):
    pass

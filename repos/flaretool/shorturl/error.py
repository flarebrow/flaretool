#!/bin/python
# -*- coding: utf-8 -*-


from flaretool.error import FlareToolError


class ShortUrlError(FlareToolError):

    def __init__(self, message, author, response, data):
        self.message = message
        self.author = author
        self.response = response
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.message


class ShortUrlAuthenticationError(ShortUrlError):
    pass


class ShortUrlDataUpdateError(ShortUrlError):
    pass

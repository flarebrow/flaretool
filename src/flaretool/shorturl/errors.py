"""Errors raised by the short URL service."""

from typing import Any

from flaretool.errors import FlareToolError


class ShortUrlError(FlareToolError):
    """Base error for the short URL service."""

    def __init__(
        self,
        message: str,
        author: str | None = None,
        response: int | None = None,
        data: Any = None,
    ) -> None:
        self.message = message
        self.author = author
        self.response = response
        self.data = data
        super().__init__(self.message)


class ShortUrlAuthenticationError(ShortUrlError):
    pass


class ShortUrlDataUpdateError(ShortUrlError):
    pass


class ShortUrlValidError(ShortUrlError):
    pass

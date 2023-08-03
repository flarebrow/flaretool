#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.logger import get_logger

logger = get_logger()


class FlareToolError(Exception):
    """Base exception class for FlareTool errors."""

    def __init__(self, message: str = None) -> None:
        """
        Initialize FlareToolError.

        Args:
            message (str): Optional error message (default: None).
        """
        super().__init__(message)
        self.message = message
        logger.error(repr(self))

    def __str__(self) -> str:
        """
        Return a string representation of the exception.

        Returns:
            str: String representation of the exception.
        """
        return self.message

    def __repr__(self) -> str:
        """
        Return a string representation of the exception.

        Returns:
            str: String representation of the exception.
        """
        columns = ', '.join([
            '{0}={1}'.format(k, repr(self.__dict__[k]))
            for k in self.__dict__.keys() if not k.startswith("_")
        ])

        return '<{0}({1})>'.format(
            self.__class__.__name__, columns
        )


class FlareToolNetworkError(FlareToolError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        **param,
    ):
        super(FlareToolError, self).__init__(message)

        # if http_body and hasattr(http_body, "decode"):
        #     try:
        #         http_body = http_body.decode("utf-8")
        #     except BaseException:
        #         http_body = (
        #             "<Could not decode body as utf-8. "
        #             "Please contact us through our help center at help.FlaresApp.com.>"
        #         )

        self.message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.request_id = self.headers.get("request-id", None)

    # def __str__(self):
    #     msg = self._message or "<empty message>"
    #     if self.request_id is not None:
    #         return "Request {0}: {1}".format(self.request_id, msg)
    #     else:
    #         return msg

    # @property
    # def user_message(self):
    #     return self._message

    # def __repr__(self):
    #     return "%s(message=%r, http_status=%r, request_id=%r)" % (
    #         self.__class__.__name__,
    #         self._message,
    #         self.http_status,
    #         self.request_id,
    #     )


class AuthenticationError(FlareToolError):
    pass

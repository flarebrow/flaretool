#!/bin/python
# -*- coding: utf-8 -*-
import flaretool
from flaretool.error import AuthenticationError
from flaretool.common import requests
from .models import ShortInfo, ShortInfoUpdate, UrlInfo, UrlRecode
import warnings


class ShortUrl:
    """Class for interacting with a short URL service."""

    base_url = "https://api.flarebrow.com/v2/shorturl"

    def __init__(self) -> None:
        """Initialize the ShortUrl class.

        Warning:
            This class may undergo updates and its usage may change in the near future.
        """
        message = "This class may undergo updates and its usage may change in the near future."
        warnings.warn(message, DeprecationWarning)
        if flaretool.api_key is None:
            raise AuthenticationError(
                "No API key provided. You can set your API key in code using 'flaretool.api_key = <API-KEY>', or you can set the environment variable api_key=<API-KEY>). "
            )

    def _request(self, method, data: dict = {}, params: dict = {}) -> dict:
        """Send a request to the short URL service.

        Args:
            method (str): HTTP method for the request.
            data (dict): Data to send in the request (default: {}).
            params (dict): Query parameters for the request (default: {}).

        Returns:
            dict: Response data from the short URL service.
        """
        params["apikey"] = flaretool.api_key
        return requests.request(
            method,
            self.base_url,
            params=params,
            data=data,
        ).json()

    def get(self, id: int = None) -> ShortInfo:
        """Get information about a short URL.

        Args:
            id (int): ID of the short URL (default: None).

        Returns:
            ShortInfo: Information about the short URL.
        """
        return ShortInfo(**self._request("get", params={"id": id if id is not None else 0}))

    def post(self, url: str) -> ShortInfo:
        """Create a new short URL.

        Args:
            url (str): Long URL to be shortened.

        Returns:
            ShortInfo: Information about the created short URL.
        """
        return ShortInfo(**self._request("post", data={"url": url}))

    def put(self, id: int, url_info: UrlInfo) -> ShortInfoUpdate:
        """Update a short URL.

        Args:
            id (int): ID of the short URL.
            url_info (UrlInfo): Updated information about the short URL.

        Returns:
            ShortInfoUpdate: Information about the updated short URL.
        """
        return ShortInfoUpdate(**self._request("put", data=url_info.dict(), params={"id": id}))

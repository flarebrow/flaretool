#!/bin/python
# -*- coding: utf-8 -*-
"""
Class for interacting with a short URL service.

Warning:
    This class may undergo updates and its usage may change in the near future.
"""
import flaretool
from flaretool.decorators import type_check
from flaretool.errors import AuthenticationError
from flaretool.common import requests
from flaretool.constants import BASE_API_URL
from flaretool.shorturl.errors import *
from flaretool.shorturl.models import ShortUrlInfo
import warnings

__all__ = []


class ShortUrlService:
    """
    Class for interacting with a short URL service.
    WebAPI Wrapper class.

    Warning:
        This class may undergo updates and its usage may change in the near future.
    """

    def __init__(self) -> None:
        """Initialize the ShortUrl class.
        WebAPI Wrapper class.

        Warning:
            This class may undergo updates and its usage may change in the near future.
        """
        message = "This class may undergo updates and its usage may change in the near future."
        warnings.warn(message, Warning)
        if not flaretool.api_key:
            raise AuthenticationError(
                "No API key provided. You can set your API key in code using 'flaretool.api_key = <API-KEY>', or you can set the environment variable api_key=<API-KEY>). "
            )

    @type_check
    def _send_request(self, method, data: dict = {}, params: dict = {}) -> dict:
        """Send a request to the short URL service.

        Args:
            method (str): HTTP method for the request.
            data (dict): Data to send in the request (default: {}).
            params (dict): Query parameters for the request (default: {}).

        Returns:
            dict: Response data from the short URL service.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlError: If the response code is not 200.
        """
        base_url = f"{BASE_API_URL}/shorturl"
        result = requests.request(
            method,
            base_url,
            params=params,
            data=data,
            auth_enabled=True,
        ).json()
        response = result["response"]
        if response == 401:
            raise ShortUrlAuthenticationError(**result)
        if response == 409:
            raise ShortUrlDataUpdateError(**result)
        if response != 200:
            raise ShortUrlError(**result)
        return result

    @type_check
    def get_short_url_info_list(self, id: int = None) -> list[ShortUrlInfo]:
        """Get informations about a short URL.

        Args:
            id (int): ID of the short URL (default: None).

        Returns:
            list[ShortUrlInfo]: Information about the short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlError: If the response code is not 200.
        """
        result = self._send_request(
            "get", params={"id": id if id is not None else 0})["data"]
        return [ShortUrlInfo(**data) for data in result] if result else []

    @type_check
    def create_short_url(self, url: str, limited: int = None) -> ShortUrlInfo:
        """Create a new short URL.

        Args:
            url (str): Long URL to be shortened.
            limited (int, optional): link limited(minutes). Defaults to None.

        Returns:
            ShortUrlInfo: Information about the created short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlError: If the response code is not 200.
        """
        data = {"url": url, "limited": limited} if limited is not None else \
            {"url": url}
        return ShortUrlInfo(**self._send_request("post", data=data)["data"][0])

    @type_check
    def update_short_url(self, url_info: ShortUrlInfo) -> ShortUrlInfo:
        """Update a short URL.

        Args:
            url_info (ShortUrlInfo): Updated information about the short URL.

        Returns:
            ShortUrlInfo: Information about the updated short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlError: If the response code is not 200.
        """
        return ShortUrlInfo(**self._send_request("put", data=url_info.model_dump(), params={
            "id": url_info.id})["data"]["after"][0])

    @type_check
    def delete_short_url(self, url_info: ShortUrlInfo) -> ShortUrlInfo:
        """Delete a short URL.

        Args:
            url_info (ShortUrlInfo): Updated information about the short URL.

        Returns:
            ShortUrlInfo: Information about the delete short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlError: If the response code is not 200.
        """
        return ShortUrlInfo(**self._send_request("delete", params={"id": url_info.id})["data"][0])

    @type_check
    def get_qr_code_raw_data(self, url_info: ShortUrlInfo) -> bytes:
        """Get QR Code raw data

        Args:
            url_info (ShortUrlInfo): target information about the short URL.

        Returns:
            bytes: image bytes data.
        """
        return requests.get(url_info.qr_url).content

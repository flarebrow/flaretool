#!/bin/python
# -*- coding: utf-8 -*-
"""
Class for interacting with a short URL service.

Warning:
    This class may undergo updates and its usage may change in the near future.
"""

import warnings

import flaretool
from flaretool.common import requests
from flaretool.constants import API_BASE_URL, API_BASE_URL_OLD
from flaretool.decorators import type_check
from flaretool.errors import AuthenticationError
from flaretool.shorturl.errors import *
from flaretool.shorturl.models import ShortUrlInfo

__all__ = []


class ShortUrlService:
    """
    Class for interacting with a short URL service.
    WebAPI Wrapper class.
    """

    def __init__(self) -> None:
        """Initialize the ShortUrl class."""
        if not flaretool.api_key:
            raise AuthenticationError(
                "No API key provided. You can set your API key in code using 'flaretool.api_key = <API-KEY>', or you can set the environment variable api_key=<API-KEY>). "
            )

    @type_check
    def _send_request(
        self, method, data: dict = {}, params: dict = {}, json: dict = {}
    ) -> dict:
        """Send a request to the short URL service.

        Args:
            method (str): HTTP method for the request.
            data (dict): Data to send in the request (default: {}).
            params (dict): Query parameters for the request (default: {}).
            json (dict): JSON data to send in the request (default: {}).

        Returns:
            dict: Response data from the short URL service.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlValidError: If the response code is 422.
            ShortUrlError: If the response code is not 200.
        """
        base_url = f"{API_BASE_URL}/short"
        response = requests.request(
            method,
            base_url,
            params=params,
            data=data,
            json=json,
            auth_enabled=True,
        )
        result = response.json()
        if response.status_code == 401:
            raise ShortUrlAuthenticationError(**result)
        if response.status_code == 409:
            raise ShortUrlDataUpdateError(result["message"])
        if response.status_code == 422:
            raise ShortUrlValidError(result["detail"][0]["msg"])
        if response.status_code != 200:
            raise ShortUrlError(result["message"])
        return result

    @type_check
    def get(self, id: int = None) -> list[ShortUrlInfo]:
        """Get informations about a short URL.

        Args:
            id (int): ID of the short URL (default: None).

        Returns:
            list[ShortUrlInfo]: Information about the short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlValidError: If the response code is 422.
            ShortUrlError: If the response code is not 200.
        """
        result = self._send_request("get").get("result", [])
        return [ShortUrlInfo(**data) for data in result if not id or data["id"] == id]

    @type_check
    def create(
        self,
        url: str,
        code: str = None,
        description: str = None,
        is_eternal: bool = None,
        is_active: bool = None,
    ) -> ShortUrlInfo:
        """Create a new short URL.

        Args:
            url (str): URL to shorten.
            code (str): Custom code for the short URL (default: None).
            description (str): Description of the short URL (default: None).
            is_eternal (bool): Whether the short URL is eternal (default: None).
            is_active (bool): Whether the short URL is active (default: None).

        Returns:
            ShortUrlInfo: Information about the created short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlValidError: If the response code is 422.
            ShortUrlError: If the response code is not 200.
        """
        data = {
            "url": url,
            **({"code": code} if code else {}),
            **({"description": description} if description else {}),
            **({"is_eternal": is_eternal} if is_eternal else {}),
            **({"is_active": is_active} if is_active else {}),
        }
        return ShortUrlInfo(**self._send_request("post", json=data)["result"])

    @type_check
    def update(self, url_info: ShortUrlInfo) -> ShortUrlInfo:
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
        return ShortUrlInfo(
            **self._send_request(
                "put",
                json=url_info.model_dump(
                    exclude={"limited_at", "updated_at", "created_at"}
                ),
            )["result"]
        )

    @type_check
    def delete(self, url_info: ShortUrlInfo):
        """Delete a short URL.

        Args:
            url_info (ShortUrlInfo): Updated information about the short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlError: If the response code is not 200.
        """
        self._send_request(
            "delete",
            json=url_info.model_dump(),
        )["result"]

    @type_check
    def get_qr_code_raw_data(self, url_info: ShortUrlInfo) -> bytes:
        """Get QR Code raw data

        Args:
            url_info (ShortUrlInfo): target information about the short URL.

        Returns:
            bytes: image bytes data.
        """
        return requests.get(url_info.qr_url).content

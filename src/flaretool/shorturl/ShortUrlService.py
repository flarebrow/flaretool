"""
Class for interacting with a short URL service.

Warning:
    This class may undergo updates and its usage may change in the near future.
"""

import flaretool
from flaretool.common import requests
from flaretool.constants import API_BASE_URL
from flaretool.decorators import type_check
from flaretool.errors import AuthenticationError
from flaretool.shorturl.errors import (
    ShortUrlAuthenticationError,
    ShortUrlDataUpdateError,
    ShortUrlError,
    ShortUrlValidError,
)
from flaretool.shorturl.models import ShortUrlInfo

__all__ = ["ShortUrlService"]


def _encode_url_for_api(url: str) -> str:
    """Percent-encode hyphens in a URL for the short URL API.

    Server-side contract: the API misinterprets literal hyphens in the
    submitted URL, so they must be sent percent-encoded ("%2D").

    The normalization is idempotent: any "%2D" already present is decoded
    first, so applying this function twice never double-encodes.

    Args:
        url (str): URL to encode.

    Returns:
        str: URL with all hyphens percent-encoded.
    """
    return url.replace("%2D", "-").replace("-", "%2D")


class ShortUrlService:
    """
    Class for interacting with a short URL service.
    WebAPI Wrapper class.
    """

    def __init__(self) -> None:
        """Initialize the ShortUrl class."""
        if not flaretool.api_key:
            raise AuthenticationError(
                "No API key provided. You can set your API key in code using "
                "'flaretool.api_key = <API-KEY>', or you can set the environment "
                "variable api_key=<API-KEY>). "
            )

    @type_check
    def _send_request(
        self,
        method: str,
        data: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
    ) -> dict:
        """Send a request to the short URL service.

        Args:
            method (str): HTTP method for the request.
            data (dict | None): Data to send in the request (default: None).
            params (dict | None): Query parameters for the request (default: None).
            json (dict | None): JSON data to send in the request (default: None).

        Returns:
            dict: Response data from the short URL service.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlValidError: If the response code is 422.
            ShortUrlError: If the response code is not 200.
        """
        response = requests.request(
            method,
            f"{API_BASE_URL}/short",
            params=params if params is not None else {},
            data=data if data is not None else {},
            json=json if json is not None else {},
            auth_enabled=True,
        )
        result = response.json()
        match response.status_code:
            case 200:
                return result
            case 401:
                raise ShortUrlAuthenticationError(**result)
            case 409:
                raise ShortUrlDataUpdateError(result["message"])
            case 422:
                raise ShortUrlValidError(result["detail"][0]["msg"])
            case _:
                raise ShortUrlError(result["message"])

    @type_check
    def get(self, id: int | None = None) -> list[ShortUrlInfo]:
        """Get informations about a short URL.

        Args:
            id (int | None): ID of the short URL (default: None).

        Returns:
            list[ShortUrlInfo]: Information about the short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlValidError: If the response code is 422.
            ShortUrlError: If the response code is not 200.
        """
        result = self._send_request("get").get("result", [])
        return [
            ShortUrlInfo(**data) for data in result if id is None or data["id"] == id
        ]

    @type_check
    def create(
        self,
        url: str,
        code: str | None = None,
        description: str | None = None,
        is_eternal: bool | None = None,
        is_active: bool | None = None,
    ) -> ShortUrlInfo:
        """Create a new short URL.

        Args:
            url (str): URL to shorten.
            code (str | None): Custom code for the short URL (default: None).
            description (str | None): Description of the short URL (default: None).
            is_eternal (bool | None): Whether the short URL is eternal (default: None).
            is_active (bool | None): Whether the short URL is active (default: None).

        Returns:
            ShortUrlInfo: Information about the created short URL.

        Raises:
            ShortUrlAuthenticationError: If the response code is 401.
            ShortUrlDataUpdateError: If the response code is 409.
            ShortUrlValidError: If the response code is 422.
            ShortUrlError: If the response code is not 200.
        """
        data = {
            "url": _encode_url_for_api(url),
            **({"code": code} if code else {}),
            **({"description": description} if description else {}),
            # `False` is a meaningful value here — only omit when unset (None).
            **({"is_eternal": is_eternal} if is_eternal is not None else {}),
            **({"is_active": is_active} if is_active is not None else {}),
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
        payload = url_info.model_dump(
            exclude={"limited_at", "updated_at", "created_at"}
        )
        payload["url"] = _encode_url_for_api(payload["url"])
        return ShortUrlInfo(**self._send_request("put", json=payload)["result"])

    @type_check
    def delete(self, url_info: ShortUrlInfo) -> None:
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
        )

    @type_check
    def get_qr_code_raw_data(self, url_info: ShortUrlInfo) -> bytes:
        """Get QR Code raw data

        Args:
            url_info (ShortUrlInfo): target information about the short URL.

        Returns:
            bytes: image bytes data.
        """
        return requests.get(url_info.qr_url).content

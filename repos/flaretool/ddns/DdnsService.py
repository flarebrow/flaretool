#!/bin/python
# -*- coding: utf-8 -*-
import warnings

from flaretool.common import requests
import flaretool
from flaretool.ddns.errors import DdnsAuthenticationError, DdnsError
from flaretool.ddns.models import DdnsInfo
from flaretool.decorators import type_check
from flaretool.errors import AuthenticationError
from flaretool.constants import BASE_API_URL

__all__ = []


class DdnsService:
    """
    Service class for Dynamic DNS (DDNS) functionality.

    Warning:
        This class may undergo updates and its usage may change in the near future.
    """

    def __init__(self) -> None:
        """
        Initialize the DDNS service.

        Warning:
            This class may undergo updates and its usage may change in the near future.
        """
        message = "This class may undergo updates and its usage may change in the near future."
        warnings.warn(message, Warning)
        if not flaretool.api_key:
            raise AuthenticationError(
                "No API key provided. You can set your API key in code using 'flaretool.api_key = <API-KEY>', or you can set the environment variable api_key=<API-KEY>). "
            )

    def _send_request(self, method: str, data: dict = {}, params: dict = {}) -> dict:
        """
        Send a request to the DDNS service.

        Args:
            method (str): HTTP method for the request.
            data (dict): Data to send in the request (default: {}).
            params (dict): Query parameters for the request (default: {}).

        Returns:
            dict: Response data from the DDNS service.

        Raises:
            DdnsAuthenticationError: If the response code is 401.
            DdnsError: If the response code is not 200.
        """
        base_url = f"{BASE_API_URL}/ddns"
        response = requests.request(
            method,
            base_url,
            params=params,
            data=data,
            auth_enabled=True,
        )
        result = response.json()
        if response.status_code == 401:
            raise DdnsAuthenticationError(**result)
        if response.status_code != 200:
            raise DdnsError(**result)
        return result

    @type_check
    def update_ddns(self, host: str, ip: str = None) -> DdnsInfo:
        """
        Update the Dynamic DNS (DDNS) for the specified host.

        Args:
            host (str): The host to update the DDNS for.
            ip (str, optional): The IP address to set for the host. If not provided, the current IP will be used.

        Returns:
            DdnsInfo: The updated DDNS information.

        Raises:
                DdnsAuthenticationError: If the response code is 401.
                DdnsError: If the response code is not 200.

        Example:
            >>> service = DdnsService()
            >>> info = service.update_ddns("example", "192.168.0.100")
            >>> print(info)
            DdnsInfo(result=200, status='success', currentIp='192.168.0.99', updateIp='192.168.0.100', domain='example.○○○.○○')
        """
        data = {"host": host}
        if ip is not None:
            data["ip"] = ip
        return DdnsInfo(**self._send_request("post", data=data))

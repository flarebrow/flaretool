"""Service class for Dynamic DNS (DDNS) functionality."""

import warnings

import flaretool
from flaretool.common import requests
from flaretool.constants import API_BASE_URL_OLD
from flaretool.ddns.errors import DdnsAuthenticationError, DdnsError
from flaretool.ddns.models import DdnsInfo
from flaretool.decorators import type_check
from flaretool.errors import AuthenticationError

__all__ = ["DdnsService"]

# The instability warning is emitted once per process instead of on every
# instantiation (services are often created per request/call).
_instability_warning_emitted = False


def _warn_unstable_api() -> None:
    global _instability_warning_emitted
    if not _instability_warning_emitted:
        warnings.warn(
            "This class may undergo updates and its usage may change "
            "in the near future.",
            Warning,
            stacklevel=3,
        )
        _instability_warning_emitted = True


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
        _warn_unstable_api()
        if not flaretool.api_key:
            raise AuthenticationError(
                "No API key provided. You can set your API key in code using "
                "'flaretool.api_key = <API-KEY>', or you can set the environment "
                "variable api_key=<API-KEY>). "
            )

    def _send_request(
        self,
        method: str,
        data: dict | None = None,
        params: dict | None = None,
    ) -> dict:
        """
        Send a request to the DDNS service.

        Args:
            method (str): HTTP method for the request.
            data (dict | None): Data to send in the request (default: None).
            params (dict | None): Query parameters for the request (default: None).

        Returns:
            dict: Response data from the DDNS service.

        Raises:
            DdnsAuthenticationError: If the response code is 401.
            DdnsError: If the response code is not 200.
        """
        response = requests.request(
            method,
            f"{API_BASE_URL_OLD}/ddns",
            params=params if params is not None else {},
            data=data if data is not None else {},
            auth_enabled=True,
        )
        result = response.json()
        match response.status_code:
            case 200:
                return result
            case 401:
                raise DdnsAuthenticationError(**result)
            case _:
                raise DdnsError(**result)

    @type_check
    def update_ddns(self, host: str, ip: str | None = None) -> DdnsInfo:
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

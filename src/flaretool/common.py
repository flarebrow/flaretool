"""HTTP layer shared by all flaretool services."""

from __future__ import annotations

import platform
from typing import Any

import requests as req

# ``Retry`` is urllib3's class, imported via requests' re-export so that
# flaretool does not depend on urllib3 directly (it is not a declared
# dependency; requests>=2.26 guarantees this re-export).
from requests.adapters import HTTPAdapter, Retry
from requests.models import Response

import flaretool
from flaretool.errors import FlareToolNetworkError
from flaretool.logger import get_logger

logger = get_logger()

#: Default ``(connect, read)`` timeout applied when the caller does not pass one.
DEFAULT_TIMEOUT: tuple[float, float] = (5, 30)

#: User-Agent sent with every request. All components (version, platform)
#: are fixed for the lifetime of the process, so this is built once at
#: import time instead of on every request.
_USER_AGENT: str = " ".join(
    f"{key}/{value}"
    for key, value in {
        "Mozilla": "5.0",
        "publisher": flaretool.__name__,
        "flaretool": flaretool.__version__,
        "lang_version": platform.python_version(),
        "os": platform.system(),
        "platform": platform.platform(),
    }.items()
)

# Shared session, created lazily on first use. ``requests.Session`` is
# thread-safe for this simple usage (no per-request session mutation).
# A modest retry policy is mounted for transient upstream errors: 2 retries
# with backoff on 502/503/504 and connection errors. Non-idempotent methods
# (e.g. POST) are NOT retried on status codes because urllib3's default
# ``allowed_methods`` only covers idempotent verbs, keeping behavior
# predictable.
_session: req.Session | None = None


def _get_session() -> req.Session:
    global _session
    if _session is None:
        session = req.Session()
        retry = Retry(
            total=2,
            backoff_factor=0.3,
            status_forcelist=(502, 503, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        _session = session
    return _session


class requests:
    """Thin wrapper around :mod:`requests` used by all flaretool services.

    The class name intentionally shadows the third-party module for
    backwards compatibility (``from flaretool.common import requests``).

    All verb helpers (:meth:`get`, :meth:`post`, ...) funnel through
    :meth:`request`, so patching ``flaretool.common.requests.request``
    in tests intercepts every call. Do not bypass this funnel.
    """

    @staticmethod
    def request(
        method: str, url: str, auth_enabled: bool = False, **kwargs: Any
    ) -> Response:
        """
        Send an HTTP request with the specified method, URL, and optional parameters.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            url (str): The URL to send the request to.
            auth_enabled (bool, optional): Whether to force authentication for the request. Defaults to False.
            **kwargs: Additional keyword arguments to be passed to the underlying request method.

        Returns:
            Response: The response object representing the server's response to the request.

        Raises:
            FlareToolNetworkError: If the request is made to a Flare service and the response status code is 403.
        """
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        headers: dict[str, str] = kwargs.pop("headers", {}) or {}
        headers["User-Agent"] = _USER_AGENT
        headers["X-UA"] = _USER_AGENT
        if auth_enabled:
            # NOTE (server contract): the ``apikey`` query parameter is sent
            # in addition to the Authorization / X-FLAREBROW-AUTH headers;
            # the API relies on it, so do not remove it.
            params = kwargs.get("params", {})
            params["apikey"] = flaretool.api_key
            kwargs["params"] = params
            headers["Authorization"] = f"Bearer {flaretool.api_key}"
            headers["X-FLAREBROW-AUTH"] = flaretool.api_key
        response = _get_session().request(
            method=method, url=url, headers=headers, **kwargs
        )
        logger.debug(
            {
                "status_code": response.status_code,
                "method": method,
                "url": url,
                "params": kwargs.get("params", {}),
                "data": kwargs.get("data", {}),
            }
        )
        if (
            auth_enabled or "flarebrow.com" in response.url
        ) and response.status_code == 403:
            raise FlareToolNetworkError(message="Only access from Japan is accepted")
        return response

    @staticmethod
    def get(url: str, **kwargs: Any) -> Response:
        return requests.request("GET", url, **kwargs)

    @staticmethod
    def post(url: str, **kwargs: Any) -> Response:
        return requests.request("POST", url, **kwargs)

    @staticmethod
    def put(url: str, **kwargs: Any) -> Response:
        return requests.request("PUT", url, **kwargs)

    @staticmethod
    def delete(url: str, **kwargs: Any) -> Response:
        return requests.request("DELETE", url, **kwargs)

    @staticmethod
    def head(url: str, **kwargs: Any) -> Response:
        kwargs.setdefault("allow_redirects", False)
        return requests.request("HEAD", url, **kwargs)

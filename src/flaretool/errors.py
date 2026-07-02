"""Exception types raised by flaretool."""

from __future__ import annotations

from typing import Any


class FlareToolError(Exception):
    """Base exception class for FlareTool errors."""

    def __init__(self, message: str | None = None) -> None:
        """
        Initialize FlareToolError.

        Args:
            message: Optional error message (default: None).
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message or ""

    def __repr__(self) -> str:
        columns = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"<{self.__class__.__name__}({columns})>"


class FlareToolNetworkError(FlareToolError):
    """Raised when a request to a Flare service fails."""

    def __init__(
        self,
        message: str | None = None,
        http_body: str | bytes | None = None,
        http_status: int | None = None,
        json_body: Any = None,
        headers: dict[str, Any] | None = None,
        code: str | None = None,
        **param: Any,
    ) -> None:
        super().__init__(message)
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.request_id = self.headers.get("request-id", None)


class AuthenticationError(FlareToolError):
    """Raised when no or invalid API credentials are provided."""

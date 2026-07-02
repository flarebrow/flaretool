"""Errors raised by the DDNS service."""

from flaretool.errors import FlareToolError


class DdnsError(FlareToolError):
    """Base error for the DDNS service.

    All fields default to ``None``/empty so the error is constructible with
    just a message: ``DdnsError("something went wrong")``. Note that the
    message (``status``) comes first; API responses are unpacked with
    keyword arguments (``DdnsError(**result)``) and are unaffected.
    """

    def __init__(
        self,
        status: str = "",
        result: int | None = None,
        currentIp: str | None = None,
        updateIp: str | None = None,
        domain: str | None = None,
    ) -> None:
        self.result = result
        self.status = status
        self.currentIp = currentIp
        self.updateIp = updateIp
        self.domain = domain
        super().__init__(self.status)


class DdnsAuthenticationError(DdnsError):
    pass

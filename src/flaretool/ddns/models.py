"""Data models for the DDNS service."""

from flaretool.basemodels import BaseDataModel


class DdnsInfo(BaseDataModel):
    """
    Represents the Dynamic DNS (DDNS) information.

    Attributes:
        result (int): The result code of the DDNS update.
        status (str): The status of the DDNS update.
        currentIp (str | None): The current IP address associated with the domain.
        updateIp (str): The IP address that was updated.
        domain (str): The domain associated with the DDNS update.
    """

    # Field names mirror the API response (camelCase); snake_case
    # aliases are provided as read-only properties below.
    result: int
    status: str
    currentIp: str | None = None
    updateIp: str
    domain: str

    @property
    def current_ip(self) -> str | None:
        """Snake-case alias for :attr:`currentIp`."""
        return self.currentIp

    @property
    def update_ip(self) -> str:
        """Snake-case alias for :attr:`updateIp`."""
        return self.updateIp

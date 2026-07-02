"""Data models for nettool."""

from flaretool.basemodels import BaseDataModel


class IpInfo(BaseDataModel):
    ipaddr: str | None = None
    hostname: str | None = None
    country: str | None = None


class PunyDomainInfo(BaseDataModel):
    originalvalue: str
    encodevalue: str
    decodevalue: str

"""Data models for the short URL service."""

from datetime import datetime
from typing import Any

from pydantic import model_validator

from flaretool.basemodels import BaseDataModel


class ShortUrlInfo(BaseDataModel):
    id: int
    url: str
    title: str
    code: str
    tag: str | None = None
    description: str | None = None
    owner: str
    is_active: bool
    is_eternal: bool
    limited_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    short_url: str | None = None
    qr_url: str | None = None

    @model_validator(mode="after")
    def _compute_qr_url(self) -> "ShortUrlInfo":
        """Derive ``qr_url`` from ``short_url``.

        The QR endpoint is always ``<short_url>/qr``, so any server-provided
        value is normalized to that form. When ``short_url`` is missing the
        QR URL cannot exist either, so ``qr_url`` is left as ``None``.
        """
        if self.short_url:
            self.qr_url = self.short_url.removesuffix("/") + "/qr"
        else:
            self.qr_url = None
        return self

    def __sub__(self, other: "ShortUrlInfo") -> dict[str, Any]:
        diff = {}
        own = self.model_dump()
        for field, value in other.model_dump().items():
            if own.get(field) != value:
                diff[field] = value
        return diff

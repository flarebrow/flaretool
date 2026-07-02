"""Data models for funcs."""

from flaretool.basemodels import BaseDataModel


class AmazonInfo(BaseDataModel):
    result: bool
    url: str | None = None
    title: str | None = None
    price: int | None = None
    sale: str | None = None
    stock: str | None = None
    distributor: str | None = None
    sender: str | None = None
    evaluation: str | None = None

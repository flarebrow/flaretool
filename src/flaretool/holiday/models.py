"""祝日オンラインAPIのレスポンスデータモデル"""

import datetime

from pydantic import Field

from flaretool.basemodels import BaseDataModel


class SupportedRange(BaseDataModel):
    """オンライン版祝日データがサポートする日付範囲"""

    from_date: datetime.date = Field(alias="from")
    to_date: datetime.date = Field(alias="to")


# 後方互換のためのエイリアス（旧クラス名）
supported = SupportedRange


class HolidaysResponseModel(BaseDataModel):
    """祝日一覧APIのレスポンスモデル"""

    title: str
    author: str
    version: str
    status: bool
    message: str
    updated: datetime.datetime
    supported: SupportedRange
    count: int
    holidays: dict[datetime.date, str] | None

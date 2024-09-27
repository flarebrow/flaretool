#!/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import validator
from flaretool.basemodels import BaseDataModel
from typing import Optional, Union


class ShortUrlInfo(BaseDataModel):
    id: int
    url: str
    title: str
    code: str
    tag: Optional[str] = None
    description: Optional[str] = None
    owner: str
    is_active: bool
    is_eternal: bool
    limited_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    short_url: str = ""
    qr_url: str = ""

    def __init__(self, *args, **param):
        # limit_time = param.pop("limit_time")
        # try:
        #     limit_time = datetime.strptime(limit_time, "%Y-%m-%d %H:%M:%S")
        # except:
        #     pass
        # param["limit_time"] = limit_time
        super(BaseDataModel, self).__init__(*args, **param)

    @validator("qr_url", pre=True, always=True)
    def get_qr_url(cls, value, values):
        return str(values.get("short_url")).removesuffix("/") + "/qr"

    def __sub__(self, other):
        diff = {}
        for field, value in other.model_dump().items():
            if field not in diff and self.model_dump().get(field) != value:
                diff[field] = value
        return diff

#!/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flaretool.basemodels import BaseDataModel
from typing import Union


class ShortUrlInfo(BaseDataModel):
    id: int
    url: str
    title: str
    code: str
    disabled: bool
    insert_time: datetime
    limit_time: Union[datetime, str]
    link: str

    def __sub__(self, other):
        diff = {}
        for field, value in other.dict().items():
            if field not in diff and self.dict().get(field) != value:
                diff[field] = value
        return diff

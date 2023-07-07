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

    def __init__(self, *args, **param):
        limit_time = param.pop("limit_time")
        try:
            limit_time = datetime.strptime(limit_time, "%Y-%m-%d %H:%M:%S")
        except:
            pass
        param["limit_time"] = limit_time
        super(BaseDataModel, self).__init__(*args, **param)

    def __sub__(self, other):
        diff = {}
        for field, value in other.dict().items():
            if field not in diff and self.dict().get(field) != value:
                diff[field] = value
        return diff

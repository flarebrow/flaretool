#!/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from flaretool.basemodels import BaseDataModel
from typing import Union


class UrlInfo(BaseDataModel):
    url: str = None
    title: str = None
    code: str = None
    disabled: bool = None


class UrlRecode(BaseDataModel):
    id: int
    url: str
    title: str
    code: str
    disabled: bool
    insert_time: datetime
    limit_time: Union[datetime, str]
    link: str


class ShortInfo(BaseDataModel):
    message: str
    author: str
    data: list[UrlRecode] = None


class ShortInfoUpdate(BaseDataModel):
    class updatedata(BaseDataModel):
        before: list[UrlRecode]
        after: list[UrlRecode]
    message: str
    author: str
    data: updatedata = None

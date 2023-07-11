#!/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, date
from flaretool.basemodels import BaseDataModel
from pydantic import Field
from typing import Union


class supported(BaseDataModel):
    from_date: date = Field(alias="from")
    to_date: date = Field(alias="to")


class HolidaysResponseModel(BaseDataModel):
    title: str
    author: str
    version: str
    status: bool
    message: str
    updated: datetime
    supported: supported
    count: int
    holidays: Union[dict[date, str], None]

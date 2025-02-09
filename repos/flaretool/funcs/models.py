#!/bin/python
# -*- coding: utf-8 -*-

from typing import Optional

from flaretool.basemodels import BaseDataModel


class AmazonInfo(BaseDataModel):
    result: bool
    url: Optional[str] = None
    title: Optional[str] = None
    price: Optional[int] = None
    sale: Optional[str] = None
    stock: Optional[str] = None
    distributor: Optional[str] = None
    sender: Optional[str] = None
    evaluation: Optional[str] = None

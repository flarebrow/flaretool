#!/bin/python
# -*- coding: utf-8 -*-

from typing import Union
from flaretool.basemodels import BaseDataModel


class AmazonInfo(BaseDataModel):
    result: bool
    url: Union[str, None] = None
    title: Union[str, None] = None
    price: Union[str, int, None] = None
    stock: Union[str, None] = None
    distributor: Union[str, None] = None
    sender: Union[str, None] = None
    evaluation: Union[str, None] = None

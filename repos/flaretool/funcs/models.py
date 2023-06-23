#!/bin/python
# -*- coding: utf-8 -*-

from flaretool.basemodels import BaseDataModel


class AmazonInfo(BaseDataModel):
    url: str = None
    title: str = None
    price: int = None
    stock: str = None
    distributor: str = None
    sender: str = None
    evaluation: str = None

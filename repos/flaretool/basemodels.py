#!/bin/python
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class BaseDataModel(BaseModel):
    pass

    def __trace__(self):
        return "\n".join(
            [f"{key}='{val}'" for key, val in self.__dict__.items()
             if not key.startswith("_")]
        )

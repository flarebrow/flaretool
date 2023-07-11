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

    def __str__(self) -> str:
        columns = ', '.join([
            '{0}={1}'.format(k, repr(self.__dict__[k]))
            for k in self.__dict__.keys() if not k.startswith("_")
        ])

        return '{0}({1})'.format(
            self.__class__.__name__, columns
        )

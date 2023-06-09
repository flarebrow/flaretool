#!/bin/python
# -*- coding: utf-8 -*-

from enum import Enum


class ConversionMode(Enum):
    HALF_WIDTH = 1
    FULL_WIDTH = 2
    UPPER = 3
    LOWER = 4


class Base64Mode(Enum):
    ENCODE = 1
    DECODE = 2


class HashMode(Enum):
    MD5 = 1
    SHA1 = 2
    SHA256 = 3
    SHA512 = 4

#!/bin/python
# -*- coding: utf-8 -*-

from enum import Enum


class Algo(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"
    sha512 = "sha512"

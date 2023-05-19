#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.enums import Algo


def get_hash(value: str, algo: Algo = Algo.md5):
    """
    文字列のハッシュ値を取得します。

    Args:
        value (str): ハッシュ化する文字列
        algo (Algo, optional): ハッシュアルゴリズム。デフォルトはAlgo.md5。

    Returns:
        str: ハッシュ値の文字列

    Examples:
        >>> get_hash("Hello, World!")
        '6cd3556deb0da54bca060b4c39479839'

        >>> get_hash("Hello, World!", Algo.sha256)
        '943a702d06f34599aee1f8da8ef9f7296031d699e7fe2c7fd97e17f19f53eca2'
    """
    import hashlib
    hash_val = hashlib.md5(value.encode()).hexdigest()
    if algo == Algo.sha1:
        hash_val = hashlib.sha1(value.encode()).hexdigest()
    if algo == Algo.sha256:
        hash_val = hashlib.sha256(value.encode()).hexdigest()
    if algo == Algo.sha512:
        hash_val = hashlib.sha512(value.encode()).hexdigest()
    return hash_val


__all__ = ["get_hash"]

#!/bin/python
# -*- coding: utf-8 -*-
import socket
from functools import wraps
from flaretool.error import FlareToolNetworkError


def network_required(func):
    """
    ネットワーク接続のチェックを行い、接続されている場合には指定されたメソッドを実行します。
    接続されていない場合にはFlareToolNetworkErrorを発生させます。

    Args:
        func (callable): ネットワーク接続を確認した後に実行するメソッド。

    Returns:
        callable: デコレートされた関数。

    Raises:
        FlareToolNetworkError: ネットワークに接続されていない場合に発生する例外。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            socket.create_connection(("google.com", 443), timeout=5)
        except OSError:
            raise FlareToolNetworkError("ネットワークに接続されていません。")
        return func(*args, **kwargs)

    return wrapper

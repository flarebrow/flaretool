#!/bin/python
# -*- coding: utf-8 -*-
import time
import socket
from functools import wraps
from flaretool.errors import FlareToolNetworkError
from flaretool.logger import get_logger


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


def retry(max_attempts: int, delay: int = 1):
    """
    リトライ処理を行うデコレーター。

    Args:
        max_attempts (int): 最大リトライ回数
        delay (float, optional): リトライ間隔（秒）（デフォルトは1秒）

    Returns:
        function: デコレートされた関数を実行する

    Examples:
        @retry(max_attempts=3, delay=2)
        def example_function():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            リトライを行うラッパー関数

            Args:
                *args: 関数への位置引数
                **kwargs: 関数へのキーワード引数

            Returns:
                Any: 関数の戻り値（もしくはリトライ上限に達した場合はNone）
            """
            logger = get_logger()
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logger.error(f"Max attempts reached. Giving up.")
                        raise e
                    logger.error(
                        f"Error occurred: {e}. Retrying in {delay} second(s).")
                    time.sleep(delay)
        return wrapper
    return decorator

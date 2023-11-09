#!/bin/python
# -*- coding: utf-8 -*-
import time
import socket
import inspect
from functools import wraps
from flaretool.errors import FlareToolNetworkError
from flaretool.logger import get_logger

__all__ = [
    "network_required",
    "retry",
    "repeat",
    "type_check",
]


def type_check(func):
    """
    型チェックを行うデコレーター

    Parameters:
        func (callable): 型チェックを行う関数。

    Returns:
        callable: デコレートされた関数。

    Raises:
        TypeError: 引数の型が予期された型と一致しない場合に発生します。

    Examples:
        >>> @type_check
        ... def my_function(arg1: int, arg2: str):
        ...     # 関数の処理...
        ...     pass

        >>> my_function(10, "Hello")
        10 Hello

        >>> my_function("10", 20)
        TypeError: Argument 'arg1' has unexpected type 'str' (expected 'int').
    """
    # デコレートされた関数の引数と型アノテーションを取得
    sig = inspect.signature(func)
    parameters = sig.parameters

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 引数の型チェックを実施
        for name, value in zip(parameters.keys(), args):
            if name in func.__annotations__:
                expected_type = func.__annotations__[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' has unexpected type '{type(value).__name__}' (expected '{expected_type.__name__}')."
                    )

        # キーワード引数がある場合の型チェックを実施
        for name, value in kwargs.items():
            if name in func.__annotations__:
                expected_type = func.__annotations__[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' has unexpected type '{type(value).__name__}' (expected '{expected_type.__name__}')."
                    )

        return func(*args, **kwargs)

    return wrapper


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
        delay (int, optional): リトライ間隔（秒）（デフォルトは1秒）

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


def repeat(repeat_count: int, interval: int = 0):
    """
    指定された間隔で関数を指定回数再実行するデコレーター。

    Args:
        repeat_count (int): リピートする回数
        interval (int, optional): 実行間隔（秒単位）。デフォルト値は0。

    Returns:
        function: デコレートされた関数

    Examples:
        >>> @repeat(5, 3)
        ... def print_hello():
        ...     print("Hello, world!")
        ...     if some_condition: # 実行を止めたい場合の条件
        ...         raise StopIteration("Stop the loop")
        ...
        >>> print_hello()
        Hello, world!
        Hello, world!
        Hello, world!
        Hello, world!
        Hello, world!
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()
            for _ in range(repeat_count):
                try:
                    result = func(*args, **kwargs)
                except StopIteration as e:
                    logger.error(str(e))
                    break
                time.sleep(interval)
            return result
        return wrapper
    return decorator

#!/bin/python
# -*- coding: utf-8 -*-
import inspect
import socket
import threading
import time
import warnings
from functools import wraps
from typing import Union, Optional, Callable, Any

from flaretool.errors import FlareToolNetworkError
from flaretool.logger import get_logger

__all__ = [
    "network_required",
    "retry",
    "repeat",
    "type_check",
    "timeout",
    "timer",
    "cache",
    "deprecate",
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


def retry(
    tries: int, delay: float = 0, backoff: float = 1, target_exception: Exception = None
):
    """指定された例外（またはすべての例外）が発生した場合に関数をリトライするデコレーター。

    Args:
        tries (int): 最大リトライ回数。
        delay (float): 最初のリトライまでの遅延秒数。デフォルトは0。
        backoff (float): リトライ間の遅延時間を増加させる係数。デフォルトは1。
        target_exception (Exception, optional): リトライのトリガーとなる例外クラス。
            Noneの場合はすべての例外をキャッチします。デフォルトはNone。

    Returns:
        function: デコレートされた関数の戻り値。

    Raises:
        Exception: 最後のリトライでも例外が発生した場合、その例外を発生させる。

    Examples:
        >>> @retry(3, target_exception=ValueError)
        ... def my_function():
        ...    # Some code that may raise a ValueError
        ...    print("Function executed successfully")
        ...    raise ValueError("Error")
        ...    pass

        >>> try:
        ...    my_function()
        ... except ValueError:
        ...    print("ValueError occurred")
        Function executed successfully
        Function executed successfully
        Function executed successfully
        ValueError occurred
    """
    target_exception = target_exception or Exception

    def decorator_retry(func):
        @wraps(func)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            logger = get_logger()
            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                except target_exception as e:
                    logger.error(
                        f"Error occurred: {e}. Retrying in {mdelay} second(s)."
                    )
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
                    if mtries <= 0:
                        logger.error(f"Max attempts reached. Giving up.")
                        raise e

        return f_retry

    return decorator_retry


def repeat(tries: int, interval: float = 0):
    """
    指定された間隔で関数を指定回数再実行するデコレーター。

    Args:
        tries (int): リピートする回数
        interval (float, optional): 実行間隔（秒単位）。デフォルト値は0。

    Returns:
        function: デコレートされた関数

    Examples:
        >>> @repeat(5, 3)
        ... def print_hello():
        ...     print("Hello, world!")
        ...     if some_condition: # 実行を止めたい場合の条件
        ...         raise StopIteration("Stop the loop")

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
            for _ in range(tries):
                try:
                    result = func(*args, **kwargs)
                except StopIteration as e:
                    logger.error(str(e))
                    break
                time.sleep(interval)
            return result

        return wrapper

    return decorator


def timeout(timeout: Union[int, float]):
    """
    指定した時間内に処理が完了しない場合に TimeoutError を発生させるデコレーター。

    Args:
        timeout (int or float): タイムアウト時間（秒）。

    Returns:
        function: タイムアウト付きのデコレーター。

    Raises:
        TimeoutError: タイムアウトが発生した場合に送出されます。

    Examples:
        >>> @timeout(5)
        ... def my_function():
        ...    # Some time-consuming operation
        ...    time.sleep(10)
        ...    return "Operation completed"

        >>> try:
        ...    result = my_function()
        ...    print(result)
        ... except TimeoutError:
        ...    print("Operation timed out")
        Operation timed out
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            関数をスレッドで実行し、指定したタイムアウト時間内に処理が完了するかをチェックします。

            Args:
                *args: デコレートする関数に渡される位置引数。
                **kwargs: デコレートする関数に渡されるキーワード引数。

            Returns:
                任意の: デコレートされた関数の戻り値。

            Raises:
                TimeoutError: タイムアウトが発生した場合に送出されます。
            """
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout)
            if thread.is_alive():
                thread.join(0)  # タイムアウト後にスレッドを強制終了するため
                raise TimeoutError(
                    f"Function '{func.__name__}' timed out after {timeout} seconds."
                )
            if exception[0]:
                raise exception[0]
            return result[0]

        return wrapper

    return decorator


def timer(func):
    """
    デコレートされた関数の実行時間を測定するデコレーター。
    flaretoolのloggerに出力。

    Args:
        timeout (int or float): タイムアウト時間（秒）。

    Returns:
        function: 実行時間を表示し、元の関数の結果を返すラッパー関数。

    Examples:
        >>> # Logger Setup
        ... from flaretool.logger import setup_logger
        ... logger = setup_logger(logging.DEBUG, console=True)
        ...
        >>> @timer
        ... def example_function(x):
        ...     time.sleep(x)
        ...     return x

        >>> example_function(2)
        [2024-08-01 00:00:00,000] DEBUG : example_function took 2.0000 seconds to execute.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        元の関数の実行時間を計算して表示するラッパー関数。

        引数:
            *args: デコレートされた関数に渡される位置引数。
            **kwargs: デコレートされた関数に渡されるキーワード引数。

        戻り値:
            任意の: デコレートされた関数の戻り値。
        """
        logger = get_logger()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(
            f"{func.__name__} took {end_time - start_time:.4f} seconds to execute."
        )
        return result

    return wrapper


def cache(ttl: Optional[int] = None, maxsize: int = 128):
    """
    関数の結果をキャッシュするデコレーター。TTL（Time To Live）とキャッシュサイズの制限をサポート。

    Args:
        ttl (int, optional): キャッシュの有効期限（秒）。Noneの場合は無期限。デフォルトはNone。
        maxsize (int, optional): キャッシュの最大サイズ。デフォルトは128。

    Returns:
        function: デコレートされた関数の戻り値。

    Examples:
        >>> @cache(ttl=300)  # 5分間キャッシュ
        ... def expensive_function(x, y):
        ...     time.sleep(2)
        ...     return x + y

        >>> result = expensive_function(1, 2)  # 2秒かかる
        >>> result = expensive_function(1, 2)  # すぐに返る（キャッシュから）

        >>> @cache(ttl=10, maxsize=100)
        ... def api_call(endpoint):
        ...     return requests.get(endpoint).json()
    """

    def decorator(func):
        cache_data = {}
        cache_times = {}
        cache_lock = threading.Lock()

        def _make_key(args, kwargs):
            """引数からキャッシュキーを生成"""
            # 関数のシグネチャを取得して引数を正規化
            sig = inspect.signature(func)
            try:
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()

                # 正規化された引数からキーを生成
                key_parts = []
                for param_name, param_value in bound_args.arguments.items():
                    key_parts.append(f"{param_name}={param_value}")
                return "|".join(key_parts)
            except:
                # バインドに失敗した場合は単純なキーを使用
                key_parts = [str(arg) for arg in args]
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                return "|".join(key_parts)

        def _is_expired(cache_time):
            """キャッシュが期限切れかチェック"""
            if ttl is None:
                return False
            return time.time() - cache_time > ttl

        def _evict_oldest():
            """最も古いキャッシュエントリを削除"""
            if cache_times:
                oldest_key = min(cache_times, key=cache_times.get)
                del cache_data[oldest_key]
                del cache_times[oldest_key]

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = _make_key(args, kwargs)

            with cache_lock:
                # キャッシュが存在し、有効期限内の場合
                if key in cache_data:
                    if not _is_expired(cache_times.get(key, 0)):
                        logger = get_logger()
                        logger.debug(f"Cache hit for {func.__name__} with key: {key}")
                        # LRUのためにアクセス時刻を更新
                        cache_times[key] = time.time()
                        return cache_data[key]
                    else:
                        # 期限切れのエントリを削除
                        del cache_data[key]
                        del cache_times[key]

            # ロックを解除して関数を実行（他のスレッドをブロックしないため）
            result = func(*args, **kwargs)

            with cache_lock:
                # キャッシュサイズ制限チェック（キーが既に存在しない場合のみ）
                if key not in cache_data and len(cache_data) >= maxsize:
                    _evict_oldest()

                # キャッシュに保存
                cache_data[key] = result
                cache_times[key] = time.time()

                logger = get_logger()
                logger.debug(f"Cache miss for {func.__name__} with key: {key}")
                return result

        def clear_cache():
            """キャッシュをクリア"""
            with cache_lock:
                cache_data.clear()
                cache_times.clear()

        # キャッシュクリア用のメソッドを追加
        wrapper.clear_cache = clear_cache
        wrapper.cache_info = lambda: {
            "size": len(cache_data),
            "maxsize": maxsize,
            "ttl": ttl,
        }

        return wrapper

    return decorator


def deprecate(
    version: Optional[str] = None,
    alternative: Optional[str] = None,
    message: Optional[str] = None,
):
    """
    関数が非推奨であることを警告するデコレーター。

    Args:
        version (str, optional): この関数が非推奨になるバージョン。デフォルトはNone。
        alternative (str, optional): 代替として推奨される関数名。デフォルトはNone。
        message (str, optional): カスタム警告メッセージ。デフォルトはNone。

    Returns:
        function: デコレートされた関数。

    Examples:
        >>> @deprecate(version="2.0.0", alternative="new_function")
        ... def old_function():
        ...     return "old"

        >>> old_function()
        DeprecationWarning: old_function is deprecated and will be removed in version 2.0.0. Use new_function instead.
        'old'

        >>> @deprecate(message="この関数は使用しないでください")
        ... def legacy_function():
        ...     return "legacy"
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # カスタムメッセージがある場合はそれを使用
            if message:
                warning_message = message
            else:
                # デフォルトメッセージを構築
                warning_message = f"{func.__name__} is deprecated"

                if version:
                    warning_message += f" and will be removed in version {version}"

                if alternative:
                    warning_message += f". Use {alternative} instead"

                warning_message += "."

            # DeprecationWarningを発行
            warnings.warn(warning_message, DeprecationWarning, stacklevel=2)

            # 元の関数を実行
            return func(*args, **kwargs)

        return wrapper

    return decorator

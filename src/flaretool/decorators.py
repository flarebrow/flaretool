"""flaretool の汎用デコレーター群。

同期関数・非同期関数（コルーチン関数）のどちらに適用しても
透過的に動作するように実装されています。
"""

import asyncio
import inspect
import random
import socket
import threading
import time
import types
import warnings
from collections import OrderedDict, deque
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from functools import wraps
from typing import Any, Literal, ParamSpec, TypeVar, Union, get_args, get_origin

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
    "rate_limit",
    "singleton",
    "suppress_errors",
    "run_in_thread",
    "synchronized",
]

P = ParamSpec("P")
R = TypeVar("R")

_UNION_TYPES = (Union, types.UnionType)


def _type_name(annotation: Any) -> str:
    """アノテーションから表示用の型名を取得する内部ヘルパー。"""
    return getattr(annotation, "__name__", None) or str(annotation)


def _matches_type(value: Any, annotation: Any) -> bool:
    """値がアノテーションに適合するかを緩やかに判定する内部ヘルパー。

    - Union / Optional / `X | None` は各メンバーのいずれかに適合すればOK
    - typing.Literal は許容値のいずれかに一致すればOK
    - パラメーター化されたジェネリクス（例: list[str]）は origin 型
      （例: list）のみをチェック
    - origin がクラスでない特殊形式（typing の特殊フォームなど）や
      型として解釈できないアノテーション（文字列など）はチェックしない
    """
    if annotation is Any or annotation is inspect.Parameter.empty:
        return True
    if annotation is None or annotation is type(None):
        return value is None
    origin = get_origin(annotation)
    if origin in _UNION_TYPES:
        return any(_matches_type(value, arg) for arg in get_args(annotation))
    if origin is Literal:
        return value in get_args(annotation)
    if origin is not None:
        if isinstance(origin, type):
            return isinstance(value, origin)
        # isinstance() に使えない特殊形式はチェックしない
        return True
    if isinstance(annotation, type):
        return isinstance(value, annotation)
    return True


def type_check[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    型チェックを行うデコレーター

    引数のアノテーションに基づいて実行時に型チェックを行います。
    デフォルト値が None のパラメーターは暗黙的に Optional として扱われ、
    None の指定を許容します。`X | None` や Optional[X] にも対応し、
    パラメーター化されたジェネリクス（例: list[str]）は origin 型
    （例: list）のみをチェックします。

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
    sig = inspect.signature(func)
    parameters = sig.parameters

    def _validate(args: tuple, kwargs: dict) -> None:
        try:
            bound = sig.bind(*args, **kwargs)
        except TypeError:
            # バインドできない場合は関数呼び出し時のエラーに任せる
            return
        for name, value in bound.arguments.items():
            param = parameters[name]
            if param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue
            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                continue
            # デフォルト値が None のパラメーターは None を許容する
            if value is None and param.default is None:
                continue
            if not _matches_type(value, annotation):
                raise TypeError(
                    f"Argument '{name}' has unexpected type "
                    f"'{type(value).__name__}' (expected '{_type_name(annotation)}')."
                )

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _validate(args, kwargs)
            return await func(*args, **kwargs)

        return async_wrapper

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        _validate(args, kwargs)
        return func(*args, **kwargs)

    return wrapper


def network_required[**P, R](
    func: Callable[P, R] | None = None,
    *,
    host: str = "google.com",
    port: int = 443,
    timeout: float = 5,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    ネットワーク接続のチェックを行い、接続されている場合には指定されたメソッドを実行します。
    接続されていない場合にはFlareToolNetworkErrorを発生させます。

    `@network_required` のように引数なしでも、
    `@network_required(host="example.com", port=80, timeout=3)` のように
    接続確認先を指定しても使用できます。

    Args:
        func (callable, optional): ネットワーク接続を確認した後に実行するメソッド。
        host (str, optional): 接続確認先ホスト。デフォルトは "google.com"。
        port (int, optional): 接続確認先ポート。デフォルトは 443。
        timeout (float, optional): 接続確認のタイムアウト秒数。デフォルトは 5。

    Returns:
        callable: デコレートされた関数。

    Raises:
        FlareToolNetworkError: ネットワークに接続されていない場合に発生する例外。

    Examples:
        >>> @network_required
        ... def fetch_data():
        ...     return "data"

        >>> @network_required(host="example.com", port=80)
        ... def fetch_other():
        ...     return "other"
    """

    def _check_connection() -> None:
        try:
            conn = socket.create_connection((host, port), timeout=timeout)
        except OSError as exc:
            raise FlareToolNetworkError("ネットワークに接続されていません。") from exc
        if conn is not None:
            conn.close()

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                _check_connection()
                return await func(*args, **kwargs)

            return async_wrapper

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _check_connection()
            return func(*args, **kwargs)

        return wrapper

    if callable(func):
        return decorator(func)
    return decorator


def retry(
    tries: int,
    delay: float = 0,
    backoff: float = 1,
    target_exception: type[BaseException]
    | tuple[type[BaseException], ...]
    | None = None,
    jitter: float = 0,
    max_delay: float | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """指定された例外（またはすべての例外）が発生した場合に関数をリトライするデコレーター。

    Args:
        tries (int): 最大リトライ回数。
        delay (float): 最初のリトライまでの遅延秒数。デフォルトは0。
        backoff (float): リトライ間の遅延時間を増加させる係数。デフォルトは1。
        target_exception (type[BaseException] | tuple[type[BaseException], ...], optional):
            リトライのトリガーとなる例外クラス（またはそのタプル）。
            Noneの場合はすべての例外をキャッチします。デフォルトはNone。
        jitter (float, optional): 遅延に加算するランダムな揺らぎの最大秒数
            （0〜jitter の一様乱数）。デフォルトは0。
        max_delay (float, optional): 遅延秒数の上限。Noneの場合は無制限。デフォルトはNone。

    Returns:
        function: デコレートされた関数の戻り値。

    Raises:
        ValueError: tries が 1 未満の場合（デコレート時に発生）。
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
    if tries < 1:
        raise ValueError("tries must be >= 1")
    exceptions = target_exception or Exception

    def _sleep_time(current_delay: float) -> float:
        sleep_for = current_delay
        if jitter:
            sleep_for += random.uniform(0, jitter)
        if max_delay is not None:
            sleep_for = min(sleep_for, max_delay)
        return sleep_for

    def decorator_retry(func: Callable[P, R]) -> Callable[P, R]:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_retry(*args: P.args, **kwargs: P.kwargs) -> R:
                logger = get_logger()
                mdelay = delay
                for attempt in range(1, tries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        if attempt >= tries:
                            logger.error("Max attempts reached. Giving up.")
                            raise
                        sleep_for = _sleep_time(mdelay)
                        logger.error(
                            f"Error occurred: {e}. Retrying in {sleep_for} second(s)."
                        )
                        await asyncio.sleep(sleep_for)
                        mdelay *= backoff

            return async_retry

        @wraps(func)
        def f_retry(*args: P.args, **kwargs: P.kwargs) -> R:
            logger = get_logger()
            mdelay = delay
            for attempt in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt >= tries:
                        logger.error("Max attempts reached. Giving up.")
                        raise
                    sleep_for = _sleep_time(mdelay)
                    logger.error(
                        f"Error occurred: {e}. Retrying in {sleep_for} second(s)."
                    )
                    time.sleep(sleep_for)
                    mdelay *= backoff

        return f_retry

    return decorator_retry


def repeat(
    tries: int, interval: float = 0
) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    """
    指定された間隔で関数を指定回数再実行するデコレーター。

    関数内で StopIteration（非同期関数では StopAsyncIteration も可）を
    送出することで繰り返しを中断できます。
    tries が 0 の場合や最初の呼び出しで中断された場合は None を返します。
    最後の実行後には待機しません。

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

    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
                logger = get_logger()
                result: R | None = None
                for i in range(tries):
                    try:
                        result = await func(*args, **kwargs)
                    except (StopIteration, StopAsyncIteration) as e:
                        logger.error(str(e))
                        break
                    except RuntimeError as e:
                        # コルーチン内で送出された StopIteration は
                        # RuntimeError にラップされる（PEP 479）
                        if isinstance(e.__cause__, StopIteration):
                            logger.error(str(e.__cause__))
                            break
                        raise
                    if i < tries - 1:
                        await asyncio.sleep(interval)
                return result

            return async_wrapper

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            logger = get_logger()
            result: R | None = None
            for i in range(tries):
                try:
                    result = func(*args, **kwargs)
                except StopIteration as e:
                    logger.error(str(e))
                    break
                if i < tries - 1:
                    time.sleep(interval)
            return result

        return wrapper

    return decorator


def timeout(timeout: int | float) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    指定した時間内に処理が完了しない場合に TimeoutError を発生させるデコレーター。

    同期関数はデーモンスレッドで実行して待機し、非同期関数は
    asyncio.wait_for によるタイムアウト制御を行います。
    なお、同期関数の場合、タイムアウト後もバックグラウンドのスレッド自体は
    処理が終わるまで動き続けます（デーモンスレッドのため
    インタープリター終了は妨げません）。

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

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                try:
                    return await asyncio.wait_for(func(*args, **kwargs), timeout)
                except TimeoutError:
                    raise TimeoutError(
                        f"Function '{func.__name__}' timed out after {timeout} seconds."
                    ) from None

            return async_wrapper

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result: list[R | None] = [None]
            exception: list[BaseException | None] = [None]

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except BaseException as e:
                    exception[0] = e

            thread = threading.Thread(target=target, daemon=True)
            thread.start()
            thread.join(timeout)
            if thread.is_alive():
                raise TimeoutError(
                    f"Function '{func.__name__}' timed out after {timeout} seconds."
                )
            if exception[0]:
                raise exception[0]
            return result[0]

        return wrapper

    return decorator


def timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    デコレートされた関数の実行時間を測定するデコレーター。
    flaretoolのloggerに出力。関数が例外を送出した場合も
    経過時間をログに出力します。

    Args:
        func (callable): 実行時間を測定する関数。

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
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logger = get_logger()
            start_time = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start_time
                logger.debug(f"{func.__name__} took {elapsed:.4f} seconds to execute.")

        return async_wrapper

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger = get_logger()
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            logger.debug(f"{func.__name__} took {elapsed:.4f} seconds to execute.")

    return wrapper


def cache(
    ttl: int | float | None = None, maxsize: int = 128
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    関数の結果をキャッシュするデコレーター。TTL（Time To Live）とキャッシュサイズの制限をサポート。

    有効期限の判定にはキャッシュ登録時刻（time.monotonic）を使用します。
    キャッシュヒットでは有効期限は延長されず、LRUの追い出し順のみが更新されます。
    キャッシュキーは引数の型を区別します（例: f(1) と f('1') は別エントリ）。
    キーワード引数を含む呼び出しはシグネチャにバインドして正規化されるため、
    f(1, 2) と f(x=1, y=2) は同じエントリを共有します。
    同期関数はスレッドセーフです。非同期関数も同じロックを使用しますが、
    ロック保持区間は辞書操作のみの短時間であり await を含まないため、
    イベントループをブロックしません。関数本体はロックの外で実行されます。

    Args:
        ttl (int | float, optional): キャッシュの有効期限（秒）。Noneの場合は無期限。デフォルトはNone。
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

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # key -> (結果, 登録時刻)。挿入/アクセス順を利用してO(1)でLRU管理する
        cache_store: OrderedDict[Any, tuple[R, float]] = OrderedDict()
        cache_lock = threading.Lock()

        try:
            sig = inspect.signature(func)
        except (TypeError, ValueError):  # pragma: no cover - 極端なケースのみ
            sig = None

        def _components(values) -> tuple:
            """値の並びから型情報付きのキー要素を生成（f(1) と f('1') を区別）"""
            return tuple((type(v).__qualname__, repr(v)) for v in values)

        def _make_key(args: tuple, kwargs: dict) -> tuple:
            """引数からキャッシュキーを生成"""
            if not kwargs:
                # 位置引数のみの呼び出しはバインドせずタプルをそのまま使う（高速パス）
                return _components(args)
            if sig is not None:
                try:
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    return _components(bound_args.arguments.values())
                except TypeError:
                    pass
            # バインドに失敗した場合は単純なキーを使用
            return _components(args) + tuple(
                (k, type(v).__qualname__, repr(v)) for k, v in sorted(kwargs.items())
            )

        def _is_expired(birth_time: float) -> bool:
            """キャッシュが期限切れかチェック"""
            if ttl is None:
                return False
            return time.monotonic() - birth_time > ttl

        def _lookup(key: tuple) -> tuple[bool, R | None]:
            """キャッシュから値を取得（ヒット有無と値を返す）"""
            with cache_lock:
                entry = cache_store.get(key)
                if entry is not None:
                    value, birth_time = entry
                    if not _is_expired(birth_time):
                        get_logger().debug(
                            f"Cache hit for {func.__name__} with key: {key}"
                        )
                        # LRUのために末尾へ移動（TTLは延長しない）
                        cache_store.move_to_end(key)
                        return True, value
                    # 期限切れのエントリを削除
                    del cache_store[key]
            return False, None

        def _store(key: tuple, result: R) -> None:
            """関数の実行結果をキャッシュに保存"""
            with cache_lock:
                if key in cache_store:
                    cache_store.move_to_end(key)
                elif len(cache_store) >= maxsize:
                    # 最も使われていないエントリ（先頭）をO(1)で削除
                    cache_store.popitem(last=False)
                cache_store[key] = (result, time.monotonic())
                get_logger().debug(f"Cache miss for {func.__name__} with key: {key}")

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                key = _make_key(args, kwargs)
                hit, value = _lookup(key)
                if hit:
                    return value
                result = await func(*args, **kwargs)
                _store(key, result)
                return result

            wrapper = async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                key = _make_key(args, kwargs)
                hit, value = _lookup(key)
                if hit:
                    return value
                result = func(*args, **kwargs)
                _store(key, result)
                return result

            wrapper = sync_wrapper

        def clear_cache() -> None:
            """キャッシュをクリア"""
            with cache_lock:
                cache_store.clear()

        # キャッシュクリア用のメソッドを追加
        wrapper.clear_cache = clear_cache
        wrapper.cache_info = lambda: {
            "size": len(cache_store),
            "maxsize": maxsize,
            "ttl": ttl,
        }

        return wrapper

    return decorator


def deprecate(
    version: str | None = None,
    alternative: str | None = None,
    message: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
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

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def _warn() -> None:
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
            warnings.warn(warning_message, DeprecationWarning, stacklevel=3)

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                _warn()
                return await func(*args, **kwargs)

            return async_wrapper

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _warn()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def rate_limit(calls: int, period: float) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    関数の呼び出し回数を制限するデコレーター（スライディングウィンドウ方式）。

    period 秒間の呼び出し回数を calls 回までに制限します。
    制限を超えた場合は空きが出るまでブロック（非同期関数の場合は待機）します。

    Args:
        calls (int): period 秒間に許可する呼び出し回数。
        period (float): 制限期間（秒）。

    Returns:
        function: デコレートされた関数。

    Examples:
        >>> @rate_limit(calls=2, period=1.0)
        ... def api_call():
        ...     return "called"

        >>> api_call()  # すぐに実行
        >>> api_call()  # すぐに実行
        >>> api_call()  # 1秒間の枠が空くまで待機してから実行
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        timestamps: deque[float] = deque()
        lock = threading.Lock()

        def _acquire() -> float:
            """スロットを取得する。取得できない場合は待機秒数を返す。"""
            with lock:
                now = time.monotonic()
                while timestamps and now - timestamps[0] >= period:
                    timestamps.popleft()
                if len(timestamps) < calls:
                    timestamps.append(now)
                    return 0
                return timestamps[0] + period - now

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                while True:
                    wait = _acquire()
                    if wait <= 0:
                        break
                    await asyncio.sleep(wait)
                return await func(*args, **kwargs)

            return async_wrapper

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            while True:
                wait = _acquire()
                if wait <= 0:
                    break
                time.sleep(wait)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def singleton[R](cls: type[R]) -> Callable[..., R]:
    """
    クラスをシングルトンにするデコレーター（スレッドセーフ）。

    最初の呼び出しでインスタンスを生成し、以降は同じインスタンスを返します。
    デコレート後の名前はインスタンスを返すファクトリー関数になります
    （生成されるインスタンスは元のクラスのインスタンスです）。

    Args:
        cls (type): シングルトンにするクラス。

    Returns:
        callable: 常に同一インスタンスを返すファクトリー関数。

    Examples:
        >>> @singleton
        ... class Config:
        ...     def __init__(self):
        ...         self.value = 42

        >>> a = Config()
        >>> b = Config()
        >>> a is b
        True
    """
    lock = threading.Lock()
    instance: R | None = None

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> R:
        nonlocal instance
        if instance is None:
            with lock:
                if instance is None:
                    instance = cls(*args, **kwargs)
        return instance

    return get_instance


def suppress_errors(
    default: Any = None,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = (Exception,),
    log: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R | Any]]:
    """
    例外を抑制してデフォルト値を返すデコレーター。

    指定した例外が発生した場合、例外を送出する代わりに default を返します。

    Args:
        default (Any, optional): 例外発生時に返す値。デフォルトはNone。
        exceptions (type | tuple, optional): 抑制する例外クラス（またはそのタプル）。
            デフォルトは (Exception,)。
        log (bool, optional): 例外発生時にログを出力するかどうか。デフォルトはTrue。

    Returns:
        function: デコレートされた関数。

    Examples:
        >>> @suppress_errors(default=0)
        ... def parse_number(text):
        ...     return int(text)

        >>> parse_number("123")
        123
        >>> parse_number("abc")  # 例外は送出されず 0 が返る
        0
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R | Any]:
        def _handle(e: BaseException) -> Any:
            if log:
                get_logger().error(f"Error suppressed in {func.__name__}: {e}")
            return default

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R | Any:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    return _handle(e)

            return async_wrapper

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                return _handle(e)

        return wrapper

    return decorator


_thread_pool: ThreadPoolExecutor | None = None
_thread_pool_lock = threading.Lock()


def _get_thread_pool() -> ThreadPoolExecutor:
    """run_in_thread 用の共有スレッドプールを取得する内部ヘルパー。"""
    global _thread_pool
    if _thread_pool is None:
        with _thread_pool_lock:
            if _thread_pool is None:
                _thread_pool = ThreadPoolExecutor(
                    max_workers=8, thread_name_prefix="flaretool-run_in_thread"
                )
    return _thread_pool


def run_in_thread[**P, R](func: Callable[P, R]) -> Callable[P, "Future[R]"]:
    """
    同期関数をバックグラウンドスレッドで実行するデコレーター。

    呼び出すと即座に concurrent.futures.Future を返します。
    結果は Future.result() で取得できます。
    実行にはモジュール共有の ThreadPoolExecutor（最大8ワーカー）を使用します。
    コルーチン関数には適用できません（asyncio.create_task 等を使用してください）。

    Args:
        func (callable): バックグラウンドで実行する同期関数。

    Returns:
        callable: Future を返すラッパー関数。

    Raises:
        TypeError: コルーチン関数に適用した場合に発生します。

    Examples:
        >>> @run_in_thread
        ... def slow_task(x):
        ...     time.sleep(1)
        ...     return x * 2

        >>> future = slow_task(5)  # すぐに返る
        >>> future.result()  # 完了を待って結果を取得
        10
    """
    if inspect.iscoroutinefunction(func):
        raise TypeError(
            "run_in_thread cannot be applied to coroutine functions. "
            "Use asyncio.create_task instead."
        )

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> "Future[R]":
        return _get_thread_pool().submit(func, *args, **kwargs)

    return wrapper


def synchronized[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """
    関数の同時実行を防ぐデコレーター。

    同期関数には関数ごとの再入可能ロック（threading.RLock）を使用します。
    非同期関数には関数ごとの asyncio.Lock を使用します
    （複数のイベントループをまたいだ使用はできません）。

    Args:
        func (callable): 排他制御を行う関数。

    Returns:
        callable: デコレートされた関数。

    Examples:
        >>> counter = {"value": 0}

        >>> @synchronized
        ... def increment():
        ...     current = counter["value"]
        ...     time.sleep(0.01)
        ...     counter["value"] = current + 1

        >>> # 複数スレッドから呼び出しても安全
    """
    if inspect.iscoroutinefunction(func):
        async_lock = asyncio.Lock()

        @wraps(func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            async with async_lock:
                return await func(*args, **kwargs)

        return async_wrapper

    lock = threading.RLock()

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        with lock:
            return func(*args, **kwargs)

    return wrapper

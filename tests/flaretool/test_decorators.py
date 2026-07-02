import asyncio
import threading
import time
import unittest
import warnings
from concurrent.futures import Future
from typing import Final, Literal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from flaretool.decorators import *
from flaretool.errors import FlareToolNetworkError


class LogCapturing:
    def __init__(self):
        self.log = []

    def error(self, message):
        self.log.append(message)

    def reset(self):
        self.log = []


class TestTypeCheckDecorator(unittest.TestCase):
    @type_check
    def add_numbers(self, a: int, b: int) -> int:
        return a + b

    @type_check
    def greet_person(self, name: str) -> str:
        return f"Hello, {name}!"

    def test_add_numbers(self):
        result = self.add_numbers(5, 10)
        self.assertEqual(result, 15)

        with self.assertRaises(TypeError):
            self.add_numbers("hello", 10)

    def test_greet_person(self):
        result = self.greet_person("Alice")
        self.assertEqual(result, "Hello, Alice!")

        with self.assertRaises(TypeError):
            self.greet_person(123)

        with self.assertRaises(TypeError):
            self.greet_person(name=123)


def test_type_check_error_message_format():
    @type_check
    def my_function(arg1: int, arg2: str):
        return arg1, arg2

    with pytest.raises(
        TypeError,
        match=r"Argument 'arg1' has unexpected type 'str' \(expected 'int'\)\.",
    ):
        my_function("10", "hello")


def test_type_check_none_default_is_implicitly_optional():
    """`x: int = None` のようなパラメーターは None を許容する"""

    @type_check
    def get(id: int = None):
        return id

    assert get() is None
    assert get(None) is None
    assert get(id=None) is None
    assert get(5) == 5
    with pytest.raises(TypeError):
        get("abc")


def test_type_check_optional_and_union_annotations():
    @type_check
    def func(x: int | None, y: str | None = "default"):
        return x, y

    assert func(None) == (None, "default")
    assert func(1, None) == (1, None)
    assert func(2, "text") == (2, "text")
    with pytest.raises(TypeError):
        func("not int")
    with pytest.raises(TypeError):
        func(1, y=123)


def test_type_check_parameterized_generics():
    """パラメーター化されたジェネリクスは origin 型のみをチェックする"""

    @type_check
    def func(items: list[str], mapping: dict = {}):
        return items, mapping

    assert func(["a", "b"]) == (["a", "b"], {})
    # origin (list) のみチェックするため要素型は検査されない
    assert func([1, 2]) == ([1, 2], {})
    with pytest.raises(
        TypeError,
        match=r"Argument 'items' has unexpected type 'str' \(expected 'list'\)\.",
    ):
        func("not a list")


def test_type_check_literal_annotation():
    """Literal アノテーションは isinstance() でクラッシュせず許容値をチェックする"""

    @type_check
    def func(x: Literal["a", "b"]):
        return x

    assert func("a") == "a"
    assert func("b") == "b"
    with pytest.raises(TypeError):
        func("c")
    with pytest.raises(TypeError):
        func(1)


def test_type_check_optional_literal():
    @type_check
    def func(x: Literal["a", "b"] | None = None):
        return x

    assert func() is None
    assert func("a") == "a"
    with pytest.raises(TypeError):
        func("c")


def test_type_check_non_class_special_form_is_skipped():
    """origin がクラスでない特殊形式はチェックせずクラッシュもしない"""

    @type_check
    def func(x: Final[int]):
        return x

    # チェック対象外なのでどんな値でも通る
    assert func(1) == 1
    assert func("text") == "text"


async def test_type_check_async_function():
    @type_check
    async def add(a: int, b: int) -> int:
        return a + b

    assert await add(1, 2) == 3
    with pytest.raises(TypeError):
        await add("1", 2)


class NetworkRequiredDecoratorTests(unittest.TestCase):
    @network_required
    def my_function(self):
        return "Success"

    def test_network_required_decorator_with_network_connection(self):
        # ネットワーク接続が確立されている場合のテスト
        with patch("socket.create_connection") as mock_create_connection:
            # モックの振る舞いを設定
            mock_create_connection.return_value = MagicMock()
            # デコレートされた関数を呼び出してテスト
            result = self.my_function()
            self.assertEqual(result, "Success")
            # socket.create_connectionが呼ばれたことを検証
            mock_create_connection.assert_called_with(("google.com", 443), timeout=5)
            # 確認用ソケットがクローズされたことを検証
            mock_create_connection.return_value.close.assert_called_once()

    def test_network_required_decorator_without_network_connection(self):
        # ネットワーク接続が確立されていない場合のテスト
        with patch("socket.create_connection") as mock_create_connection:
            # モックの振る舞いを設定
            mock_create_connection.side_effect = OSError
            # デコレートされた関数を呼び出して例外の発生を検証
            with self.assertRaises(FlareToolNetworkError):
                self.my_function()
            # socket.create_connectionが呼ばれたことを検証
            mock_create_connection.assert_called_with(("google.com", 443), timeout=5)


def test_network_required_with_custom_host_port_timeout():
    @network_required(host="example.com", port=80, timeout=3)
    def my_function():
        return "Success"

    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.return_value = MagicMock()
        assert my_function() == "Success"
        mock_create_connection.assert_called_with(("example.com", 80), timeout=3)
        mock_create_connection.return_value.close.assert_called_once()


async def test_network_required_async():
    @network_required
    async def my_function():
        return "Success"

    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.return_value = MagicMock()
        assert await my_function() == "Success"
        mock_create_connection.return_value.close.assert_called_once()

    with patch("socket.create_connection") as mock_create_connection:
        mock_create_connection.side_effect = OSError
        with pytest.raises(FlareToolNetworkError):
            await my_function()


class RetryDecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = LogCapturing()

    def tearDown(self):
        self.logger.reset()

    def test_retry_success(self):
        # Mock function that always succeeds
        @retry(3)
        def success_function():
            return "Success"

        result = success_function()
        self.assertEqual(result, "Success")

    def test_retry_failure(self):
        # Mock function that always fails
        @retry(3)
        def failure_function():
            raise ValueError("Always fails")

        with self.assertRaises(ValueError):
            failure_function()

    def test_retry_error_logging(self):
        # Mock function that always fails
        @retry(3)
        def failure_function():
            raise ValueError("Always fails")

        with patch("logging.getLogger") as mock_logger:
            mock_logger.return_value = self.logger

            with self.assertRaises(ValueError):
                failure_function()

            self.assertIn(
                "Error occurred: Always fails. Retrying in 0 second(s).",
                self.logger.log,
            )
            self.assertIn("Max attempts reached. Giving up.", self.logger.log)


def test_retry_no_sleep_after_final_attempt():
    """最後の失敗後には待機しないこと（バグ修正の確認）"""
    with patch("time.sleep") as mock_sleep:

        @retry(3, delay=1)
        def failure_function():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            failure_function()

        # 3回試行 → リトライ間の待機は2回のみ
        assert mock_sleep.call_count == 2


def test_retry_backoff():
    with patch("time.sleep") as mock_sleep:

        @retry(3, delay=1, backoff=2)
        def failure_function():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            failure_function()

        assert [c.args[0] for c in mock_sleep.call_args_list] == [1, 2]


def test_retry_jitter_bounds():
    with (
        patch("time.sleep") as mock_sleep,
        patch("flaretool.decorators.random.uniform", return_value=0.25) as mock_uniform,
    ):

        @retry(3, delay=1, jitter=0.5)
        def failure_function():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            failure_function()

        mock_uniform.assert_called_with(0, 0.5)
        assert [c.args[0] for c in mock_sleep.call_args_list] == [1.25, 1.25]


def test_retry_max_delay():
    with patch("time.sleep") as mock_sleep:

        @retry(3, delay=10, backoff=2, max_delay=5)
        def failure_function():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            failure_function()

        assert [c.args[0] for c in mock_sleep.call_args_list] == [5, 5]


def test_retry_target_exception_not_caught():
    @retry(3, target_exception=ValueError)
    def failure_function():
        raise KeyError("not retried")

    call_count = {"count": 0}

    @retry(3, target_exception=(ValueError, KeyError))
    def tuple_target():
        call_count["count"] += 1
        raise KeyError("retried")

    with pytest.raises(KeyError):
        failure_function()
    with pytest.raises(KeyError):
        tuple_target()
    assert call_count["count"] == 3


def test_retry_invalid_tries_raises_at_decoration_time():
    """tries < 1 はデコレート時に ValueError（黙って None を返さない）"""
    with pytest.raises(ValueError, match="tries must be >= 1"):

        @retry(0)
        def never_called():
            raise ValueError("never")

    with pytest.raises(ValueError, match="tries must be >= 1"):
        retry(-1)


async def test_retry_async_success_after_failures():
    attempts = {"count": 0}

    @retry(3)
    async def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("fail")
        return "Success"

    assert await flaky() == "Success"
    assert attempts["count"] == 3


async def test_retry_async_failure_uses_asyncio_sleep():
    logger = LogCapturing()
    with (
        patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep,
        patch("flaretool.decorators.get_logger", return_value=logger),
    ):

        @retry(3, delay=1, backoff=2)
        async def failure_function():
            raise ValueError("Always fails")

        with pytest.raises(ValueError):
            await failure_function()

        assert [c.args[0] for c in mock_sleep.call_args_list] == [1, 2]
        assert "Max attempts reached. Giving up." in logger.log


class RepeatDecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = LogCapturing()

    def tearDown(self):
        self.logger.reset()

    # モック用の関数を定義
    def mock_function(self):
        pass

    def test_repeat_decorator(self):
        # モック関数の作成
        with patch("logging.getLogger") as mock_logger, patch("time.sleep"):
            mock_logger.return_value = self.logger
            mock_func = MagicMock(
                side_effect=[self.mock_function, StopIteration("Stop the loop")]
            )

            # テスト対象の関数とデコレーターの組み合わせを作成します
            @repeat(5, 3)
            def test_function():
                mock_func()

            # テスト関数を呼び出します
            test_function()

            self.assertEqual(mock_func.call_count, 2)

            self.assertIn("Stop the loop", self.logger.log)


def test_repeat_zero_tries_returns_none():
    """tries=0 でも UnboundLocalError にならず None を返す（バグ修正の確認）"""
    mock_func = MagicMock()

    @repeat(0)
    def test_function():
        mock_func()
        return "value"

    assert test_function() is None
    assert mock_func.call_count == 0


def test_repeat_stop_on_first_call_returns_none():
    """最初の呼び出しで StopIteration が発生しても None を返す（バグ修正の確認）"""
    logger = LogCapturing()
    with patch("flaretool.decorators.get_logger", return_value=logger):

        @repeat(5)
        def test_function():
            raise StopIteration("Stop immediately")

        assert test_function() is None
        assert "Stop immediately" in logger.log


def test_repeat_no_sleep_after_last_iteration():
    with patch("time.sleep") as mock_sleep:

        @repeat(3, 1)
        def test_function():
            return "ok"

        assert test_function() == "ok"
        # 3回実行 → 実行間の待機は2回のみ
        assert mock_sleep.call_count == 2


async def test_repeat_async():
    calls = {"count": 0}

    @repeat(3)
    async def test_function():
        calls["count"] += 1
        return calls["count"]

    result = await test_function()
    assert result == 3
    assert calls["count"] == 3


async def test_repeat_async_stop_iteration():
    """非同期関数内の StopIteration（PEP 479 で RuntimeError にラップ）でも停止する"""
    logger = LogCapturing()
    mock_func = MagicMock(side_effect=[None, StopIteration("Stop the loop")])
    with patch("flaretool.decorators.get_logger", return_value=logger):

        @repeat(5)
        async def test_function():
            mock_func()

        assert await test_function() is None
        assert mock_func.call_count == 2
        assert "Stop the loop" in logger.log


async def test_repeat_async_stop_async_iteration():
    logger = LogCapturing()
    calls = {"count": 0}
    with patch("flaretool.decorators.get_logger", return_value=logger):

        @repeat(5)
        async def test_function():
            calls["count"] += 1
            if calls["count"] >= 2:
                raise StopAsyncIteration("Stop async loop")

        await test_function()
        assert calls["count"] == 2
        assert "Stop async loop" in logger.log


class TestTimeoutDecorator(unittest.TestCase):
    def test_timeout_success(self):
        """
        Test the `timeout` decorator with a function that completes within the timeout period.
        """

        @timeout(2)
        def quick_function():
            time.sleep(0.2)
            return "Completed"

        result = quick_function()
        self.assertEqual(result, "Completed")

    def test_timeout_failure(self):
        """
        Test the `timeout` decorator with a function that exceeds the timeout period.
        """

        @timeout(0.5)
        def slow_function():
            time.sleep(2)
            return "Should not reach here"

        with self.assertRaises(TimeoutError):
            slow_function()

    def test_timeout_exception(self):
        """
        Test the `timeout` decorator with a function that raises an exception.
        """

        @timeout(2)
        def function_with_exception():
            time.sleep(0.1)
            raise ValueError("An error occurred")

        with self.assertRaises(ValueError):
            function_with_exception()


async def test_timeout_async_success():
    @timeout(2)
    async def quick_function():
        await asyncio.sleep(0.05)
        return "Completed"

    assert await quick_function() == "Completed"


async def test_timeout_async_failure():
    @timeout(0.2)
    async def slow_function():
        await asyncio.sleep(2)
        return "Should not reach here"

    with pytest.raises(
        TimeoutError, match="'slow_function' timed out after 0.2 seconds"
    ):
        await slow_function()


async def test_timeout_async_exception():
    @timeout(2)
    async def function_with_exception():
        raise ValueError("An error occurred")

    with pytest.raises(ValueError):
        await function_with_exception()


class TimerDecoratorTestCase(unittest.TestCase):
    def test_timer_decorator(self):
        # Mock function that takes some time to execute
        @timer
        def long_running_function():
            time.sleep(0.2)
            return "Success"

        result = long_running_function()
        self.assertEqual(result, "Success")

    def test_timer_decorator_with_mock_logger(self):
        # Mock function that takes some time to execute
        @timer
        def long_running_function():
            time.sleep(0.2)
            return "Success"

        with patch("flaretool.decorators.get_logger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            result = long_running_function()
            self.assertEqual(result, "Success")

            self.assertIn(
                "long_running_function took", mock_logger.debug.call_args[0][0]
            )
            self.assertIn("seconds to execute.", mock_logger.debug.call_args[0][0])


def test_timer_logs_even_on_exception():
    """関数が例外を送出しても経過時間がログに出力される"""
    with patch("flaretool.decorators.get_logger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        @timer
        def failing_function():
            raise ValueError("boom")

        with pytest.raises(ValueError):
            failing_function()

        message = mock_logger.debug.call_args[0][0]
        assert "failing_function took" in message
        assert "seconds to execute." in message


async def test_timer_async():
    with patch("flaretool.decorators.get_logger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        @timer
        async def async_function():
            await asyncio.sleep(0.05)
            return "Success"

        assert await async_function() == "Success"
        message = mock_logger.debug.call_args[0][0]
        assert "async_function took" in message
        assert "seconds to execute." in message


class CacheDecoratorTestCase(unittest.TestCase):
    def test_cache_basic(self):
        """キャッシュの基本動作テスト"""
        call_count = {"count": 0}

        @cache()
        def expensive_function(x, y):
            call_count["count"] += 1
            return x + y

        # 最初の呼び出し
        result1 = expensive_function(1, 2)
        self.assertEqual(result1, 3)
        self.assertEqual(call_count["count"], 1)

        # 同じ引数での2回目の呼び出し（キャッシュから取得）
        result2 = expensive_function(1, 2)
        self.assertEqual(result2, 3)
        self.assertEqual(call_count["count"], 1)

        # 異なる引数での呼び出し
        result3 = expensive_function(2, 3)
        self.assertEqual(result3, 5)
        self.assertEqual(call_count["count"], 2)

    def test_cache_with_ttl(self):
        """TTL付きキャッシュのテスト"""
        call_count = {"count": 0}

        @cache(ttl=0.5)
        def timed_function(x):
            call_count["count"] += 1
            return x * 2

        # 最初の呼び出し
        result1 = timed_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count["count"], 1)

        # TTL内での2回目の呼び出し（キャッシュから取得）
        result2 = timed_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count["count"], 1)

        # TTL経過後の呼び出し（再計算）
        time.sleep(0.6)
        result3 = timed_function(5)
        self.assertEqual(result3, 10)
        self.assertEqual(call_count["count"], 2)

    def test_cache_with_maxsize(self):
        """maxsizeのテスト（LRU動作確認）"""
        call_count = {"count": 0}

        @cache(maxsize=2)
        def limited_cache_function(x):
            call_count["count"] += 1
            return x**2

        # 2つの異なる引数で呼び出し（キャッシュ: 1, 2）
        limited_cache_function(1)
        limited_cache_function(2)
        self.assertEqual(call_count["count"], 2)

        # 1をアクセス（キャッシュヒット、1のアクセス時刻更新）
        limited_cache_function(1)
        self.assertEqual(call_count["count"], 2)

        # 3を呼び出し（キャッシュ: 1, 3、2が削除される）
        limited_cache_function(3)
        self.assertEqual(call_count["count"], 3)

        # 1はまだキャッシュにあるはず（キャッシュヒット）
        limited_cache_function(1)
        self.assertEqual(call_count["count"], 3)

        # 3もまだキャッシュにあるはず（キャッシュヒット）
        limited_cache_function(3)
        self.assertEqual(call_count["count"], 3)

        # 2は削除されているのでキャッシュミス
        limited_cache_function(2)
        self.assertEqual(call_count["count"], 4)

    def test_cache_clear(self):
        """キャッシュクリア機能のテスト"""
        call_count = {"count": 0}

        @cache()
        def cacheable_function(x):
            call_count["count"] += 1
            return x + 100

        # 最初の呼び出し
        cacheable_function(1)
        self.assertEqual(call_count["count"], 1)

        # キャッシュから取得
        cacheable_function(1)
        self.assertEqual(call_count["count"], 1)

        # キャッシュをクリア
        cacheable_function.clear_cache()

        # クリア後は再計算
        cacheable_function(1)
        self.assertEqual(call_count["count"], 2)

    def test_cache_info(self):
        """キャッシュ情報取得のテスト"""

        @cache(ttl=300, maxsize=50)
        def info_function(x):
            return x

        info = info_function.cache_info()
        self.assertEqual(info["ttl"], 300)
        self.assertEqual(info["maxsize"], 50)
        self.assertEqual(info["size"], 0)

        info_function(1)
        info = info_function.cache_info()
        self.assertEqual(info["size"], 1)

    def test_cache_with_kwargs(self):
        """キーワード引数を含むキャッシュのテスト"""
        call_count = {"count": 0}

        @cache()
        def kwargs_function(x, y=10):
            call_count["count"] += 1
            return x + y

        # 異なる呼び出し方法でも正しくキャッシュされることを確認
        result1 = kwargs_function(5, 10)
        self.assertEqual(call_count["count"], 1)

        result2 = kwargs_function(5, y=10)
        self.assertEqual(call_count["count"], 1)

        result3 = kwargs_function(x=5, y=10)
        self.assertEqual(call_count["count"], 1)

    def test_cache_with_bind_failure(self):
        """inspect.signature().bind()が失敗した場合のフォールバック処理テスト"""
        call_count = {"count": 0}

        # デコレーター適用前にinspect.signatureをモック
        with patch("flaretool.decorators.inspect.signature") as mock_signature:
            # bind()が呼ばれた時に例外を投げる
            mock_sig = MagicMock()
            mock_sig.bind.side_effect = TypeError("Mock bind error")
            mock_signature.return_value = mock_sig

            # デコレーターを適用（この時点でモックされたinspectが使われる）
            @cache()
            def test_function(x, y):
                call_count["count"] += 1
                return x + y

            # 関数を呼び出し（フォールバックロジックが使用される）
            result1 = test_function(1, 2)
            self.assertEqual(result1, 3)
            self.assertEqual(call_count["count"], 1)

            # 同じ引数で再度呼び出し（キャッシュヒット）
            result2 = test_function(1, 2)
            self.assertEqual(result2, 3)
            self.assertEqual(call_count["count"], 1)


def test_cache_ttl_not_refreshed_on_hit():
    """キャッシュヒットで有効期限（TTL）が延長されないこと（バグ修正の確認）"""
    clock = {"now": 0.0}
    with patch("flaretool.decorators.time.monotonic", side_effect=lambda: clock["now"]):
        call_count = {"count": 0}

        @cache(ttl=10)
        def cached_function(x):
            call_count["count"] += 1
            return x * 2

        # t=0: キャッシュミス（登録）
        assert cached_function(1) == 2
        assert call_count["count"] == 1

        # t=8: TTL内なのでキャッシュヒット（アクセス時刻のみ更新）
        clock["now"] = 8.0
        assert cached_function(1) == 2
        assert call_count["count"] == 1

        # t=12: 登録時刻(t=0)から10秒超過 → 直前のヒットに関係なく期限切れ
        clock["now"] = 12.0
        assert cached_function(1) == 2
        assert call_count["count"] == 2


def test_cache_uses_monotonic_clock():
    """TTL判定に time.monotonic が使用されること"""
    with patch(
        "flaretool.decorators.time.monotonic", return_value=100.0
    ) as mock_monotonic:

        @cache(ttl=5)
        def cached_function(x):
            return x

        cached_function(1)
        assert mock_monotonic.called


def test_cache_key_is_type_aware():
    """f(1) と f('1') が同じキャッシュエントリを共有しないこと（バグ修正の確認）"""
    call_count = {"count": 0}

    @cache()
    def identity(x):
        call_count["count"] += 1
        return x

    assert identity(1) == 1
    assert identity("1") == "1"
    assert call_count["count"] == 2
    # それぞれのエントリはヒットする
    assert identity(1) == 1
    assert identity("1") == "1"
    assert call_count["count"] == 2
    assert identity.cache_info()["size"] == 2

    # bool と int も区別される（repr が異なる）
    assert identity(True) is True
    assert call_count["count"] == 3


def test_cache_lru_eviction_order():
    """LRU: 最も使われていないエントリから追い出されること"""
    call_count = {"count": 0}

    @cache(maxsize=2)
    def f(x):
        call_count["count"] += 1
        return x

    f(1)
    f(2)
    f(1)  # 1 を最近使用に
    f(3)  # 2 が追い出される
    assert f.cache_info()["size"] == 2
    assert call_count["count"] == 3
    f(1)
    f(3)
    assert call_count["count"] == 3
    f(2)  # キャッシュミス
    assert call_count["count"] == 4


def test_cache_unhashable_arguments():
    """リストなどハッシュ不可能な引数でもキャッシュできること（reprベースのキー）"""
    call_count = {"count": 0}

    @cache()
    def f(items):
        call_count["count"] += 1
        return sum(items)

    assert f([1, 2, 3]) == 6
    assert f([1, 2, 3]) == 6
    assert call_count["count"] == 1


async def test_cache_async():
    call_count = {"count": 0}

    @cache()
    async def async_function(x):
        call_count["count"] += 1
        return x * 2

    assert await async_function(2) == 4
    assert call_count["count"] == 1

    # キャッシュヒット
    assert await async_function(2) == 4
    assert call_count["count"] == 1

    # 異なる引数はキャッシュミス
    assert await async_function(3) == 6
    assert call_count["count"] == 2

    # クリア後は再計算
    async_function.clear_cache()
    assert await async_function(2) == 4
    assert call_count["count"] == 3
    assert async_function.cache_info()["size"] == 1


async def test_cache_async_with_ttl():
    call_count = {"count": 0}

    @cache(ttl=0.2)
    async def async_function(x):
        call_count["count"] += 1
        return x

    await async_function(1)
    await async_function(1)
    assert call_count["count"] == 1

    await asyncio.sleep(0.3)
    await async_function(1)
    assert call_count["count"] == 2


class DeprecateDecoratorTestCase(unittest.TestCase):
    def test_deprecate_with_version(self):
        """バージョン指定での非推奨警告テスト"""

        @deprecate(version="2.0.0")
        def old_function():
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_function()

            self.assertEqual(result, "old")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("old_function is deprecated", str(w[0].message))
            self.assertIn("version 2.0.0", str(w[0].message))

    def test_deprecate_with_alternative(self):
        """代替関数指定での非推奨警告テスト"""

        @deprecate(alternative="new_function")
        def old_function():
            return "old"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_function()

            self.assertEqual(result, "old")
            self.assertEqual(len(w), 1)
            self.assertIn("Use new_function instead", str(w[0].message))

    def test_deprecate_with_version_and_alternative(self):
        """バージョンと代替関数の両方を指定したテスト"""

        @deprecate(version="3.0.0", alternative="better_function")
        def legacy_function():
            return "legacy"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = legacy_function()

            self.assertEqual(result, "legacy")
            self.assertEqual(len(w), 1)
            self.assertIn("legacy_function is deprecated", str(w[0].message))
            self.assertIn("version 3.0.0", str(w[0].message))
            self.assertIn("Use better_function instead", str(w[0].message))

    def test_deprecate_with_custom_message(self):
        """カスタムメッセージでの非推奨警告テスト"""

        @deprecate(message="この関数は使用しないでください")
        def custom_message_function():
            return "custom"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = custom_message_function()

            self.assertEqual(result, "custom")
            self.assertEqual(len(w), 1)
            self.assertEqual(str(w[0].message), "この関数は使用しないでください")

    def test_deprecate_multiple_calls(self):
        """複数回呼び出した場合のテスト"""

        @deprecate(version="1.0.0")
        def multi_call_function():
            return "result"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            multi_call_function()
            multi_call_function()
            multi_call_function()

            # 3回呼び出したので3回警告が出るはず
            self.assertEqual(len(w), 3)

    def test_deprecate_with_arguments(self):
        """引数を持つ関数での非推奨警告テスト"""

        @deprecate(version="2.0.0", alternative="new_add")
        def old_add(x, y):
            return x + y

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_add(5, 3)

            self.assertEqual(result, 8)
            self.assertEqual(len(w), 1)
            self.assertIn("old_add is deprecated", str(w[0].message))


async def test_deprecate_async():
    @deprecate(version="2.0.0", alternative="new_async_function")
    async def old_async_function():
        return "old"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = await old_async_function()

    assert result == "old"
    assert len(w) == 1
    assert issubclass(w[0].category, DeprecationWarning)
    assert "old_async_function is deprecated" in str(w[0].message)
    assert "version 2.0.0" in str(w[0].message)
    assert "Use new_async_function instead" in str(w[0].message)


# ---------------------------------------------------------------------------
# 新規デコレーターのテスト
# ---------------------------------------------------------------------------


def test_rate_limit_sync():
    period = 0.3

    @rate_limit(calls=2, period=period)
    def limited_function():
        return "called"

    start = time.monotonic()
    limited_function()
    limited_function()
    fast_elapsed = time.monotonic() - start
    # 最初の2回はブロックされない
    assert fast_elapsed < period

    # 3回目は枠が空くまでブロックされる
    limited_function()
    total_elapsed = time.monotonic() - start
    assert total_elapsed >= period


async def test_rate_limit_async():
    period = 0.2

    @rate_limit(calls=1, period=period)
    async def limited_function():
        return "called"

    start = time.monotonic()
    assert await limited_function() == "called"
    assert await limited_function() == "called"
    assert time.monotonic() - start >= period


def test_singleton_returns_same_instance():
    @singleton
    class Config:
        def __init__(self, value=42):
            self.value = value

    a = Config()
    b = Config()
    assert a is b
    assert a.value == 42
    # 2回目以降の引数は無視される（最初のインスタンスを返す）
    c = Config(value=100)
    assert c is a
    assert c.value == 42


def test_singleton_thread_safety():
    init_count = {"count": 0}

    @singleton
    class SlowInit:
        def __init__(self):
            init_count["count"] += 1
            time.sleep(0.05)

    instances = []

    def create():
        instances.append(SlowInit())

    threads = [threading.Thread(target=create) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert init_count["count"] == 1
    assert all(instance is instances[0] for instance in instances)


def test_suppress_errors_returns_default():
    @suppress_errors(default=0)
    def parse_number(text):
        return int(text)

    assert parse_number("123") == 123
    assert parse_number("abc") == 0


def test_suppress_errors_logging():
    logger = LogCapturing()
    with patch(
        "flaretool.decorators.get_logger", return_value=logger
    ) as mock_get_logger:

        @suppress_errors(default="fallback")
        def failing_function():
            raise ValueError("boom")

        assert failing_function() == "fallback"
        assert any("boom" in message for message in logger.log)

    with patch("flaretool.decorators.get_logger") as mock_get_logger:

        @suppress_errors(default=None, log=False)
        def silent_function():
            raise ValueError("quiet")

        assert silent_function() is None
        mock_get_logger.assert_not_called()


def test_suppress_errors_specific_exceptions():
    @suppress_errors(default=-1, exceptions=(ValueError,))
    def failing_function():
        raise KeyError("not suppressed")

    with pytest.raises(KeyError):
        failing_function()


async def test_suppress_errors_async():
    @suppress_errors(default="fallback")
    async def failing_function():
        raise ValueError("async boom")

    @suppress_errors(default="fallback")
    async def ok_function():
        return "ok"

    assert await failing_function() == "fallback"
    assert await ok_function() == "ok"


def test_run_in_thread_returns_future():
    main_thread = threading.current_thread().name

    @run_in_thread
    def background_task(x):
        return x * 2, threading.current_thread().name

    future = background_task(5)
    assert isinstance(future, Future)
    value, thread_name = future.result(timeout=5)
    assert value == 10
    assert thread_name != main_thread
    assert thread_name.startswith("flaretool-run_in_thread")


def test_run_in_thread_propagates_exception():
    @run_in_thread
    def failing_task():
        raise ValueError("thread boom")

    future = failing_task()
    with pytest.raises(ValueError, match="thread boom"):
        future.result(timeout=5)


def test_run_in_thread_rejects_coroutine_function():
    with pytest.raises(TypeError):

        @run_in_thread
        async def async_task():
            return "never"


def test_synchronized_sync_mutual_exclusion():
    counter = {"value": 0}

    @synchronized
    def increment():
        current = counter["value"]
        time.sleep(0.005)
        counter["value"] = current + 1

    threads = [threading.Thread(target=increment) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert counter["value"] == 10


def test_synchronized_sync_is_reentrant():
    @synchronized
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    assert factorial(5) == 120


async def test_synchronized_async_mutual_exclusion():
    state = {"running": 0, "max_running": 0}

    @synchronized
    async def task():
        state["running"] += 1
        state["max_running"] = max(state["max_running"], state["running"])
        await asyncio.sleep(0.02)
        state["running"] -= 1

    await asyncio.gather(task(), task(), task())
    assert state["max_running"] == 1

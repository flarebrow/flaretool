from time import sleep
import time
import unittest
import warnings
from unittest.mock import MagicMock
from unittest.mock import patch

from flaretool.errors import FlareToolNetworkError
from flaretool.decorators import *


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


class NetworkRequiredDecoratorTests(unittest.TestCase):

    @network_required
    def my_function(self):
        return "Success"

    def test_network_required_decorator_with_network_connection(self):
        # ネットワーク接続が確立されている場合のテスト
        with patch('socket.create_connection') as mock_create_connection:
            # モックの振る舞いを設定
            mock_create_connection.return_value = None
            # デコレートされた関数を呼び出してテスト
            result = self.my_function()
            self.assertEqual(result, "Success")
            # socket.create_connectionが呼ばれたことを検証
            mock_create_connection.assert_called_with(
                ("google.com", 443), timeout=5)

    def test_network_required_decorator_without_network_connection(self):
        # ネットワーク接続が確立されていない場合のテスト
        with patch('socket.create_connection') as mock_create_connection:
            # モックの振る舞いを設定
            mock_create_connection.side_effect = OSError
            # デコレートされた関数を呼び出して例外の発生を検証
            with self.assertRaises(FlareToolNetworkError):
                self.my_function()
            # socket.create_connectionが呼ばれたことを検証
            mock_create_connection.assert_called_with(
                ("google.com", 443), timeout=5)


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

        with patch('logging.getLogger') as mock_logger:
            mock_logger.return_value = self.logger

            with self.assertRaises(ValueError):
                failure_function()

            self.assertIn(
                "Error occurred: Always fails. Retrying in 0 second(s).", self.logger.log)
            self.assertIn("Max attempts reached. Giving up.", self.logger.log)


# class RetryDecoratorTestCase(unittest.TestCase):

#     # テスト用のダミー関数
#     def always_fail(self):
#         raise ValueError("Always fails")

#     @retry()
#     def retry_function(self):
#         return "Success"

#     @retry()
#     def retry_function2(self):
#         self.always_fail()

#     def test_retry_success(self):
#         result = self.retry_function()
#         self.assertEqual(result, "Success")

#     def test_retry_failure(self):
#         with self.assertRaises(ValueError):
#             self.retry_function2()

#     def test_error_logging(self):
#         with patch('logging.getLogger') as mock_logger:
#             mock_logger.return_value = self.logger

#             with self.assertRaises(ValueError):
#                 self.retry_function2()

#             self.assertIn(
#                 "Error occurred: Always fails. Retrying in 1 second(s).", self.logger.log)
#             self.assertIn("Max attempts reached. Giving up.", self.logger.log)


    def setUp(self):
        self.logger = LogCapturing()

    def tearDown(self):
        self.logger.reset()


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
        with patch('logging.getLogger') as mock_logger:
            mock_logger.return_value = self.logger
            mock_func = MagicMock(
                side_effect=[self.mock_function, StopIteration("Stop the loop")])

            # テスト対象の関数とデコレーターの組み合わせを作成します
            @repeat(5, 3)
            def test_function():
                mock_func()

            # テスト関数を呼び出します
            test_function()

            self.assertEqual(mock_func.call_count, 2)

            self.assertIn("Stop the loop", self.logger.log)


class LogCapturing:
    def __init__(self):
        self.log = []

    def error(self, message):
        self.log.append(message)

    def reset(self):
        self.log = []


class TestTimeoutDecorator(unittest.TestCase):

    def test_timeout_success(self):
        """
        Test the `timeout` decorator with a function that completes within the timeout period.
        """
        @timeout(2)
        def quick_function():
            time.sleep(1)
            return "Completed"

        result = quick_function()
        self.assertEqual(result, "Completed")

    def test_timeout_failure(self):
        """
        Test the `timeout` decorator with a function that exceeds the timeout period.
        """
        @timeout(2)
        def slow_function():
            time.sleep(5)
            return "Should not reach here"

        with self.assertRaises(TimeoutError):
            slow_function()

    def test_timeout_exception(self):
        """
        Test the `timeout` decorator with a function that raises an exception.
        """
        @timeout(2)
        def function_with_exception():
            time.sleep(1)
            raise ValueError("An error occurred")

        with self.assertRaises(ValueError):
            function_with_exception()


class TimerDecoratorTestCase(unittest.TestCase):
    def test_timer_decorator(self):
        # Mock function that takes some time to execute
        @timer
        def long_running_function():
            time.sleep(2)
            return "Success"

        result = long_running_function()
        self.assertEqual(result, "Success")

    def test_timer_decorator_with_mock_logger(self):
        # Mock function that takes some time to execute
        @timer
        def long_running_function():
            time.sleep(2)
            return "Success"

        with patch('flaretool.decorators.get_logger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            result = long_running_function()
            self.assertEqual(result, "Success")

            self.assertIn("long_running_function took",
                          mock_logger.debug.call_args[0][0])
            self.assertIn("seconds to execute.",
                          mock_logger.debug.call_args[0][0])


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

        @cache(ttl=1)
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
        time.sleep(1.1)
        result3 = timed_function(5)
        self.assertEqual(result3, 10)
        self.assertEqual(call_count["count"], 2)

    def test_cache_with_maxsize(self):
        """maxsizeのテスト（LRU動作確認）"""
        call_count = {"count": 0}

        @cache(maxsize=2)
        def limited_cache_function(x):
            call_count["count"] += 1
            return x ** 2

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
        with patch('flaretool.decorators.inspect.signature') as mock_signature:
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

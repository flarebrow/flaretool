from time import sleep
import time
import unittest
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

import unittest
from unittest.mock import patch

from flaretool.errors import FlareToolNetworkError
from flaretool.decorators import *


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

    # テスト用のダミー関数
    def always_fail(self):
        raise ValueError("Always fails")

    @retry(max_attempts=3, delay=1)
    def retry_function(self):
        return "Success"

    @retry(max_attempts=2, delay=1)
    def retry_function2(self):
        self.always_fail()

    def test_retry_success(self):
        result = self.retry_function()
        self.assertEqual(result, "Success")

    def test_retry_failure(self):
        with self.assertRaises(ValueError):
            self.retry_function2()

    def test_error_logging(self):
        with patch('logging.getLogger') as mock_logger:
            mock_logger.return_value = self.logger

            with self.assertRaises(ValueError):
                self.retry_function2()

            self.assertIn(
                "Error occurred: Always fails. Retrying in 1 second(s).", self.logger.log)
            self.assertIn("Max attempts reached. Giving up.", self.logger.log)

    def setUp(self):
        self.logger = LogCapturing()

    def tearDown(self):
        self.logger.reset()


class LogCapturing:
    def __init__(self):
        self.log = []

    def error(self, message):
        self.log.append(message)

    def reset(self):
        self.log = []

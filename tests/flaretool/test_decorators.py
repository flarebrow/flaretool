import unittest
from unittest.mock import patch

from flaretool.error import FlareToolNetworkError
from flaretool.decorators import network_required


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

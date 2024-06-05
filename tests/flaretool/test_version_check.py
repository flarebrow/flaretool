import os
import unittest
from unittest.mock import patch
from flaretool import *

import unittest
from unittest.mock import patch, MagicMock
import warnings

# この部分にテスト対象の関数やクラスをインポートする必要があります


class TestVersionCheck(unittest.TestCase):
    @patch('flaretool.common.requests.get')
    def test_check_version_newer_version(self, mock_get):
        # モックリクエストの設定
        mock_response = {
            "info": {
                "version": "99.99.99"
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # テスト対象の関数を呼び出す
        with warnings.catch_warnings(record=True) as warning_list:
            check_version()

        self.assertEqual(len(warning_list), 1)
        self.assertTrue(issubclass(warning_list[0].category, Warning))

    @patch('flaretool.common.requests.get')
    def test_check_version_same_version(self, mock_get):
        # モックリクエストの設定
        mock_response = {
            "info": {
                "version": get_lib_version()
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # テスト対象の関数を呼び出す
        with warnings.catch_warnings(record=True) as warning_list:
            check_version()

        self.assertEqual(len(warning_list), 0)

    @patch('flaretool.common.requests.get')
    def test_check_version_exception(self, mock_get):
        # モックリクエストを例外を起こすように設定
        mock_get.side_effect = Exception("Mocked exception")

        # テスト対象の関数を呼び出す
        with warnings.catch_warnings(record=True) as warning_list:
            check_version()

        self.assertEqual(len(warning_list), 0)

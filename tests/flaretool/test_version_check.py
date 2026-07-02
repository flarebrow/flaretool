import unittest
import warnings
from unittest.mock import patch

from flaretool import *


class TestVersionCheck(unittest.TestCase):
    # check_version() はインポート時には実行されない(明示的な呼び出しが必要)

    @patch("requests.get")
    def test_check_version_newer_version(self, mock_get):
        # モックリクエストの設定
        mock_response = {"info": {"version": "99.99.99"}}
        mock_get.return_value.json.return_value = mock_response

        # テスト対象の関数を呼び出す
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            check_version()

        self.assertEqual(len(warning_list), 1)
        self.assertTrue(issubclass(warning_list[0].category, Warning))
        # 警告メッセージに新旧両方のバージョンが含まれること
        message = str(warning_list[0].message)
        self.assertIn("99.99.99", message)
        self.assertIn(get_lib_version(), message)

    @patch("requests.get")
    def test_check_version_same_version(self, mock_get):
        # モックリクエストの設定
        mock_response = {"info": {"version": get_lib_version()}}
        mock_get.return_value.json.return_value = mock_response

        # テスト対象の関数を呼び出す
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            check_version()

        self.assertEqual(len(warning_list), 0)

    @patch("requests.get")
    def test_check_version_exception(self, mock_get):
        # モックリクエストを例外を起こすように設定
        mock_get.side_effect = Exception("Mocked exception")

        # テスト対象の関数を呼び出す(get_latest_versionが現行版へフォールバック)
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            check_version()

        self.assertEqual(len(warning_list), 0)

    @patch("requests.get")
    def test_get_latest_version_fallback(self, mock_get):
        mock_get.side_effect = Exception("Mocked exception")
        self.assertEqual(get_latest_version(), get_lib_version())

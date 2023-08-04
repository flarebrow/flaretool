import unittest
from unittest.mock import patch, MagicMock
from flaretool.common import *
from flaretool.logger import Logger
from logging import DEBUG


class RequestsTestCase(unittest.TestCase):

    @patch('flaretool.logger.get_logger')
    def setUp(self, mock_get_logger):
        self.logger = Logger(__name__, DEBUG)
        mock_get_logger.return_value = self.logger
        self.requests_patcher = patch('flaretool.common.req')
        self.mock_requests = self.requests_patcher.start()
        self.mock_requests.Session.return_value = self.mock_requests
        response = MagicMock()
        response.status_code = 200
        self.mock_requests.request.return_value = response
        self.mock_requests.__enter__.return_value.request.return_value = response

        platform = MagicMock()
        platform.system.return_value = 'TestOS'
        platform.python_version.return_value = 'TestPythonVersion'
        platform.platform.return_value = 'TestPlatform'
        self.mock_platform = patch('flaretool.common.platform', platform)
        self.mock_platform.start()

        ua = {
            "Mozilla": "5.0",
            "publisher": flaretool.__name__,
            "flaretool": flaretool.VERSION,
            "lang_version": "TestPythonVersion",
            "os": "TestOS",
            "platform": "TestPlatform",
        }
        user_agent = " ".join([f"{key}/{value}" for key, value in ua.items()])
        self.headers = {
            'User-Agent': user_agent,
            'X-UA': user_agent,
        }

    def tearDown(self):
        self.requests_patcher.stop()
        self.mock_platform.stop()

    @patch('flaretool.api_key', "test")
    def test_request(self):
        # テスト用のダミーデータとしてURLとパラメータを設定します
        url = "https://flarebrow.com"
        params = {"key": "value"}

        # requestメソッドをテストします
        response = requests.request("GET", url, params=params)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        headers = self.headers
        headers["X-FLAREBROW-AUTH"] = "test"

       # モックされたrequestsクラスのrequestメソッドが正しく呼び出されたことを確認します
        self.mock_requests.__enter__.return_value.request.assert_called_with(
            method="GET",
            url=url,
            headers=headers,
            params=params
        )

    def test_requests_403(self):
        response = MagicMock()
        response.status_code = 403
        self.mock_requests.request.return_value = response
        self.mock_requests.__enter__.return_value.request.return_value = response
        url = "https://example.flarebrow.com"
        params = {"key": "value"}

        with self.assertRaises(FlareToolNetworkError) as e:
            response = requests.request("GET", url, params=params)
            self.assertEqual(e.exception.message,
                             "Only access from Japan is accepted")

    def test_get(self):
        # テスト用のダミーデータとしてURLを設定します
        url = "https://example.com"

        # getメソッドをテストします
        response = requests.get(url)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_requests.__enter__.return_value.request.assert_called_with(
            method="GET",
            url=url,
            headers=self.headers,
        )

    def test_post(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"
        data = {"key": "value"}

        # postメソッドをテストします
        response = requests.post(url, data=data)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_requests.__enter__.return_value.request.assert_called_with(
            method="POST",
            url=url,
            headers=self.headers,
            data=data,
        )

    def test_put(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"
        data = {"key": "value"}

        # putメソッドをテストします
        response = requests.put(url, data=data)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_requests.__enter__.return_value.request.assert_called_with(
            method="PUT",
            url=url,
            headers=self.headers,
            data=data,
        )

    def test_delete(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"
        data = {"key": "value"}

        # deleteメソッドをテストします
        response = requests.delete(url, data=data)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_requests.__enter__.return_value.request.assert_called_with(
            method="DELETE",
            url=url,
            headers=self.headers,
            data=data,
        )

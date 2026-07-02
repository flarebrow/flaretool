import unittest
from unittest.mock import MagicMock, patch

import flaretool
from flaretool.common import _USER_AGENT, DEFAULT_TIMEOUT, requests
from flaretool.errors import FlareToolNetworkError


class RequestsTestCase(unittest.TestCase):
    def setUp(self):
        # Patch the shared session used by flaretool.common.requests.
        self.session_patcher = patch("flaretool.common._session", MagicMock())
        self.mock_session = self.session_patcher.start()
        response = MagicMock()
        response.status_code = 200
        self.mock_session.request.return_value = response

        # User-Agentはプロセス起動時に一度だけ構築されるモジュール定数
        self.headers = {
            "User-Agent": _USER_AGENT,
            "X-UA": _USER_AGENT,
        }

    def tearDown(self):
        self.session_patcher.stop()

    @patch("flaretool.api_key", "test")
    def test_request(self):
        # テスト用のダミーデータとしてURLとパラメータを設定します
        url = "https://flarebrow.com"
        params = {"key": "value"}

        # requestメソッドをテストします
        response = requests.request("GET", url, params=params, auth_enabled=True)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        headers = self.headers
        headers["X-FLAREBROW-AUTH"] = "test"
        headers["Authorization"] = "Bearer test"
        params["apikey"] = "test"

        # 共有セッションのrequestメソッドが正しく呼び出されたことを確認します
        self.mock_session.request.assert_called_with(
            method="GET",
            url=url,
            headers=headers,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_request_custom_timeout(self):
        # 呼び出し側が指定したtimeoutが優先されることを確認します
        url = "https://example.com"
        requests.request("GET", url, timeout=1)

        self.mock_session.request.assert_called_with(
            method="GET",
            url=url,
            headers=self.headers,
            timeout=1,
        )

    def test_requests_403(self):
        response = MagicMock()
        response.status_code = 403
        self.mock_session.request.return_value = response
        url = "https://example.flarebrow.com"
        params = {"key": "value"}

        with self.assertRaises(FlareToolNetworkError) as e:
            requests.request("GET", url, params=params, auth_enabled=True)
        self.assertEqual(e.exception.message, "Only access from Japan is accepted")

    def test_get(self):
        # テスト用のダミーデータとしてURLを設定します
        url = "https://example.com"

        # getメソッドをテストします
        response = requests.get(url)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_session.request.assert_called_with(
            method="GET",
            url=url,
            headers=self.headers,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_post(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"
        data = {"key": "value"}

        # postメソッドをテストします
        response = requests.post(url, data=data)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_session.request.assert_called_with(
            method="POST",
            url=url,
            headers=self.headers,
            data=data,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_put(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"
        data = {"key": "value"}

        # putメソッドをテストします
        response = requests.put(url, data=data)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_session.request.assert_called_with(
            method="PUT",
            url=url,
            headers=self.headers,
            data=data,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_delete(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"
        data = {"key": "value"}

        # deleteメソッドをテストします
        response = requests.delete(url, data=data)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_session.request.assert_called_with(
            method="DELETE",
            url=url,
            headers=self.headers,
            data=data,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_head(self):
        # テスト用のダミーデータとしてURLとデータを設定します
        url = "https://example.com"

        # headメソッドをテストします
        response = requests.head(url)

        # レスポンスのステータスコードが正常であることを確認します
        self.assertEqual(response.status_code, 200)

        self.mock_session.request.assert_called_with(
            method="HEAD",
            url=url,
            headers=self.headers,
            allow_redirects=False,
            timeout=DEFAULT_TIMEOUT,
        )

    def test_verbs_route_through_request(self):
        # 互換性の要: 各verbヘルパーは requests.request を経由するため、
        # `flaretool.common.requests.request` のパッチで全て捕捉できること
        with patch("flaretool.common.requests.request") as mock_request:
            requests.get("https://example.com")
            mock_request.assert_called_once_with("GET", "https://example.com")
            requests.head("https://example.com")
            mock_request.assert_called_with(
                "HEAD", "https://example.com", allow_redirects=False
            )


class UserAgentTestCase(unittest.TestCase):
    def test_user_agent_contains_library_metadata(self):
        # User-Agent定数にライブラリ名とバージョンが含まれること
        self.assertIn("Mozilla/5.0", _USER_AGENT)
        self.assertIn(f"publisher/{flaretool.__name__}", _USER_AGENT)
        self.assertIn(f"flaretool/{flaretool.__version__}", _USER_AGENT)


class SharedSessionTestCase(unittest.TestCase):
    def test_get_session_is_shared(self):
        import flaretool.common as common

        original = common._session
        try:
            common._session = None
            first = common._get_session()
            second = common._get_session()
            self.assertIs(first, second)
        finally:
            common._session = original

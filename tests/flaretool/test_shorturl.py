import unittest
from datetime import datetime
from unittest.mock import patch

import flaretool
from flaretool.errors import AuthenticationError
from flaretool.shorturl import ShortUrlService
from flaretool.shorturl.errors import (
    ShortUrlAuthenticationError,
    ShortUrlDataUpdateError,
    ShortUrlError,
    ShortUrlValidError,
)
from flaretool.shorturl.models import ShortUrlInfo


class ShortUrlServiceTest(unittest.TestCase):
    def setUp(self):
        flaretool.api_key = "API_KEY"
        self.service = ShortUrlService()

    def test_init_no_api_key(self):
        flaretool.api_key = None
        with self.assertRaises(AuthenticationError):
            self.service.__init__()

    def test_init_with_api_key(self):
        flaretool.api_key = "API_KEY"
        self.service.__init__()

    @patch("flaretool.common.requests.request")
    def test_send_request_401_error(self, mock_requests):
        mock_requests.return_value.status_code = 401
        mock_requests.return_value.json.return_value = {
            "response": 401,
            "message": "Authentication failed",
        }
        with self.assertRaises(ShortUrlAuthenticationError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_409_error(self, mock_requests):
        mock_requests.return_value.status_code = 409
        mock_requests.return_value.json.return_value = {
            "response": 409,
            "message": "Authentication failed",
        }
        with self.assertRaises(ShortUrlDataUpdateError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_422_errors(self, mock_requests):
        mock_requests.return_value.status_code = 422
        mock_requests.return_value.json.return_value = {
            "response": 422,
            "message": "Internal server error",
            "detail": [{"msg": "Invalid data"}],
        }
        with self.assertRaises(ShortUrlValidError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_other_errors(self, mock_requests):
        mock_requests.return_value.status_code = 500
        mock_requests.return_value.json.return_value = {
            "response": 500,
            "message": "Internal server error",
        }
        with self.assertRaises(ShortUrlError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_get_short_url_info_list(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": [
                {
                    "id": 1,
                    "url": "https://example.com",
                    "title": "Example",
                    "code": "abcd",
                    "owner": "owner",
                    "is_active": False,
                    "is_eternal": False,
                    "limited_at": "2023-06-20T12:00:00",
                    "created_at": "2023-06-10T12:00:00",
                    "updated_at": "2023-06-10T12:00:00",
                    "short_url": "https://example.com/abcd",
                    "qr_url": "https://example.com/qrcode",
                },
                {
                    "id": 2,
                    "url": "https://example.org",
                    "title": "Example.org",
                    "code": "efgh",
                    "owner": "owner",
                    "is_active": True,
                    "is_eternal": False,
                    "limited_at": "2023-06-20T12:00:00",
                    "created_at": "2023-06-11T12:00:00",
                    "updated_at": "2023-06-10T12:00:00",
                    "short_url": "https://example.com/efgh",
                    "qr_url": "https://example.com/qrcode",
                },
            ],
        }

        service = ShortUrlService()
        result = service.get()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ShortUrlInfo)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].url, "https://example.com")
        self.assertEqual(result[0].title, "Example")
        self.assertEqual(result[0].code, "abcd")
        self.assertEqual(result[0].is_active, False)
        self.assertEqual(
            result[0].created_at, datetime.fromisoformat("2023-06-10T12:00:00")
        )
        self.assertEqual(
            result[0].limited_at, datetime.fromisoformat("2023-06-20T12:00:00")
        )
        self.assertEqual(result[0].short_url, "https://example.com/abcd")

        self.assertIsInstance(result[1], ShortUrlInfo)
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].url, "https://example.org")
        self.assertEqual(result[1].title, "Example.org")
        self.assertEqual(result[1].code, "efgh")
        self.assertEqual(result[1].is_active, True)
        self.assertEqual(
            result[1].created_at, datetime.fromisoformat("2023-06-11T12:00:00")
        )
        self.assertEqual(
            result[1].limited_at, datetime.fromisoformat("2023-06-20T12:00:00")
        )
        self.assertEqual(result[1].short_url, "https://example.com/efgh")

    @patch("flaretool.common.requests.request")
    def test_create_short_url(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": {
                "id": 1,
                "url": "https://example.com",
                "title": "Example",
                "code": "abcd",
                "type": "type",
                "owner": "owner",
                "is_active": True,
                "is_eternal": False,
                "limited_at": None,
                "created_at": "2023-06-10T12:00:00",
                "updated_at": "2023-06-20 12:00:00",
                "short_url": "https://example.com/abcd",
                "qr_url": "https://example.com/abcd/qr",
            },
        }

        service = ShortUrlService()
        result = service.create("https://example.com")

        self.assertIsInstance(result, ShortUrlInfo)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.title, "Example")
        self.assertEqual(result.code, "abcd")
        self.assertEqual(result.is_active, True)
        self.assertEqual(result.limited_at, None)
        self.assertEqual(
            result.created_at, datetime.fromisoformat("2023-06-10T12:00:00")
        )
        self.assertEqual(
            result.updated_at, datetime.fromisoformat("2023-06-20T12:00:00")
        )
        self.assertEqual(result.short_url, "https://example.com/abcd")
        self.assertEqual(result.qr_url, "https://example.com/abcd/qr")

    @patch("flaretool.common.requests.request")
    def test_create_short_url_sends_false_flags(self, mock_request):
        # is_eternal=False / is_active=False が省略されずに送信されることを検証
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": {
                "id": 1,
                "url": "https://example.com",
                "title": "Example",
                "code": "abcd",
                "owner": "owner",
                "is_active": False,
                "is_eternal": False,
                "limited_at": None,
                "created_at": "2023-06-10T12:00:00",
                "updated_at": "2023-06-10T12:00:00",
                "short_url": "https://example.com/abcd",
                "qr_url": "https://example.com/abcd/qr",
            },
        }

        service = ShortUrlService()
        service.create("https://example.com", is_eternal=False, is_active=False)

        _, kwargs = mock_request.call_args
        self.assertEqual(
            kwargs["json"],
            {
                "url": "https://example.com",
                "is_eternal": False,
                "is_active": False,
            },
        )

    def test_encode_url_for_api_is_idempotent(self):
        # ハイフンは%2Dにエンコードされ、二重適用しても二重エンコードされない
        from flaretool.shorturl.ShortUrlService import _encode_url_for_api

        encoded = _encode_url_for_api("https://example.com/foo-bar")
        self.assertEqual(encoded, "https://example.com/foo%2Dbar")
        self.assertEqual(_encode_url_for_api(encoded), encoded)

    @patch("flaretool.common.requests.request")
    def test_create_short_url_encodes_hyphen(self, mock_request):
        # create() はサーバー仕様に合わせてURL中のハイフンを%2Dエンコードして送信する
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": {
                "id": 1,
                "url": "https://example.com/foo-bar",
                "title": "Example",
                "code": "abcd",
                "owner": "owner",
                "is_active": True,
                "is_eternal": False,
                "limited_at": None,
                "created_at": "2023-06-10T12:00:00",
                "updated_at": "2023-06-10T12:00:00",
                "short_url": "https://example.com/abcd",
                "qr_url": "https://example.com/abcd/qr",
            },
        }

        service = ShortUrlService()
        service.create("https://example.com/foo-bar")

        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["json"]["url"], "https://example.com/foo%2Dbar")

    @patch("flaretool.common.requests.request")
    def test_update_short_url_encodes_hyphen(self, mock_request):
        # update() も create() と同様にURL中のハイフンを%2Dエンコードして送信する
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": {
                "id": 1,
                "url": "https://example.com/foo-bar",
                "title": "Example",
                "code": "abcd",
                "owner": "owner",
                "is_active": True,
                "is_eternal": False,
                "limited_at": None,
                "created_at": "2023-06-10T12:00:00",
                "updated_at": "2023-06-10T12:00:00",
                "short_url": "https://example.com/abcd",
                "qr_url": "https://example.com/abcd/qr",
            },
        }

        service = ShortUrlService()
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com/foo-bar",
            title="Example",
            code="abcd",
            owner="owner",
            is_active=True,
            is_eternal=False,
            limited_at=None,
            created_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            updated_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            short_url="https://example.com/abcd",
            qr_url="https://example.com/abcd/qr",
        )
        service.update(url_info)

        _, kwargs = mock_request.call_args
        payload = kwargs["json"]
        self.assertEqual(payload["url"], "https://example.com/foo%2Dbar")
        # 除外フィールドは送信されない（既存仕様の維持）
        for excluded in ("limited_at", "updated_at", "created_at"):
            self.assertNotIn(excluded, payload)

    def test_qr_url_is_derived_from_short_url(self):
        # qr_url は常に short_url から導出される
        info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            owner="owner",
            is_active=False,
            is_eternal=False,
            created_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            updated_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            short_url="https://example.com/abcd/",
            qr_url="https://example.com/qrcode",
        )
        self.assertEqual(info.qr_url, "https://example.com/abcd/qr")

    def test_qr_url_none_when_short_url_missing(self):
        # short_url がない場合、qr_url は "None/qr" ではなく None になる
        info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            owner="owner",
            is_active=False,
            is_eternal=False,
            created_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            updated_at=datetime.fromisoformat("2023-06-10T12:00:00"),
        )
        self.assertIsNone(info.short_url)
        self.assertIsNone(info.qr_url)

    @patch("flaretool.common.requests.request")
    def test_update_short_url(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": {
                "id": 1,
                "url": "https://example.com",
                "title": "Example Updated",
                "code": "efgh",
                "owner": "owner",
                "is_active": True,
                "is_eternal": False,
                "limited_at": "2023-06-20T12:00:00",
                "created_at": "2023-06-10T12:00:00",
                "updated_at": "2023-06-20T12:00:00",
                "short_url": "https://example.com/efgh",
                "qr_url": "https://example.com/efgh/qr",
            },
        }

        service = ShortUrlService()
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            owner="owner",
            is_active=False,
            is_eternal=False,
            limited_at=datetime.fromisoformat("2023-06-20T12:00:00"),
            created_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            updated_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            short_url="https://example.com/abcd",
            qr_url="https://example.com/qrcode",
        )
        result = service.update(url_info)
        result_diff = url_info - result
        self.assertEqual(result_diff["title"], "Example Updated")
        self.assertEqual(result_diff["code"], "efgh")
        self.assertEqual(result_diff["is_active"], True)
        self.assertEqual(result_diff["short_url"], "https://example.com/efgh")

        self.assertIsInstance(result, ShortUrlInfo)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.title, "Example Updated")
        self.assertEqual(result.code, "efgh")
        self.assertEqual(result.is_active, True)
        self.assertEqual(
            result.updated_at, datetime.fromisoformat("2023-06-20T12:00:00")
        )
        self.assertEqual(result.short_url, "https://example.com/efgh")
        self.assertEqual(result.qr_url, "https://example.com/efgh/qr")

    @patch("flaretool.common.requests.request")
    def test_delete_short_url(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "response": 200,
            "result": [],
        }

        service = ShortUrlService()
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            owner="owner",
            is_active=False,
            is_eternal=False,
            limited_at=None,
            created_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            updated_at=datetime.fromisoformat("2023-06-20T12:00:00"),
            short_url="https://example.com/abcd",
            qr_url="https://example.com/qrcode",
        )
        result = service.delete(url_info)
        self.assertIsNone(result)

    def test_get_qr_code_raw_data(self):
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            owner="owner",
            is_active=False,
            is_eternal=False,
            limited_at=None,
            created_at=datetime.fromisoformat("2023-06-10T12:00:00"),
            updated_at=datetime.fromisoformat("2023-06-20T12:00:00"),
            short_url="https://example.com/abcd",
            qr_url="https://example.com/qrcode",
        )
        service = ShortUrlService()
        service.get_qr_code_raw_data(url_info)

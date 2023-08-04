import unittest
from unittest.mock import patch
from datetime import datetime
import flaretool
from flaretool.errors import AuthenticationError
from flaretool.shorturl.errors import (
    ShortUrlError,
    ShortUrlAuthenticationError,
    ShortUrlDataUpdateError,
)
from flaretool.shorturl.models import ShortUrlInfo
from flaretool.shorturl import ShortUrlService


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
            "response": 401, "message": "Authentication failed"
        }
        with self.assertRaises(ShortUrlAuthenticationError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_409_error(self, mock_requests):
        mock_requests.return_value.status_code = 409
        mock_requests.return_value.json.return_value = {
            "response": 409, "message": "Authentication failed"
        }
        with self.assertRaises(ShortUrlDataUpdateError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_other_errors(self, mock_requests):
        mock_requests.return_value.status_code = 500
        mock_requests.return_value.json.return_value = {
            "response": 500, "message": "Internal server error"
        }
        with self.assertRaises(ShortUrlError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_get_short_url_info_list(self, mock_request):
        mock_request.return_value.json.return_value = {
            "response": 200,
            "data": [
                {
                    "id": 1,
                    "url": "https://example.com",
                    "title": "Example",
                    "code": "abcd",
                    "disabled": False,
                    "insert_time": "2023-06-10T12:00:00",
                    "limit_time": "2023-06-20 12:00:00",
                    "link": "https://example.com/abcd",
                    "qr_url": "https://example.com/qrcode",
                },
                {
                    "id": 2,
                    "url": "https://example.org",
                    "title": "Example.org",
                    "code": "efgh",
                    "disabled": True,
                    "insert_time": "2023-06-11T12:00:00",
                    "limit_time": "2023-06-20 12:00:00",
                    "link": "https://example.com/efgh",
                    "qr_url": "https://example.com/qrcode",
                },
            ],
        }

        service = ShortUrlService()
        result = service.get_short_url_info_list()

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], ShortUrlInfo)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].url, "https://example.com")
        self.assertEqual(result[0].title, "Example")
        self.assertEqual(result[0].code, "abcd")
        self.assertEqual(result[0].disabled, False)
        self.assertEqual(result[0].insert_time,
                         datetime.fromisoformat("2023-06-10T12:00:00"))
        self.assertEqual(result[0].limit_time,
                         datetime.fromisoformat("2023-06-20T12:00:00"))
        self.assertEqual(result[0].link, "https://example.com/abcd")

        self.assertIsInstance(result[1], ShortUrlInfo)
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].url, "https://example.org")
        self.assertEqual(result[1].title, "Example.org")
        self.assertEqual(result[1].code, "efgh")
        self.assertEqual(result[1].disabled, True)
        self.assertEqual(result[1].insert_time,
                         datetime.fromisoformat("2023-06-11T12:00:00"))
        self.assertEqual(result[1].limit_time,
                         datetime.fromisoformat("2023-06-20T12:00:00"))
        self.assertEqual(result[1].link, "https://example.com/efgh")

    @patch("flaretool.common.requests.request")
    def test_create_short_url(self, mock_request):
        mock_request.return_value.json.return_value = {
            "response": 200,
            "data": [
                {
                    "id": 1,
                    "url": "https://example.com",
                    "title": "Example",
                    "code": "abcd",
                    "disabled": False,
                    "insert_time": "2023-06-10T12:00:00",
                    "limit_time": "2023-06-20 12:00:00",
                    "link": "https://example.com/abcd",
                    "qr_url": "https://example.com/qrcode",
                }
            ],
        }

        service = ShortUrlService()
        result = service.create_short_url("https://example.com")

        self.assertIsInstance(result, ShortUrlInfo)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.title, "Example")
        self.assertEqual(result.code, "abcd")
        self.assertEqual(result.disabled, False)
        self.assertEqual(result.insert_time,
                         datetime.fromisoformat("2023-06-10T12:00:00"))
        self.assertEqual(result.limit_time,
                         datetime.fromisoformat("2023-06-20T12:00:00"))
        self.assertEqual(result.link, "https://example.com/abcd")
        self.assertEqual(result.qr_url, "https://example.com/qrcode")

    @patch("flaretool.common.requests.request")
    def test_update_short_url(self, mock_request):
        mock_request.return_value.json.return_value = {
            "response": 200,
            "data": {
                "before": [
                    {
                        "id": 1,
                        "url": "https://example.com",
                        "title": "Example",
                        "code": "abcd",
                        "disabled": False,
                        "insert_time": "2023-06-10T12:00:00",
                        "limit_time": "2023-06-20 12:00:00",
                        "link": "https://example.com/abcd",
                        "qr_url": "https://example.com/qrcode",
                    }
                ],
                "after": [
                    {
                        "id": 1,
                        "url": "https://example.org",
                        "title": "Example Updated",
                        "code": "efgh",
                        "disabled": True,
                        "insert_time": "2023-06-11T12:00:00",
                        "limit_time": "2023-06-20 12:00:00",
                        "link": "https://example.com/efgh",
                        "qr_url": "https://example.com/qrcode",
                    }
                ],
            },
        }

        service = ShortUrlService()
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            disabled=False,
            insert_time=datetime.fromisoformat("2023-06-10T12:00:00"),
            limit_time=datetime.fromisoformat("2023-06-20T12:00:00"),
            link="https://example.com/abcd",
            qr_url="https://example.com/qrcode",
        )
        result = service.update_short_url(url_info)
        result_diff = url_info - result
        self.assertEqual(result_diff["title"], "Example Updated")
        self.assertEqual(result_diff["code"], "efgh")
        self.assertEqual(result_diff["disabled"], True)
        self.assertEqual(result_diff["insert_time"],
                         datetime.fromisoformat("2023-06-11T12:00:00"))
        self.assertEqual(result_diff["link"], "https://example.com/efgh")

        self.assertIsInstance(result, ShortUrlInfo)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.url, "https://example.org")
        self.assertEqual(result.title, "Example Updated")
        self.assertEqual(result.code, "efgh")
        self.assertEqual(result.disabled, True)
        self.assertEqual(result.insert_time,
                         datetime.fromisoformat("2023-06-11T12:00:00"))
        self.assertEqual(result.limit_time,
                         datetime.fromisoformat("2023-06-20T12:00:00"))
        self.assertEqual(result.link, "https://example.com/efgh")
        self.assertEqual(result.qr_url, "https://example.com/qrcode")

    @patch("flaretool.common.requests.request")
    def test_delete_short_url(self, mock_request):
        mock_request.return_value.json.return_value = {
            "response": 200,
            "data": [
                {
                    "id": 1,
                    "url": "https://example.com",
                    "title": "Example",
                    "code": "abcd",
                    "disabled": False,
                    "insert_time": "2023-06-10T12:00:00",
                    "limit_time": "2023-06-20 12:00:00",
                    "link": "https://example.com/abcd",
                    "qr_url": "https://example.com/qrcode",
                }
            ],
        }

        service = ShortUrlService()
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            disabled=False,
            insert_time=datetime.fromisoformat("2023-06-10T12:00:00"),
            limit_time=datetime.fromisoformat("2023-06-20T12:00:00"),
            link="https://example.com/abcd",
            qr_url="https://example.com/qrcode",
        )
        result = service.delete_short_url(url_info)

        self.assertIsInstance(result, ShortUrlInfo)
        self.assertEqual(result.id, 1)
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.title, "Example")
        self.assertEqual(result.code, "abcd")
        self.assertEqual(result.disabled, False)
        self.assertEqual(result.insert_time,
                         datetime.fromisoformat("2023-06-10T12:00:00"))
        self.assertEqual(result.limit_time,
                         datetime.fromisoformat("2023-06-20T12:00:00"))
        self.assertEqual(result.link, "https://example.com/abcd")

    def test_get_qr_code_raw_data(self):
        url_info = ShortUrlInfo(
            id=1,
            url="https://example.com",
            title="Example",
            code="abcd",
            disabled=False,
            insert_time=datetime.fromisoformat("2023-06-10T12:00:00"),
            limit_time=datetime.fromisoformat("2023-06-20T12:00:00"),
            link="https://example.com/abcd",
            qr_url="https://example.com/qrcode",
        )
        service = ShortUrlService()
        service.get_qr_code_raw_data(url_info)

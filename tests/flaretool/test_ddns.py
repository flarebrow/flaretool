import unittest
from unittest.mock import MagicMock, patch

import flaretool
from flaretool.ddns.errors import DdnsAuthenticationError, DdnsError
from flaretool.ddns.models import DdnsInfo
from flaretool.ddns import DdnsService
from flaretool.errors import AuthenticationError


class DdnsServiceTest(unittest.TestCase):
    def setUp(self):
        flaretool.api_key = "API_KEY"
        self.service = DdnsService()

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
            "result": 401, "status": "Authentication failed",
            "currentIp": None, "updateIp": None, "domain": None,
        }
        with self.assertRaises(DdnsAuthenticationError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_other_errors(self, mock_requests):
        mock_requests.return_value.status_code = 500
        mock_requests.return_value.json.return_value = {
            "result": 500, "status": "Internal server error",
            "currentIp": None, "updateIp": None, "domain": None,
        }
        with self.assertRaises(DdnsError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_success(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {"result": 200, "status": "success",
                                                        "currentIp": "192.168.0.99", "updateIp": "192.168.0.100", "domain": "example.○○○.○○"}

        result = self.service._send_request("get", params={"param": "value"})
        self.assertEqual(result["result"], 200)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["currentIp"], "192.168.0.99")
        self.assertEqual(result["updateIp"], "192.168.0.100")
        self.assertEqual(result["domain"], "example.○○○.○○")

    @patch("flaretool.common.requests.request")
    def test_update_ddns_with_ip(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            "result": 200, "status": "success", "currentIp": "192.168.0.99", "updateIp": "192.168.0.100", "domain": "example.○○○.○○"}
        info = self.service.update_ddns("example", "192.168.0.100")
        self.assertIsInstance(info, DdnsInfo)
        self.assertEqual(info.result, 200)
        self.assertEqual(info.status, "success")
        self.assertEqual(info.currentIp, "192.168.0.99")
        self.assertEqual(info.updateIp, "192.168.0.100")
        self.assertEqual(info.domain, "example.○○○.○○")
        mock_requests.assert_called_once_with("post", "https://api.flarebrow.com/v2/ddns", params={
            "apikey": flaretool.api_key}, data={"host": "example", "ip": "192.168.0.100"})

    @patch("flaretool.common.requests.request")
    def test_update_ddns_without_ip(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            "result": 200, "status": "success", "currentIp": "192.168.0.99", "updateIp": "192.168.0.100", "domain": "example.○○○.○○"}
        info = self.service.update_ddns("example")
        self.assertIsInstance(info, DdnsInfo)
        self.assertEqual(info.result, 200)
        self.assertEqual(info.status, "success")
        self.assertEqual(info.currentIp, "192.168.0.99")
        self.assertEqual(info.updateIp, "192.168.0.100")
        self.assertEqual(info.domain, "example.○○○.○○")
        mock_requests.assert_called_once_with(
            "post", "https://api.flarebrow.com/v2/ddns", params={"apikey": flaretool.api_key}, data={"host": "example"})

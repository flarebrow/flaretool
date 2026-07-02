import importlib
import unittest
import warnings
from unittest.mock import patch

import flaretool
from flaretool.ddns import DdnsService
from flaretool.ddns.errors import DdnsAuthenticationError, DdnsError
from flaretool.ddns.models import DdnsInfo
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
            "result": 401,
            "status": "Authentication failed",
            "currentIp": None,
            "updateIp": None,
            "domain": None,
        }
        with self.assertRaises(DdnsAuthenticationError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_other_errors(self, mock_requests):
        mock_requests.return_value.status_code = 500
        mock_requests.return_value.json.return_value = {
            "result": 500,
            "status": "Internal server error",
            "currentIp": None,
            "updateIp": None,
            "domain": None,
        }
        with self.assertRaises(DdnsError):
            self.service._send_request("get", params={"param": "value"})

    @patch("flaretool.common.requests.request")
    def test_send_request_success(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            "result": 200,
            "status": "success",
            "currentIp": "192.168.0.99",
            "updateIp": "192.168.0.100",
            "domain": "example.○○○.○○",
        }

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
            "result": 200,
            "status": "success",
            "currentIp": "192.168.0.99",
            "updateIp": "192.168.0.100",
            "domain": "example.○○○.○○",
        }
        info = self.service.update_ddns("example", "192.168.0.100")
        self.assertIsInstance(info, DdnsInfo)
        self.assertEqual(info.result, 200)
        self.assertEqual(info.status, "success")
        self.assertEqual(info.currentIp, "192.168.0.99")
        self.assertEqual(info.updateIp, "192.168.0.100")
        self.assertEqual(info.domain, "example.○○○.○○")
        mock_requests.assert_called_once_with(
            "post",
            "https://api.flarebrow.com/v2/ddns",
            params={},
            data={"host": "example", "ip": "192.168.0.100"},
            auth_enabled=True,
        )

    @patch("flaretool.common.requests.request")
    def test_update_ddns_without_ip(self, mock_requests):
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            "result": 200,
            "status": "success",
            "currentIp": "192.168.0.99",
            "updateIp": "192.168.0.100",
            "domain": "example.○○○.○○",
        }
        info = self.service.update_ddns("example")
        self.assertIsInstance(info, DdnsInfo)
        self.assertEqual(info.result, 200)
        self.assertEqual(info.status, "success")
        self.assertEqual(info.currentIp, "192.168.0.99")
        self.assertEqual(info.updateIp, "192.168.0.100")
        self.assertEqual(info.domain, "example.○○○.○○")
        mock_requests.assert_called_once_with(
            "post",
            "https://api.flarebrow.com/v2/ddns",
            params={},
            data={"host": "example"},
            auth_enabled=True,
        )

    def test_instability_warning_emitted_once_per_process(self):
        # 不安定APIの警告はプロセスごとに1回だけ出力される
        ddns_service_module = importlib.import_module("flaretool.ddns.DdnsService")
        ddns_service_module._instability_warning_emitted = False
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            DdnsService()
            DdnsService()
        matched = [w for w in caught if "may undergo updates" in str(w.message)]
        self.assertEqual(len(matched), 1)

    def test_ddns_error_constructible_with_message_only(self):
        err = DdnsError("something went wrong")
        self.assertEqual(str(err), "something went wrong")
        self.assertEqual(err.status, "something went wrong")
        self.assertIsNone(err.result)
        self.assertIsNone(err.currentIp)
        self.assertIsNone(err.updateIp)
        self.assertIsNone(err.domain)

    def test_ddns_info_snake_case_aliases(self):
        info = DdnsInfo(
            result=200,
            status="success",
            currentIp="192.168.0.99",
            updateIp="192.168.0.100",
            domain="example.○○○.○○",
        )
        # camelCase属性は引き続き利用可能
        self.assertEqual(info.currentIp, "192.168.0.99")
        self.assertEqual(info.updateIp, "192.168.0.100")
        # snake_caseのエイリアスも利用可能
        self.assertEqual(info.current_ip, "192.168.0.99")
        self.assertEqual(info.update_ip, "192.168.0.100")

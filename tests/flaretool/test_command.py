import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from flaretool import nettool
from flaretool.command import *


class CommandTest(unittest.TestCase):
    def setUp(self):
        self.mock_create_connection = MagicMock()
        self.patcher = patch(
            "argparse.ArgumentParser.parse_args", self.mock_create_connection
        )
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_main_with_info(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(nettool, "get_global_ipaddr_info") as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr="192.168.0.1", hostname="example.com", country="US"
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(func="nettool", mode="info", args=[])
                    self.mock_create_connection.return_value = args
                    main()
                self.assertEqual(e.type, SystemExit)
                self.assertEqual(e.value.code, 0)
                self.assertEqual(
                    fake_out.getvalue(),
                    "=== Your IP Infomation ===\nip: 192.168.0.1\nhostname: example.com\ncountry: US\n",
                )

    def test_main_with_get_global_ipaddr_info(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(nettool, "get_global_ipaddr_info") as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr="192.168.0.1", hostname="example.com", country="US"
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(
                        func="nettool", mode="get_global_ipaddr_info", args=[]
                    )
                    self.mock_create_connection.return_value = args
                    main()
                self.assertEqual(e.type, SystemExit)
                self.assertEqual(e.value.code, 0)
                self.assertEqual(
                    fake_out.getvalue(),
                    "ipaddr='192.168.0.1'\nhostname='example.com'\ncountry='US'\n",
                )

    def test_main_with_invalid_mode(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(nettool, "get_global_ipaddr_info") as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr="192.168.0.1", hostname="example.com", country="US"
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(func="nettool", mode="lookup_ip", args=[])
                    self.mock_create_connection.return_value = args
                    main()
                self.assertEqual(e.type, SystemExit)
                self.assertEqual(e.value.code, 1)
                self.assertEqual(
                    fake_out.getvalue(),
                    "lookup_ip() missing 1 required positional argument: 'domain'\n",
                )

    def test_cli_with_nettool_info(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(nettool, "get_global_ipaddr_info") as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr="192.168.0.1", hostname="example.com", country="US"
                )
                args = argparse.Namespace(func="nettool", mode="info", args=[])
                self.mock_create_connection.return_value = args
                result = cli()
                self.assertEqual(result, 0)
                self.assertEqual(
                    fake_out.getvalue(),
                    "=== Your IP Infomation ===\nip: 192.168.0.1\nhostname: example.com\ncountry: US\n",
                )

    def test_cli_with_shorturl(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(ShortUrlService, "create") as mock_method:
                mock_method.return_value = "http://short.url/test"
                args = argparse.Namespace(
                    func="shorturl",
                    url="http://example.com",
                    apikey="apikey",
                    mode="create",
                )
                self.mock_create_connection.return_value = args
                result = cli()
                self.assertEqual(result, 0)
                self.assertEqual(fake_out.getvalue(), "http://short.url/test\n")

    def test_cli_with_shorturl_none(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(ShortUrlService, "get") as mock_method:
                mock_method.return_value = "http://short.url/test"
                args = argparse.Namespace(
                    func="shorturl",
                    url=None,
                    apikey="apikey",
                    mode="show",
                )
                self.mock_create_connection.return_value = args
                result = cli()
                # self.assertEqual(result, 0)
                # self.assertEqual(fake_out.getvalue(), "http://short.url/test\n")

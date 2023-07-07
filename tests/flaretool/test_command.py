import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from flaretool import nettool
from flaretool.command import *
import pytest


class CommandTest(unittest.TestCase):

    def setUp(self):
        self.mock_create_connection = MagicMock()
        # self.mock_create_connection.return_value = [
        #     "command.py", "nettool", "info"]
        self.patcher = patch("argparse.ArgumentParser.parse_args",
                             self.mock_create_connection)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_main_with_info(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(nettool, 'get_global_ipaddr_info') as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr='192.168.0.1', hostname='example.com', country='US'
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(
                        func='nettool', mode='info', args=[])
                    self.mock_create_connection.return_value = args
                    main()
                    self.assertEqual(e.type, SystemExit)
                    self.assertEqual(e.value.code, 0)
                self.assertEqual(fake_out.getvalue(
                ), "=== Your IP Infomation ===\nip: 192.168.0.1\nhostname: example.com\ncountry: US\n")

    def test_main_with_get_global_ipaddr_info(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(nettool, 'get_global_ipaddr_info') as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr='192.168.0.1', hostname='example.com', country='US'
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(
                        func='nettool', mode='get_global_ipaddr_info', args=[])
                    self.mock_create_connection.return_value = args
                    main()
                    self.assertEqual(e.type, SystemExit)
                    self.assertEqual(e.value.code, 0)
                self.assertEqual(fake_out.getvalue(
                ), "ipaddr='192.168.0.1'\nhostname='example.com'\ncountry='US'\n")

    def test_main_with_invalid_mode(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(nettool, 'get_global_ipaddr_info') as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr='192.168.0.1', hostname='example.com', country='US'
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(
                        func='nettool', mode='lookup_ip', args=[])
                    self.mock_create_connection.return_value = args
                    main()
                    self.assertEqual(e.type, SystemExit)
                    self.assertEqual(e.value.code, 9)
                self.assertEqual(fake_out.getvalue(
                ), "lookup_ip() missing 1 required positional argument: 'domain'\n")

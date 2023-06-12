import unittest
from flaretool.nettool import *
from flaretool.nettool.models import *

from unittest.mock import patch


class TestMyModule(unittest.TestCase):

    def test_get_global_ipaddr_info(self):
        # グローバルIPアドレス情報を取得する場合のテスト
        with patch('flaretool.common.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'ipaddr': '192.0.2.1',
                'hostname': 'example.com',
                'country': 'JP'
            }
            ip_info = get_global_ipaddr_info()
            self.assertIsInstance(ip_info, IpInfo)
            self.assertEqual(ip_info.ipaddr, '192.0.2.1')
            self.assertEqual(ip_info.hostname, 'example.com')
            self.assertEqual(ip_info.country, 'JP')

    def test_lookup_ip(self):
        # ドメイン名からIPアドレスを取得する場合のテスト
        with patch('socket.gethostbyname') as mock_gethostbyname:
            mock_gethostbyname.return_value = '192.0.2.1'
            ip = lookup_ip('example.com')
            self.assertEqual(ip, '192.0.2.1')

        with patch('socket.gethostbyname') as mock_gethostbyname:
            import socket
            mock_gethostbyname.side_effect = socket.gaierror
            ip = lookup_ip('example.com')
            self.assertIsNone(ip)

    def test_lookup_domain(self):
        # IPアドレスからドメイン名を取得する場合のテスト
        with patch('socket.gethostbyaddr') as mock_gethostbyaddr:
            mock_gethostbyaddr.return_value = ('example.com', [], [])
            domain = lookup_domain('192.0.2.1')
            self.assertEqual(domain, 'example.com')

        with patch('socket.gethostbyaddr') as mock_gethostbyaddr:
            import socket
            mock_gethostbyaddr.side_effect = socket.herror
            domain = lookup_domain('192.0.2.1')
            self.assertIsNone(domain)

    def test_is_ip_in_allowed_networks(self):
        # IPアドレスが許可されたネットワークに属している場合のテスト
        ipaddr = '192.0.2.1'
        allow_networks = ['192.0.2.0/24', '198.51.100.0/24']
        result = is_ip_in_allowed_networks(ipaddr, allow_networks)
        self.assertTrue(result)

        # IPアドレスが許可されたネットワークに属していない場合のテスト
        ipaddr = '203.0.113.1'
        allow_networks = ['192.0.2.0/24', '198.51.100.0/24']
        result = is_ip_in_allowed_networks(ipaddr, allow_networks)
        self.assertFalse(result)

    def test_domain_exists(self):
        # 存在するドメイン名の場合のテスト
        with patch('whois.whois') as mock_whois:
            mock_whois.return_value.status = True
            result = domain_exists('example.com')
            self.assertTrue(result)

        # 存在しないドメイン名の場合のテスト
        with patch('whois.whois') as mock_whois:
            import whois
            mock_whois.side_effect = whois.parser.PywhoisError
            result = domain_exists('example.com')
            self.assertFalse(result)

    @patch('flaretool.common.requests.get')
    def test_get_japanip_list_success(self, mock_get):
        # モックの振る舞いを設定
        mock_get.return_value.text = "192.0.2.0\n198.51.100.0\n"

        # 関数を呼び出して結果を検証
        result = get_japanip_list()
        self.assertEqual(result, ["192.0.2.0", "198.51.100.0"])

        # requests.getが呼ばれたことを検証
        mock_get.assert_called_with(
            "https://raw.githubusercontent.com/flarebrow/public/master/IPAddress/japan_ipv4.txt"
        )

    def test_is_japan_ip(self):
        # 日本のIPアドレスの場合のテスト
        with patch('flaretool.nettool.common.get_japanip_list') as mock_get_japanip_list:
            mock_get_japanip_list.return_value = [
                '192.0.2.0/24', '198.51.100.0/24']
            result = is_japan_ip('192.0.2.1')
            self.assertTrue(result)

        # 日本のIPアドレスではない場合のテスト
        with patch('flaretool.nettool.common.get_japanip_list') as mock_get_japanip_list:
            mock_get_japanip_list.return_value = [
                '192.0.2.0/24', '198.51.100.0/24']
            result = is_japan_ip('203.0.113.1')
            self.assertFalse(result)

    def test_get_puny_code(self):
        # Punycodeに変換する場合のテスト
        with patch('flaretool.common.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'originalvalue': 'ドメイン名',
                'encodevalue': 'xn--eckwd4c7c',
                'decodevalue': 'ドメイン名'
            }
            puny_info = get_puny_code('ドメイン名')
            self.assertIsInstance(puny_info, PunyDomainInfo)
            self.assertEqual(puny_info.originalvalue, 'ドメイン名')
            self.assertEqual(puny_info.encodevalue, 'xn--eckwd4c7c')
            self.assertEqual(puny_info.decodevalue, 'ドメイン名')

    def test_get_adhost(self):
        # ホストリストを取得する場合のテスト
        with patch('flaretool.common.requests.get') as mock_get:
            mock_get.return_value.content = b'example.com\nsub.example.com\n'
            host_list = get_adhost()
            self.assertIsInstance(host_list, list)
            self.assertEqual(len(host_list), 2)
            self.assertIn('example.com', host_list)
            self.assertIn('sub.example.com', host_list)

        # 特定のドメインのホストリストを取得する場合のテスト
        with patch('flaretool.common.requests.get') as mock_get:
            mock_get.return_value.content = b'example.com\nsub.example.com\n'
            host_list = get_adhost('sub.example.com')
            self.assertIsInstance(host_list, list)
            self.assertEqual(len(host_list), 1)
            self.assertNotIn('example.com', host_list)
            self.assertIn('sub.example.com', host_list)

    def test_get_robots_txt_url(self):
        # robots.txtファイルのURLを生成する場合のテスト
        url = 'https://example.com/path/to/page'
        robots_txt_url = get_robots_txt_url(url)
        self.assertEqual(robots_txt_url, 'https://example.com/robots.txt')

    def test_is_scraping_allowed(self):
        # スクレイピングが許可されている場合のテスト
        with patch('urllib.robotparser.RobotFileParser') as mock_parser:
            mock_can_fetch = mock_parser.return_value.can_fetch
            mock_can_fetch.return_value = True
            url = 'https://example.com'
            is_allowed = is_scraping_allowed(url, 'My User Agent')
            self.assertTrue(is_allowed)

        # スクレイピングが禁止されている場合のテスト
        with patch('urllib.robotparser.RobotFileParser') as mock_parser:
            mock_can_fetch = mock_parser.return_value.can_fetch
            mock_can_fetch.return_value = False
            url = 'https://example.com'
            is_allowed = is_scraping_allowed(url, 'My User Agent')
            self.assertFalse(is_allowed)

import json
import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from flaretool import nettool
from flaretool.command import *
from flaretool.errors import FlareToolNetworkError


class CommandTest(unittest.TestCase):
    def setUp(self):
        self.mock_create_connection = MagicMock()
        self.patcher = patch(
            "argparse.ArgumentParser.parse_args", self.mock_create_connection
        )
        self.patcher.start()
        # main() はCLI起動時にバージョンチェックを行うため、
        # テストでは実際のネットワークアクセスを避ける
        self.version_patcher = patch("flaretool.check_version")
        self.mock_check_version = self.version_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.version_patcher.stop()

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
                # main() はCLI起動時にバージョンチェックを実行する
                self.mock_check_version.assert_called_once_with()

    def test_main_check_version_failure_does_not_break_cli(self):
        # バージョンチェックが失敗してもCLIは動作する
        self.mock_check_version.side_effect = RuntimeError("offline")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch.object(nettool, "get_global_ipaddr_info") as mock_method:
                mock_method.return_value = nettool.IpInfo(
                    ipaddr="192.168.0.1", hostname="example.com", country="US"
                )
                with pytest.raises(SystemExit) as e:
                    args = argparse.Namespace(func="nettool", mode="info", args=[])
                    self.mock_create_connection.return_value = args
                    main()
                self.assertEqual(e.value.code, 0)

    def test_summary_docstring_fallbacks(self):
        # 単一行のdocstringや空のdocstringでもIndexErrorにならない
        from flaretool import command

        self.assertEqual(command._summary("single line only"), "single line only")
        self.assertEqual(command._summary("\n    概要行\n\n    詳細\n"), "概要行")
        self.assertEqual(command._summary(None), "unknown")
        self.assertEqual(command._summary("   \n  \n"), "unknown")

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

    def test_cli_shorturl_create_without_url_exits_1(self):
        # createモードでURL未指定の場合は一覧表示にフォールバックせずエラー終了
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("sys.stderr", new=StringIO()) as fake_err:
                with patch.object(ShortUrlService, "get") as mock_get:
                    args = argparse.Namespace(
                        func="shorturl",
                        url=None,
                        apikey="apikey",
                        mode="create",
                    )
                    self.mock_create_connection.return_value = args
                    result = cli()
                    self.assertEqual(result, 1)
                    self.assertEqual(fake_out.getvalue(), "")
                    self.assertIn("url is required", fake_err.getvalue())
                    mock_get.assert_not_called()

    def test_cli_shorturl_network_error_exits_1(self):
        # ネットワークエラーはトレースバックではなくstderrにメッセージを出して終了コード1
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("sys.stderr", new=StringIO()) as fake_err:
                with patch.object(ShortUrlService, "create") as mock_create:
                    mock_create.side_effect = FlareToolNetworkError(
                        message="Only access from Japan is accepted"
                    )
                    args = argparse.Namespace(
                        func="shorturl",
                        url="http://example.com",
                        apikey="apikey",
                        mode="create",
                    )
                    self.mock_create_connection.return_value = args
                    result = cli()
                    self.assertEqual(result, 1)
                    self.assertEqual(fake_out.getvalue(), "")
                    self.assertIn(
                        "Only access from Japan is accepted", fake_err.getvalue()
                    )

    def test_cli_nettool_network_error_exits_1(self):
        # nettoolサブコマンドでもFlareToolErrorは統一的に処理される
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with patch("sys.stderr", new=StringIO()) as fake_err:
                with patch.object(nettool, "get_global_ipaddr_info") as mock_method:
                    mock_method.side_effect = FlareToolNetworkError(
                        message="Only access from Japan is accepted"
                    )
                    args = argparse.Namespace(func="nettool", mode="info", args=[])
                    self.mock_create_connection.return_value = args
                    result = cli()
                    self.assertEqual(result, 1)
                    self.assertEqual(fake_out.getvalue(), "")
                    self.assertIn(
                        "Only access from Japan is accepted", fake_err.getvalue()
                    )


class NewSubcommandTest(unittest.TestCase):
    """新しいサブコマンド（holiday/business/wareki/seireki/convert/hash/base64/track）のテスト

    こちらのクラスでは parse_args をモックせず、sys.argv を差し替えて
    実際の argparse のパース処理ごと main() を検証する。
    holiday / business はオフライン計算のためネットワークアクセスは発生しない。
    """

    def setUp(self):
        # main() のバージョンチェックによるネットワークアクセスを避ける
        self.version_patcher = patch("flaretool.check_version")
        self.mock_check_version = self.version_patcher.start()

    def tearDown(self):
        self.version_patcher.stop()

    def run_cli(self, *argv):
        """main() を実行して (終了コード, 標準出力, 標準エラー出力) を返すヘルパー"""
        with patch.object(sys, "argv", ["flaretool", *argv]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                with patch("sys.stderr", new=StringIO()) as fake_err:
                    with pytest.raises(SystemExit) as e:
                        main()
        return e.value.code, fake_out.getvalue(), fake_err.getvalue()

    # ---- holiday ----

    def test_holiday_single_date_holiday(self):
        code, out, _ = self.run_cli("holiday", "2026-01-01")
        self.assertEqual(code, 0)
        self.assertEqual(out, "元日\n")

    def test_holiday_single_date_not_holiday(self):
        # 祝日ではない日でも終了コードは0
        code, out, _ = self.run_cli("holiday", "2026/07/02")
        self.assertEqual(code, 0)
        self.assertEqual(out, "祝日ではありません\n")

    def test_holiday_year_month_listing(self):
        code, out, _ = self.run_cli("holiday", "2026-01")
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-01-01 元日\n2026-01-12 成人の日\n")

    def test_holiday_year_listing(self):
        code, out, _ = self.run_cli("holiday", "2026")
        self.assertEqual(code, 0)
        lines = out.splitlines()
        self.assertEqual(len(lines), 18)  # 2026年の祝日（振替休日含む）は18日
        self.assertEqual(lines[0], "2026-01-01 元日")

    def test_holiday_single_date_json(self):
        code, out, _ = self.run_cli("holiday", "2026-01-01", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"date": "2026-01-01", "name": "元日"})

    def test_holiday_listing_json(self):
        code, out, _ = self.run_cli("holiday", "2026-01", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(
            json.loads(out),
            [
                {"date": "2026-01-01", "name": "元日"},
                {"date": "2026-01-12", "name": "成人の日"},
            ],
        )

    # ---- business ----

    def test_business_is_business_day(self):
        code, out, _ = self.run_cli("business", "2026-07-02")
        self.assertEqual(code, 0)
        self.assertEqual(out, "true\n")

    def test_business_is_business_day_false(self):
        # 祝日でも終了コードは0（出力で判定する）
        code, out, _ = self.run_cli("business", "2026-01-01")
        self.assertEqual(code, 0)
        self.assertEqual(out, "false\n")

    def test_business_add(self):
        code, out, _ = self.run_cli("business", "2026-07-02", "--add", "3")
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-07\n")

    def test_business_add_json(self):
        code, out, _ = self.run_cli("business", "2026-07-02", "--add", "3", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(
            json.loads(out),
            {"date": "2026-07-02", "days": 3, "result": "2026-07-07"},
        )

    def test_business_count(self):
        code, out, _ = self.run_cli("business", "2026-07-01", "--count", "2026-07-07")
        self.assertEqual(code, 0)
        self.assertEqual(out, "5\n")

    def test_business_next_and_prev(self):
        code, out, _ = self.run_cli("business", "2026-07-04", "--next")
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-06\n")
        code, out, _ = self.run_cli("business", "2026-07-04", "--prev")
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-03\n")

    # ---- wareki / seireki ----

    def test_wareki(self):
        code, out, _ = self.run_cli("wareki", "2026-07-02")
        self.assertEqual(code, 0)
        self.assertEqual(out, "令和8年7月2日\n")

    def test_wareki_format_json(self):
        code, out, _ = self.run_cli(
            "wareki",
            "2026-07-02",
            "--format",
            "{era_short}{year}.{month}.{day}",
            "--json",
        )
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"date": "2026-07-02", "wareki": "R8.7.2"})

    def test_seireki_round_trip(self):
        # wareki の出力を seireki に戻すと元の日付になる
        _, wareki_out, _ = self.run_cli("wareki", "2026-07-02")
        code, out, _ = self.run_cli("seireki", wareki_out.strip())
        self.assertEqual(code, 0)
        self.assertEqual(out, "2026-07-02\n")

    def test_seireki_json(self):
        code, out, _ = self.run_cli("seireki", "R8.7.2", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"text": "R8.7.2", "date": "2026-07-02"})

    # ---- convert / hash / base64 ----

    def test_convert_half(self):
        code, out, _ = self.run_cli("convert", "ＡＢＣ１２３", "--mode", "half")
        self.assertEqual(code, 0)
        self.assertEqual(out, "ABC123\n")

    def test_convert_full(self):
        code, out, _ = self.run_cli("convert", "ABC123", "--mode", "full")
        self.assertEqual(code, 0)
        self.assertEqual(out, "ＡＢＣ１２３\n")

    def test_convert_json(self):
        code, out, _ = self.run_cli("convert", "abc", "--mode", "upper", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(
            json.loads(out), {"text": "abc", "mode": "upper", "result": "ABC"}
        )

    def test_hash_md5(self):
        code, out, _ = self.run_cli("hash", "hello")
        self.assertEqual(code, 0)
        self.assertEqual(out, "5d41402abc4b2a76b9719d911017c592\n")

    def test_hash_sha256_json(self):
        code, out, _ = self.run_cli("hash", "hello", "--mode", "sha256", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["mode"], "sha256")
        self.assertEqual(
            data["hash"],
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_base64_round_trip(self):
        code, out, _ = self.run_cli("base64", "hello")
        self.assertEqual(code, 0)
        self.assertEqual(out, "aGVsbG8=\n")
        code, out, _ = self.run_cli("base64", "aGVsbG8=", "--decode")
        self.assertEqual(code, 0)
        self.assertEqual(out, "hello\n")

    # ---- track ----

    def test_track_yamato(self):
        with patch("socket.create_connection", MagicMock(return_value=None)):
            with patch("flaretool.common.requests.get") as mock_get:
                mock_get.return_value.json.return_value = {
                    "result": [{"status": "Delivered"}]
                }
                code, out, _ = self.run_cli("track", "yamato", "1234567890123")
                self.assertEqual(code, 0)
                self.assertEqual(out, "status: Delivered\n")
                mock_get.assert_called_once_with(
                    "https://api.flarebrow.com/v2/yamato",
                    params={"n1": "1234-5678-9012-3"},
                )

    def test_track_yamato_json(self):
        with patch("socket.create_connection", MagicMock(return_value=None)):
            with patch("flaretool.common.requests.get") as mock_get:
                mock_get.return_value.json.return_value = {
                    "result": [{"status": "In Transit"}]
                }
                code, out, _ = self.run_cli(
                    "track", "yamato", "1234567890123", "--json"
                )
                self.assertEqual(code, 0)
                self.assertEqual(json.loads(out), [{"status": "In Transit"}])

    def test_track_japanpost(self):
        with patch("socket.create_connection", MagicMock(return_value=None)):
            with patch("flaretool.common.requests.get") as mock_get:
                mock_get.return_value.json.return_value = {"status": "In Transit"}
                code, out, _ = self.run_cli("track", "japanpost", "1234567890123")
                self.assertEqual(code, 0)
                self.assertEqual(out, "status: In Transit\n")
                mock_get.assert_called_once_with(
                    "https://api.flarebrow.com/v2/japanpost",
                    params={"n": "1234-5678-9012-3"},
                )

    # ---- エラーハンドリング ----

    def test_business_invalid_date_exit_code_1(self):
        code, out, err = self.run_cli("business", "not-a-date")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Unsupported date format", err)

    def test_seireki_invalid_text_exit_code_1(self):
        code, out, err = self.run_cli("seireki", "でたらめ")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("和暦として解釈できない", err)

    def test_handler_flaretool_error_exit_code_1(self):
        # ハンドラがFlareToolError（例: オフライン時のネットワークエラー）を
        # 送出しても、トレースバックではなくstderrにメッセージを出して終了コード1
        from flaretool import command
        from flaretool.errors import FlareToolNetworkError

        handler = MagicMock(
            side_effect=FlareToolNetworkError(
                message="Only access from Japan is accepted"
            )
        )
        with patch.dict(command._HANDLERS, {"holiday": handler}):
            code, out, err = self.run_cli("holiday", "2026-01-01", "--online")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Only access from Japan is accepted", err)
        self.assertNotIn("Traceback", err)
        handler.assert_called_once()

"""flaretool command line interface."""

import argparse
import inspect
import json
import re
import sys
from collections.abc import Callable

import flaretool
from flaretool import nettool, utils, wareki
from flaretool.basemodels import BaseDataModel
from flaretool.enums import Base64Mode, ConversionMode, HashMode
from flaretool.errors import FlareToolError
from flaretool.holiday import JapaneseHolidays
from flaretool.shorturl import ShortUrlService

description = f"{flaretool.__name__} ver{flaretool.__version__}"

#: convert サブコマンドのモード名と ConversionMode の対応表
_CONVERT_MODES: dict[str, ConversionMode] = {
    "half": ConversionMode.HALF_WIDTH,
    "full": ConversionMode.FULL_WIDTH,
    "upper": ConversionMode.UPPER,
    "lower": ConversionMode.LOWER,
    "hiragana": ConversionMode.HIRAGANA,
    "katakana": ConversionMode.KATAKANA,
}

#: hash サブコマンドのモード名と HashMode の対応表
_HASH_MODES: dict[str, HashMode] = {
    "md5": HashMode.MD5,
    "sha1": HashMode.SHA1,
    "sha256": HashMode.SHA256,
    "sha512": HashMode.SHA512,
}


def _summary(doc: str | None) -> str:
    """Return the first non-empty docstring line (or "unknown")."""
    if not doc:
        return "unknown"
    lines = [line.strip() for line in doc.splitlines() if line.strip()]
    return lines[0] if lines else "unknown"


def _dumps(data: object) -> str:
    """JSON文字列に変換する内部ヘルパー（日本語はそのまま、日付はISO文字列）"""
    return json.dumps(data, ensure_ascii=False, default=str)


def _print_fields(data: dict) -> None:
    """辞書の各フィールドを「キー: 値」形式で1行ずつ出力する内部ヘルパー"""
    for key, value in data.items():
        print(f"{key}: {value}")


def _is_full_date(text: str) -> bool:
    """
    文字列が年月日まで指定された日付かどうかを判定する内部ヘルパー

    "2026-07-02" / "2026/07/02" / "20260702" は日付、
    "2026" や "2026-07" は年・年月の指定とみなします。

    Args:
        text (str): 判定する文字列

    Returns:
        bool: 年月日まで指定されていればTrue
    """
    text = text.strip()
    parts = re.split(r"[/-]", text)
    if len(parts) == 3:
        return True
    return len(parts) == 1 and text.isdigit() and len(text) == 8


def _cmd_holiday(args: argparse.Namespace) -> int:
    """
    holiday サブコマンド: 日本の祝日を判定・一覧表示します

    年月日まで指定された場合は祝日名（祝日でなければ「祝日ではありません」）を、
    年または年月が指定された場合は祝日の一覧を出力します。

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0。日付の解釈エラーは呼び出し元で処理）
    """
    if args.online:
        # オンライン版は明示的に指定された場合のみ使用する
        # （デフォルトはオフライン計算でネットワークアクセスなし）
        from flaretool.holiday import JapaneseHolidaysOnline

        service: JapaneseHolidays = JapaneseHolidaysOnline()
    else:
        service = JapaneseHolidays()

    if _is_full_date(args.date):
        target = service.to_date(args.date)
        name = service.get_holiday_name(target)
        if args.json:
            print(_dumps({"date": target, "name": name}))
        else:
            print(name if name is not None else "祝日ではありません")
        return 0

    holidays = service.get_holidays(args.date)
    if args.json:
        print(_dumps([{"date": date, "name": name} for date, name in holidays]))
    else:
        for date, name in holidays:
            print(f"{date} {name}")
    return 0


def _cmd_business(args: argparse.Namespace) -> int:
    """
    business サブコマンド: 営業日の計算を行います（オフライン計算）

    --add / --count / --next / --prev のいずれかを指定して営業日を計算します。
    フラグを指定しない場合は営業日判定の結果を true / false で出力します
    （終了コードはどちらも0。スクリプトからは出力を解析してください）。

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0。日付の解釈エラーは呼び出し元で処理）
    """
    service = JapaneseHolidays()
    target = service.to_date(args.date)

    payload: dict[str, object]
    if args.add is not None:
        result = service.add_business_days(target, args.add)
        payload = {"date": target, "days": args.add, "result": result}
        output = result.isoformat()
    elif args.count is not None:
        end = service.to_date(args.count)
        count = service.count_business_days(target, end)
        payload = {"start": target, "end": end, "count": count}
        output = str(count)
    elif args.next:
        result = service.next_business_day(target)
        payload = {"date": target, "next": result}
        output = result.isoformat()
    elif args.prev:
        result = service.previous_business_day(target)
        payload = {"date": target, "prev": result}
        output = result.isoformat()
    else:
        business = service.is_business_day(target)
        payload = {"date": target, "business_day": business}
        output = "true" if business else "false"

    print(_dumps(payload) if args.json else output)
    return 0


def _cmd_wareki(args: argparse.Namespace) -> int:
    """
    wareki サブコマンド: 西暦の日付を和暦の文字列に変換します

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0。日付の解釈エラーは呼び出し元で処理）
    """
    if args.format:
        result = wareki.to_wareki(args.date, format=args.format)
    else:
        result = wareki.to_wareki(args.date)
    if args.json:
        print(_dumps({"date": args.date, "wareki": result}))
    else:
        print(result)
    return 0


def _cmd_seireki(args: argparse.Namespace) -> int:
    """
    seireki サブコマンド: 和暦の文字列を西暦の日付(ISO形式)に変換します

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0。和暦の解釈エラーは呼び出し元で処理）
    """
    result = wareki.to_seireki(args.text)
    if args.json:
        print(_dumps({"text": args.text, "date": result}))
    else:
        print(result.isoformat())
    return 0


def _cmd_convert(args: argparse.Namespace) -> int:
    """
    convert サブコマンド: 文字列を変換します（半角/全角/大文字/小文字/かな）

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0）
    """
    result = utils.convert_value(args.text, _CONVERT_MODES[args.mode])
    if args.json:
        print(_dumps({"text": args.text, "mode": args.mode, "result": result}))
    else:
        print(result)
    return 0


def _cmd_hash(args: argparse.Namespace) -> int:
    """
    hash サブコマンド: 文字列のハッシュ値を計算します

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0）
    """
    result = utils.hash_value(args.text, _HASH_MODES[args.mode])
    if args.json:
        print(_dumps({"text": args.text, "mode": args.mode, "hash": result}))
    else:
        print(result)
    return 0


def _cmd_base64(args: argparse.Namespace) -> int:
    """
    base64 サブコマンド: 文字列のBase64エンコード/デコードを行います

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0）
    """
    mode = Base64Mode.DECODE if args.decode else Base64Mode.ENCODE
    print(utils.base64_convert(args.text, mode))
    return 0


def _cmd_track(args: argparse.Namespace) -> int:
    """
    track サブコマンド: 荷物の配送状況を追跡します（ネットワークアクセスあり）

    Args:
        args (argparse.Namespace): パース済みのコマンドライン引数

    Returns:
        int: 終了コード（常に0。追跡番号のエラーは呼び出し元で処理）
    """
    # ネットワーク関連の依存はコマンド実行時にのみ読み込む
    from flaretool.funcs import tracking

    if args.service == "yamato":
        results = tracking.yamato([args.code])
        if args.json:
            print(_dumps(results))
        else:
            for index, item in enumerate(results):
                if index:
                    print()
                _print_fields(item)
    else:
        result = tracking.japanpost(args.code)
        if args.json:
            print(_dumps(result))
        else:
            _print_fields(result)
    return 0


#: サブコマンド名とハンドラ関数の対応表（nettool / shorturl は cli() 内で処理）
_HANDLERS: dict[str, Callable[[argparse.Namespace], int]] = {
    "holiday": _cmd_holiday,
    "business": _cmd_business,
    "wareki": _cmd_wareki,
    "seireki": _cmd_seireki,
    "convert": _cmd_convert,
    "hash": _cmd_hash,
    "base64": _cmd_base64,
    "track": _cmd_track,
}


def _register_extra_subcommands(subparsers: argparse._SubParsersAction) -> None:
    """
    nettool / shorturl 以外のサブコマンドを登録する内部ヘルパー

    Args:
        subparsers (argparse._SubParsersAction): サブコマンドの登録先
    """
    # holiday
    parser_holiday = subparsers.add_parser(
        "holiday",
        help="日本の祝日を判定・一覧表示します",
        description="日本の祝日を判定・一覧表示します（デフォルトはオフライン計算でネットワークアクセスなし）",
    )
    parser_holiday.add_argument(
        "date",
        help="判定する日付（例: 2026-07-02）または一覧表示する年・年月（例: 2026, 2026-07）",
    )
    parser_holiday.add_argument(
        "--online",
        action="store_true",
        help="オンライン版(JapaneseHolidaysOnline)を使用します（デフォルトはオフライン計算）",
    )
    parser_holiday.add_argument(
        "--json", action="store_true", help="JSON形式で出力します"
    )

    # business
    parser_business = subparsers.add_parser(
        "business",
        help="営業日の計算を行います",
        description=(
            "営業日の計算を行います（オフライン計算）。"
            "フラグを指定しない場合は営業日判定の結果を true / false で出力します"
            "（終了コードはどちらも0）"
        ),
    )
    parser_business.add_argument("date", help="起点の日付（例: 2026-07-02）")
    business_group = parser_business.add_mutually_exclusive_group()
    business_group.add_argument(
        "--add",
        type=int,
        metavar="N",
        help="N営業日後の日付を表示します（負の値でN営業日前）",
    )
    business_group.add_argument(
        "--count",
        metavar="END",
        help="dateからENDまで（両端を含む）の営業日数を表示します",
    )
    business_group.add_argument(
        "--next", action="store_true", help="翌営業日を表示します"
    )
    business_group.add_argument(
        "--prev", action="store_true", help="前営業日を表示します"
    )
    parser_business.add_argument(
        "--json", action="store_true", help="JSON形式で出力します"
    )

    # wareki
    parser_wareki = subparsers.add_parser("wareki", help="西暦の日付を和暦に変換します")
    parser_wareki.add_argument("date", help="変換する日付（例: 2026-07-02）")
    parser_wareki.add_argument(
        "--format",
        metavar="FMT",
        help="出力書式（例: {era_short}{year}.{month}.{day} -> R8.7.2）",
    )
    parser_wareki.add_argument(
        "--json", action="store_true", help="JSON形式で出力します"
    )

    # seireki
    parser_seireki = subparsers.add_parser(
        "seireki", help="和暦の文字列を西暦の日付に変換します"
    )
    parser_seireki.add_argument(
        "text", help="変換する和暦の文字列（例: 令和8年7月2日, R8.7.2）"
    )
    parser_seireki.add_argument(
        "--json", action="store_true", help="JSON形式で出力します"
    )

    # convert
    parser_convert = subparsers.add_parser(
        "convert", help="文字列を変換します（半角/全角/大文字/小文字/かな）"
    )
    parser_convert.add_argument("text", help="変換する文字列")
    parser_convert.add_argument(
        "--mode",
        required=True,
        choices=sorted(_CONVERT_MODES),
        help="変換モード",
    )
    parser_convert.add_argument(
        "--json", action="store_true", help="JSON形式で出力します"
    )

    # hash
    parser_hash = subparsers.add_parser("hash", help="文字列のハッシュ値を計算します")
    parser_hash.add_argument("text", help="ハッシュ計算する文字列")
    parser_hash.add_argument(
        "--mode",
        choices=sorted(_HASH_MODES),
        default="md5",
        help="ハッシュアルゴリズム（デフォルト: md5）",
    )
    parser_hash.add_argument("--json", action="store_true", help="JSON形式で出力します")

    # base64
    parser_base64 = subparsers.add_parser(
        "base64", help="文字列のBase64エンコード/デコードを行います"
    )
    parser_base64.add_argument("text", help="エンコードまたはデコードする文字列")
    parser_base64.add_argument(
        "--decode",
        action="store_true",
        help="デコードします（デフォルトはエンコード）",
    )

    # track
    parser_track = subparsers.add_parser(
        "track", help="荷物の配送状況を追跡します（ネットワークアクセスあり）"
    )
    parser_track.add_argument(
        "service", choices=["yamato", "japanpost"], help="配送業者"
    )
    parser_track.add_argument("code", help="追跡番号")
    parser_track.add_argument(
        "--json", action="store_true", help="JSON形式で出力します"
    )


def cli() -> int:
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="func", required=True)

    # nettool
    parser_nettool = subparsers.add_parser("nettool")
    nettool_func_list = [
        func for func in dir(nettool) if inspect.isfunction(getattr(nettool, func))
    ]
    nettool_func_doc = "".join(
        f"[{func}]:{_summary(getattr(nettool, func).__doc__)} \t"
        for func in nettool_func_list
    )
    parser_nettool.add_argument(
        "mode",
        choices=["info"] + nettool_func_list,
        help=nettool_func_doc,
    )
    parser_nettool.add_argument("args", nargs="*", default=[], help="引数")

    # shorturl
    parser_shorturl = subparsers.add_parser("shorturl")
    parser_shorturl.add_argument("--apikey", "-key", help="API Key")
    parser_shorturl.add_argument("mode", choices=["create", "show"], help="Mode")
    parser_shorturl.add_argument(
        "url", nargs="?", help="URL to shorten (required for 'create' mode)"
    )

    # holiday / business / wareki / seireki / convert / hash / base64 / track
    _register_extra_subcommands(subparsers)

    args = parser.parse_args()

    try:
        match args.func:
            case "shorturl":
                if args.apikey:
                    flaretool.api_key = args.apikey
                if args.mode == "create" and not args.url:
                    print("url is required for 'create' mode", file=sys.stderr)
                    return 1
                service = ShortUrlService()
                if args.mode == "create":
                    result = service.create(args.url)
                else:
                    result = service.get()
                print(
                    result
                    if not isinstance(result, BaseDataModel)
                    else result.__trace__()
                )
            case "nettool":
                match args.mode:
                    case "info":
                        network_info = nettool.get_global_ipaddr_info()
                        print("=== Your IP Infomation ===")
                        print("ip:", network_info.ipaddr)
                        print("hostname:", network_info.hostname)
                        print("country:", network_info.country)
                    case _:
                        try:
                            result = getattr(nettool, args.mode)(*args.args)
                            print(
                                result
                                if not isinstance(result, BaseDataModel)
                                else result.__trace__()
                            )
                        except TypeError as e:
                            print(e)
                            return 1
            case command if command in _HANDLERS:
                try:
                    return _HANDLERS[command](args)
                except ValueError as error:
                    # 日付や和暦の解釈エラーなどはメッセージを表示して終了コード1
                    print(error, file=sys.stderr)
                    return 1
    except FlareToolError as error:
        # ネットワークエラーや祝日データ取得エラーなどのflaretool固有の
        # エラーはトレースバックを出さずメッセージを表示して終了コード1
        print(error, file=sys.stderr)
        return 1
    return 0


def main() -> None:
    try:
        # バージョンチェックはインポート時に自動実行されなくなったため、
        # CLI起動時に明示的に実行する（オフラインでもCLIが動作するよう
        # 例外はすべて無視する）
        flaretool.check_version()
    except Exception:
        pass
    sys.exit(cli())

"""和暦(元号)と西暦の相互変換ユーティリティ(明治/大正/昭和/平成/令和対応)."""

import datetime
import re
import unicodedata
from dataclasses import dataclass

__all__ = [
    "Era",
    "ERAS",
    "get_era",
    "to_wareki",
    "to_seireki",
    "today_wareki",
    "kanji_to_int",
    "int_to_kanji",
    "get_fiscal_year",
]


@dataclass(frozen=True)
class Era:
    """
    元号を表すデータクラス

    Attributes:
        name (str): 元号名 (例: "令和")
        name_short (str): 元号の頭文字 (例: "R")
        romaji (str): 元号のローマ字表記 (例: "Reiwa")
        start (datetime.date): 元号の開始日(グレゴリオ暦)
        end (datetime.date or None): 元号の終了日. 現行元号の場合はNone.
    """

    name: str
    name_short: str
    romaji: str
    start: datetime.date
    end: datetime.date | None


ERAS: tuple[Era, ...] = (
    Era("明治", "M", "Meiji", datetime.date(1868, 10, 23), datetime.date(1912, 7, 29)),
    Era("大正", "T", "Taisho", datetime.date(1912, 7, 30), datetime.date(1926, 12, 24)),
    Era("昭和", "S", "Showa", datetime.date(1926, 12, 25), datetime.date(1989, 1, 7)),
    Era("平成", "H", "Heisei", datetime.date(1989, 1, 8), datetime.date(2019, 4, 30)),
    Era("令和", "R", "Reiwa", datetime.date(2019, 5, 1), None),
)

# 漢数字(一桁)の対応表 (インデックス = 数値)
_KANJI_DIGITS = "〇一二三四五六七八九"
_KANJI_DIGIT_VALUES = {char: value for value, char in enumerate(_KANJI_DIGITS)}

# 日付文字列のパースで試す書式 (ISO形式はdatetime.fromisoformatで先に処理)
_DATE_FORMATS = ("%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日")

# 元号表記(元号名/頭文字/ローマ字)の検索テーブル (小文字キー)
_ERA_LOOKUP: dict[str, Era] = {}
for _era in ERAS:
    _ERA_LOOKUP[_era.name] = _era
    _ERA_LOOKUP[_era.name_short.lower()] = _era
    _ERA_LOOKUP[_era.romaji.lower()] = _era

# 長い表記から優先してマッチさせる (例: "Meiji" が "M" に分割されないように)
_ERA_PATTERN = "|".join(
    re.escape(key) for key in sorted(_ERA_LOOKUP, key=len, reverse=True)
)
_NUMBER_PATTERN = r"\d+|元|[〇一二三四五六七八九十百]+"
_WAREKI_RE = re.compile(
    rf"\s*(?P<era>{_ERA_PATTERN})\s*"
    rf"(?P<year>{_NUMBER_PATTERN})\s*[年./-]\s*"
    rf"(?P<month>{_NUMBER_PATTERN})\s*[月./-]\s*"
    rf"(?P<day>{_NUMBER_PATTERN})\s*日?\s*",
    re.IGNORECASE,
)
_KANJI_NUMBER_RE = re.compile(
    r"(?:(?P<hundreds>[一二三四五六七八九])?(?P<hyaku>百))?"
    r"(?:(?P<tens>[一二三四五六七八九])?(?P<ju>十))?"
    r"(?P<ones>[〇一二三四五六七八九])?"
)


def _to_date(value: datetime.date | datetime.datetime | str) -> datetime.date:
    """
    date/datetime/文字列をdatetime.dateに変換する内部ヘルパー

    Args:
        value (datetime.date or datetime.datetime or str): 変換する値

    Returns:
        datetime.date: 変換後の日付

    Raises:
        ValueError: 日付として解釈できない場合
    """
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        text = unicodedata.normalize("NFKC", value).strip()
        if text:
            try:
                return datetime.datetime.fromisoformat(text).date()
            except ValueError:
                pass
            for fmt in _DATE_FORMATS:
                try:
                    return datetime.datetime.strptime(text, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"日付として解釈できない文字列です: {value!r}")
    raise ValueError(f"日付として解釈できない型です: {type(value).__name__}")


def kanji_to_int(text: str) -> int:
    """
    漢数字(1〜999)を整数に変換します。"元" は 1 として扱います。

    Args:
        text (str): 変換する漢数字 (例: "八", "十二", "二十九", "百一", "元")

    Returns:
        int: 変換後の整数 (1〜999)

    Raises:
        ValueError: 漢数字として解釈できない場合、または1〜999の範囲外の場合

    Examples:
        >>> kanji_to_int("八")
        8
        >>> kanji_to_int("二十九")
        29
        >>> kanji_to_int("百")
        100
        >>> kanji_to_int("二百一")
        201
        >>> kanji_to_int("元")
        1
    """
    if not isinstance(text, str):
        raise ValueError(f"漢数字として解釈できない型です: {type(text).__name__}")
    normalized = unicodedata.normalize("NFKC", text).strip()
    if normalized == "元":
        return 1
    match = _KANJI_NUMBER_RE.fullmatch(normalized)
    if not normalized or match is None:
        raise ValueError(f"漢数字として解釈できない文字列です: {text!r}")
    if match.group("hyaku"):
        hundreds = (
            _KANJI_DIGIT_VALUES[match.group("hundreds")]
            if match.group("hundreds")
            else 1
        )
    else:
        hundreds = 0
    if match.group("ju"):
        tens = _KANJI_DIGIT_VALUES[match.group("tens")] if match.group("tens") else 1
    else:
        tens = 0
    ones = _KANJI_DIGIT_VALUES[match.group("ones")] if match.group("ones") else 0
    value = hundreds * 100 + tens * 10 + ones
    if not 1 <= value <= 999:
        raise ValueError(f"1〜999の範囲外です: {text!r} -> {value}")
    return value


def int_to_kanji(value: int) -> str:
    """
    整数(1〜999)を漢数字に変換します。1〜99の出力は従来と同一です。

    Args:
        value (int): 変換する整数 (1〜999)

    Returns:
        str: 変換後の漢数字 (例: 8 -> "八", 29 -> "二十九", 101 -> "百一")

    Raises:
        ValueError: 1〜999の範囲外、または整数でない場合

    Examples:
        >>> int_to_kanji(8)
        '八'
        >>> int_to_kanji(12)
        '十二'
        >>> int_to_kanji(29)
        '二十九'
        >>> int_to_kanji(100)
        '百'
        >>> int_to_kanji(201)
        '二百一'
    """
    if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 999:
        raise ValueError(f"1〜999の整数を指定してください: {value!r}")
    hundreds, remainder = divmod(value, 100)
    tens, ones = divmod(remainder, 10)
    result = ""
    if hundreds >= 2:
        result += _KANJI_DIGITS[hundreds]
    if hundreds >= 1:
        result += "百"
    if tens >= 2:
        result += _KANJI_DIGITS[tens]
    if tens >= 1:
        result += "十"
    if ones >= 1:
        result += _KANJI_DIGITS[ones]
    return result


def get_era(date: datetime.date | datetime.datetime | str) -> Era:
    """
    指定した日付が属する元号を取得します。

    Args:
        date (datetime.date or datetime.datetime or str): 対象の日付.
            文字列はISO形式("2019-05-01")のほか "2019/05/01",
            "2019年5月1日" などを受け付けます(全角数字も可).

    Returns:
        Era: 該当する元号

    Raises:
        ValueError: 明治より前の日付、または日付として解釈できない場合

    Examples:
        >>> get_era("2019-05-01").name
        '令和'
        >>> get_era(datetime.date(1989, 1, 7)).name
        '昭和'
    """
    target = _to_date(date)
    for era in reversed(ERAS):
        if target >= era.start:
            return era
    raise ValueError(f"明治より前の日付は対応していません: {target.isoformat()}")


def to_wareki(
    date: datetime.date | datetime.datetime | str,
    *,
    format: str = "{era}{year}年{month}月{day}日",
    gannen: bool = True,
) -> str:
    """
    西暦の日付を和暦の文字列に変換します。

    formatで使用できるプレースホルダー:
        {era} 令和 / {era_short} R / {era_romaji} Reiwa /
        {year} 8 / {year_kanji} 八 / {month} 7 / {month_kanji} 七 /
        {day} 2 / {day_kanji} 二

    漢数字プレースホルダー({year_kanji}など)は書式で参照された場合のみ
    計算されます。{year_kanji}は999年まで対応し、100以上は"百"を使った
    表記になります(例: 100 -> "百", 101 -> "百一")。

    Args:
        date (datetime.date or datetime.datetime or str): 変換する日付
        format (str, optional): 出力書式. デフォルトは"{era}{year}年{month}月{day}日".
        gannen (bool, optional): Trueの場合、元号1年目の{year}を"元"として
            出力します(例: "令和元年"). {year_kanji}には影響せず、1年目は
            常に"一"となります. Falseの場合は{year}も"1"になります.
            デフォルトはTrue.

    Returns:
        str: 和暦の文字列 (例: "令和8年7月2日")

    Raises:
        ValueError: 明治より前の日付、日付として解釈できない場合、
            またはformatに未知のプレースホルダーが含まれる場合

    Examples:
        >>> to_wareki("2026-07-02")
        '令和8年7月2日'
        >>> to_wareki("2019-05-01")
        '令和元年5月1日'
        >>> to_wareki("2019-05-01", gannen=False)
        '令和1年5月1日'
        >>> to_wareki("2026-07-02", format="{era_short}{year}.{month}.{day}")
        'R8.7.2'
    """
    target = _to_date(date)
    era = get_era(target)
    year = target.year - era.start.year + 1
    values = {
        "era": era.name,
        "era_short": era.name_short,
        "era_romaji": era.romaji,
        "year": "元" if gannen and year == 1 else year,
        "month": target.month,
        "day": target.day,
    }
    # 漢数字プレースホルダーは書式で参照されている場合のみ計算する
    # (漢数字化できない値でも、参照されなければエラーにしない)
    for name, number in (
        ("year_kanji", year),
        ("month_kanji", target.month),
        ("day_kanji", target.day),
    ):
        if "{" + name in format:
            values[name] = int_to_kanji(number)
    try:
        return format.format(**values)
    except (KeyError, IndexError) as error:
        raise ValueError(
            f"formatに未知のプレースホルダーが含まれています: {error}"
        ) from None


def today_wareki(**kwargs) -> str:
    """
    今日の日付を和暦の文字列に変換します。

    Args:
        **kwargs: to_wareki()に渡すキーワード引数 (format, gannen)

    Returns:
        str: 今日の和暦文字列 (例: "令和8年7月2日")

    Examples:
        >>> today_wareki()  # doctest: +SKIP
        '令和8年7月2日'
    """
    return to_wareki(datetime.date.today(), **kwargs)


def _parse_number(token: str) -> int:
    """和暦文字列中の数値トークン(算用数字/漢数字/元)を整数に変換する内部ヘルパー"""
    if token.isdigit():
        return int(token)
    return kanji_to_int(token)


def to_seireki(text: str) -> datetime.date:
    """
    和暦の文字列を西暦の日付に変換します。

    "令和8年7月2日"、"令和元年5月1日"、"R8.7.2"、"R8/7/2"、"R8-7-2"、
    "H31.4.30"、"Reiwa 8-7-2"、漢数字("令和八年七月二日")、
    全角文字("Ｒ８年７月２日")などを受け付けます。
    年月日がすべて揃っていない場合や、元号の期間外の日付
    (例: "昭和65年1月1日")はValueErrorとなります。

    Args:
        text (str): 変換する和暦の文字列

    Returns:
        datetime.date: 変換後の西暦の日付

    Raises:
        ValueError: 和暦として解釈できない場合、存在しない日付の場合、
            または元号の期間外の日付の場合

    Examples:
        >>> to_seireki("令和8年7月2日")
        datetime.date(2026, 7, 2)
        >>> to_seireki("令和元年5月1日")
        datetime.date(2019, 5, 1)
        >>> to_seireki("H31.4.30")
        datetime.date(2019, 4, 30)
    """
    if not isinstance(text, str):
        raise ValueError(f"和暦として解釈できない型です: {type(text).__name__}")
    normalized = unicodedata.normalize("NFKC", text).strip()
    match = _WAREKI_RE.fullmatch(normalized)
    if match is None:
        raise ValueError(f"和暦として解釈できない文字列です: {text!r}")
    era = _ERA_LOOKUP[match.group("era").lower()]
    year = _parse_number(match.group("year"))
    month = _parse_number(match.group("month"))
    day = _parse_number(match.group("day"))
    if year < 1:
        raise ValueError(f"年は1以上を指定してください: {text!r}")
    seireki_year = era.start.year + year - 1
    try:
        result = datetime.date(seireki_year, month, day)
    except ValueError as error:
        raise ValueError(f"無効な日付です: {text!r} ({error})") from None
    if result < era.start or (era.end is not None and result > era.end):
        raise ValueError(
            f"元号'{era.name}'の期間外の日付です: {text!r} -> {result.isoformat()}"
        )
    return result


def get_fiscal_year(
    date: datetime.date | datetime.datetime | str,
    *,
    start_month: int = 4,
) -> int:
    """
    指定した日付の年度(日本の会計年度)を取得します。

    Args:
        date (datetime.date or datetime.datetime or str): 対象の日付
        start_month (int, optional): 年度の開始月 (1〜12). デフォルトは4.

    Returns:
        int: 年度 (例: 2026-03-31 -> 2025)

    Raises:
        ValueError: start_monthが1〜12の範囲外、または日付として解釈できない場合

    Examples:
        >>> get_fiscal_year("2026-03-31")
        2025
        >>> get_fiscal_year("2026-04-01")
        2026
    """
    if not isinstance(start_month, int) or not 1 <= start_month <= 12:
        raise ValueError(f"start_monthは1〜12の整数を指定してください: {start_month!r}")
    target = _to_date(date)
    return target.year if target.month >= start_month else target.year - 1

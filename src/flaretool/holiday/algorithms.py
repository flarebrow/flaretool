"""
日本の祝日判定ルール（純粋関数とデータ駆動の定義テーブル）

このモジュールは日付計算のみを行う純粋関数の集まりで、
ネットワークやインスタンス状態には依存しません。

- :data:`HOLIDAY_RULES`: 祝日の宣言的な定義テーブル
  （名称・適用年範囲・日付ルール）。並び順は
  :meth:`JapaneseHolidays.get_holiday_name` の判定優先順位と同じです。
- :func:`holidays_of_year`: 1年分の法定休日（国民の休日・振替休日を含む）を
  ``{日付: 名称}`` の辞書として算出します。結果はキャッシュされるため、
  期間検索やカレンダー出力は辞書引きだけで済みます。
"""

import calendar
import datetime
import functools
from collections.abc import Callable
from dataclasses import dataclass

TRANSFER_HOLIDAY_SUFFIX = "（振替休日）"
NATIONAL_HOLIDAY_NAME = "国民の休日"

# 振替休日制度の施行日（昭和48年 祝日法改正、1973年4月12日施行）。
# この日以降に日曜日と重なった祝日のみ振替休日が発生する
# （史上初の振替休日は1973年4月30日）。
SUBSTITUTE_HOLIDAY_LAW_EFFECTIVE = datetime.date(1973, 4, 12)

# 年を受け取り、その年の該当日付を返す（適用外の年は None）
DateRule = Callable[[int], datetime.date | None]


def fixed(month: int, day: int) -> DateRule:
    """毎年同じ月日の祝日ルールを返す"""

    def rule(year: int) -> datetime.date:
        return datetime.date(year, month, day)

    return rule


def nth_monday(month: int, n: int) -> DateRule:
    """第n月曜日（ハッピーマンデー）の祝日ルールを返す"""

    def rule(year: int) -> datetime.date | None:
        first = datetime.date(year, month, 1)
        offset = (0 - first.weekday()) % 7  # 月初から最初の月曜日まで
        day = 1 + offset + 7 * (n - 1)
        # 第n月曜日がその月に存在しない場合は None（翌月へ繰り越さない）
        if day > calendar.monthrange(year, month)[1]:
            return None
        return datetime.date(year, month, day)

    return rule


def equinox(month: int, base: float) -> DateRule:
    """春分・秋分の日の祝日ルールを返す（1900年～2099年の近似式）"""

    def rule(year: int) -> datetime.date | None:
        if year < 1900 or year > 2099:
            return None
        day = int(base + 0.242194 * (year - 1980) - (year - 1980) // 4)
        return datetime.date(year, month, day)

    return rule


def segments(*parts: tuple[int | None, int | None, DateRule]) -> DateRule:
    """
    適用年範囲付きのルールを合成する

    (開始年, 終了年, 日付ルール) のタプルを順に評価し、
    最初に年が範囲内となったルールを適用します（Noneは無制限）。
    どの範囲にも該当しない年は None（祝日なし）です。
    """

    def rule(year: int) -> datetime.date | None:
        for since, until, sub_rule in parts:
            if (since is None or year >= since) and (until is None or year <= until):
                return sub_rule(year)
        return None

    return rule


@dataclass(frozen=True, slots=True)
class HolidayRule:
    """
    祝日1件分の宣言的な定義

    Attributes:
        key (str): 英語識別子（JapaneseHolidaysのis_<key>メソッドに対応）
        name (str or Callable[[int], str]): 祝日名（年によって変わる場合は関数）
        date_rule (DateRule): 年からその年の日付を求めるルール
    """

    key: str
    name: str | Callable[[int], str]
    date_rule: DateRule

    def date_for_year(self, year: int) -> datetime.date | None:
        """その年の該当日付を返す（適用外の年は None）"""
        return self.date_rule(year)

    def name_for_year(self, year: int) -> str:
        """その年に用いる祝日名を返す"""
        return self.name(year) if callable(self.name) else self.name

    def matches(self, date: datetime.date) -> bool:
        """日付がこの祝日に該当するかを判定する"""
        return self.date_rule(date.year) == date


# 判定の優先順位（get_holiday_nameの判定順）に並べた祝日定義テーブル。
# 「国民の休日」は憲法記念日の直後に判定される（holidays_of_year参照）。
HOLIDAY_RULES: tuple[HolidayRule, ...] = (
    HolidayRule("new_year", "元日", fixed(1, 1)),
    HolidayRule(
        "coming_of_age_day",
        "成人の日",
        segments(
            (None, 1999, fixed(1, 15)),
            (2000, None, nth_monday(1, 2)),
        ),
    ),
    HolidayRule(
        "foundation_day",
        "建国記念の日",
        segments((1967, None, fixed(2, 11))),
    ),
    HolidayRule("spring_equinox", "春分の日", equinox(3, 20.8431)),
    HolidayRule(
        "showa_day",
        # 1989年以前の4月29日は天皇誕生日（昭和天皇）
        lambda year: "天皇誕生日" if year < 1990 else "昭和の日",
        segments(
            (None, 1988, fixed(4, 29)),
            (2007, None, fixed(4, 29)),  # 1989年～2006年は対象外
        ),
    ),
    HolidayRule("constitution_day", "憲法記念日", fixed(5, 3)),
    HolidayRule(
        "greenery_day",
        "みどりの日",
        segments(
            (1989, 2006, fixed(4, 29)),
            (2007, None, fixed(5, 4)),
        ),
    ),
    HolidayRule("childrens_day", "こどもの日", fixed(5, 5)),
    HolidayRule(
        "marine_day",
        "海の日",
        segments(
            (1996, 2002, fixed(7, 20)),
            (2020, 2020, fixed(7, 23)),  # 東京五輪特例
            (2021, 2021, fixed(7, 22)),  # 東京五輪特例
            (2003, None, nth_monday(7, 3)),
        ),
    ),
    HolidayRule(
        "mountain_day",
        "山の日",
        segments(
            (2020, 2020, fixed(8, 10)),  # 東京五輪特例
            (2021, 2021, fixed(8, 8)),  # 東京五輪特例
            (2016, None, fixed(8, 11)),
        ),
    ),
    HolidayRule(
        "respect_for_the_aged_day",
        "敬老の日",
        segments(
            (None, 2002, fixed(9, 15)),
            (2003, None, nth_monday(9, 3)),
        ),
    ),
    HolidayRule("autumn_equinox", "秋分の日", equinox(9, 23.2488)),
    HolidayRule(
        "health_and_sports_day",
        lambda year: "体育の日" if year < 2020 else "スポーツの日",
        segments(
            (None, 1999, fixed(10, 10)),
            (2020, 2020, fixed(7, 24)),  # 東京五輪特例
            (2021, 2021, fixed(7, 23)),  # 東京五輪特例
            (2000, None, nth_monday(10, 2)),
        ),
    ),
    HolidayRule("culture_day", "文化の日", fixed(11, 3)),
    HolidayRule("labour_thanksgiving_day", "勤労感謝の日", fixed(11, 23)),
    HolidayRule(
        "emperors_birthday",
        "天皇誕生日",
        segments(
            (1948, 1988, fixed(4, 29)),  # 昭和
            (1989, 2018, fixed(12, 23)),  # 平成
            (2020, None, fixed(2, 23)),  # 令和（2019年は祝日なし）
        ),
    ),
)

RULES_BY_KEY: dict[str, HolidayRule] = {rule.key: rule for rule in HOLIDAY_RULES}

# 「国民の休日」を判定テーブルへ差し込む位置（このルールの直後）
_NATIONAL_HOLIDAY_AFTER = "constitution_day"

# 皇室慶弔行事等による単発の休日（本実装では「国民の休日」として扱う）
_EXTRA_NATIONAL_HOLIDAYS = frozenset(
    {
        datetime.date(1989, 2, 24),  # 昭和天皇の大喪の礼
        datetime.date(1990, 11, 12),  # 即位礼正殿の儀
        datetime.date(1993, 6, 9),  # 皇太子徳仁親王の結婚の儀
        datetime.date(2019, 10, 22),  # 即位礼正殿の儀
    }
)


def matches(key: str, date: datetime.date) -> bool:
    """定義テーブル上の祝日 ``key`` に日付が該当するかを判定する"""
    return RULES_BY_KEY[key].matches(date)


def is_national_holiday(date: datetime.date) -> bool:
    """
    国民の休日（祝日に挟まれた平日等）の判定

    Args:
        date (datetime.date): 判定する日付

    Returns:
        bool: 国民の休日であればTrue、そうでなければFalse
    """
    # 2019年は改元に伴う特例（4/30～5/2が休日）
    if datetime.date(2019, 4, 30) <= date <= datetime.date(2019, 5, 2):
        return True
    if date in _EXTRA_NATIONAL_HOLIDAYS:
        return True
    # 2007年以降の5月4日はみどりの日のため対象外
    if 2007 <= date.year and date.month == 5:
        return False
    if date.year <= 1985:
        return False
    previous_date = date - datetime.timedelta(days=1)
    next_date = date + datetime.timedelta(days=1)
    is_may_holiday = matches("constitution_day", previous_date) and matches(
        "childrens_day", next_date
    )
    is_sep_holiday = matches("respect_for_the_aged_day", previous_date) and matches(
        "autumn_equinox", next_date
    )
    return (is_may_holiday or is_sep_holiday) and date.weekday() < 6


def _national_holidays_of_year(year: int) -> list[datetime.date]:
    """その年の「国民の休日」をすべて返す"""
    candidates: list[datetime.date] = [
        d for d in _EXTRA_NATIONAL_HOLIDAYS if d.year == year
    ]
    if year == 2019:
        candidates.extend(datetime.date(2019, 5, day) for day in (1, 2))
        candidates.append(datetime.date(2019, 4, 30))
    # 5月の飛石連休（1986年～2006年のみ成立し得る）
    candidates.append(datetime.date(year, 5, 4))
    # 敬老の日と秋分の日に挟まれた日（シルバーウィーク）
    respect_day = RULES_BY_KEY["respect_for_the_aged_day"].date_for_year(year)
    if respect_day is not None:
        candidates.append(respect_day + datetime.timedelta(days=1))
    return sorted(d for d in set(candidates) if is_national_holiday(d))


@functools.cache
def holidays_of_year(year: int) -> dict[datetime.date, str]:
    """
    1年分の法定休日を算出する

    国民の休日と振替休日を含みます（利用者が追加した独自の休日は含みません）。
    結果はキャッシュされるため、2回目以降の呼び出しは辞書参照のみです。

    Args:
        year (int): 西暦年

    Returns:
        dict[datetime.date, str]: 日付をキー、祝日名を値とする辞書（日付昇順）
    """
    table: dict[datetime.date, str] = {}
    for rule in HOLIDAY_RULES:
        holiday_date = rule.date_for_year(year)
        if holiday_date is not None:
            table.setdefault(holiday_date, rule.name_for_year(year))
        if rule.key == _NATIONAL_HOLIDAY_AFTER:
            for national_date in _national_holidays_of_year(year):
                table.setdefault(national_date, NATIONAL_HOLIDAY_NAME)

    # 振替休日: 日曜日の祝日は翌月曜日が休日となる
    # （昭和48年 祝日法改正の施行日1973年4月12日以降の祝日のみ対象）
    for holiday_date, name in sorted(table.items()):
        if holiday_date.weekday() != 6:
            continue
        if holiday_date < SUBSTITUTE_HOLIDAY_LAW_EFFECTIVE:
            continue
        monday = holiday_date + datetime.timedelta(days=1)
        if monday.year == year and monday not in table:
            table[monday] = name + TRANSFER_HOLIDAY_SUFFIX

    # 2007年以降、5月3日～5日のいずれかが日曜日の場合は5月6日が振替休日
    if year >= 2007:
        may_6 = datetime.date(year, 5, 6)
        if may_6 not in table and any(
            datetime.date(year, 5, day).weekday() == 6 for day in (3, 4, 5)
        ):
            table[may_6] = table[datetime.date(year, 5, 5)] + TRANSFER_HOLIDAY_SUFFIX

    return dict(sorted(table.items()))

"""日本の祝日を管理するクラス（オフライン版）"""

import calendar
import datetime
from collections.abc import Iterable

from flaretool.holiday import algorithms
from flaretool.holiday.algorithms import (
    TRANSFER_HOLIDAY_SUFFIX,
    holidays_of_year,
    matches,
)

__all__ = ["JapaneseHolidays"]

# 月日の組 (month, day)
_MonthDay = tuple[int, int]

# 毎年繰り返すカスタム休日ルール (名称, 開始月日, 終了月日)
_AnnualRule = tuple[str, _MonthDay, _MonthDay]

# デフォルトの週末（土曜日=5, 日曜日=6）
_DEFAULT_WEEKEND: frozenset[int] = frozenset({5, 6})


def _parse_month_day(text: str) -> _MonthDay:
    """
    "MM/DD" 形式の文字列を (月, 日) のタプルに変換する

    Args:
        text (str): "MM/DD" 形式の文字列（例: "12/29"）

    Returns:
        tuple[int, int]: (月, 日) のタプル

    Raises:
        ValueError: 形式が不正、または存在しない月日の場合
    """
    parts = text.split("/")
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise ValueError(f"Invalid month/day format: {text!r} (expected 'MM/DD')")
    month, day = int(parts[0]), int(parts[1])
    try:
        # 2000年はうるう年のため 2/29 も有効な月日として許容する
        datetime.date(2000, month, day)
    except ValueError:
        raise ValueError(f"Invalid month/day value: {text!r}") from None
    return month, day


class JapaneseHolidays:
    """
    日本の祝日を管理するクラス(オフライン版)

    祝日の定義は :mod:`flaretool.holiday.algorithms` の宣言的な
    ルールテーブルに基づいて計算されます。

    法定の祝日に加えて、単発の追加休日（:meth:`set_additional_holiday` /
    :meth:`add_custom_holidays`）や毎年繰り返すカスタム休日ルール
    （:meth:`add_custom_holiday_rule`）をインスタンス単位で登録できます。
    これらの独自休日は法定祝日の判定結果（キャッシュ）には影響しません。
    """

    _additional_holidays: dict[datetime.date, str]
    _custom_holiday_rules: list[_AnnualRule]
    _weekend_weekdays: frozenset[int]

    def __init__(self) -> None:
        self._additional_holidays = {}
        self._custom_holiday_rules = []
        self._weekend_weekdays = _DEFAULT_WEEKEND

    def is_new_year(self, date: datetime.date) -> bool:
        """
        元日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 元日であればTrue、そうでなければFalse
        """
        return matches("new_year", date)

    def is_coming_of_age_day(self, date: datetime.date) -> bool:
        """
        成人の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 成人の日であればTrue、そうでなければFalse
        """
        return matches("coming_of_age_day", date)

    def is_foundation_day(self, date: datetime.date) -> bool:
        """
        建国記念日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 建国記念日であればTrue、そうでなければFalse
        """
        return matches("foundation_day", date)

    def is_spring_equinox(self, date: datetime.date) -> bool:
        """
        春分の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 春分の日であればTrue、そうでなければFalse
        """
        return matches("spring_equinox", date)

    def is_showa_day(self, date: datetime.date) -> bool:
        """
        昭和の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 昭和の日であればTrue、そうでなければFalse
        """
        return matches("showa_day", date)

    def is_constitution_day(self, date: datetime.date) -> bool:
        """
        憲法記念日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 憲法記念日であればTrue、そうでなければFalse
        """
        return matches("constitution_day", date)

    def is_greenery_day(self, date: datetime.date) -> bool:
        """
        みどりの日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: みどりの日であればTrue、そうでなければFalse
        """
        return matches("greenery_day", date)

    def is_childrens_day(self, date: datetime.date) -> bool:
        """
        こどもの日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: こどもの日であればTrue、そうでなければFalse
        """
        return matches("childrens_day", date)

    def is_marine_day(self, date: datetime.date) -> bool:
        """
        海の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 海の日であればTrue、そうでなければFalse
        """
        return matches("marine_day", date)

    def is_mountain_day(self, date: datetime.date) -> bool:
        """
        山の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 山の日であればTrue、そうでなければFalse
        """
        return matches("mountain_day", date)

    def is_respect_for_the_aged_day(self, date: datetime.date) -> bool:
        """
        敬老の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 敬老の日であればTrue、そうでなければFalse
        """
        return matches("respect_for_the_aged_day", date)

    def is_autumn_equinox(self, date: datetime.date) -> bool:
        """
        秋分の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 秋分の日であればTrue、そうでなければFalse
        """
        return matches("autumn_equinox", date)

    def is_health_and_sports_day(self, date: datetime.date) -> bool:
        """
        スポーツの日（2019年以前は体育の日）の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: スポーツの日であればTrue、そうでなければFalse
        """
        return matches("health_and_sports_day", date)

    def is_culture_day(self, date: datetime.date) -> bool:
        """
        文化の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 文化の日であればTrue、そうでなければFalse
        """
        return matches("culture_day", date)

    def is_labour_thanksgiving_day(self, date: datetime.date) -> bool:
        """
        勤労感謝の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 勤労感謝であればTrue、そうでなければFalse
        """
        return matches("labour_thanksgiving_day", date)

    def is_emperors_birthday(self, date: datetime.date) -> bool:
        """
        天皇誕生日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 天皇誕生日であればTrue、そうでなければFalse
        """
        return matches("emperors_birthday", date)

    def is_national_holiday(self, date: datetime.date) -> bool:
        """
        国民の休日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 国民の休日であればTrue、そうでなければFalse
        """
        return algorithms.is_national_holiday(date)

    def is_transfer_holiday(self, date: datetime.date) -> bool:
        """
        振替休日チェック

        法定の振替休日（1973年4月12日の祝日法改正の施行以降）と、
        単発の追加休日が日曜日と重なった場合の翌月曜日を振替休日と
        判定します。判定は算出済みの休日名が
        「（振替休日）」で終わるかどうかに基づくため、
        祝日そのもの（例: 2026年5月4日のみどりの日）を誤って
        振替休日と判定することはありません。

        Args:
            date (datetime.date): 日付

        Returns:
            bool: 振替休日の場合はTrue、そうでない場合はFalse
        """
        name = self._holiday_name_without_custom_rules(date)
        return name is not None and name.endswith(TRANSFER_HOLIDAY_SUFFIX)

    def is_additional_holiday(self, date: datetime.date) -> bool:
        """
        追加休日チェック

        単発の追加休日（set_additional_holiday / add_custom_holidays）と、
        毎年繰り返すカスタム休日ルール（add_custom_holiday_rule）の
        いずれかに該当するかを判定します。

        Args:
            date (datetime.date): 日付

        Returns:
            bool: 追加休日の場合はTrue、そうでない場合はFalse
        """
        return (
            date in self._additional_holidays
            or self._custom_rule_holiday_name(date) is not None
        )

    def is_holiday(self, date: str | datetime.datetime | datetime.date) -> bool:
        """
        祝日（振替休日・国民の休日・追加休日を含む）の判定

        Args:
            date (str or datetime or date): 判定する日付

        Returns:
            bool: 祝日であればTrue、そうでなければFalse
        """
        return self.get_holiday_name(date) is not None

    def is_business_day(self, date: str | datetime.datetime | datetime.date) -> bool:
        """
        営業日（週末でも祝日・独自休日でもない日）の判定

        週末とみなす曜日は set_weekend で変更できます
        （デフォルトは土曜日・日曜日）。

        Args:
            date (str or datetime or date): 判定する日付

        Returns:
            bool: 営業日であればTrue、そうでなければFalse
        """
        date = self.to_date(date)
        return (
            date.weekday() not in self._weekend_weekdays
            and self.get_holiday_name(date) is None
        )

    def set_additional_holiday(self, name: str, date: datetime.date) -> None:
        """
        独自の休日を追加

        Args:
            name (str): 休日名
            date (datetime.date): 休日の日付
        """
        self._additional_holidays[date] = name

    def add_custom_holidays(
        self,
        name: str,
        dates: Iterable[str | datetime.datetime | datetime.date],
    ) -> None:
        """
        独自の休日をまとめて追加

        set_additional_holiday の一括登録版です。同じ名称で複数の日付を
        単発の追加休日として登録します。

        Args:
            name (str): 休日名
            dates (Iterable[str or datetime or date]): 休日の日付の一覧

        Raises:
            ValueError: サポートされていない日付形式が含まれる場合
        """
        for date in dates:
            self.set_additional_holiday(name, self.to_date(date))

    def add_custom_holiday_rule(self, name: str, rule: str) -> None:
        """
        毎年繰り返すカスタム休日ルールを追加

        ルール文字列の書式:
            - "MM/DD" : 毎年その日を休日とする（例: "8/15"）
            - "MM/DD-MM/DD" : 毎年その期間（両端を含む）を休日とする
              （例: "12/29-1/3"）

        開始月日が終了月日より後の場合（例: "12/29-1/3"）は年をまたぐ
        期間として扱います。判定対象の日付それ自身の年で評価されるため、
        例えば "12/29-1/3" は 2025年12月30日にも 2026年1月2日にも
        該当します（12/29～12/31 と 1/1～1/3 のどちらの側も、判定する
        日付と同じ年で照合されます）。

        注意:
            - ルールは判定時に遅延評価され、法定祝日のキャッシュには
              影響しません。
            - 法定祝日と重なる日は法定祝日名が優先されます。
            - ルールに該当する日が日曜日でも振替休日は発生しません
              （振替休日は法令に基づく祝日と単発の追加休日のみが対象）。

        Args:
            name (str): 休日名
            rule (str): ルール文字列（"MM/DD" または "MM/DD-MM/DD"）

        Raises:
            ValueError: ルール文字列の書式が不正な場合
        """
        parts = rule.split("-")
        if len(parts) == 1:
            start = end = _parse_month_day(parts[0])
        elif len(parts) == 2:
            start = _parse_month_day(parts[0])
            end = _parse_month_day(parts[1])
        else:
            raise ValueError(
                f"Invalid rule format: {rule!r} (expected 'MM/DD' or 'MM/DD-MM/DD')"
            )
        self._custom_holiday_rules.append((name, start, end))

    def clear_custom_holidays(self) -> None:
        """
        独自の休日をすべてクリア

        単発の追加休日（set_additional_holiday / add_custom_holidays）と
        毎年繰り返すカスタム休日ルール（add_custom_holiday_rule）の両方を
        削除します。週末の設定（set_weekend）は変更しません。
        """
        self._additional_holidays.clear()
        self._custom_holiday_rules.clear()

    def set_weekend(self, saturday: bool = True, sunday: bool = True) -> None:
        """
        営業日判定で週末（休業日）とみなす曜日を設定

        この設定は営業日関連の判定
        （is_business_day / get_business_date_range / add_business_days /
        count_business_days / next_business_day / previous_business_day /
        get_first_business_day / get_last_business_day）にのみ影響します。

        祝日の判定そのもの（is_holiday / get_holiday_name / 振替休日など）や、
        get_rest_days_in_range の「土曜日」「日曜日」のラベル付けには
        影響しません（これらは法令・暦に基づいたままです）。

        両方を False にすると、祝日・独自休日を除くすべての曜日が
        営業日として扱われます。

        Args:
            saturday (bool): 土曜日を週末として扱う場合はTrue（デフォルト: True）
            sunday (bool): 日曜日を週末として扱う場合はTrue（デフォルト: True）
        """
        self._weekend_weekdays = frozenset(
            weekday for weekday, is_rest in ((5, saturday), (6, sunday)) if is_rest
        )

    def _custom_rule_holiday_name(self, date: datetime.date) -> str | None:
        """
        毎年繰り返すカスタム休日ルールに該当する場合はその名称を返す

        Args:
            date (datetime.date): 判定する日付

        Returns:
            str or None: 該当するルールの休日名（該当しない場合はNone）
        """
        month_day = (date.month, date.day)
        for name, start, end in self._custom_holiday_rules:
            if start <= end:
                if start <= month_day <= end:
                    return name
            # 年をまたぐ期間（例: 12/29-1/3）は判定する日付自身の年で
            # 年末側・年始側のどちらかに該当すればよい
            elif month_day >= start or month_day <= end:
                return name
        return None

    def add_business_days(
        self, date: str | datetime.datetime | datetime.date, days: int
    ) -> datetime.date:
        """
        指定日からn営業日後（または前）の日付を取得

        days が正の場合はn営業日後、負の場合はn営業日前を返します。
        days が 0 の場合は変換した日付をそのまま返します
        （その日が営業日かどうかは判定しません）。

        週末（set_weekendの設定に従う）・祝日・独自休日をスキップします。

        Args:
            date (str or datetime or date): 起点の日付
            days (int): 進める営業日数（負の値で過去方向）

        Returns:
            datetime.date: n営業日後（前）の日付
        """
        current_date = self.to_date(date)
        if days == 0:
            return current_date
        step = datetime.timedelta(days=1 if days > 0 else -1)
        remaining = abs(days)
        while remaining > 0:
            current_date += step
            if self.is_business_day(current_date):
                remaining -= 1
        return current_date

    def next_business_day(
        self,
        date: str | datetime.datetime | datetime.date,
        *,
        include_start: bool = False,
    ) -> datetime.date:
        """
        指定日以降で直近の営業日を取得

        Args:
            date (str or datetime or date): 起点の日付
            include_start (bool): Trueの場合、起点が営業日ならその日を返す
                （デフォルト: False = 翌営業日から探索）

        Returns:
            datetime.date: 直近の営業日
        """
        current_date = self.to_date(date)
        if include_start and self.is_business_day(current_date):
            return current_date
        return self.add_business_days(current_date, 1)

    def previous_business_day(
        self,
        date: str | datetime.datetime | datetime.date,
        *,
        include_start: bool = False,
    ) -> datetime.date:
        """
        指定日以前で直近の営業日を取得

        Args:
            date (str or datetime or date): 起点の日付
            include_start (bool): Trueの場合、起点が営業日ならその日を返す
                （デフォルト: False = 前営業日から探索）

        Returns:
            datetime.date: 直近の営業日
        """
        current_date = self.to_date(date)
        if include_start and self.is_business_day(current_date):
            return current_date
        return self.add_business_days(current_date, -1)

    def count_business_days(
        self,
        start_date: str | datetime.datetime | datetime.date,
        end_date: str | datetime.datetime | datetime.date,
    ) -> int:
        """
        指定期間内（両端を含む）の営業日数を取得

        Args:
            start_date (str or datetime or date): 開始日
            end_date (str or datetime or date): 終了日

        Returns:
            int: 営業日数

        Raises:
            ValueError: 開始日が終了日より後の場合
        """
        start_date = self.to_date(start_date)
        end_date = self.to_date(end_date)
        if start_date > end_date:
            raise ValueError(
                f"start_date ({start_date}) must not be after end_date ({end_date})"
            )
        return len(self.get_business_date_range(start_date, end_date))

    def week_day(
        self, date: datetime.date, week: int, weekday: int
    ) -> datetime.date | None:
        """
        指定された日付の月の「第week weekday曜日」に該当する日付を取得

        Args:
            date (datetime.date): 対象の年月を含む日付
            week (int): 週 (1から5)
            weekday (int): 曜日 (1から7, 月曜日を1とする)

        Returns:
            datetime.date or None: 該当する日付。
            week・weekdayが範囲外の場合や、その月に第week週の
            該当曜日が存在しない場合はNone
        """
        if week < 1 or week > 5:
            return None
        if weekday < 1 or weekday > 7:
            return None
        # グローバルなcalendar.setfirstweekday()の影響を受けないよう
        # 月曜始まりのCalendarインスタンスを使用する
        lines = calendar.Calendar(firstweekday=calendar.MONDAY).monthdayscalendar(
            date.year, date.month
        )
        days = [line[weekday - 1] for line in lines if line[weekday - 1] != 0]
        if week > len(days):
            return None
        return datetime.date(date.year, date.month, days[week - 1])

    @staticmethod
    def to_date(date: str | datetime.datetime | datetime.date) -> datetime.date:
        """
        日付文字列をdateオブジェクトに変換します

        Args:
            date (str or datetime or date): 変換する日付文字列。

        Returns:
            date: 変換されたdateオブジェクト。

        Raises:
            ValueError: サポートされていない日付形式の場合に発生します。
        """
        if isinstance(date, datetime.datetime):
            return date.date()
        if isinstance(date, datetime.date):
            return date

        # ISO 8601形式 (2021-01-01, 2021-01-01 12:34:56, 20210101 など) の高速パス
        try:
            return datetime.datetime.fromisoformat(date).date()
        except ValueError:
            pass

        formats = [
            "%Y-%m-%d",  # 2021-01-01
            "%Y-%m-%d %H:%M",  # 2021-01-01 12:34
            "%Y-%m-%d %H:%M:%S",  # 2021-01-01 12:34:56
            "%Y/%m/%d",  # 2021/01/01
            "%Y/%m/%d %H:%M",  # 2021/01/01 12:34
            "%Y/%m/%d %H:%M:%S",  # 2021/01/01 12:34:56
            "%Y%m%d",  # 20210101
            "%d-%b-%Y",  # 01-Jan-2021
            "%d-%b-%Y %H:%M:%S",  # 01-Jan-2021 12:34:56
            "%m-%d-%Y",  # 01-01-2021
            "%b %d, %Y",  # Jan 01, 2021
            "%B %d, %Y",  # January 01, 2021
            "%d %b %Y",  # 01 Jan 2021
            "%d %B %Y",  # 01 January 2021
        ]

        for fmt in formats:
            try:
                return datetime.datetime.strptime(date, fmt).date()
            except ValueError:
                pass

        raise ValueError("Unsupported date format")

    @staticmethod
    def get_last_day(date: datetime.date) -> datetime.date:
        """
        指定された月の最終日を取得

        Args:
            date (datetime.date): 月を指定した日付

        Returns:
            datetime.date: 最終日の日付オブジェクト
        """
        last_day = calendar.monthrange(date.year, date.month)[1]
        return datetime.date(date.year, date.month, last_day)

    def _statutory_holiday_name(self, date: datetime.date) -> str | None:
        """
        法定祝日名（国民の休日・振替休日を含む）を取得（内部用）

        算出済みの祝日テーブルのみを参照します。単発の追加休日や
        振替休日（追加休日由来）の合成は
        :meth:`_holiday_name_without_custom_rules` が行うため、
        オンライン版はこのメソッドだけをオーバーライドすれば
        判定の優先順位が共通化されます。

        Args:
            date (datetime.date): 日付

        Returns:
            str or None: 法定祝日名（該当しない場合はNone）
        """
        return holidays_of_year(date.year).get(date)

    def _holiday_name_without_custom_rules(self, date: datetime.date) -> str | None:
        """
        毎年繰り返すカスタム休日ルールを除いた休日名を取得（内部用）

        法定祝日（国民の休日・振替休日を含む）→ 単発の追加休日 →
        追加休日が日曜日の場合の翌月曜日（振替休日）の順に判定します
        （法定祝日名が常に優先されます）。振替休日の判定元にも
        このメソッドを用いることで、カスタム休日ルールが振替休日を
        発生させないことを保証します。

        Args:
            date (datetime.date): 日付

        Returns:
            str or None: 休日名（該当しない場合はNone）
        """
        name = self._statutory_holiday_name(date)
        if name is not None:
            return name
        name = self._additional_holidays.get(date)
        if name is not None:
            return name
        # 独自の追加休日が日曜日の場合、翌月曜日は振替休日となる
        # （振替休日制度の施行日以降のみ）
        if (
            date.weekday() == 0
            and date - datetime.timedelta(days=1)
            >= algorithms.SUBSTITUTE_HOLIDAY_LAW_EFFECTIVE
        ):
            previous_name = self._holiday_name_without_custom_rules(
                date - datetime.timedelta(days=1)
            )
            if previous_name and not previous_name.endswith(TRANSFER_HOLIDAY_SUFFIX):
                return previous_name + TRANSFER_HOLIDAY_SUFFIX
        return None

    def get_holiday_name(
        self, date: str | datetime.datetime | datetime.date
    ) -> str | None:
        """
        祝日名を取得

        法定祝日（国民の休日・振替休日を含む）、単発の追加休日、
        毎年繰り返すカスタム休日ルールの順に判定します
        （法定祝日名が常に優先されます）。

        Args:
            date (datetime or date or str): 日時

        Returns:
            str: 祝日名（祝日ではない場合はNone）
        """
        date = self.to_date(date)
        name = self._holiday_name_without_custom_rules(date)
        if name is not None:
            return name
        return self._custom_rule_holiday_name(date)

    def get_holidays(self, date: str) -> list[tuple[datetime.date, str]]:
        """
        祝日の一覧を取得

        Args:
            date (str): 年 or 年月 の日時

        Raises:
            ValueError: 日時のフォーマットエラー

        Returns:
            list[tuple[datetime.date, str]]: (日付, 祝日名) のタプルのリスト。

        Note:
            v0.3.0 でタプルの並びを (祝日名, 日付) から (日付, 祝日名) に変更し、
            get_holidays_in_range / get_rest_days_in_range と統一しました。

        Example:
            >>> get_holidays("2023")
            >>> get_holidays("2023-01")
            >>> get_holidays("2023/01")
            >>> get_holidays("202301")
        """
        start_date = date
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y").date()
            end_date = datetime.date(start_date.year, 12, 31)
        except ValueError:
            pass

        if isinstance(start_date, str):
            for fmt in ["%Y/%m", "%Y-%m", "%Y%m"]:
                try:
                    start_date = datetime.datetime.strptime(start_date, fmt).date()
                    end_date = self.get_last_day(start_date)
                    break
                except ValueError:
                    pass

        if isinstance(start_date, str):
            # 完全な日付形式の解釈は to_date に委譲する（日付形式の一元化）。
            # 未対応の形式は to_date が ValueError("Unsupported date format")
            # を送出する。
            start_date = self.to_date(start_date)
            end_date = start_date

        return self.get_holidays_in_range(start_date, end_date)

    def get_rest_days_in_range(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> list[tuple[datetime.date, str]]:
        """
        特定の期間内の休みの一覧を取得（土日含む）

        「土曜日」「日曜日」のラベル付けは暦に基づいており、
        set_weekend による営業日設定の影響を受けません。

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            list[tuple[datetime.date, str]]: (日付, 名称) のタプルのリスト
        """
        rest_days = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == 5:
                rest_days.append((current_date, "土曜日"))
            elif current_date.weekday() == 6:
                rest_days.append((current_date, "日曜日"))
            else:
                holiday_name = self.get_holiday_name(current_date)
                if holiday_name is not None:
                    rest_days.append((current_date, holiday_name))
            current_date += datetime.timedelta(days=1)
        return rest_days

    def get_holidays_in_range(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> list[tuple[datetime.date, str]]:
        """
        特定の期間内の祝日一覧を取得

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            list[tuple[datetime.date, str]]: (日付, 祝日名) のタプルのリスト。
        """
        holidays = []
        current_date = start_date
        while current_date <= end_date:
            holiday_name = self.get_holiday_name(current_date)
            if holiday_name is not None:
                holidays.append((current_date, holiday_name))
            current_date += datetime.timedelta(days=1)
        return holidays

    def get_business_date_range(
        self, start_date: datetime.date, end_date: datetime.date
    ) -> list[datetime.date]:
        """
        指定期間内の営業日の一覧を取得

        週末とみなす曜日は set_weekend の設定に従います
        （デフォルトは土曜日・日曜日）。

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            list[datetime.date]: 日付のリスト
        """
        business_days = []
        current_date = start_date
        while current_date <= end_date:
            if self.is_business_day(current_date):
                business_days.append(current_date)
            current_date += datetime.timedelta(days=1)
        return business_days

    def get_first_business_day(
        self, date: datetime.date, days: int = 1
    ) -> datetime.date:
        """
        指定された月の営業日を取得（デフォルトは第1営業日）

        Args:
            date (datetime.date): 日付
            days (int): 営業日数（デフォルトは1）

        Returns:
            datetime.date: 営業日
        """
        first_date = datetime.date(date.year, date.month, 1)
        return self.get_business_date_range(first_date, self.get_last_day(first_date))[
            days - 1
        ]

    def get_last_business_day(self, date: datetime.date) -> datetime.date:
        """
        指定された月の最終営業日を取得

        Args:
            date (datetime.date): 日付

        Returns:
            datetime.date: 最終営業日
        """
        first_date = datetime.date(date.year, date.month, 1)
        return self.get_business_date_range(first_date, self.get_last_day(first_date))[
            -1
        ]

    def print_calendar(self, date: datetime.date) -> None:
        """
        カレンダーを出力

        日曜始まりで、日曜日は赤・土曜日は青・祝日は緑で表示します。

        Args:
            date (datetime.date): 対象年月
        """
        # 重い依存を避けるため関数内でインポート
        from flaretool.constants import ConsoleColor as Color

        year = date.year
        month = date.month

        def format_day(day: int, weekday: int) -> str:
            if weekday == 0:
                return f"{Color.RED}{day:2d}{Color.RESET} "
            if weekday == 6:
                return f"{Color.BLUE}{day:2d}{Color.RESET} "
            if self.get_holiday_name(datetime.date(year, month, day)):
                return f"{Color.GREEN}{day:2d}{Color.RESET} "
            return f"{day:2d} "

        # グローバルなcalendar.setfirstweekday()の状態を変更しないよう
        # 日曜始まりのCalendarインスタンスを使用する
        cal = calendar.Calendar(firstweekday=calendar.SUNDAY).monthdayscalendar(
            year, month
        )

        # 月と年を出力
        print("    ", calendar.month_name[month], year)
        print("Su Mo Tu We Th Fr Sa")

        # カレンダーを出力
        for week in cal:
            line = ""
            for w, day in enumerate(week):
                if day == 0:
                    line += "   "
                else:
                    line += format_day(day, w)
            print(line)

    def get_date_information(
        self, date: datetime.date
    ) -> tuple[int, str, int, str | None]:
        """
        指定された日付から週番号、曜日、および祝日の名称を取得

        Args:
            date (datetime.date): 日付

        Returns:
            tuple: 週番号(int)(0-4)、曜日(str)、曜日(int)(0-6)、祝日の名称(str)のタプル
        """
        _, last_day = calendar.monthrange(date.year, date.month)
        first_day = datetime.date(date.year, date.month, 1)
        if first_day.weekday() == 6:
            first_sunday = first_day
        else:
            first_sunday = first_day + datetime.timedelta(
                days=(6 - first_day.weekday() + 1)
            )
        weeks = ((date - first_sunday).days + 1) // 7
        if date.day > last_day - 6:
            weeks += 1
        week_number = weeks

        weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        weekday = weekdays[date.weekday()]

        holiday_name = self.get_holiday_name(date)

        return week_number, weekday, date.weekday(), holiday_name

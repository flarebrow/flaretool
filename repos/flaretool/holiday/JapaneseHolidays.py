#!/bin/python
# -*- coding: utf-8 -*-
import datetime
import calendar
from typing import Union

__all__ = []


class JapaneseHolidays:
    """
    日本の祝日を管理するクラス(オフライン版)
    """
    _additional_holidays: dict[datetime.date, str]

    def __init__(self):
        self._additional_holidays = {}

    def is_new_year(self, date: datetime.date) -> bool:
        """
        元日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 元日であればTrue、そうでなければFalse
        """
        return date.month == 1 and date.day == 1

    def is_coming_of_age_day(self, date: datetime.date) -> bool:
        """
        成人の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 成人の日であればTrue、そうでなければFalse
        """
        if date.year < 2000:
            return date.month == 1 and date.day == 15
        return date.month == 1 and date.weekday() == 0 and 8 <= date.day <= 14

    def is_foundation_day(self, date: datetime.date) -> bool:
        """
        建国記念日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 建国記念日であればTrue、そうでなければFalse
        """
        if date.year < 1967:
            return False
        return date.month == 2 and date.day == 11

    def is_spring_equinox(self, date: datetime.date) -> bool:
        """
        春分の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 春分の日であればTrue、そうでなければFalse
        """
        if date.year < 1900 or date.year > 2099:
            return False
        spring_equinox = 20.8431 + 0.242194 * \
            (date.year - 1980) - (date.year - 1980) // 4
        return date == datetime.date(date.year, 3, int(spring_equinox))

    def is_showa_day(self, date: datetime.date) -> bool:
        """
        昭和の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 昭和の日であればTrue、そうでなければFalse
        """
        if 1989 <= date.year <= 2006:
            return False
        return date.month == 4 and date.day == 29

    def is_constitution_day(self, date: datetime.date) -> bool:
        """
        憲法記念日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 憲法記念日であればTrue、そうでなければFalse
        """
        return date.month == 5 and date.day == 3

    def is_greenery_day(self, date: datetime.date) -> bool:
        """
        みどりの日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: みどりの日であればTrue、そうでなければFalse
        """
        if date.year < 1989:
            return False
        if 1989 <= date.year <= 2006:
            return date.month == 4 and date.day == 29
        return date.month == 5 and date.day == 4

    def is_childrens_day(self, date: datetime.date) -> bool:
        """
        こどもの日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: こどもの日であればTrue、そうでなければFalse
        """
        return date.month == 5 and date.day == 5

    def is_marine_day(self, date: datetime.date) -> bool:
        """
        海の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 海の日であればTrue、そうでなければFalse
        """
        if date.year < 1996:
            return False
        if date.month != 7:
            return False
        if date.year < 2003:
            return date.day == 20
        if date.year == 2020:
            return date.day == 23
        if date.year == 2021:
            return date.day == 22
        return date.weekday() == 0 and 15 <= date.day <= 21

    def is_mountain_day(self, date: datetime.date) -> bool:
        """
        山の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 山の日であればTrue、そうでなければFalse
        """
        if date.year < 2016:
            return False
        if date.year == 2020 and date.month == 8:
            return date.day == 10
        if date.year == 2021 and date.month == 8:
            return date.day == 8
        return date.month == 8 and date.day == 11

    def is_respect_for_the_aged_day(self, date: datetime.date) -> bool:
        """
        敬老の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 敬老の日であればTrue、そうでなければFalse
        """
        if date.year <= 2002:
            return date.month == 9 and date.day == 15
        return date.month == 9 and date.weekday() == 0 and 15 <= date.day <= 21

    def is_autumn_equinox(self, date: datetime.date) -> bool:
        """
        秋分の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 秋分の日であればTrue、そうでなければFalse
        """
        if date.year < 1900 or date.year > 2099:
            return False
        autumn_equinox = 23.2488 + 0.242194 * \
            (date.year - 1980) - (date.year - 1980) // 4
        return date == datetime.date(date.year, 9, int(autumn_equinox))

    def is_health_and_sports_day(self, date: datetime.date) -> bool:
        """
        スポーツの日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: スポーツの日であればTrue、そうでなければFalse
        """
        if date.year < 2000:
            return date.month == 10 and date.day == 10
        if date.year == 2020:
            return date == datetime.date(2020, 7, 24)
        if date.year == 2021:
            return date == datetime.date(2021, 7, 23)
        if date.year >= 2020 and date.month == 10 and date.day == self.week_day(date, 2, 1).day:
            return True

        return date.month == 10 and date.weekday() == 0 and 8 <= date.day <= 14

    def is_culture_day(self, date: datetime.date) -> bool:
        """
        文化の日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 文化の日であればTrue、そうでなければFalse
        """
        return date.month == 11 and date.day == 3

    def is_labour_thanksgiving_day(self, date: datetime.date) -> bool:
        """
        勤労感謝の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 勤労感謝であればTrue、そうでなければFalse
        """
        return date.month == 11 and date.day == 23

    def is_emperors_birthday(self, date: datetime.date) -> bool:
        """
        天皇誕生日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 天皇誕生日であればTrue、そうでなければFalse
        """
        # 1948-1988年
        if date.year in range(1948, 1988 + 1) and date.month == 4 and date.day == 29:
            return True
        # 1989-2018年
        # 2019: 国民の祝日に関する法律(昭和23年法律第178号)の一部改正
        elif date.year in range(1989, 2018 + 1) and date.month == 12 and date.day == 23:
            return True
        # 2019: 国民の祝日に関する法律(昭和23年法律第178号)の一部改正
        elif date.year >= 2020 and date.month == 2 and date.day == 23:
            return True
        return False

    def is_national_holiday(self, date: datetime.date) -> bool:
        """
        国民の休日の判定

        Args:
            date (datetime.date): 判定する日付

        Returns:
            bool: 国民の休日であればTrue、そうでなければFalse
        """
        if datetime.date(2019, 4, 30) <= date <= datetime.date(2019, 5, 2):
            return True
        if date in [
            datetime.date(1989, 2, 24),
            datetime.date(1990, 11, 12),
            datetime.date(1993, 6, 9),
            datetime.date(2019, 10, 22),
        ]:
            return True
        if 2007 <= date.year and date.month == 5:
            return False
        if date.year <= 1985:
            return False
        previous_date = date - datetime.timedelta(days=1)
        next_date = date + datetime.timedelta(days=1)
        is_may_holiday = self.is_constitution_day(
            previous_date) and self.is_childrens_day(next_date)
        is_sep_holiday = self.is_respect_for_the_aged_day(
            previous_date) and self.is_autumn_equinox(next_date)
        if (is_may_holiday or is_sep_holiday) and date.weekday() < 6:
            return True
        return False

    def is_transfer_holiday(self, date: datetime.date) -> bool:
        """
        振替休日チェック

        Args:
            date (datetime.date): 日付

        Returns:
            bool: 振替休日の場合はTrue、そうでない場合はFalse
        """
        if date.weekday() == 0:  # 月曜日の場合
            return bool(self.get_holiday_name(date - datetime.timedelta(days=1)))
        if date.year in [2008, 2009, 2014, 2015, 2020, 2025] and date.month == 5 and date.day == 6:
            return True
        return False

    def is_additional_holiday(self, date: datetime.date) -> bool:
        """
        追加休日チェック

        Args:
            date (datetime.date): 日付

        Returns:
            bool: 追加休日の場合はTrue、そうでない場合はFalse
        """
        return date in self._additional_holidays.keys()

    def set_additional_holiday(self, name: str, date: datetime.date):
        """
        独自の休日を追加

        Args:
            name (str): 休日名
            date (datetime.date): 休日の日付
        """
        self._additional_holidays[date] = name

    def week_day(self, date: datetime.date, week: int, weekday: int) -> datetime.date:
        """
        指定された日付の週と曜日に該当する日付を取得

        Args:
            date (datetime.date): 日付
            week (int): 週 (1から5)
            weekday (int): 曜日 (1から7, 月曜日を1とする)

        Returns:
            datetime.date: 週と曜日に該当する日付
        """
        if week < 1 or week > 5:
            return None
        if weekday < 1 or weekday > 7:
            return None
        lines = calendar.monthcalendar(date.year, date.month)
        days = []
        for line in lines:
            if line[weekday - 1] == 0:
                continue
            days.append(line[weekday - 1])
        return datetime.date(date.year, date.month, days[week - 1])

    @staticmethod
    def to_date(date: Union[
        str, datetime.datetime, datetime.date
    ]) -> datetime.date:
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

        formats = [
            '%Y-%m-%d',           # 2021-01-01
            '%Y-%m-%d %H:%M',     # 2021-01-01 12:34
            '%Y-%m-%d %H:%M:%S',  # 2021-01-01 12:34:56
            '%Y/%m/%d',           # 2021/01/01
            '%Y/%m/%d %H:%M',     # 2021/01/01 12:34
            '%Y/%m/%d %H:%M:%S',  # 2021/01/01 12:34:56
            '%Y%m%d',             # 20210101
            '%d-%b-%Y',           # 01-Jan-2021
            '%d-%b-%Y %H:%M:%S',  # 01-Jan-2021 12:34:56
            '%m-%d-%Y',           # 01-01-2021
            '%b %d, %Y',          # Jan 01, 2021
            '%B %d, %Y',          # January 01, 2021
            '%d %b %Y',           # 01 Jan 2021
            '%d %B %Y',           # 01 January 2021
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
        last_date = datetime.date(date.year, date.month, last_day)
        return last_date

    def get_holiday_name(self, date: Union[
        str, datetime.datetime, datetime.date
    ]) -> Union[str, None]:
        """
        祝日名を取得

        Args:
            date (datetime or date or str): 日時

        Returns:
            str: 祝日名（祝日ではない場合はNone）
        """
        date = self.to_date(date)
        if self.is_new_year(date):
            return "元日"
        elif self.is_coming_of_age_day(date):
            return "成人の日"
        elif self.is_foundation_day(date):
            return "建国記念の日"
        elif self.is_spring_equinox(date):
            return "春分の日"
        elif self.is_showa_day(date):
            if date.year < 1990:
                return "天皇誕生日"
            return "昭和の日"
        elif self.is_constitution_day(date):
            return "憲法記念日"
        elif self.is_national_holiday(date):
            return "国民の休日"
        elif self.is_greenery_day(date):
            return "みどりの日"
        elif self.is_childrens_day(date):
            return "こどもの日"
        elif self.is_marine_day(date):
            return "海の日"
        elif self.is_mountain_day(date):
            return "山の日"
        elif self.is_respect_for_the_aged_day(date):
            return "敬老の日"
        elif self.is_autumn_equinox(date):
            return "秋分の日"
        elif self.is_health_and_sports_day(date):
            if date.year < 2020:
                return "体育の日"
            return "スポーツの日"
        elif self.is_culture_day(date):
            return "文化の日"
        elif self.is_labour_thanksgiving_day(date):
            return "勤労感謝の日"
        elif self.is_emperors_birthday(date):
            return "天皇誕生日"
        elif self.is_transfer_holiday(date):
            return self.get_holiday_name(date - datetime.timedelta(days=1)) + "（振替休日）"
        elif self.is_additional_holiday(date):
            return self._additional_holidays.get(date)
        else:
            return None

    def get_holidays(self, date: str) -> list[tuple[str, datetime.datetime]]:
        """
        祝日の一覧を取得

        Args:
            date (str): 年 or 年月 の日時

        Raises:
            ValueError: 日時のフォーマットエラー

        Returns:
            list[tuple[str, datetime.datetime]]: 祝日リスト

        Example:
            >>> get_holidays("2023")
            >>> get_holidays("2023-01")
            >>> get_holidays("2023/01")
            >>> get_holidays("202301")
        """
        start_date = date
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y').date()
            end_date = datetime.date(start_date.year, 12, 31)
        except ValueError:
            pass

        if isinstance(start_date, str):
            for fmt in ['%Y/%m', '%Y-%m', '%Y%m']:
                try:
                    start_date = datetime.datetime.strptime(
                        start_date, fmt).date()
                    end_date = self.get_last_day(start_date)
                    break
                except ValueError:
                    pass

        if isinstance(start_date, str):
            for fmt in ['%Y/%m/%d', '%Y-%m-%d', '%Y%m%d']:
                try:
                    start_date = datetime.datetime.strptime(
                        start_date, fmt).date()
                    end_date = start_date
                    break
                except ValueError:
                    pass

        if not isinstance(start_date, datetime.date):
            raise ValueError("Unsupported date format")

        holidays = []
        current_date = start_date
        while current_date <= end_date:
            holiday_name = self.get_holiday_name(current_date)
            if holiday_name is not None:
                holidays.append((holiday_name, current_date))
            current_date += datetime.timedelta(days=1)
        return holidays

    def get_rest_days_in_range(self, start_date: datetime.date, end_date: datetime.date) -> list[tuple[str, datetime.datetime]]:
        """
        特定の期間内の休みの一覧を取得（土日含む）

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            list[tuple[str, datetime.datetime]]: 休み一覧
        """
        holidays = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == 5:
                holidays.append(("土曜日", current_date))
            elif current_date.weekday() == 6:
                holidays.append(("日曜日", current_date))
            else:
                holiday_name = self.get_holiday_name(current_date)
                if holiday_name is not None:
                    holidays.append((holiday_name, current_date))
            current_date += datetime.timedelta(days=1)
        return holidays

    def get_holidays_in_range(self, start_date: datetime.date, end_date: datetime.date) -> list[tuple[str, datetime.datetime]]:
        """
        特定の期間内の祝日一覧を取得

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            list[tuple[str, datetime.datetime]]: 祝日一覧
        """
        holidays = []
        current_date = start_date
        while current_date <= end_date:
            holiday_name = self.get_holiday_name(current_date)
            if holiday_name is not None:
                holidays.append((holiday_name, current_date))
            current_date += datetime.timedelta(days=1)
        return holidays

    def get_business_date_range(self, start_date: datetime.date, end_date: datetime.date) -> list[datetime.date]:
        """
        指定期間内の営業日の一覧を取得

        Args:
            start_date (datetime.date): 開始日
            end_date (datetime.date): 終了日

        Returns:
            list[datetime.date]: 日付のリスト
        """
        business_days = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # 土曜日(5)と日曜日(6)を除外
                holiday_name = self.get_holiday_name(current_date)
                if holiday_name is None:
                    business_days.append(current_date)
            current_date += datetime.timedelta(days=1)
        return business_days

    def get_first_business_day(self, date: datetime.date, days: int = 1) -> datetime.date:
        """
        指定された月の営業日を取得（デフォルトは第1営業日）

        Args:
            date (datetime.date): 日付
            days (int): 営業日数（デフォルトは1）

        Returns:
            datetime.date: 営業日
        """
        return self.get_business_date_range(
            datetime.date(date.year, date.month, 1),
            self.get_last_day(datetime.date(date.year, date.month, 1)),
        )[days - 1]

    def get_last_business_day(self, date: datetime.date) -> datetime.date:
        """
        指定された月の最終営業日を取得

        Args:
            date (datetime.date): 日付

        Returns:
            datetime.date: 最終営業日
        """
        return self.get_business_date_range(
            datetime.date(date.year, date.month, 1),
            self.get_last_day(datetime.date(date.year, date.month, 1)),
        )[-1]

    def print_calendar(self, date: datetime.date):
        """
        カレンダーを出力

        Args:
            date (datetime.date): 対象年月

        """
        from flaretool.constants import ConsoleColor as Color
        year = date.year
        month = date.month

        def format_day(year, month, day, weekday):
            if weekday == 0:
                return f'{Color.RED}{day:2d}{Color.RESET} '
            elif weekday == 6:
                return f'{Color.BLUE}{day:2d}{Color.RESET} '
            else:
                if self.get_holiday_name(datetime.date(year, month, day)):
                    return f'{Color.GREEN}{day:2d}{Color.RESET} '
                else:
                    return f"{day:2d} "
        calendar.setfirstweekday(calendar.SUNDAY)

        # カレンダーを取得
        cal = calendar.monthcalendar(year, month)

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
                    line += format_day(year, month, day, w)
            print(line)
        calendar.setfirstweekday(calendar.MONDAY)

    def get_date_information(self, date: datetime.date) -> tuple:
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
            first_sunday = first_day + \
                datetime.timedelta(days=(6 - first_day.weekday() + 1))
        weeks = ((date - first_sunday).days + 1) // 7
        if date.day > last_day - 6:
            weeks += 1
        week_number = weeks

        weekdays = ['Monday', 'Tuesday', 'Wednesday',
                    'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = weekdays[date.weekday()]

        holiday_name = self.get_holiday_name(date)

        return week_number, weekday, date.weekday(), holiday_name

#!/bin/python
# -*- coding: utf-8 -*-
import datetime
import calendar


class JapaneseHolidays:
    """
    日本の祝日を取得するクラス
    """

    def __init__(self):
        pass

    def is_new_year(self, date: datetime.date) -> bool:
        return date.month == 1 and date.day == 1

    def is_coming_of_age_day(self, date: datetime.date) -> bool:
        return date.month == 1 and date.weekday() == 0 and 8 <= date.day <= 14

    def is_foundation_day(self, date: datetime.date) -> bool:
        return date.month == 2 and date.day == 11

    def is_spring_equinox(self, date: datetime.date) -> bool:
        if date.year < 1900 or date.year > 2099:
            return False
        spring_equinox = 20.8431 + 0.242194 * \
            (date.year - 1980) - (date.year - 1980) // 4
        return date == datetime.date(date.year, 3, int(spring_equinox))

    def is_showa_day(self, date: datetime.date) -> bool:
        return date.month == 4 and date.day == 29

    def is_constitution_day(self, date: datetime.date) -> bool:
        return date.month == 5 and date.day == 3

    def is_greenery_day(self, date: datetime.date) -> bool:
        return date.month == 5 and date.day == 4

    def is_childrens_day(self, date: datetime.date) -> bool:
        return date.month == 5 and date.day == 5

    def is_marine_day(self, date: datetime.date) -> bool:
        return date.month == 7 and date.weekday() == 0 and 15 <= date.day <= 21

    def is_mountain_day(self, date: datetime.date) -> bool:
        return date.month == 8 and date.day == 11

    def is_respect_for_the_aged_day(self, date: datetime.date) -> bool:
        return date.month == 9 and date.weekday() == 0 and 15 <= date.day <= 21

    def is_autumn_equinox(self, date: datetime.date) -> bool:
        if date.year < 1900 or date.year > 2099:
            return False
        autumn_equinox = 23.2488 + 0.242194 * \
            (date.year - 1980) - (date.year - 1980) // 4
        return date == datetime.date(date.year, 9, int(autumn_equinox))

    def is_health_and_sports_day(self, date: datetime.date) -> bool:
        # 2020: 国民の祝日に関する法律(昭和23年法律第178号)の特例
        if date.year == 2020:
            if date == datetime.date(2020, 7, 24):
                return True
            return False
        # 2021: 五輪特別措置法改正案
        if date.year == 2021:
            if date == datetime.date(2021, 7, 23):
                return True
            return False
        # 2020: 国民の祝日に関する法律の一部を改正する法律(平成30年法律第57号)
        #       国民の祝日に関する法律(昭和23年法律第178号)の特例
        if date.year >= 2020 and date.month == 10 and date.day == self._week_day(date, 2, 1).day:
            return True

        return date.month == 10 and date.weekday() == 0 and 8 <= date.day <= 14

    def is_culture_day(self, date: datetime.date) -> bool:
        return date.month == 11 and date.day == 3

    def is_labour_thanksgiving_day(self, date: datetime.date) -> bool:
        return date.month == 11 and date.day == 23

    def is_emperors_birthday(self, date: datetime.date) -> bool:
        # 1948-1988年
        if date.year in range(1948, 1988 + 1) and date.month == 4 and date.day == 29:
            return True
        # 1988-2018年
        # 2019: 国民の祝日に関する法律(昭和23年法律第178号)の一部改正
        elif date.year in range(1988, 2018 + 1) and date.month == 12 and date.day == 23:
            return True
        # 2019: 国民の祝日に関する法律(昭和23年法律第178号)の一部改正
        elif date.year >= 2020 and date.month == 2 and date.day == 23:
            return True
        return False

    def is_transfer_holiday(self, date: datetime.date) -> bool:
        if date.weekday() == 0:  # 日曜日の場合
            previous_date = date - datetime.timedelta(days=1)
            return self.get_holiday_name(previous_date)
        return False

    def _week_day(self, date: datetime.date, week: int, weekday: int) -> datetime.date:
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

    def _to_date(self, value):
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value

    def get_holiday_name(self, date) -> str:
        date = self._to_date(date)
        if self.is_new_year(date):
            return "元日"
        elif self.is_coming_of_age_day(date):
            return "成人の日"
        elif self.is_foundation_day(date):
            return "建国記念の日"
        elif self.is_spring_equinox(date):
            return "春分の日"
        elif self.is_showa_day(date):
            return "昭和の日"
        elif self.is_constitution_day(date):
            return "憲法記念日"
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
            return "スポーツの日"
        elif self.is_culture_day(date):
            return "文化の日"
        elif self.is_labour_thanksgiving_day(date):
            return "勤労感謝の日"
        elif self.is_emperors_birthday(date):
            return "天皇誕生日"
        elif self.is_transfer_holiday(date):
            return self.is_transfer_holiday(date) + "（振替休日）"
        else:
            return None

    def get_holidays_in_range(self, start_datetime: datetime.date, end_datetime: datetime.date) -> list[tuple[str, datetime.datetime]]:
        """
        特定の期間内の祝日一覧を取得

        Args:
            start_datetime (datetime.date): 開始日
            end_datetime (datetime.date): 終了日

        Returns:
            list[tuple[str, datetime.datetime]]: 祝日一覧
        """
        holidays = []
        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            holiday_name = self.get_holiday_name(current_datetime)
            if holiday_name is not None:
                holidays.append((holiday_name, current_datetime))
            current_datetime += datetime.timedelta(days=1)
        return holidays

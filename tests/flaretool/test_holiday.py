#!/bin/python
# -*- coding: utf-8 -*-
import unittest
from flaretool.holiday import JapaneseHolidays
import datetime
from unittest.mock import patch
from io import StringIO

import calendar


class JapaneseHolidaysTest(unittest.TestCase):
    def setUp(self):
        self.holidays = JapaneseHolidays()

    def test_is_new_year(self):
        date = datetime.date(2023, 1, 1)
        self.assertTrue(self.holidays.is_new_year(date))

        date = datetime.date(2023, 1, 2)
        self.assertFalse(self.holidays.is_new_year(date))

    def test_is_coming_of_age_day(self):
        date = datetime.date(2023, 1, 9)
        self.assertTrue(self.holidays.is_coming_of_age_day(date))

        date = datetime.date(2023, 1, 15)
        self.assertFalse(self.holidays.is_coming_of_age_day(date))

    def test_is_foundation_day(self):
        date = datetime.date(2023, 2, 11)
        self.assertTrue(self.holidays.is_foundation_day(date))
        self.holidays.get_holiday_name(date)

        date = datetime.date(2023, 2, 12)
        self.assertFalse(self.holidays.is_foundation_day(date))

        date = datetime.date(1965, 2, 12)
        self.assertFalse(self.holidays.is_foundation_day(date))

    def test_is_spring_equinox(self):
        date = datetime.date(2023, 3, 21)
        self.assertTrue(self.holidays.is_spring_equinox(date))

        date = datetime.date(2023, 3, 22)
        self.assertFalse(self.holidays.is_spring_equinox(date))

        date = datetime.date(1800, 1, 1)
        self.assertFalse(self.holidays.is_spring_equinox(date))

    def test_is_showa_day(self):
        date = datetime.date(2023, 4, 29)
        self.assertTrue(self.holidays.is_showa_day(date))
        self.holidays.get_holiday_name(date)

        date = datetime.date(2023, 4, 30)
        self.assertFalse(self.holidays.is_showa_day(date))

    def test_is_constitution_day(self):
        date = datetime.date(2023, 5, 3)
        self.assertTrue(self.holidays.is_constitution_day(date))

        date = datetime.date(2023, 5, 4)
        self.assertFalse(self.holidays.is_constitution_day(date))

    def test_is_greenery_day(self):
        date = datetime.date(2023, 5, 4)
        self.assertTrue(self.holidays.is_greenery_day(date))

        date = datetime.date(2023, 5, 5)
        self.assertFalse(self.holidays.is_greenery_day(date))

    def test_is_childrens_day(self):
        date = datetime.date(2023, 5, 5)
        self.assertTrue(self.holidays.is_childrens_day(date))

        date = datetime.date(2023, 5, 6)
        self.assertFalse(self.holidays.is_childrens_day(date))

    def test_is_marine_day(self):
        date = datetime.date(2023, 7, 17)
        self.assertTrue(self.holidays.is_marine_day(date))

        date = datetime.date(2023, 7, 22)
        self.assertFalse(self.holidays.is_marine_day(date))

    def test_is_mountain_day(self):
        date = datetime.date(2023, 8, 11)
        self.assertTrue(self.holidays.is_mountain_day(date))

        date = datetime.date(2023, 8, 12)
        self.assertFalse(self.holidays.is_mountain_day(date))

    def test_is_respect_for_the_aged_day(self):
        date = datetime.date(2023, 9, 18)
        self.assertTrue(self.holidays.is_respect_for_the_aged_day(date))

        date = datetime.date(2023, 9, 22)
        self.assertFalse(self.holidays.is_respect_for_the_aged_day(date))

    def test_is_autumn_equinox(self):
        date = datetime.date(2023, 9, 23)
        self.assertTrue(self.holidays.is_autumn_equinox(date))
        self.holidays.get_holiday_name(date)

        date = datetime.date(2023, 9, 24)
        self.assertFalse(self.holidays.is_autumn_equinox(date))

        date = datetime.date(1800, 1, 1)
        self.assertFalse(self.holidays.is_autumn_equinox(date))

    def test_is_health_and_sports_day(self):
        date = datetime.date(2023, 10, 9)
        self.assertTrue(self.holidays.is_health_and_sports_day(date))

        date = datetime.date(2023, 10, 15)
        self.assertFalse(self.holidays.is_health_and_sports_day(date))

        date = datetime.date(2020, 7, 24)
        self.assertTrue(self.holidays.is_health_and_sports_day(date))

        date = datetime.date(2020, 7, 25)
        self.assertFalse(self.holidays.is_health_and_sports_day(date))

        date = datetime.date(2021, 7, 23)
        self.assertTrue(self.holidays.is_health_and_sports_day(date))

        date = datetime.date(2021, 7, 24)
        self.assertFalse(self.holidays.is_health_and_sports_day(date))

    def test_is_culture_day(self):
        date = datetime.date(2023, 11, 3)
        self.assertTrue(self.holidays.is_culture_day(date))

        date = datetime.date(2023, 11, 4)
        self.assertFalse(self.holidays.is_culture_day(date))

    def test_is_labour_thanksgiving_day(self):
        date = datetime.date(2023, 11, 23)
        self.assertTrue(self.holidays.is_labour_thanksgiving_day(date))

        date = datetime.date(2023, 11, 24)
        self.assertFalse(self.holidays.is_labour_thanksgiving_day(date))

    def test_is_emperors_birthday(self):
        date = datetime.date(2023, 2, 23)
        self.assertTrue(self.holidays.is_emperors_birthday(date))

        date = datetime.date(1950, 4, 29)
        self.assertTrue(self.holidays.is_emperors_birthday(date))

        date = datetime.date(1989, 12, 23)
        self.assertTrue(self.holidays.is_emperors_birthday(date))

    def test_is_transfer_holiday(self):
        date = datetime.date(2023, 1, 2)
        self.assertTrue(self.holidays.is_transfer_holiday(date))

    def test_is_additional_holiday(self):
        date = datetime.date(2023, 6, 12)
        self.holidays.set_additional_holiday("Additional Holiday", date)
        self.assertTrue(self.holidays.is_additional_holiday(date))
        self.assertEqual(self.holidays.get_holiday_name(
            date), "Additional Holiday")

    def test_set_additional_holiday(self):
        date = datetime.date(2023, 12, 25)
        self.holidays.set_additional_holiday("Additional Holiday", date)
        self.assertEqual(
            self.holidays._additional_holidays[date], "Additional Holiday")

    def test_week_day(self):
        date = datetime.date(2023, 6, 10)
        expected_date = datetime.date(2023, 6, 12)
        self.assertEqual(self.holidays.week_day(date, 2, 1), expected_date)
        self.assertIsNone(self.holidays.week_day(date, 0, 0))
        self.assertIsNone(self.holidays.week_day(date, 1, 0))

    def test__to_date(self):
        datetime_value = datetime.datetime(2023, 6, 10, 12, 30, 0)
        expected_date = datetime.date(2023, 6, 10)
        self.assertEqual(self.holidays._to_date(datetime_value), expected_date)

        date_value = datetime.date(2023, 6, 10)
        self.assertEqual(self.holidays._to_date(date_value), date_value)

    def test_get_last_day(self):
        date = datetime.date(2023, 6, 10)
        expected_date = datetime.date(2023, 6, 30)
        self.assertEqual(self.holidays.get_last_day(date), expected_date)

    def test_get_holiday_name(self):
        date = datetime.date(2023, 1, 1)
        expected_name = "元日"
        self.assertEqual(self.holidays.get_holiday_name(date), expected_name)

        date = datetime.date(2023, 5, 4)
        expected_name = "みどりの日"
        self.assertEqual(self.holidays.get_holiday_name(date), expected_name)

        date = datetime.date(2023, 12, 24)
        expected_name = None  # Not a holiday
        self.assertEqual(self.holidays.get_holiday_name(date), expected_name)

        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 12, 31)
        self.assertEqual(
            self.holidays.get_rest_days_in_range(
                start_date, end_date),
            [
                ('日曜日', datetime.date(2023, 1, 1)),
                ('元日（振替休日）', datetime.date(2023, 1, 2)),
                ('土曜日', datetime.date(2023, 1, 7)),
                ('日曜日', datetime.date(2023, 1, 8)),
                ('成人の日', datetime.date(2023, 1, 9)),
                ('土曜日', datetime.date(2023, 1, 14)),
                ('日曜日', datetime.date(2023, 1, 15)),
                ('土曜日', datetime.date(2023, 1, 21)),
                ('日曜日', datetime.date(2023, 1, 22)),
                ('土曜日', datetime.date(2023, 1, 28)),
                ('日曜日', datetime.date(2023, 1, 29)),
                ('土曜日', datetime.date(2023, 2, 4)),
                ('日曜日', datetime.date(2023, 2, 5)),
                ('土曜日', datetime.date(2023, 2, 11)),
                ('日曜日', datetime.date(2023, 2, 12)),
                ('土曜日', datetime.date(2023, 2, 18)),
                ('日曜日', datetime.date(2023, 2, 19)),
                ('天皇誕生日', datetime.date(2023, 2, 23)),
                ('土曜日', datetime.date(2023, 2, 25)),
                ('日曜日', datetime.date(2023, 2, 26)),
                ('土曜日', datetime.date(2023, 3, 4)),
                ('日曜日', datetime.date(2023, 3, 5)),
                ('土曜日', datetime.date(2023, 3, 11)),
                ('日曜日', datetime.date(2023, 3, 12)),
                ('土曜日', datetime.date(2023, 3, 18)),
                ('日曜日', datetime.date(2023, 3, 19)),
                ('春分の日', datetime.date(2023, 3, 21)),
                ('土曜日', datetime.date(2023, 3, 25)),
                ('日曜日', datetime.date(2023, 3, 26)),
                ('土曜日', datetime.date(2023, 4, 1)),
                ('日曜日', datetime.date(2023, 4, 2)),
                ('土曜日', datetime.date(2023, 4, 8)),
                ('日曜日', datetime.date(2023, 4, 9)),
                ('土曜日', datetime.date(2023, 4, 15)),
                ('日曜日', datetime.date(2023, 4, 16)),
                ('土曜日', datetime.date(2023, 4, 22)),
                ('日曜日', datetime.date(2023, 4, 23)),
                ('土曜日', datetime.date(2023, 4, 29)),
                ('日曜日', datetime.date(2023, 4, 30)),
                ('憲法記念日', datetime.date(2023, 5, 3)),
                ('みどりの日', datetime.date(2023, 5, 4)),
                ('こどもの日', datetime.date(2023, 5, 5)),
                ('土曜日', datetime.date(2023, 5, 6)),
                ('日曜日', datetime.date(2023, 5, 7)),
                ('土曜日', datetime.date(2023, 5, 13)),
                ('日曜日', datetime.date(2023, 5, 14)),
                ('土曜日', datetime.date(2023, 5, 20)),
                ('日曜日', datetime.date(2023, 5, 21)),
                ('土曜日', datetime.date(2023, 5, 27)),
                ('日曜日', datetime.date(2023, 5, 28)),
                ('土曜日', datetime.date(2023, 6, 3)),
                ('日曜日', datetime.date(2023, 6, 4)),
                ('土曜日', datetime.date(2023, 6, 10)),
                ('日曜日', datetime.date(2023, 6, 11)),
                ('土曜日', datetime.date(2023, 6, 17)),
                ('日曜日', datetime.date(2023, 6, 18)),
                ('土曜日', datetime.date(2023, 6, 24)),
                ('日曜日', datetime.date(2023, 6, 25)),
                ('土曜日', datetime.date(2023, 7, 1)),
                ('日曜日', datetime.date(2023, 7, 2)),
                ('土曜日', datetime.date(2023, 7, 8)),
                ('日曜日', datetime.date(2023, 7, 9)),
                ('土曜日', datetime.date(2023, 7, 15)),
                ('日曜日', datetime.date(2023, 7, 16)),
                ('海の日', datetime.date(2023, 7, 17)),
                ('土曜日', datetime.date(2023, 7, 22)),
                ('日曜日', datetime.date(2023, 7, 23)),
                ('土曜日', datetime.date(2023, 7, 29)),
                ('日曜日', datetime.date(2023, 7, 30)),
                ('土曜日', datetime.date(2023, 8, 5)),
                ('日曜日', datetime.date(2023, 8, 6)),
                ('山の日', datetime.date(2023, 8, 11)),
                ('土曜日', datetime.date(2023, 8, 12)),
                ('日曜日', datetime.date(2023, 8, 13)),
                ('土曜日', datetime.date(2023, 8, 19)),
                ('日曜日', datetime.date(2023, 8, 20)),
                ('土曜日', datetime.date(2023, 8, 26)),
                ('日曜日', datetime.date(2023, 8, 27)),
                ('土曜日', datetime.date(2023, 9, 2)),
                ('日曜日', datetime.date(2023, 9, 3)),
                ('土曜日', datetime.date(2023, 9, 9)),
                ('日曜日', datetime.date(2023, 9, 10)),
                ('土曜日', datetime.date(2023, 9, 16)),
                ('日曜日', datetime.date(2023, 9, 17)),
                ('敬老の日', datetime.date(2023, 9, 18)),
                ('土曜日', datetime.date(2023, 9, 23)),
                ('日曜日', datetime.date(2023, 9, 24)),
                ('土曜日', datetime.date(2023, 9, 30)),
                ('日曜日', datetime.date(2023, 10, 1)),
                ('土曜日', datetime.date(2023, 10, 7)),
                ('日曜日', datetime.date(2023, 10, 8)),
                ('スポーツの日', datetime.date(2023, 10, 9)),
                ('土曜日', datetime.date(2023, 10, 14)),
                ('日曜日', datetime.date(2023, 10, 15)),
                ('土曜日', datetime.date(2023, 10, 21)),
                ('日曜日', datetime.date(2023, 10, 22)),
                ('土曜日', datetime.date(2023, 10, 28)),
                ('日曜日', datetime.date(2023, 10, 29)),
                ('文化の日', datetime.date(2023, 11, 3)),
                ('土曜日', datetime.date(2023, 11, 4)),
                ('日曜日', datetime.date(2023, 11, 5)),
                ('土曜日', datetime.date(2023, 11, 11)),
                ('日曜日', datetime.date(2023, 11, 12)),
                ('土曜日', datetime.date(2023, 11, 18)),
                ('日曜日', datetime.date(2023, 11, 19)),
                ('勤労感謝の日', datetime.date(2023, 11, 23)),
                ('土曜日', datetime.date(2023, 11, 25)),
                ('日曜日', datetime.date(2023, 11, 26)),
                ('土曜日', datetime.date(2023, 12, 2)),
                ('日曜日', datetime.date(2023, 12, 3)),
                ('土曜日', datetime.date(2023, 12, 9)),
                ('日曜日', datetime.date(2023, 12, 10)),
                ('土曜日', datetime.date(2023, 12, 16)),
                ('日曜日', datetime.date(2023, 12, 17)),
                ('土曜日', datetime.date(2023, 12, 23)),
                ('日曜日', datetime.date(2023, 12, 24)),
                ('土曜日', datetime.date(2023, 12, 30)),
                ('日曜日', datetime.date(2023, 12, 31)),
            ]
        )

    def test_get_rest_days_in_range(self):
        start_date = datetime.date(2023, 7, 10)
        end_date = datetime.date(2023, 7, 20)
        expected_rest_days = [
            ("土曜日", datetime.date(2023, 7, 15)),
            ("日曜日", datetime.date(2023, 7, 16)),
            ("海の日", datetime.date(2023, 7, 17)),
        ]
        self.assertEqual(self.holidays.get_rest_days_in_range(
            start_date, end_date), expected_rest_days)

    def test_get_holidays_in_range(self):
        start_date = datetime.date(1980, 1, 1)
        end_date = datetime.date(2024, 12, 31)
        expected_holidays = [
            ('元日', datetime.date(1980, 1, 1)),
            ('成人の日', datetime.date(1980, 1, 15)),
            ('建国記念の日', datetime.date(1980, 2, 11)),
            ('春分の日', datetime.date(1980, 3, 20)),
            ('天皇誕生日', datetime.date(1980, 4, 29)),
            ('憲法記念日', datetime.date(1980, 5, 3)),
            ('こどもの日', datetime.date(1980, 5, 5)),
            ('敬老の日', datetime.date(1980, 9, 15)),
            ('秋分の日', datetime.date(1980, 9, 23)),
            ('体育の日', datetime.date(1980, 10, 10)),
            ('文化の日', datetime.date(1980, 11, 3)),
            ('勤労感謝の日', datetime.date(1980, 11, 23)),
            ('勤労感謝の日（振替休日）', datetime.date(1980, 11, 24)),
            ('元日', datetime.date(1981, 1, 1)),
            ('成人の日', datetime.date(1981, 1, 15)),
            ('建国記念の日', datetime.date(1981, 2, 11)),
            ('春分の日', datetime.date(1981, 3, 21)),
            ('天皇誕生日', datetime.date(1981, 4, 29)),
            ('憲法記念日', datetime.date(1981, 5, 3)),
            ('憲法記念日（振替休日）', datetime.date(1981, 5, 4)),
            ('こどもの日', datetime.date(1981, 5, 5)),
            ('敬老の日', datetime.date(1981, 9, 15)),
            ('秋分の日', datetime.date(1981, 9, 23)),
            ('体育の日', datetime.date(1981, 10, 10)),
            ('文化の日', datetime.date(1981, 11, 3)),
            ('勤労感謝の日', datetime.date(1981, 11, 23)),
            ('元日', datetime.date(1982, 1, 1)),
            ('成人の日', datetime.date(1982, 1, 15)),
            ('建国記念の日', datetime.date(1982, 2, 11)),
            ('春分の日', datetime.date(1982, 3, 21)),
            ('春分の日（振替休日）', datetime.date(1982, 3, 22)),
            ('天皇誕生日', datetime.date(1982, 4, 29)),
            ('憲法記念日', datetime.date(1982, 5, 3)),
            ('こどもの日', datetime.date(1982, 5, 5)),
            ('敬老の日', datetime.date(1982, 9, 15)),
            ('秋分の日', datetime.date(1982, 9, 23)),
            ('体育の日', datetime.date(1982, 10, 10)),
            ('体育の日（振替休日）', datetime.date(1982, 10, 11)),
            ('文化の日', datetime.date(1982, 11, 3)),
            ('勤労感謝の日', datetime.date(1982, 11, 23)),
            ('元日', datetime.date(1983, 1, 1)),
            ('成人の日', datetime.date(1983, 1, 15)),
            ('建国記念の日', datetime.date(1983, 2, 11)),
            ('春分の日', datetime.date(1983, 3, 21)),
            ('天皇誕生日', datetime.date(1983, 4, 29)),
            ('憲法記念日', datetime.date(1983, 5, 3)),
            ('こどもの日', datetime.date(1983, 5, 5)),
            ('敬老の日', datetime.date(1983, 9, 15)),
            ('秋分の日', datetime.date(1983, 9, 23)),
            ('体育の日', datetime.date(1983, 10, 10)),
            ('文化の日', datetime.date(1983, 11, 3)),
            ('勤労感謝の日', datetime.date(1983, 11, 23)),
            ('元日', datetime.date(1984, 1, 1)),
            ('元日（振替休日）', datetime.date(1984, 1, 2)),
            ('成人の日', datetime.date(1984, 1, 15)),
            ('成人の日（振替休日）', datetime.date(1984, 1, 16)),
            ('建国記念の日', datetime.date(1984, 2, 11)),
            ('春分の日', datetime.date(1984, 3, 20)),
            ('天皇誕生日', datetime.date(1984, 4, 29)),
            ('天皇誕生日（振替休日）', datetime.date(1984, 4, 30)),
            ('憲法記念日', datetime.date(1984, 5, 3)),
            ('こどもの日', datetime.date(1984, 5, 5)),
            ('敬老の日', datetime.date(1984, 9, 15)),
            ('秋分の日', datetime.date(1984, 9, 23)),
            ('秋分の日（振替休日）', datetime.date(1984, 9, 24)),
            ('体育の日', datetime.date(1984, 10, 10)),
            ('文化の日', datetime.date(1984, 11, 3)),
            ('勤労感謝の日', datetime.date(1984, 11, 23)),
            ('元日', datetime.date(1985, 1, 1)),
            ('成人の日', datetime.date(1985, 1, 15)),
            ('建国記念の日', datetime.date(1985, 2, 11)),
            ('春分の日', datetime.date(1985, 3, 21)),
            ('天皇誕生日', datetime.date(1985, 4, 29)),
            ('憲法記念日', datetime.date(1985, 5, 3)),
            ('こどもの日', datetime.date(1985, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(1985, 5, 6)),
            ('敬老の日', datetime.date(1985, 9, 15)),
            ('敬老の日（振替休日）', datetime.date(1985, 9, 16)),
            ('秋分の日', datetime.date(1985, 9, 23)),
            ('体育の日', datetime.date(1985, 10, 10)),
            ('文化の日', datetime.date(1985, 11, 3)),
            ('文化の日（振替休日）', datetime.date(1985, 11, 4)),
            ('勤労感謝の日', datetime.date(1985, 11, 23)),
            ('元日', datetime.date(1986, 1, 1)),
            ('成人の日', datetime.date(1986, 1, 15)),
            ('建国記念の日', datetime.date(1986, 2, 11)),
            ('春分の日', datetime.date(1986, 3, 21)),
            ('天皇誕生日', datetime.date(1986, 4, 29)),
            ('憲法記念日', datetime.date(1986, 5, 3)),
            ('こどもの日', datetime.date(1986, 5, 5)),
            ('敬老の日', datetime.date(1986, 9, 15)),
            ('秋分の日', datetime.date(1986, 9, 23)),
            ('体育の日', datetime.date(1986, 10, 10)),
            ('文化の日', datetime.date(1986, 11, 3)),
            ('勤労感謝の日', datetime.date(1986, 11, 23)),
            ('勤労感謝の日（振替休日）', datetime.date(1986, 11, 24)),
            ('元日', datetime.date(1987, 1, 1)),
            ('成人の日', datetime.date(1987, 1, 15)),
            ('建国記念の日', datetime.date(1987, 2, 11)),
            ('春分の日', datetime.date(1987, 3, 21)),
            ('天皇誕生日', datetime.date(1987, 4, 29)),
            ('憲法記念日', datetime.date(1987, 5, 3)),
            ('国民の休日', datetime.date(1987, 5, 4)),
            ('こどもの日', datetime.date(1987, 5, 5)),
            ('敬老の日', datetime.date(1987, 9, 15)),
            ('秋分の日', datetime.date(1987, 9, 23)),
            ('体育の日', datetime.date(1987, 10, 10)),
            ('文化の日', datetime.date(1987, 11, 3)),
            ('勤労感謝の日', datetime.date(1987, 11, 23)),
            ('元日', datetime.date(1988, 1, 1)),
            ('成人の日', datetime.date(1988, 1, 15)),
            ('建国記念の日', datetime.date(1988, 2, 11)),
            ('春分の日', datetime.date(1988, 3, 20)),
            ('春分の日（振替休日）', datetime.date(1988, 3, 21)),
            ('天皇誕生日', datetime.date(1988, 4, 29)),
            ('憲法記念日', datetime.date(1988, 5, 3)),
            ('国民の休日', datetime.date(1988, 5, 4)),
            ('こどもの日', datetime.date(1988, 5, 5)),
            ('敬老の日', datetime.date(1988, 9, 15)),
            ('秋分の日', datetime.date(1988, 9, 23)),
            ('体育の日', datetime.date(1988, 10, 10)),
            ('文化の日', datetime.date(1988, 11, 3)),
            ('勤労感謝の日', datetime.date(1988, 11, 23)),
            ('元日', datetime.date(1989, 1, 1)),
            ('元日（振替休日）', datetime.date(1989, 1, 2)),
            ('成人の日', datetime.date(1989, 1, 15)),
            ('成人の日（振替休日）', datetime.date(1989, 1, 16)),
            ('建国記念の日', datetime.date(1989, 2, 11)),
            ('国民の休日', datetime.date(1989, 2, 24)),
            ('春分の日', datetime.date(1989, 3, 21)),
            ('みどりの日', datetime.date(1989, 4, 29)),
            ('憲法記念日', datetime.date(1989, 5, 3)),
            ('国民の休日', datetime.date(1989, 5, 4)),
            ('こどもの日', datetime.date(1989, 5, 5)),
            ('敬老の日', datetime.date(1989, 9, 15)),
            ('秋分の日', datetime.date(1989, 9, 23)),
            ('体育の日', datetime.date(1989, 10, 10)),
            ('文化の日', datetime.date(1989, 11, 3)),
            ('勤労感謝の日', datetime.date(1989, 11, 23)),
            ('天皇誕生日', datetime.date(1989, 12, 23)),
            ('元日', datetime.date(1990, 1, 1)),
            ('成人の日', datetime.date(1990, 1, 15)),
            ('建国記念の日', datetime.date(1990, 2, 11)),
            ('建国記念の日（振替休日）', datetime.date(1990, 2, 12)),
            ('春分の日', datetime.date(1990, 3, 21)),
            ('みどりの日', datetime.date(1990, 4, 29)),
            ('みどりの日（振替休日）', datetime.date(1990, 4, 30)),
            ('憲法記念日', datetime.date(1990, 5, 3)),
            ('国民の休日', datetime.date(1990, 5, 4)),
            ('こどもの日', datetime.date(1990, 5, 5)),
            ('敬老の日', datetime.date(1990, 9, 15)),
            ('秋分の日', datetime.date(1990, 9, 23)),
            ('秋分の日（振替休日）', datetime.date(1990, 9, 24)),
            ('体育の日', datetime.date(1990, 10, 10)),
            ('文化の日', datetime.date(1990, 11, 3)),
            ('国民の休日', datetime.date(1990, 11, 12)),
            ('勤労感謝の日', datetime.date(1990, 11, 23)),
            ('天皇誕生日', datetime.date(1990, 12, 23)),
            ('天皇誕生日（振替休日）', datetime.date(1990, 12, 24)),
            ('元日', datetime.date(1991, 1, 1)),
            ('成人の日', datetime.date(1991, 1, 15)),
            ('建国記念の日', datetime.date(1991, 2, 11)),
            ('春分の日', datetime.date(1991, 3, 21)),
            ('みどりの日', datetime.date(1991, 4, 29)),
            ('憲法記念日', datetime.date(1991, 5, 3)),
            ('国民の休日', datetime.date(1991, 5, 4)),
            ('こどもの日', datetime.date(1991, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(1991, 5, 6)),
            ('敬老の日', datetime.date(1991, 9, 15)),
            ('敬老の日（振替休日）', datetime.date(1991, 9, 16)),
            ('秋分の日', datetime.date(1991, 9, 23)),
            ('体育の日', datetime.date(1991, 10, 10)),
            ('文化の日', datetime.date(1991, 11, 3)),
            ('文化の日（振替休日）', datetime.date(1991, 11, 4)),
            ('勤労感謝の日', datetime.date(1991, 11, 23)),
            ('天皇誕生日', datetime.date(1991, 12, 23)),
            ('元日', datetime.date(1992, 1, 1)),
            ('成人の日', datetime.date(1992, 1, 15)),
            ('建国記念の日', datetime.date(1992, 2, 11)),
            ('春分の日', datetime.date(1992, 3, 20)),
            ('みどりの日', datetime.date(1992, 4, 29)),
            ('憲法記念日', datetime.date(1992, 5, 3)),
            ('国民の休日', datetime.date(1992, 5, 4)),
            ('こどもの日', datetime.date(1992, 5, 5)),
            ('敬老の日', datetime.date(1992, 9, 15)),
            ('秋分の日', datetime.date(1992, 9, 23)),
            ('体育の日', datetime.date(1992, 10, 10)),
            ('文化の日', datetime.date(1992, 11, 3)),
            ('勤労感謝の日', datetime.date(1992, 11, 23)),
            ('天皇誕生日', datetime.date(1992, 12, 23)),
            ('元日', datetime.date(1993, 1, 1)),
            ('成人の日', datetime.date(1993, 1, 15)),
            ('建国記念の日', datetime.date(1993, 2, 11)),
            ('春分の日', datetime.date(1993, 3, 20)),
            ('みどりの日', datetime.date(1993, 4, 29)),
            ('憲法記念日', datetime.date(1993, 5, 3)),
            ('国民の休日', datetime.date(1993, 5, 4)),
            ('こどもの日', datetime.date(1993, 5, 5)),
            ('国民の休日', datetime.date(1993, 6, 9)),
            ('敬老の日', datetime.date(1993, 9, 15)),
            ('秋分の日', datetime.date(1993, 9, 23)),
            ('体育の日', datetime.date(1993, 10, 10)),
            ('体育の日（振替休日）', datetime.date(1993, 10, 11)),
            ('文化の日', datetime.date(1993, 11, 3)),
            ('勤労感謝の日', datetime.date(1993, 11, 23)),
            ('天皇誕生日', datetime.date(1993, 12, 23)),
            ('元日', datetime.date(1994, 1, 1)),
            ('成人の日', datetime.date(1994, 1, 15)),
            ('建国記念の日', datetime.date(1994, 2, 11)),
            ('春分の日', datetime.date(1994, 3, 21)),
            ('みどりの日', datetime.date(1994, 4, 29)),
            ('憲法記念日', datetime.date(1994, 5, 3)),
            ('国民の休日', datetime.date(1994, 5, 4)),
            ('こどもの日', datetime.date(1994, 5, 5)),
            ('敬老の日', datetime.date(1994, 9, 15)),
            ('秋分の日', datetime.date(1994, 9, 23)),
            ('体育の日', datetime.date(1994, 10, 10)),
            ('文化の日', datetime.date(1994, 11, 3)),
            ('勤労感謝の日', datetime.date(1994, 11, 23)),
            ('天皇誕生日', datetime.date(1994, 12, 23)),
            ('元日', datetime.date(1995, 1, 1)),
            ('元日（振替休日）', datetime.date(1995, 1, 2)),
            ('成人の日', datetime.date(1995, 1, 15)),
            ('成人の日（振替休日）', datetime.date(1995, 1, 16)),
            ('建国記念の日', datetime.date(1995, 2, 11)),
            ('春分の日', datetime.date(1995, 3, 21)),
            ('みどりの日', datetime.date(1995, 4, 29)),
            ('憲法記念日', datetime.date(1995, 5, 3)),
            ('国民の休日', datetime.date(1995, 5, 4)),
            ('こどもの日', datetime.date(1995, 5, 5)),
            ('敬老の日', datetime.date(1995, 9, 15)),
            ('秋分の日', datetime.date(1995, 9, 23)),
            ('体育の日', datetime.date(1995, 10, 10)),
            ('文化の日', datetime.date(1995, 11, 3)),
            ('勤労感謝の日', datetime.date(1995, 11, 23)),
            ('天皇誕生日', datetime.date(1995, 12, 23)),
            ('元日', datetime.date(1996, 1, 1)),
            ('成人の日', datetime.date(1996, 1, 15)),
            ('建国記念の日', datetime.date(1996, 2, 11)),
            ('建国記念の日（振替休日）', datetime.date(1996, 2, 12)),
            ('春分の日', datetime.date(1996, 3, 20)),
            ('みどりの日', datetime.date(1996, 4, 29)),
            ('憲法記念日', datetime.date(1996, 5, 3)),
            ('国民の休日', datetime.date(1996, 5, 4)),
            ('こどもの日', datetime.date(1996, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(1996, 5, 6)),
            ('海の日', datetime.date(1996, 7, 20)),
            ('敬老の日', datetime.date(1996, 9, 15)),
            ('敬老の日（振替休日）', datetime.date(1996, 9, 16)),
            ('秋分の日', datetime.date(1996, 9, 23)),
            ('体育の日', datetime.date(1996, 10, 10)),
            ('文化の日', datetime.date(1996, 11, 3)),
            ('文化の日（振替休日）', datetime.date(1996, 11, 4)),
            ('勤労感謝の日', datetime.date(1996, 11, 23)),
            ('天皇誕生日', datetime.date(1996, 12, 23)),
            ('元日', datetime.date(1997, 1, 1)),
            ('成人の日', datetime.date(1997, 1, 15)),
            ('建国記念の日', datetime.date(1997, 2, 11)),
            ('春分の日', datetime.date(1997, 3, 20)),
            ('みどりの日', datetime.date(1997, 4, 29)),
            ('憲法記念日', datetime.date(1997, 5, 3)),
            ('こどもの日', datetime.date(1997, 5, 5)),
            ('海の日', datetime.date(1997, 7, 20)),
            ('海の日（振替休日）', datetime.date(1997, 7, 21)),
            ('敬老の日', datetime.date(1997, 9, 15)),
            ('秋分の日', datetime.date(1997, 9, 23)),
            ('体育の日', datetime.date(1997, 10, 10)),
            ('文化の日', datetime.date(1997, 11, 3)),
            ('勤労感謝の日', datetime.date(1997, 11, 23)),
            ('勤労感謝の日（振替休日）', datetime.date(1997, 11, 24)),
            ('天皇誕生日', datetime.date(1997, 12, 23)),
            ('元日', datetime.date(1998, 1, 1)),
            ('成人の日', datetime.date(1998, 1, 15)),
            ('建国記念の日', datetime.date(1998, 2, 11)),
            ('春分の日', datetime.date(1998, 3, 21)),
            ('みどりの日', datetime.date(1998, 4, 29)),
            ('憲法記念日', datetime.date(1998, 5, 3)),
            ('国民の休日', datetime.date(1998, 5, 4)),
            ('こどもの日', datetime.date(1998, 5, 5)),
            ('海の日', datetime.date(1998, 7, 20)),
            ('敬老の日', datetime.date(1998, 9, 15)),
            ('秋分の日', datetime.date(1998, 9, 23)),
            ('体育の日', datetime.date(1998, 10, 10)),
            ('文化の日', datetime.date(1998, 11, 3)),
            ('勤労感謝の日', datetime.date(1998, 11, 23)),
            ('天皇誕生日', datetime.date(1998, 12, 23)),
            ('元日', datetime.date(1999, 1, 1)),
            ('成人の日', datetime.date(1999, 1, 15)),
            ('建国記念の日', datetime.date(1999, 2, 11)),
            ('春分の日', datetime.date(1999, 3, 21)),
            ('春分の日（振替休日）', datetime.date(1999, 3, 22)),
            ('みどりの日', datetime.date(1999, 4, 29)),
            ('憲法記念日', datetime.date(1999, 5, 3)),
            ('国民の休日', datetime.date(1999, 5, 4)),
            ('こどもの日', datetime.date(1999, 5, 5)),
            ('海の日', datetime.date(1999, 7, 20)),
            ('敬老の日', datetime.date(1999, 9, 15)),
            ('秋分の日', datetime.date(1999, 9, 23)),
            ('体育の日', datetime.date(1999, 10, 10)),
            ('体育の日（振替休日）', datetime.date(1999, 10, 11)),
            ('文化の日', datetime.date(1999, 11, 3)),
            ('勤労感謝の日', datetime.date(1999, 11, 23)),
            ('天皇誕生日', datetime.date(1999, 12, 23)),
            ('元日', datetime.date(2000, 1, 1)),
            ('成人の日', datetime.date(2000, 1, 10)),
            ('建国記念の日', datetime.date(2000, 2, 11)),
            ('春分の日', datetime.date(2000, 3, 20)),
            ('みどりの日', datetime.date(2000, 4, 29)),
            ('憲法記念日', datetime.date(2000, 5, 3)),
            ('国民の休日', datetime.date(2000, 5, 4)),
            ('こどもの日', datetime.date(2000, 5, 5)),
            ('海の日', datetime.date(2000, 7, 20)),
            ('敬老の日', datetime.date(2000, 9, 15)),
            ('秋分の日', datetime.date(2000, 9, 23)),
            ('体育の日', datetime.date(2000, 10, 9)),
            ('文化の日', datetime.date(2000, 11, 3)),
            ('勤労感謝の日', datetime.date(2000, 11, 23)),
            ('天皇誕生日', datetime.date(2000, 12, 23)),
            ('元日', datetime.date(2001, 1, 1)),
            ('成人の日', datetime.date(2001, 1, 8)),
            ('建国記念の日', datetime.date(2001, 2, 11)),
            ('建国記念の日（振替休日）', datetime.date(2001, 2, 12)),
            ('春分の日', datetime.date(2001, 3, 20)),
            ('みどりの日', datetime.date(2001, 4, 29)),
            ('みどりの日（振替休日）', datetime.date(2001, 4, 30)),
            ('憲法記念日', datetime.date(2001, 5, 3)),
            ('国民の休日', datetime.date(2001, 5, 4)),
            ('こどもの日', datetime.date(2001, 5, 5)),
            ('海の日', datetime.date(2001, 7, 20)),
            ('敬老の日', datetime.date(2001, 9, 15)),
            ('秋分の日', datetime.date(2001, 9, 23)),
            ('秋分の日（振替休日）', datetime.date(2001, 9, 24)),
            ('体育の日', datetime.date(2001, 10, 8)),
            ('文化の日', datetime.date(2001, 11, 3)),
            ('勤労感謝の日', datetime.date(2001, 11, 23)),
            ('天皇誕生日', datetime.date(2001, 12, 23)),
            ('天皇誕生日（振替休日）', datetime.date(2001, 12, 24)),
            ('元日', datetime.date(2002, 1, 1)),
            ('成人の日', datetime.date(2002, 1, 14)),
            ('建国記念の日', datetime.date(2002, 2, 11)),
            ('春分の日', datetime.date(2002, 3, 21)),
            ('みどりの日', datetime.date(2002, 4, 29)),
            ('憲法記念日', datetime.date(2002, 5, 3)),
            ('国民の休日', datetime.date(2002, 5, 4)),
            ('こどもの日', datetime.date(2002, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2002, 5, 6)),
            ('海の日', datetime.date(2002, 7, 20)),
            ('敬老の日', datetime.date(2002, 9, 15)),
            ('敬老の日（振替休日）', datetime.date(2002, 9, 16)),
            ('秋分の日', datetime.date(2002, 9, 23)),
            ('体育の日', datetime.date(2002, 10, 14)),
            ('文化の日', datetime.date(2002, 11, 3)),
            ('文化の日（振替休日）', datetime.date(2002, 11, 4)),
            ('勤労感謝の日', datetime.date(2002, 11, 23)),
            ('天皇誕生日', datetime.date(2002, 12, 23)),
            ('元日', datetime.date(2003, 1, 1)),
            ('成人の日', datetime.date(2003, 1, 13)),
            ('建国記念の日', datetime.date(2003, 2, 11)),
            ('春分の日', datetime.date(2003, 3, 21)),
            ('みどりの日', datetime.date(2003, 4, 29)),
            ('憲法記念日', datetime.date(2003, 5, 3)),
            ('こどもの日', datetime.date(2003, 5, 5)),
            ('海の日', datetime.date(2003, 7, 21)),
            ('敬老の日', datetime.date(2003, 9, 15)),
            ('秋分の日', datetime.date(2003, 9, 23)),
            ('体育の日', datetime.date(2003, 10, 13)),
            ('文化の日', datetime.date(2003, 11, 3)),
            ('勤労感謝の日', datetime.date(2003, 11, 23)),
            ('勤労感謝の日（振替休日）', datetime.date(2003, 11, 24)),
            ('天皇誕生日', datetime.date(2003, 12, 23)),
            ('元日', datetime.date(2004, 1, 1)),
            ('成人の日', datetime.date(2004, 1, 12)),
            ('建国記念の日', datetime.date(2004, 2, 11)),
            ('春分の日', datetime.date(2004, 3, 20)),
            ('みどりの日', datetime.date(2004, 4, 29)),
            ('憲法記念日', datetime.date(2004, 5, 3)),
            ('国民の休日', datetime.date(2004, 5, 4)),
            ('こどもの日', datetime.date(2004, 5, 5)),
            ('海の日', datetime.date(2004, 7, 19)),
            ('敬老の日', datetime.date(2004, 9, 20)),
            ('秋分の日', datetime.date(2004, 9, 23)),
            ('体育の日', datetime.date(2004, 10, 11)),
            ('文化の日', datetime.date(2004, 11, 3)),
            ('勤労感謝の日', datetime.date(2004, 11, 23)),
            ('天皇誕生日', datetime.date(2004, 12, 23)),
            ('元日', datetime.date(2005, 1, 1)),
            ('成人の日', datetime.date(2005, 1, 10)),
            ('建国記念の日', datetime.date(2005, 2, 11)),
            ('春分の日', datetime.date(2005, 3, 20)),
            ('春分の日（振替休日）', datetime.date(2005, 3, 21)),
            ('みどりの日', datetime.date(2005, 4, 29)),
            ('憲法記念日', datetime.date(2005, 5, 3)),
            ('国民の休日', datetime.date(2005, 5, 4)),
            ('こどもの日', datetime.date(2005, 5, 5)),
            ('海の日', datetime.date(2005, 7, 18)),
            ('敬老の日', datetime.date(2005, 9, 19)),
            ('秋分の日', datetime.date(2005, 9, 23)),
            ('体育の日', datetime.date(2005, 10, 10)),
            ('文化の日', datetime.date(2005, 11, 3)),
            ('勤労感謝の日', datetime.date(2005, 11, 23)),
            ('天皇誕生日', datetime.date(2005, 12, 23)),
            ('元日', datetime.date(2006, 1, 1)),
            ('元日（振替休日）', datetime.date(2006, 1, 2)),
            ('成人の日', datetime.date(2006, 1, 9)),
            ('建国記念の日', datetime.date(2006, 2, 11)),
            ('春分の日', datetime.date(2006, 3, 21)),
            ('みどりの日', datetime.date(2006, 4, 29)),
            ('憲法記念日', datetime.date(2006, 5, 3)),
            ('国民の休日', datetime.date(2006, 5, 4)),
            ('こどもの日', datetime.date(2006, 5, 5)),
            ('海の日', datetime.date(2006, 7, 17)),
            ('敬老の日', datetime.date(2006, 9, 18)),
            ('秋分の日', datetime.date(2006, 9, 23)),
            ('体育の日', datetime.date(2006, 10, 9)),
            ('文化の日', datetime.date(2006, 11, 3)),
            ('勤労感謝の日', datetime.date(2006, 11, 23)),
            ('天皇誕生日', datetime.date(2006, 12, 23)),
            ('元日', datetime.date(2007, 1, 1)),
            ('成人の日', datetime.date(2007, 1, 8)),
            ('建国記念の日', datetime.date(2007, 2, 11)),
            ('建国記念の日（振替休日）', datetime.date(2007, 2, 12)),
            ('春分の日', datetime.date(2007, 3, 21)),
            ('昭和の日', datetime.date(2007, 4, 29)),
            ('昭和の日（振替休日）', datetime.date(2007, 4, 30)),
            ('憲法記念日', datetime.date(2007, 5, 3)),
            ('みどりの日', datetime.date(2007, 5, 4)),
            ('こどもの日', datetime.date(2007, 5, 5)),
            ('海の日', datetime.date(2007, 7, 16)),
            ('敬老の日', datetime.date(2007, 9, 17)),
            ('秋分の日', datetime.date(2007, 9, 23)),
            ('秋分の日（振替休日）', datetime.date(2007, 9, 24)),
            ('体育の日', datetime.date(2007, 10, 8)),
            ('文化の日', datetime.date(2007, 11, 3)),
            ('勤労感謝の日', datetime.date(2007, 11, 23)),
            ('天皇誕生日', datetime.date(2007, 12, 23)),
            ('天皇誕生日（振替休日）', datetime.date(2007, 12, 24)),
            ('元日', datetime.date(2008, 1, 1)),
            ('成人の日', datetime.date(2008, 1, 14)),
            ('建国記念の日', datetime.date(2008, 2, 11)),
            ('春分の日', datetime.date(2008, 3, 20)),
            ('昭和の日', datetime.date(2008, 4, 29)),
            ('憲法記念日', datetime.date(2008, 5, 3)),
            ('みどりの日', datetime.date(2008, 5, 4)),
            ('こどもの日', datetime.date(2008, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2008, 5, 6)),
            ('海の日', datetime.date(2008, 7, 21)),
            ('敬老の日', datetime.date(2008, 9, 15)),
            ('秋分の日', datetime.date(2008, 9, 23)),
            ('体育の日', datetime.date(2008, 10, 13)),
            ('文化の日', datetime.date(2008, 11, 3)),
            ('勤労感謝の日', datetime.date(2008, 11, 23)),
            ('勤労感謝の日（振替休日）', datetime.date(2008, 11, 24)),
            ('天皇誕生日', datetime.date(2008, 12, 23)),
            ('元日', datetime.date(2009, 1, 1)),
            ('成人の日', datetime.date(2009, 1, 12)),
            ('建国記念の日', datetime.date(2009, 2, 11)),
            ('春分の日', datetime.date(2009, 3, 20)),
            ('昭和の日', datetime.date(2009, 4, 29)),
            ('憲法記念日', datetime.date(2009, 5, 3)),
            ('みどりの日', datetime.date(2009, 5, 4)),
            ('こどもの日', datetime.date(2009, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2009, 5, 6)),
            ('海の日', datetime.date(2009, 7, 20)),
            ('敬老の日', datetime.date(2009, 9, 21)),
            ('国民の休日', datetime.date(2009, 9, 22)),
            ('秋分の日', datetime.date(2009, 9, 23)),
            ('体育の日', datetime.date(2009, 10, 12)),
            ('文化の日', datetime.date(2009, 11, 3)),
            ('勤労感謝の日', datetime.date(2009, 11, 23)),
            ('天皇誕生日', datetime.date(2009, 12, 23)),
            ('元日', datetime.date(2010, 1, 1)),
            ('成人の日', datetime.date(2010, 1, 11)),
            ('建国記念の日', datetime.date(2010, 2, 11)),
            ('春分の日', datetime.date(2010, 3, 21)),
            ('春分の日（振替休日）', datetime.date(2010, 3, 22)),
            ('昭和の日', datetime.date(2010, 4, 29)),
            ('憲法記念日', datetime.date(2010, 5, 3)),
            ('みどりの日', datetime.date(2010, 5, 4)),
            ('こどもの日', datetime.date(2010, 5, 5)),
            ('海の日', datetime.date(2010, 7, 19)),
            ('敬老の日', datetime.date(2010, 9, 20)),
            ('秋分の日', datetime.date(2010, 9, 23)),
            ('体育の日', datetime.date(2010, 10, 11)),
            ('文化の日', datetime.date(2010, 11, 3)),
            ('勤労感謝の日', datetime.date(2010, 11, 23)),
            ('天皇誕生日', datetime.date(2010, 12, 23)),
            ('元日', datetime.date(2011, 1, 1)),
            ('成人の日', datetime.date(2011, 1, 10)),
            ('建国記念の日', datetime.date(2011, 2, 11)),
            ('春分の日', datetime.date(2011, 3, 21)),
            ('昭和の日', datetime.date(2011, 4, 29)),
            ('憲法記念日', datetime.date(2011, 5, 3)),
            ('みどりの日', datetime.date(2011, 5, 4)),
            ('こどもの日', datetime.date(2011, 5, 5)),
            ('海の日', datetime.date(2011, 7, 18)),
            ('敬老の日', datetime.date(2011, 9, 19)),
            ('秋分の日', datetime.date(2011, 9, 23)),
            ('体育の日', datetime.date(2011, 10, 10)),
            ('文化の日', datetime.date(2011, 11, 3)),
            ('勤労感謝の日', datetime.date(2011, 11, 23)),
            ('天皇誕生日', datetime.date(2011, 12, 23)),
            ('元日', datetime.date(2012, 1, 1)),
            ('元日（振替休日）', datetime.date(2012, 1, 2)),
            ('成人の日', datetime.date(2012, 1, 9)),
            ('建国記念の日', datetime.date(2012, 2, 11)),
            ('春分の日', datetime.date(2012, 3, 20)),
            ('昭和の日', datetime.date(2012, 4, 29)),
            ('昭和の日（振替休日）', datetime.date(2012, 4, 30)),
            ('憲法記念日', datetime.date(2012, 5, 3)),
            ('みどりの日', datetime.date(2012, 5, 4)),
            ('こどもの日', datetime.date(2012, 5, 5)),
            ('海の日', datetime.date(2012, 7, 16)),
            ('敬老の日', datetime.date(2012, 9, 17)),
            ('秋分の日', datetime.date(2012, 9, 22)),
            ('体育の日', datetime.date(2012, 10, 8)),
            ('文化の日', datetime.date(2012, 11, 3)),
            ('勤労感謝の日', datetime.date(2012, 11, 23)),
            ('天皇誕生日', datetime.date(2012, 12, 23)),
            ('天皇誕生日（振替休日）', datetime.date(2012, 12, 24)),
            ('元日', datetime.date(2013, 1, 1)),
            ('成人の日', datetime.date(2013, 1, 14)),
            ('建国記念の日', datetime.date(2013, 2, 11)),
            ('春分の日', datetime.date(2013, 3, 20)),
            ('昭和の日', datetime.date(2013, 4, 29)),
            ('憲法記念日', datetime.date(2013, 5, 3)),
            ('みどりの日', datetime.date(2013, 5, 4)),
            ('こどもの日', datetime.date(2013, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2013, 5, 6)),
            ('海の日', datetime.date(2013, 7, 15)),
            ('敬老の日', datetime.date(2013, 9, 16)),
            ('秋分の日', datetime.date(2013, 9, 23)),
            ('体育の日', datetime.date(2013, 10, 14)),
            ('文化の日', datetime.date(2013, 11, 3)),
            ('文化の日（振替休日）', datetime.date(2013, 11, 4)),
            ('勤労感謝の日', datetime.date(2013, 11, 23)),
            ('天皇誕生日', datetime.date(2013, 12, 23)),
            ('元日', datetime.date(2014, 1, 1)),
            ('成人の日', datetime.date(2014, 1, 13)),
            ('建国記念の日', datetime.date(2014, 2, 11)),
            ('春分の日', datetime.date(2014, 3, 21)),
            ('昭和の日', datetime.date(2014, 4, 29)),
            ('憲法記念日', datetime.date(2014, 5, 3)),
            ('みどりの日', datetime.date(2014, 5, 4)),
            ('こどもの日', datetime.date(2014, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2014, 5, 6)),
            ('海の日', datetime.date(2014, 7, 21)),
            ('敬老の日', datetime.date(2014, 9, 15)),
            ('秋分の日', datetime.date(2014, 9, 23)),
            ('体育の日', datetime.date(2014, 10, 13)),
            ('文化の日', datetime.date(2014, 11, 3)),
            ('勤労感謝の日', datetime.date(2014, 11, 23)),
            ('勤労感謝の日（振替休日）', datetime.date(2014, 11, 24)),
            ('天皇誕生日', datetime.date(2014, 12, 23)),
            ('元日', datetime.date(2015, 1, 1)),
            ('成人の日', datetime.date(2015, 1, 12)),
            ('建国記念の日', datetime.date(2015, 2, 11)),
            ('春分の日', datetime.date(2015, 3, 21)),
            ('昭和の日', datetime.date(2015, 4, 29)),
            ('憲法記念日', datetime.date(2015, 5, 3)),
            ('みどりの日', datetime.date(2015, 5, 4)),
            ('こどもの日', datetime.date(2015, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2015, 5, 6)),
            ('海の日', datetime.date(2015, 7, 20)),
            ('敬老の日', datetime.date(2015, 9, 21)),
            ('国民の休日', datetime.date(2015, 9, 22)),
            ('秋分の日', datetime.date(2015, 9, 23)),
            ('体育の日', datetime.date(2015, 10, 12)),
            ('文化の日', datetime.date(2015, 11, 3)),
            ('勤労感謝の日', datetime.date(2015, 11, 23)),
            ('天皇誕生日', datetime.date(2015, 12, 23)),
            ('元日', datetime.date(2016, 1, 1)),
            ('成人の日', datetime.date(2016, 1, 11)),
            ('建国記念の日', datetime.date(2016, 2, 11)),
            ('春分の日', datetime.date(2016, 3, 20)),
            ('春分の日（振替休日）', datetime.date(2016, 3, 21)),
            ('昭和の日', datetime.date(2016, 4, 29)),
            ('憲法記念日', datetime.date(2016, 5, 3)),
            ('みどりの日', datetime.date(2016, 5, 4)),
            ('こどもの日', datetime.date(2016, 5, 5)),
            ('海の日', datetime.date(2016, 7, 18)),
            ('山の日', datetime.date(2016, 8, 11)),
            ('敬老の日', datetime.date(2016, 9, 19)),
            ('秋分の日', datetime.date(2016, 9, 22)),
            ('体育の日', datetime.date(2016, 10, 10)),
            ('文化の日', datetime.date(2016, 11, 3)),
            ('勤労感謝の日', datetime.date(2016, 11, 23)),
            ('天皇誕生日', datetime.date(2016, 12, 23)),
            ('元日', datetime.date(2017, 1, 1)),
            ('元日（振替休日）', datetime.date(2017, 1, 2)),
            ('成人の日', datetime.date(2017, 1, 9)),
            ('建国記念の日', datetime.date(2017, 2, 11)),
            ('春分の日', datetime.date(2017, 3, 20)),
            ('昭和の日', datetime.date(2017, 4, 29)),
            ('憲法記念日', datetime.date(2017, 5, 3)),
            ('みどりの日', datetime.date(2017, 5, 4)),
            ('こどもの日', datetime.date(2017, 5, 5)),
            ('海の日', datetime.date(2017, 7, 17)),
            ('山の日', datetime.date(2017, 8, 11)),
            ('敬老の日', datetime.date(2017, 9, 18)),
            ('秋分の日', datetime.date(2017, 9, 23)),
            ('体育の日', datetime.date(2017, 10, 9)),
            ('文化の日', datetime.date(2017, 11, 3)),
            ('勤労感謝の日', datetime.date(2017, 11, 23)),
            ('天皇誕生日', datetime.date(2017, 12, 23)),
            ('元日', datetime.date(2018, 1, 1)),
            ('成人の日', datetime.date(2018, 1, 8)),
            ('建国記念の日', datetime.date(2018, 2, 11)),
            ('建国記念の日（振替休日）', datetime.date(2018, 2, 12)),
            ('春分の日', datetime.date(2018, 3, 21)),
            ('昭和の日', datetime.date(2018, 4, 29)),
            ('昭和の日（振替休日）', datetime.date(2018, 4, 30)),
            ('憲法記念日', datetime.date(2018, 5, 3)),
            ('みどりの日', datetime.date(2018, 5, 4)),
            ('こどもの日', datetime.date(2018, 5, 5)),
            ('海の日', datetime.date(2018, 7, 16)),
            ('山の日', datetime.date(2018, 8, 11)),
            ('敬老の日', datetime.date(2018, 9, 17)),
            ('秋分の日', datetime.date(2018, 9, 23)),
            ('秋分の日（振替休日）', datetime.date(2018, 9, 24)),
            ('体育の日', datetime.date(2018, 10, 8)),
            ('文化の日', datetime.date(2018, 11, 3)),
            ('勤労感謝の日', datetime.date(2018, 11, 23)),
            ('天皇誕生日', datetime.date(2018, 12, 23)),
            ('天皇誕生日（振替休日）', datetime.date(2018, 12, 24)),
            ('元日', datetime.date(2019, 1, 1)),
            ('成人の日', datetime.date(2019, 1, 14)),
            ('建国記念の日', datetime.date(2019, 2, 11)),
            ('春分の日', datetime.date(2019, 3, 21)),
            ('昭和の日', datetime.date(2019, 4, 29)),
            ('国民の休日', datetime.date(2019, 4, 30)),
            ('国民の休日', datetime.date(2019, 5, 1)),
            ('国民の休日', datetime.date(2019, 5, 2)),
            ('憲法記念日', datetime.date(2019, 5, 3)),
            ('みどりの日', datetime.date(2019, 5, 4)),
            ('こどもの日', datetime.date(2019, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2019, 5, 6)),
            ('海の日', datetime.date(2019, 7, 15)),
            ('山の日', datetime.date(2019, 8, 11)),
            ('山の日（振替休日）', datetime.date(2019, 8, 12)),
            ('敬老の日', datetime.date(2019, 9, 16)),
            ('秋分の日', datetime.date(2019, 9, 23)),
            ('体育の日', datetime.date(2019, 10, 14)),
            ('国民の休日', datetime.date(2019, 10, 22)),
            ('文化の日', datetime.date(2019, 11, 3)),
            ('文化の日（振替休日）', datetime.date(2019, 11, 4)),
            ('勤労感謝の日', datetime.date(2019, 11, 23)),
            ('元日', datetime.date(2020, 1, 1)),
            ('成人の日', datetime.date(2020, 1, 13)),
            ('建国記念の日', datetime.date(2020, 2, 11)),
            ('天皇誕生日', datetime.date(2020, 2, 23)),
            ('天皇誕生日（振替休日）', datetime.date(2020, 2, 24)),
            ('春分の日', datetime.date(2020, 3, 20)),
            ('昭和の日', datetime.date(2020, 4, 29)),
            ('憲法記念日', datetime.date(2020, 5, 3)),
            ('みどりの日', datetime.date(2020, 5, 4)),
            ('こどもの日', datetime.date(2020, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2020, 5, 6)),
            ('海の日', datetime.date(2020, 7, 23)),
            ('スポーツの日', datetime.date(2020, 7, 24)),
            ('山の日', datetime.date(2020, 8, 10)),
            ('敬老の日', datetime.date(2020, 9, 21)),
            ('秋分の日', datetime.date(2020, 9, 22)),
            ('文化の日', datetime.date(2020, 11, 3)),
            ('勤労感謝の日', datetime.date(2020, 11, 23)),
            ('元日', datetime.date(2021, 1, 1)),
            ('成人の日', datetime.date(2021, 1, 11)),
            ('建国記念の日', datetime.date(2021, 2, 11)),
            ('天皇誕生日', datetime.date(2021, 2, 23)),
            ('春分の日', datetime.date(2021, 3, 20)),
            ('昭和の日', datetime.date(2021, 4, 29)),
            ('憲法記念日', datetime.date(2021, 5, 3)),
            ('みどりの日', datetime.date(2021, 5, 4)),
            ('こどもの日', datetime.date(2021, 5, 5)),
            ('海の日', datetime.date(2021, 7, 22)),
            ('スポーツの日', datetime.date(2021, 7, 23)),
            ('山の日', datetime.date(2021, 8, 8)),
            ('山の日（振替休日）', datetime.date(2021, 8, 9)),
            ('敬老の日', datetime.date(2021, 9, 20)),
            ('秋分の日', datetime.date(2021, 9, 23)),
            ('文化の日', datetime.date(2021, 11, 3)),
            ('勤労感謝の日', datetime.date(2021, 11, 23)),
            ('元日', datetime.date(2022, 1, 1)),
            ('成人の日', datetime.date(2022, 1, 10)),
            ('建国記念の日', datetime.date(2022, 2, 11)),
            ('天皇誕生日', datetime.date(2022, 2, 23)),
            ('春分の日', datetime.date(2022, 3, 21)),
            ('昭和の日', datetime.date(2022, 4, 29)),
            ('憲法記念日', datetime.date(2022, 5, 3)),
            ('みどりの日', datetime.date(2022, 5, 4)),
            ('こどもの日', datetime.date(2022, 5, 5)),
            ('海の日', datetime.date(2022, 7, 18)),
            ('山の日', datetime.date(2022, 8, 11)),
            ('敬老の日', datetime.date(2022, 9, 19)),
            ('秋分の日', datetime.date(2022, 9, 23)),
            ('スポーツの日', datetime.date(2022, 10, 10)),
            ('文化の日', datetime.date(2022, 11, 3)),
            ('勤労感謝の日', datetime.date(2022, 11, 23)),
            ('元日', datetime.date(2023, 1, 1)),
            ('元日（振替休日）', datetime.date(2023, 1, 2)),
            ('成人の日', datetime.date(2023, 1, 9)),
            ('建国記念の日', datetime.date(2023, 2, 11)),
            ('天皇誕生日', datetime.date(2023, 2, 23)),
            ('春分の日', datetime.date(2023, 3, 21)),
            ('昭和の日', datetime.date(2023, 4, 29)),
            ('憲法記念日', datetime.date(2023, 5, 3)),
            ('みどりの日', datetime.date(2023, 5, 4)),
            ('こどもの日', datetime.date(2023, 5, 5)),
            ('海の日', datetime.date(2023, 7, 17)),
            ('山の日', datetime.date(2023, 8, 11)),
            ('敬老の日', datetime.date(2023, 9, 18)),
            ('秋分の日', datetime.date(2023, 9, 23)),
            ('スポーツの日', datetime.date(2023, 10, 9)),
            ('文化の日', datetime.date(2023, 11, 3)),
            ('勤労感謝の日', datetime.date(2023, 11, 23)),
            ('元日', datetime.date(2024, 1, 1)),
            ('成人の日', datetime.date(2024, 1, 8)),
            ('建国記念の日', datetime.date(2024, 2, 11)),
            ('建国記念の日（振替休日）', datetime.date(2024, 2, 12)),
            ('天皇誕生日', datetime.date(2024, 2, 23)),
            ('春分の日', datetime.date(2024, 3, 20)),
            ('昭和の日', datetime.date(2024, 4, 29)),
            ('憲法記念日', datetime.date(2024, 5, 3)),
            ('みどりの日', datetime.date(2024, 5, 4)),
            ('こどもの日', datetime.date(2024, 5, 5)),
            ('こどもの日（振替休日）', datetime.date(2024, 5, 6)),
            ('海の日', datetime.date(2024, 7, 15)),
            ('山の日', datetime.date(2024, 8, 11)),
            ('山の日（振替休日）', datetime.date(2024, 8, 12)),
            ('敬老の日', datetime.date(2024, 9, 16)),
            ('秋分の日', datetime.date(2024, 9, 22)),
            ('秋分の日（振替休日）', datetime.date(2024, 9, 23)),
            ('スポーツの日', datetime.date(2024, 10, 14)),
            ('文化の日', datetime.date(2024, 11, 3)),
            ('文化の日（振替休日）', datetime.date(2024, 11, 4)),
            ('勤労感謝の日', datetime.date(2024, 11, 23))]
        self.assertEqual(self.holidays.get_holidays_in_range(
            start_date, end_date), expected_holidays)

    def test_get_business_date_range(self):
        start_date = datetime.date(2023, 6, 1)
        end_date = datetime.date(2023, 6, 10)
        expected_business_days = [
            datetime.date(2023, 6, 1),
            datetime.date(2023, 6, 2),
            datetime.date(2023, 6, 5),
            datetime.date(2023, 6, 6),
            datetime.date(2023, 6, 7),
            datetime.date(2023, 6, 8),
            datetime.date(2023, 6, 9),
        ]
        self.assertEqual(self.holidays.get_business_date_range(
            start_date, end_date), expected_business_days)

    def test_get_last_business_day(self):
        date = datetime.date(2023, 6, 10)
        expected_last_business_day = datetime.date(2023, 6, 30)
        self.assertEqual(self.holidays.get_last_business_day(
            date), expected_last_business_day)

    def test_get_date_information(self):
        date = datetime.date(2023, 7, 17)
        expected_info = (2, 'Monday', 0, '海の日')
        self.assertEqual(
            self.holidays.get_date_information(date), expected_info)

        date = datetime.date(2023, 6, 10)
        expected_info = (0, 'Saturday', 5, None)
        self.assertEqual(
            self.holidays.get_date_information(date), expected_info)

        date = datetime.date(2023, 6, 11)
        expected_info = (1, 'Sunday', 6, None)
        self.assertEqual(
            self.holidays.get_date_information(date), expected_info)

        date = datetime.date(2023, 6, 12)
        expected_info = (1, 'Monday', 0, None)
        self.assertEqual(
            self.holidays.get_date_information(date), expected_info)

        date = datetime.date(2023, 10, 1)
        expected_info = (0, 'Sunday', 6, None)
        self.assertEqual(
            self.holidays.get_date_information(date), expected_info)

        date = datetime.date(2023, 10, 29)
        expected_info = (5, 'Sunday', 6, None)
        self.assertEqual(
            self.holidays.get_date_information(date), expected_info)

    def test_print_calendar(self):
        from flaretool.constants import ConsoleColor as Color
        with patch('sys.stdout', new=StringIO()) as fake_out:
            date = datetime.date(2023, 8, 1)
            year = date.year
            month = date.month
            expected_output = ""

            def format_day(year, month, day, weekday):
                if weekday == 0:
                    return f'{Color.RED}{day:2d}{Color.RESET} '
                elif weekday == 6:
                    return f'{Color.BLUE}{day:2d}{Color.RESET} '
                else:
                    if self.holidays.get_holiday_name(datetime.date(year, month, day)):
                        return f'{Color.GREEN}{day:2d}{Color.RESET} '
                    else:
                        return f"{day:2d} "
            calendar.setfirstweekday(calendar.SUNDAY)

            # カレンダーを取得
            cal = calendar.monthcalendar(year, month)

            # 月と年を出力
            expected_output += "     " + \
                calendar.month_name[month] + " " + str(year)
            expected_output += "\nSu Mo Tu We Th Fr Sa\n"

            # カレンダーを出力
            for week in cal:
                line = ""
                for w, day in enumerate(week):
                    if day == 0:
                        line += "   "
                    else:
                        line += format_day(year, month, day, w)
                expected_output += line + "\n"
            self.holidays.print_calendar(date)
            self.assertEqual(fake_out.getvalue(), expected_output)

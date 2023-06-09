#!/bin/python
# -*- coding: utf-8 -*-
import unittest
from flaretool.holiday import JapaneseHolidays
import datetime


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

        date = datetime.date(2023, 2, 12)
        self.assertFalse(self.holidays.is_foundation_day(date))

    def test_is_spring_equinox(self):
        date = datetime.date(2023, 3, 21)
        self.assertTrue(self.holidays.is_spring_equinox(date))

        date = datetime.date(2023, 3, 22)
        self.assertFalse(self.holidays.is_spring_equinox(date))

    def test_is_showa_day(self):
        date = datetime.date(2023, 4, 29)
        self.assertTrue(self.holidays.is_showa_day(date))

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

        date = datetime.date(2023, 9, 24)
        self.assertFalse(self.holidays.is_autumn_equinox(date))

    def test_is_health_and_sports_day(self):
        date = datetime.date(2023, 10, 9)
        self.assertTrue(self.holidays.is_health_and_sports_day(date))

        date = datetime.date(2023, 10, 15)
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

    def test_is_transfer_holiday(self):
        date = datetime.date(2023, 1, 2)
        self.assertTrue(self.holidays.is_transfer_holiday(date))

    def test_is_additional_holiday(self):
        date = datetime.date(2023, 1, 2)
        self.holidays.set_additional_holiday("Additional Holiday", date)
        self.assertTrue(self.holidays.is_additional_holiday(date))

    def test_set_additional_holiday(self):
        date = datetime.date(2023, 12, 25)
        self.holidays.set_additional_holiday("Additional Holiday", date)
        self.assertEqual(
            self.holidays._additional_holidays[date], "Additional Holiday")

    def test_week_day(self):
        date = datetime.date(2023, 6, 10)
        expected_date = datetime.date(2023, 6, 12)
        self.assertEqual(self.holidays.week_day(date, 2, 1), expected_date)

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
        start_date = datetime.date(2023, 7, 1)
        end_date = datetime.date(2023, 7, 20)
        expected_holidays = [
            ("海の日", datetime.date(2023, 7, 17)),
        ]
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


if __name__ == '__main__':
    unittest.main()
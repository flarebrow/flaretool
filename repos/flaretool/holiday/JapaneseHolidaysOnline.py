#!/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
from typing import Any, Union
import warnings
from flaretool.holiday import JapaneseHolidays
from flaretool.holiday.errors import JapaneseHolidaysError
from flaretool.holiday.models import HolidaysResponseModel
from flaretool.common import requests
from flaretool.decorators import network_required
from flaretool.logger import get_logger
from flaretool.constants import BASE_API_URL

logger = get_logger()

__all__ = []

class JapaneseHolidaysOnline(JapaneseHolidays):
    """
    日本の祝日を管理するクラス(オンライン版)
    """

    def __init__(self):
        super().__init__()
        self.holidays = self.__request_get_holiday()
        self.version = self.holidays.version
        self.__is_warning = False
        logger.info(str(self).replace("\n", " "))

    def __str__(self):
        return "{}\n{} v{}\nPowered By {}\nUpdated {}\nSupported {} ~ {}\n".format(
            self.__class__.__name__,
            self.holidays.title,
            self.holidays.version,
            self.holidays.author,
            self.holidays.updated,
            self.holidays.supported.from_date,
            self.holidays.supported.to_date,
        )

    def show_info(self):
        """
        祝日の対応情報を表示
        """
        print(self.__str__())

    @network_required
    def __request_get_holiday(self) -> HolidaysResponseModel:
        response = requests.get(f"{BASE_API_URL}/japanholiday.json")
        result = response.json()
        holidays = HolidaysResponseModel(**result)
        if not holidays.status:
            warnings.warn(holidays.message, Warning)
        if holidays.count == 0:
            raise JapaneseHolidaysError(message=holidays.message)
        return holidays

    def __super_method(self, method: str, date: datetime.date):
        if not self.holidays.supported.from_date <= date <= self.holidays.supported.to_date:
            if not self.__is_warning:
                message = "The online version does not support '{}'. It supports dates from '{}' to '{}'. execute it offline.".format(
                    date, self.holidays.supported.from_date, self.holidays.supported.to_date)
                warnings.warn(message, Warning)
                self.__is_warning = True
            return True, getattr(super(), method)(date)
        return False, None

    def get_holiday_name(self, date: Union[str, datetime.datetime, datetime.date]) -> Union[str, None]:
        date = self.to_date(date)

        unsupport, is_holiday = self.__super_method(
            sys._getframe().f_code.co_name, date)
        if unsupport:
            return is_holiday

        if self.is_additional_holiday(date):
            return self._additional_holidays.get(date)
        return self.holidays.holidays.get(date, None)

    def __is_holiday_not_substitute(self, method, holiday_name, date) -> bool:
        unsupport, is_holiday = self.__super_method(method, date)
        return is_holiday if unsupport else \
            date in [date for date, name in self.holidays.holidays.items()
                     if holiday_name in name and not "振替" in name]

    def is_new_year(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "元日", date)

    def is_coming_of_age_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "成人の日", date)

    def is_foundation_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "建国記念", date)

    def is_spring_equinox(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "春分の日", date)

    def is_showa_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "昭和の日", date)

    def is_constitution_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "憲法記念日", date)

    def is_greenery_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "みどりの日", date)

    def is_childrens_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "こどもの日", date)

    def is_marine_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "海の日", date)

    def is_mountain_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "山の日", date)

    def is_respect_for_the_aged_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "敬老の日", date)

    def is_autumn_equinox(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "秋分の日", date)

    def is_health_and_sports_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "体育の日", date) \
            or self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "スポーツの日", date)

    def is_culture_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "文化の日", date)

    def is_labour_thanksgiving_day(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "勤労感謝", date)

    def is_emperors_birthday(self, date: datetime.date) -> bool:
        return self.__is_holiday_not_substitute(sys._getframe().f_code.co_name, "天皇誕生日", date)

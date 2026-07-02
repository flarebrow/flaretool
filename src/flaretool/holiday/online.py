"""日本の祝日を管理するクラス（オンライン版）"""

import datetime
import warnings
from collections.abc import Callable
from typing import override

from flaretool.common import requests
from flaretool.constants import API_BASE_URL_OLD
from flaretool.decorators import network_required
from flaretool.holiday.errors import JapaneseHolidaysError
from flaretool.holiday.japanese_holidays import JapaneseHolidays
from flaretool.holiday.models import HolidaysResponseModel
from flaretool.logger import get_logger

logger = get_logger()

__all__ = ["JapaneseHolidaysOnline"]


class JapaneseHolidaysOnline(JapaneseHolidays):
    """
    日本の祝日を管理するクラス(オンライン版)

    コンストラクタで祝日データをAPIから取得します。
    サポート範囲外の日付はオフライン版のロジックにフォールバックします
    （その際、インスタンスごとに一度だけ警告を出します）。
    """

    holidays: HolidaysResponseModel
    version: str

    def __init__(self) -> None:
        super().__init__()
        self.holidays = self._request_get_holiday()
        self.version = self.holidays.version
        self._out_of_range_warned = False
        # 祝日名キーワード -> 該当日付集合 の遅延キャッシュ
        self._holiday_dates_cache: dict[str, frozenset[datetime.date]] = {}
        logger.info(str(self).replace("\n", " "))

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}\n"
            f"{self.holidays.title} v{self.holidays.version}\n"
            f"Powered By {self.holidays.author}\n"
            f"Updated {self.holidays.updated}\n"
            f"Supported {self.holidays.supported.from_date}"
            f" ~ {self.holidays.supported.to_date}\n"
        )

    def show_info(self) -> None:
        """
        祝日の対応情報を表示
        """
        print(self)

    @network_required
    def _request_get_holiday(self) -> HolidaysResponseModel:
        response = requests.get(f"{API_BASE_URL_OLD}/japanholiday.json")
        holidays = HolidaysResponseModel(**response.json())
        if not holidays.status:
            warnings.warn(holidays.message, Warning, stacklevel=2)
        if holidays.count == 0:
            raise JapaneseHolidaysError(message=holidays.message)
        return holidays

    def _is_supported(self, date: datetime.date) -> bool:
        """オンラインデータのサポート範囲内かを判定する（範囲外は一度だけ警告）"""
        supported = self.holidays.supported
        if supported.from_date <= date <= supported.to_date:
            return True
        if not self._out_of_range_warned:
            warnings.warn(
                f"The online version does not support '{date}'. "
                f"It supports dates from '{supported.from_date}' "
                f"to '{supported.to_date}'. execute it offline.",
                Warning,
                stacklevel=2,
            )
            self._out_of_range_warned = True
        return False

    def _holiday_dates(self, keyword: str) -> frozenset[datetime.date]:
        """祝日名にキーワードを含む日付集合を返す（振替休日は除く）"""
        dates = self._holiday_dates_cache.get(keyword)
        if dates is None:
            dates = frozenset(
                date
                for date, name in (self.holidays.holidays or {}).items()
                if keyword in name and "振替" not in name
            )
            self._holiday_dates_cache[keyword] = dates
        return dates

    def _is_online_holiday(
        self,
        keyword: str,
        date: datetime.date,
        offline: Callable[[datetime.date], bool],
    ) -> bool:
        """オンラインデータで祝日判定する（範囲外はオフライン判定に委譲）"""
        if not self._is_supported(date):
            return offline(date)
        return date in self._holiday_dates(keyword)

    @override
    def _statutory_holiday_name(self, date: datetime.date) -> str | None:
        """
        法定祝日名を取得（オンライン版）

        サポート範囲内はオンラインデータで判定し、範囲外は
        オフライン版のロジックにフォールバックします
        （その際、インスタンスごとに一度だけ警告を出します）。

        単発の追加休日・追加休日由来の振替休日・カスタム休日ルールの
        評価は基底クラス側で行われるため、判定の優先順位
        （法定祝日 → 追加休日 → 追加休日の振替休日 → カスタムルール）は
        オフライン版と同一です。
        """
        if not self._is_supported(date):
            return super()._statutory_holiday_name(date)
        return (self.holidays.holidays or {}).get(date)

    @override
    def is_new_year(self, date: datetime.date) -> bool:
        return self._is_online_holiday("元日", date, super().is_new_year)

    @override
    def is_coming_of_age_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("成人の日", date, super().is_coming_of_age_day)

    @override
    def is_foundation_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("建国記念", date, super().is_foundation_day)

    @override
    def is_spring_equinox(self, date: datetime.date) -> bool:
        return self._is_online_holiday("春分の日", date, super().is_spring_equinox)

    @override
    def is_showa_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("昭和の日", date, super().is_showa_day)

    @override
    def is_constitution_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("憲法記念日", date, super().is_constitution_day)

    @override
    def is_greenery_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("みどりの日", date, super().is_greenery_day)

    @override
    def is_childrens_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("こどもの日", date, super().is_childrens_day)

    @override
    def is_marine_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("海の日", date, super().is_marine_day)

    @override
    def is_mountain_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("山の日", date, super().is_mountain_day)

    @override
    def is_respect_for_the_aged_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday(
            "敬老の日", date, super().is_respect_for_the_aged_day
        )

    @override
    def is_autumn_equinox(self, date: datetime.date) -> bool:
        return self._is_online_holiday("秋分の日", date, super().is_autumn_equinox)

    @override
    def is_health_and_sports_day(self, date: datetime.date) -> bool:
        # 範囲外はオフライン判定を一度だけ評価して返す
        # （2つのキーワードそれぞれでフォールバックを重複評価しない）
        if not self._is_supported(date):
            return super().is_health_and_sports_day(date)
        return date in self._holiday_dates("体育の日") or date in self._holiday_dates(
            "スポーツの日"
        )

    @override
    def is_culture_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday("文化の日", date, super().is_culture_day)

    @override
    def is_labour_thanksgiving_day(self, date: datetime.date) -> bool:
        return self._is_online_holiday(
            "勤労感謝", date, super().is_labour_thanksgiving_day
        )

    @override
    def is_emperors_birthday(self, date: datetime.date) -> bool:
        return self._is_online_holiday("天皇誕生日", date, super().is_emperors_birthday)

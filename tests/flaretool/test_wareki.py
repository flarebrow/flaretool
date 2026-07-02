import datetime
import unittest

from flaretool.wareki import (
    ERAS,
    Era,
    get_era,
    get_fiscal_year,
    int_to_kanji,
    kanji_to_int,
    to_seireki,
    to_wareki,
    today_wareki,
)

# 元号の境界日テーブル: (日付, 元号名, 和暦年)
ERA_BOUNDARY_CASES = [
    (datetime.date(1868, 10, 23), "明治", 1),
    (datetime.date(1912, 7, 29), "明治", 45),
    (datetime.date(1912, 7, 30), "大正", 1),
    (datetime.date(1926, 12, 24), "大正", 15),
    (datetime.date(1926, 12, 25), "昭和", 1),
    (datetime.date(1989, 1, 7), "昭和", 64),
    (datetime.date(1989, 1, 8), "平成", 1),
    (datetime.date(2019, 4, 30), "平成", 31),
    (datetime.date(2019, 5, 1), "令和", 1),
]


class ErasTestCase(unittest.TestCase):
    def test_eras_structure(self):
        self.assertEqual(len(ERAS), 5)
        names = [era.name for era in ERAS]
        self.assertEqual(names, ["明治", "大正", "昭和", "平成", "令和"])
        # 各元号の終了日は次の元号の開始日の前日
        for current, following in zip(ERAS, ERAS[1:]):
            self.assertEqual(current.end, following.start - datetime.timedelta(days=1))
        self.assertIsNone(ERAS[-1].end)

    def test_era_attributes(self):
        reiwa = ERAS[-1]
        self.assertIsInstance(reiwa, Era)
        self.assertEqual(reiwa.name, "令和")
        self.assertEqual(reiwa.name_short, "R")
        self.assertEqual(reiwa.romaji, "Reiwa")
        self.assertEqual(reiwa.start, datetime.date(2019, 5, 1))

    def test_era_frozen(self):
        with self.assertRaises(Exception):
            ERAS[0].name = "改元"


class GetEraTestCase(unittest.TestCase):
    def test_boundary_days(self):
        for date, era_name, _ in ERA_BOUNDARY_CASES:
            with self.subTest(date=date):
                self.assertEqual(get_era(date).name, era_name)

    def test_input_types(self):
        self.assertEqual(get_era(datetime.date(2019, 5, 1)).name, "令和")
        self.assertEqual(
            get_era(datetime.datetime(2019, 5, 1, 12, 34, 56)).name, "令和"
        )
        self.assertEqual(get_era("2019-05-01").name, "令和")
        self.assertEqual(get_era("2019/05/01").name, "令和")
        self.assertEqual(get_era("2019.05.01").name, "令和")
        self.assertEqual(get_era("2019年5月1日").name, "令和")
        self.assertEqual(get_era("２０１９年５月１日").name, "令和")

    def test_pre_meiji_raises(self):
        with self.assertRaises(ValueError):
            get_era(datetime.date(1868, 10, 22))
        with self.assertRaises(ValueError):
            get_era("1600-01-01")

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            get_era("not a date")
        with self.assertRaises(ValueError):
            get_era("")
        with self.assertRaises(ValueError):
            get_era(20190501)


class ToWarekiTestCase(unittest.TestCase):
    def test_default_format(self):
        self.assertEqual(to_wareki(datetime.date(2026, 7, 2)), "令和8年7月2日")
        self.assertEqual(to_wareki("1970-12-25"), "昭和45年12月25日")

    def test_boundary_days(self):
        for date, era_name, year in ERA_BOUNDARY_CASES:
            with self.subTest(date=date):
                year_text = "元" if year == 1 else str(year)
                expected = f"{era_name}{year_text}年{date.month}月{date.day}日"
                self.assertEqual(to_wareki(date), expected)

    def test_gannen_rendering(self):
        self.assertEqual(to_wareki("2019-05-01"), "令和元年5月1日")
        self.assertEqual(to_wareki("2019-05-01", gannen=False), "令和1年5月1日")
        self.assertEqual(to_wareki("1989-01-08"), "平成元年1月8日")
        # {year_kanji}はgannenの影響を受けず常に漢数字
        self.assertEqual(
            to_wareki("2019-05-01", format="{era}{year_kanji}年"), "令和一年"
        )

    def test_custom_formats(self):
        date = datetime.date(2026, 7, 2)
        self.assertEqual(
            to_wareki(date, format="{era_short}{year}.{month}.{day}"), "R8.7.2"
        )
        self.assertEqual(
            to_wareki(date, format="{era_romaji} {year}-{month}-{day}"),
            "Reiwa 8-7-2",
        )
        self.assertEqual(
            to_wareki(date, format="{era}{year_kanji}年{month_kanji}月{day_kanji}日"),
            "令和八年七月二日",
        )
        # 数値プレースホルダーは書式指定が使える
        self.assertEqual(
            to_wareki(
                date,
                format="{era_short}{year:02}.{month:02}.{day:02}",
                gannen=False,
            ),
            "R08.07.02",
        )

    def test_datetime_input(self):
        self.assertEqual(
            to_wareki(datetime.datetime(2019, 4, 30, 23, 59)), "平成31年4月30日"
        )

    def test_unknown_placeholder_raises(self):
        with self.assertRaises(ValueError):
            to_wareki("2026-07-02", format="{unknown}")

    def test_era_year_100_or_more(self):
        """元号100年以降でもデフォルト書式で変換できる（バグ修正の確認）"""
        # 2118年は令和100年
        self.assertEqual(to_wareki("2118-07-02"), "令和100年7月2日")
        self.assertEqual(
            to_wareki("2118-07-02", format="{era_short}{year}.{month}.{day}"),
            "R100.7.2",
        )
        # {year_kanji}を参照した場合は「百」を使った漢数字になる
        self.assertEqual(
            to_wareki("2118-07-02", format="{era}{year_kanji}年"), "令和百年"
        )
        self.assertEqual(
            to_wareki(
                "2119-07-02",
                format="{era}{year_kanji}年{month_kanji}月{day_kanji}日",
            ),
            "令和百一年七月二日",
        )

    def test_era_year_100_round_trip(self):
        date = datetime.date(2118, 7, 2)
        self.assertEqual(to_seireki(to_wareki(date)), date)
        fmt = "{era}{year_kanji}年{month_kanji}月{day_kanji}日"
        self.assertEqual(to_seireki(to_wareki(date, format=fmt)), date)

    def test_pre_meiji_raises(self):
        with self.assertRaises(ValueError):
            to_wareki("1868-10-22")


class ToSeirekiTestCase(unittest.TestCase):
    def test_various_formats(self):
        cases = [
            ("令和8年7月2日", datetime.date(2026, 7, 2)),
            ("令和元年5月1日", datetime.date(2019, 5, 1)),
            ("R8.7.2", datetime.date(2026, 7, 2)),
            ("R8/7/2", datetime.date(2026, 7, 2)),
            ("R8-7-2", datetime.date(2026, 7, 2)),
            ("r8.7.2", datetime.date(2026, 7, 2)),
            ("H31.4.30", datetime.date(2019, 4, 30)),
            ("S64.1.7", datetime.date(1989, 1, 7)),
            ("T15.12.24", datetime.date(1926, 12, 24)),
            ("M45.7.29", datetime.date(1912, 7, 29)),
            ("明治元年10月23日", datetime.date(1868, 10, 23)),
            ("Reiwa 8-7-2", datetime.date(2026, 7, 2)),
            ("Heisei 31-4-30", datetime.date(2019, 4, 30)),
            ("Ｒ８年７月２日", datetime.date(2026, 7, 2)),
            ("令和八年七月二日", datetime.date(2026, 7, 2)),
            ("昭和六十四年一月七日", datetime.date(1989, 1, 7)),
            ("令和8年12月31日", datetime.date(2026, 12, 31)),
            ("  令和8年7月2日  ", datetime.date(2026, 7, 2)),
            ("令和100年7月2日", datetime.date(2118, 7, 2)),
            ("令和百年7月2日", datetime.date(2118, 7, 2)),
            ("令和百一年七月二日", datetime.date(2119, 7, 2)),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(to_seireki(text), expected)

    def test_invalid_parses(self):
        invalid_texts = [
            "安政2年1月1日",  # 未対応の元号
            "R0.1.1",  # 年0
            "R8.13.1",  # 月13
            "R8.1.32",  # 日32
            "令和8年2月30日",  # 存在しない日付
            "令和8年7月",  # 日なし
            "令和8年",  # 月日なし
            "令和",  # 年月日なし
            "2026-07-02",  # 元号なし
            "",
            "H32.1.1",  # 平成の期間外 (2020年)
            "昭和65年1月1日",  # 昭和の期間外 (1990年)
            "昭和百年1月1日",  # 昭和の期間外 (2025年)
            "令和千年1月1日",  # 漢数字の範囲外 (千は未対応)
        ]
        for text in invalid_texts:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    to_seireki(text)

    def test_invalid_type_raises(self):
        with self.assertRaises(ValueError):
            to_seireki(20260702)


class RoundTripTestCase(unittest.TestCase):
    def _sweep_dates(self, step_days: int = 97):
        date = ERAS[0].start
        end = datetime.date(2035, 12, 31)
        step = datetime.timedelta(days=step_days)
        while date <= end:
            yield date
            date += step
        # 境界日も必ず含める
        for boundary, _, _ in ERA_BOUNDARY_CASES:
            yield boundary

    def test_round_trip_default_format(self):
        for date in self._sweep_dates():
            with self.subTest(date=date):
                self.assertEqual(to_seireki(to_wareki(date)), date)

    def test_round_trip_short_format(self):
        fmt = "{era_short}{year}.{month}.{day}"
        for date in self._sweep_dates(step_days=203):
            with self.subTest(date=date):
                self.assertEqual(
                    to_seireki(to_wareki(date, format=fmt, gannen=False)), date
                )

    def test_round_trip_kanji_format(self):
        fmt = "{era}{year_kanji}年{month_kanji}月{day_kanji}日"
        for date in self._sweep_dates(step_days=203):
            with self.subTest(date=date):
                self.assertEqual(to_seireki(to_wareki(date, format=fmt)), date)


class KanjiNumberTestCase(unittest.TestCase):
    def test_kanji_to_int(self):
        cases = [
            ("一", 1),
            ("八", 8),
            ("十", 10),
            ("十二", 12),
            ("二十", 20),
            ("二十九", 29),
            ("六十四", 64),
            ("九十九", 99),
            ("百", 100),
            ("百一", 101),
            ("百十", 110),
            ("二百", 200),
            ("九百九十九", 999),
            ("元", 1),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(kanji_to_int(text), expected)

    def test_int_to_kanji(self):
        cases = [
            (1, "一"),
            (8, "八"),
            (10, "十"),
            (12, "十二"),
            (20, "二十"),
            (29, "二十九"),
            (64, "六十四"),
            (99, "九十九"),
            (100, "百"),
            (101, "百一"),
            (110, "百十"),
            (200, "二百"),
            (999, "九百九十九"),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(int_to_kanji(value), expected)

    def test_round_trip_1_to_999(self):
        for value in range(1, 1000):
            with self.subTest(value=value):
                self.assertEqual(kanji_to_int(int_to_kanji(value)), value)

    def test_kanji_to_int_invalid(self):
        for text in ["", "〇", "千", "二三", "abc", "十十", "百百", "元年"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    kanji_to_int(text)
        with self.assertRaises(ValueError):
            kanji_to_int(8)

    def test_int_to_kanji_invalid(self):
        for value in [0, -1, 1000, 10000]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    int_to_kanji(value)
        with self.assertRaises(ValueError):
            int_to_kanji("八")
        with self.assertRaises(ValueError):
            int_to_kanji(True)


class FiscalYearTestCase(unittest.TestCase):
    def test_default_start_month(self):
        self.assertEqual(get_fiscal_year("2026-03-31"), 2025)
        self.assertEqual(get_fiscal_year("2026-04-01"), 2026)
        self.assertEqual(get_fiscal_year(datetime.date(2026, 12, 31)), 2026)
        self.assertEqual(get_fiscal_year(datetime.datetime(2026, 1, 1)), 2025)

    def test_custom_start_month(self):
        self.assertEqual(get_fiscal_year("2026-03-31", start_month=1), 2026)
        self.assertEqual(get_fiscal_year("2026-09-30", start_month=10), 2025)
        self.assertEqual(get_fiscal_year("2026-10-01", start_month=10), 2026)

    def test_invalid_start_month(self):
        for start_month in [0, 13, -1, "4"]:
            with self.subTest(start_month=start_month):
                with self.assertRaises(ValueError):
                    get_fiscal_year("2026-07-02", start_month=start_month)


class TodayWarekiTestCase(unittest.TestCase):
    def test_matches_to_wareki_today(self):
        today = datetime.date.today()
        self.assertEqual(today_wareki(), to_wareki(today))
        self.assertEqual(
            today_wareki(format="{era_short}{year}.{month}.{day}", gannen=False),
            to_wareki(today, format="{era_short}{year}.{month}.{day}", gannen=False),
        )


if __name__ == "__main__":
    unittest.main()

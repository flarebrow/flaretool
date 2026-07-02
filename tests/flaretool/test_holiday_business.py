#!/bin/python
"""営業日計算・カスタム休日ルール機能のテスト"""

import base64
import datetime
import json
import unittest
import warnings
from unittest.mock import patch

from flaretool.holiday import JapaneseHolidays, JapaneseHolidaysOnline


class JapaneseHolidaysBusinessTest(unittest.TestCase):
    @patch("flaretool.common.requests.request")
    def setUp(self, mock_requests):
        self.holidays = JapaneseHolidays()
        mock_requests.return_value.status_code = 200
        with open("tests/flaretool/testdata/japanholiday.dat", "rb") as f:
            japanholiday_json = json.loads(base64.b64decode(f.read()).decode("utf-8"))
        mock_requests.return_value.json.return_value = japanholiday_json
        self.holidays_online = JapaneseHolidaysOnline()

    # ------------------------------------------------------------------
    # add_business_days
    # ------------------------------------------------------------------

    def test_add_business_days_forward(self):
        # 2026年GW: 4/29(水・昭和の日), 5/2(土), 5/3(日・憲法記念日),
        # 5/4(月・みどりの日), 5/5(火・こどもの日), 5/6(水・振替休日)
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 4, 28), 1),
            datetime.date(2026, 4, 30),
        )
        # 5/1(金)の翌営業日はGWをまたいで5/7(木)
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 5, 1), 1),
            datetime.date(2026, 5, 7),
        )
        # 4/28(火)から3営業日後: 4/30, 5/1, 5/7
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 4, 28), 3),
            datetime.date(2026, 5, 7),
        )
        # 文字列でも指定可能
        self.assertEqual(
            self.holidays.add_business_days("2026/05/01", 1),
            datetime.date(2026, 5, 7),
        )

    def test_add_business_days_backward(self):
        # 5/7(木)の1営業日前はGWをまたいで5/1(金)
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 5, 7), -1),
            datetime.date(2026, 5, 1),
        )
        # 5/11(月)から2営業日前: 5/8(金), 5/7(木)
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 5, 11), -2),
            datetime.date(2026, 5, 7),
        )

    def test_add_business_days_zero(self):
        # days=0 は変換した日付をそのまま返す（休日でも判定しない）
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 5, 3), 0),
            datetime.date(2026, 5, 3),
        )
        self.assertEqual(
            self.holidays.add_business_days("2026-05-03", 0),
            datetime.date(2026, 5, 3),
        )

    def test_add_business_days_online(self):
        # オンライン版（フィクスチャのサポート範囲内: 2024年GW）
        # 2024年: 5/3(金), 5/4(土), 5/5(日), 5/6(月・振替休日)
        self.assertEqual(
            self.holidays_online.add_business_days(datetime.date(2024, 5, 1), 2),
            datetime.date(2024, 5, 7),
        )
        self.assertEqual(
            self.holidays_online.add_business_days(datetime.date(2024, 5, 7), -1),
            datetime.date(2024, 5, 2),
        )

    # ------------------------------------------------------------------
    # next_business_day / previous_business_day
    # ------------------------------------------------------------------

    def test_next_business_day(self):
        # 5/3(日・祝)以降の直近の営業日は5/7(木)
        self.assertEqual(
            self.holidays.next_business_day(datetime.date(2026, 5, 3)),
            datetime.date(2026, 5, 7),
        )
        # include_start=True なら営業日の起点はそのまま返す
        self.assertEqual(
            self.holidays.next_business_day(
                datetime.date(2026, 5, 1), include_start=True
            ),
            datetime.date(2026, 5, 1),
        )
        # include_start=False（デフォルト）なら翌営業日
        self.assertEqual(
            self.holidays.next_business_day(datetime.date(2026, 5, 1)),
            datetime.date(2026, 5, 7),
        )
        # 休日起点ならinclude_start=Trueでも次の営業日
        self.assertEqual(
            self.holidays.next_business_day(
                datetime.date(2026, 5, 3), include_start=True
            ),
            datetime.date(2026, 5, 7),
        )

    def test_previous_business_day(self):
        # 5/6(水・振替休日)以前の直近の営業日は5/1(金)
        self.assertEqual(
            self.holidays.previous_business_day(datetime.date(2026, 5, 6)),
            datetime.date(2026, 5, 1),
        )
        self.assertEqual(
            self.holidays.previous_business_day(
                datetime.date(2026, 5, 7), include_start=True
            ),
            datetime.date(2026, 5, 7),
        )
        self.assertEqual(
            self.holidays.previous_business_day(datetime.date(2026, 5, 7)),
            datetime.date(2026, 5, 1),
        )

    def test_next_previous_business_day_online(self):
        # 2024年GW（サポート範囲内）
        self.assertEqual(
            self.holidays_online.next_business_day(datetime.date(2024, 5, 3)),
            datetime.date(2024, 5, 7),
        )
        self.assertEqual(
            self.holidays_online.previous_business_day(datetime.date(2024, 5, 6)),
            datetime.date(2024, 5, 2),
        )

    # ------------------------------------------------------------------
    # count_business_days
    # ------------------------------------------------------------------

    def test_count_business_days(self):
        # 2026年6月は祝日がなく、平日は22日
        self.assertEqual(
            self.holidays.count_business_days(
                datetime.date(2026, 6, 1), datetime.date(2026, 6, 30)
            ),
            22,
        )
        # 2026年GW週（4/28～5/7）の営業日は 4/28, 4/30, 5/1, 5/7 の4日
        self.assertEqual(
            self.holidays.count_business_days("2026/04/28", "2026/05/07"),
            4,
        )
        # 単日（営業日）は1
        self.assertEqual(
            self.holidays.count_business_days(
                datetime.date(2026, 6, 1), datetime.date(2026, 6, 1)
            ),
            1,
        )
        # 単日（休日）は0
        self.assertEqual(
            self.holidays.count_business_days(
                datetime.date(2026, 5, 3), datetime.date(2026, 5, 3)
            ),
            0,
        )

    def test_count_business_days_invalid_range(self):
        with self.assertRaises(ValueError):
            self.holidays.count_business_days(
                datetime.date(2026, 6, 30), datetime.date(2026, 6, 1)
            )
        with self.assertRaises(ValueError):
            self.holidays_online.count_business_days("2024/05/07", "2024/05/01")

    def test_count_business_days_online(self):
        # 2024年GW週（4/30～5/7）の営業日は 4/30, 5/1, 5/2, 5/7 の4日
        self.assertEqual(
            self.holidays_online.count_business_days(
                datetime.date(2024, 4, 30), datetime.date(2024, 5, 7)
            ),
            4,
        )

    # ------------------------------------------------------------------
    # カスタム休日（単発・一括）
    # ------------------------------------------------------------------

    def test_add_custom_holidays(self):
        self.holidays.add_custom_holidays(
            "社休日", ["2026-06-15", datetime.date(2026, 6, 16)]
        )
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 6, 15)), "社休日"
        )
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 6, 16)), "社休日"
        )
        self.assertFalse(self.holidays.is_business_day(datetime.date(2026, 6, 15)))
        self.assertFalse(self.holidays.is_business_day(datetime.date(2026, 6, 16)))
        # 登録していない日は営業日のまま
        self.assertTrue(self.holidays.is_business_day(datetime.date(2026, 6, 17)))

    def test_add_custom_holidays_online(self):
        self.holidays_online.add_custom_holidays(
            "社休日", ["2024-06-10", datetime.date(2024, 6, 11)]
        )
        self.assertEqual(
            self.holidays_online.get_holiday_name(datetime.date(2024, 6, 10)),
            "社休日",
        )
        self.assertFalse(
            self.holidays_online.is_business_day(datetime.date(2024, 6, 11))
        )

    # ------------------------------------------------------------------
    # 年次カスタム休日ルール
    # ------------------------------------------------------------------

    def test_custom_holiday_rule_year_end_wrap(self):
        # "12/29-1/3" は年をまたぐ期間ルール:
        # 12/29～12/31 と 1/1～1/3 のどちらも判定する日付自身の年で照合される
        self.holidays.add_custom_holiday_rule("年末年始休業", "12/29-1/3")
        # 連続する2つの年で年末側・年始側の両方が休日になる
        for date in [
            datetime.date(2025, 12, 30),
            datetime.date(2026, 1, 2),
            datetime.date(2026, 12, 30),
            datetime.date(2027, 1, 2),
            datetime.date(2026, 12, 29),
            datetime.date(2026, 12, 31),
            datetime.date(2027, 1, 3),
        ]:
            self.assertEqual(self.holidays.get_holiday_name(date), "年末年始休業", date)
            self.assertTrue(self.holidays.is_holiday(date), date)
            self.assertTrue(self.holidays.is_additional_holiday(date), date)
        # 期間外は該当しない
        self.assertIsNone(self.holidays.get_holiday_name(datetime.date(2026, 12, 28)))
        # 1/4(2028年は火曜)は営業日
        self.assertTrue(self.holidays.is_business_day(datetime.date(2028, 1, 4)))
        # 営業日計算にも反映される: 2026/12/28(月)の翌営業日は2027/1/4(月)
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 12, 28), 1),
            datetime.date(2027, 1, 4),
        )

    def test_custom_holiday_rule_single_day(self):
        self.holidays.add_custom_holiday_rule("創立記念日", "8/15")
        # 毎年8/15が休日になる
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 8, 15)), "創立記念日"
        )
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2027, 8, 15)), "創立記念日"
        )
        self.assertIsNone(self.holidays.get_holiday_name(datetime.date(2026, 8, 14)))
        # 2027/8/15は日曜だが、ルール由来の休日は振替休日を発生させない
        self.assertEqual(datetime.date(2027, 8, 15).weekday(), 6)
        self.assertIsNone(self.holidays.get_holiday_name(datetime.date(2027, 8, 16)))
        self.assertTrue(self.holidays.is_business_day(datetime.date(2027, 8, 16)))

    def test_custom_holiday_rule_no_transfer(self):
        # 2027/1/3は日曜。ルール該当日が日曜でも翌月曜(1/4)は振替休日にならない
        self.holidays.add_custom_holiday_rule("年末年始休業", "12/29-1/3")
        self.assertEqual(datetime.date(2027, 1, 3).weekday(), 6)
        self.assertIsNone(self.holidays.get_holiday_name(datetime.date(2027, 1, 4)))
        self.assertTrue(self.holidays.is_business_day(datetime.date(2027, 1, 4)))

    def test_custom_holiday_rule_invalid(self):
        for rule in [
            "13/1",
            "1/32",
            "garbage",
            "1/1-",
            "2/30",
            "",
            "1-2",
            "1/1-2/3-4/5",
            "1/1 - 2/3",
            "a/b",
        ]:
            with self.assertRaises(ValueError, msg=rule):
                self.holidays.add_custom_holiday_rule("不正ルール", rule)

    def test_custom_holiday_rule_leap_day(self):
        # 2/29はうるう年にのみ存在する有効な月日として受け付ける
        self.holidays.add_custom_holiday_rule("うるう日", "2/29")
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2028, 2, 29)), "うるう日"
        )

    def test_custom_holiday_rule_online(self):
        # オンライン版でもルールは透過的に機能する（サポート範囲内: 2024年）
        self.holidays_online.add_custom_holiday_rule("年末年始休業", "12/29-1/3")
        self.assertEqual(
            self.holidays_online.get_holiday_name(datetime.date(2024, 1, 2)),
            "年末年始休業",
        )
        self.assertEqual(
            self.holidays_online.get_holiday_name(datetime.date(2023, 12, 30)),
            "年末年始休業",
        )
        # 法定祝日(元日)はオンラインデータの名称が優先される
        self.assertEqual(
            self.holidays_online.get_holiday_name(datetime.date(2024, 1, 1)), "元日"
        )
        self.assertFalse(
            self.holidays_online.is_business_day(datetime.date(2024, 1, 2))
        )

    # ------------------------------------------------------------------
    # 優先順位・境界
    # ------------------------------------------------------------------

    def test_statutory_name_precedence_over_custom(self):
        # 法定祝日と重なるルールは法定祝日名が優先される
        self.holidays.add_custom_holiday_rule("会社休日", "1/1")
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 1, 1)), "元日"
        )
        # 単発の追加休日も法定祝日名を上書きしない（オフライン版の既存動作）
        self.holidays.set_additional_holiday("独自の日", datetime.date(2026, 5, 5))
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 5, 5)), "こどもの日"
        )

    def test_custom_holiday_skipped_by_add_business_days(self):
        # 2026/6/17(水)を独自休日にすると営業日計算でスキップされる
        self.holidays.set_additional_holiday("臨時休業", datetime.date(2026, 6, 17))
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 6, 16), 1),
            datetime.date(2026, 6, 18),
        )
        # ルール由来の休日もスキップされる
        self.holidays.add_custom_holiday_rule("創立記念日", "6/18")
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 6, 16), 1),
            datetime.date(2026, 6, 19),
        )

    def test_clear_custom_holidays(self):
        self.holidays.set_additional_holiday("臨時休業", datetime.date(2026, 6, 17))
        self.holidays.add_custom_holiday_rule("年末年始休業", "12/29-1/3")
        self.assertFalse(self.holidays.is_business_day(datetime.date(2026, 6, 17)))
        self.assertFalse(self.holidays.is_business_day(datetime.date(2026, 12, 29)))

        self.holidays.clear_custom_holidays()

        self.assertIsNone(self.holidays.get_holiday_name(datetime.date(2026, 6, 17)))
        self.assertTrue(self.holidays.is_business_day(datetime.date(2026, 6, 17)))
        self.assertTrue(self.holidays.is_business_day(datetime.date(2026, 12, 29)))
        # 法定祝日には影響しない
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 1, 1)), "元日"
        )

    # ------------------------------------------------------------------
    # set_weekend
    # ------------------------------------------------------------------

    def test_set_weekend_saturday_business(self):
        saturday = datetime.date(2026, 6, 6)
        sunday = datetime.date(2026, 6, 7)
        # デフォルトは土日とも休業日
        self.assertFalse(self.holidays.is_business_day(saturday))
        self.assertFalse(self.holidays.is_business_day(sunday))

        self.holidays.set_weekend(saturday=False)
        # 土曜日は営業日になるが日曜日は休業日のまま
        self.assertTrue(self.holidays.is_business_day(saturday))
        self.assertFalse(self.holidays.is_business_day(sunday))
        # 祝日はset_weekendに関係なく非営業日（2026/8/15は土曜ではないが祝日確認用に別日）
        self.assertFalse(self.holidays.is_business_day(datetime.date(2026, 5, 3)))

        # get_rest_days_in_range のラベル付けは暦基準のまま（境界の確認）
        rest_days = self.holidays.get_rest_days_in_range(saturday, sunday)
        self.assertEqual(rest_days, [(saturday, "土曜日"), (sunday, "日曜日")])

        # 祝日判定（振替休日など）も影響を受けない
        self.assertEqual(
            self.holidays.get_holiday_name(datetime.date(2026, 5, 6)),
            "こどもの日（振替休日）",
        )

        # デフォルトに戻す
        self.holidays.set_weekend()
        self.assertFalse(self.holidays.is_business_day(saturday))

    def test_set_weekend_no_weekend(self):
        self.holidays.set_weekend(saturday=False, sunday=False)
        # 祝日・独自休日以外はすべて営業日
        self.assertTrue(self.holidays.is_business_day(datetime.date(2026, 6, 6)))
        self.assertTrue(self.holidays.is_business_day(datetime.date(2026, 6, 7)))
        # 祝日は営業日にならない（2026/5/3は日曜かつ憲法記念日）
        self.assertFalse(self.holidays.is_business_day(datetime.date(2026, 5, 3)))
        # 2026年6月は全30日が営業日
        self.assertEqual(
            self.holidays.count_business_days(
                datetime.date(2026, 6, 1), datetime.date(2026, 6, 30)
            ),
            30,
        )

    def test_set_weekend_business_day_helpers(self):
        # 2026年8月は1日(土)始まり。デフォルトの第1営業日は8/3(月)
        date = datetime.date(2026, 8, 1)
        self.assertEqual(
            self.holidays.get_first_business_day(date), datetime.date(2026, 8, 3)
        )
        # 土曜日を営業日にすると第1営業日は8/1(土)
        self.holidays.set_weekend(saturday=False)
        self.assertEqual(
            self.holidays.get_first_business_day(date), datetime.date(2026, 8, 1)
        )
        # 2026/8/31は月曜のため最終営業日は変わらず8/31
        self.assertEqual(
            self.holidays.get_last_business_day(date), datetime.date(2026, 8, 31)
        )
        # add_business_days / next_business_day にも反映される
        self.assertEqual(
            self.holidays.add_business_days(datetime.date(2026, 6, 5), 1),
            datetime.date(2026, 6, 6),
        )
        self.assertEqual(
            self.holidays.next_business_day(
                datetime.date(2026, 6, 6), include_start=True
            ),
            datetime.date(2026, 6, 6),
        )

    def test_set_weekend_online(self):
        saturday = datetime.date(2024, 6, 8)
        self.assertFalse(self.holidays_online.is_business_day(saturday))
        self.holidays_online.set_weekend(saturday=False)
        self.assertTrue(self.holidays_online.is_business_day(saturday))
        rest_days = self.holidays_online.get_rest_days_in_range(saturday, saturday)
        self.assertEqual(rest_days, [(saturday, "土曜日")])

    # ------------------------------------------------------------------
    # オンライン版: サポート範囲外はオフラインへフォールバック
    # ------------------------------------------------------------------

    def test_online_out_of_range_fallback(self):
        # フィクスチャのサポート範囲は2024-12-31まで。2026年GWは警告付きで
        # オフライン判定にフォールバックし、結果はオフライン版と一致する
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertEqual(
                self.holidays_online.add_business_days(datetime.date(2026, 5, 1), 1),
                datetime.date(2026, 5, 7),
            )
            self.assertEqual(
                self.holidays_online.count_business_days(
                    datetime.date(2026, 4, 28), datetime.date(2026, 5, 7)
                ),
                4,
            )


if __name__ == "__main__":
    unittest.main()

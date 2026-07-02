"""日本の祝日を扱うパッケージ"""

# 旧モジュールパス互換のシムを先にimportしておくことで、後から
# ``import flaretool.holiday.JapaneseHolidays`` されてもパッケージ属性の
# クラス束縛（下記のfrom-import）がモジュールで上書きされないようにする
import flaretool.holiday.JapaneseHolidays  # noqa: F401
import flaretool.holiday.JapaneseHolidaysOnline  # noqa: F401
from flaretool.holiday.japanese_holidays import JapaneseHolidays
from flaretool.holiday.online import JapaneseHolidaysOnline

__all__ = [
    "JapaneseHolidays",
    "JapaneseHolidaysOnline",
]

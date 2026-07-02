"""
旧モジュールパス互換のためのシム

実装は :mod:`flaretool.holiday.japanese_holidays` に移動しました。
`flaretool.holiday.JapaneseHolidays` というモジュールパスを
importしている既存コードのために残しています。
"""

from flaretool.holiday.japanese_holidays import JapaneseHolidays

__all__ = ["JapaneseHolidays"]

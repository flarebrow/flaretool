"""
旧モジュールパス互換のためのシム

実装は :mod:`flaretool.holiday.online` に移動しました。
`flaretool.holiday.JapaneseHolidaysOnline` というモジュールパスを
importしている既存コードのために残しています。
"""

from flaretool.holiday.online import JapaneseHolidaysOnline

__all__ = ["JapaneseHolidaysOnline"]

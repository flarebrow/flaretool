"""flaretool 全体で使用する列挙型の定義."""

from enum import Enum


class ConversionMode(Enum):
    """:func:`flaretool.utils.convert_value` の変換モード."""

    HALF_WIDTH = 1
    """半角に変換"""
    FULL_WIDTH = 2
    """全角に変換"""
    UPPER = 3
    """大文字に変換"""
    LOWER = 4
    """小文字に変換"""
    HIRAGANA = 5
    """ひらがなに変換"""
    KATAKANA = 6
    """カタカナに変換"""


class Base64Mode(Enum):
    """:func:`flaretool.utils.base64_convert` の処理モード."""

    ENCODE = 1
    """Base64エンコード"""
    DECODE = 2
    """Base64デコード"""


class HashMode(Enum):
    """:func:`flaretool.utils.hash_value` のハッシュアルゴリズム."""

    MD5 = 1
    SHA1 = 2
    SHA256 = 3
    SHA512 = 4

#!/bin/python
# -*- coding: utf-8 -*-
import base64
import hashlib
import os
import tempfile
import time
import flaretool
from flaretool.enums import ConversionMode, Base64Mode, HashMode


ASCII_ZENKAKU_CHARS = (
    u'ａ', u'ｂ', u'ｃ', u'ｄ', u'ｅ', u'ｆ', u'ｇ', u'ｈ', u'ｉ', u'ｊ', u'ｋ',
    u'ｌ', u'ｍ', u'ｎ', u'ｏ', u'ｐ', u'ｑ', u'ｒ', u'ｓ', u'ｔ', u'ｕ', u'ｖ',
    u'ｗ', u'ｘ', u'ｙ', u'ｚ',
    u'Ａ', u'Ｂ', u'Ｃ', u'Ｄ', u'Ｅ', u'Ｆ', u'Ｇ', u'Ｈ', u'Ｉ', u'Ｊ', u'Ｋ',
    u'Ｌ', u'Ｍ', u'Ｎ', u'Ｏ', u'Ｐ', u'Ｑ', u'Ｒ', u'Ｓ', u'Ｔ', u'Ｕ', u'Ｖ',
    u'Ｗ', u'Ｘ', u'Ｙ', u'Ｚ',
    u'！', u'”', u'＃', u'＄', u'％', u'＆', u'’', u'（', u'）', u'＊', u'＋',
    u'，', u'－', u'．', u'／', u'：', u'；', u'＜', u'＝', u'＞', u'？', u'＠',
    u'［', u'￥', u'］', u'＾', u'＿', u'‘', u'｛', u'｜', u'｝', u'～', u'　'
)

ASCII_HANKAKU_CHARS = (
    u'a', u'b', u'c', u'd', u'e', u'f', u'g', u'h', u'i', u'j', u'k',
    u'l', u'm', u'n', u'o', u'p', u'q', u'r', u's', u't', u'u', u'v',
    u'w', u'x', u'y', u'z',
    u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'I', u'J', u'K',
    u'L', u'M', u'N', u'O', u'P', u'Q', u'R', u'S', u'T', u'U', u'V',
    u'W', u'X', u'Y', u'Z',
    u'!', u'"', u'#', u'$', u'%', u'&', u'\'', u'(', u')', u'*', u'+',
    u',', u'-', u'.', u'/', u':', u';', u'<', u'=', u'>', u'?', u'@',
    u'[', u"¥", u']', u'^', u'_', u'`', u'{', u'|', u'}', u'~', u' '
)

KANA_ZENKAKU_CHARS = (
    u'ア', u'イ', u'ウ', u'エ', u'オ', u'カ', u'キ', u'ク', u'ケ', u'コ',
    u'サ', u'シ', u'ス', u'セ', u'ソ', u'タ', u'チ', u'ツ', u'テ', u'ト',
    u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ', u'ハ', u'ヒ', u'フ', u'ヘ', u'ホ',
    u'マ', u'ミ', u'ム', u'メ', u'モ', u'ヤ', u'ユ', u'ヨ',
    u'ラ', u'リ', u'ル', u'レ', u'ロ', u'ワ', u'ヲ', u'ン',
    u'ァ', u'ィ', u'ゥ', u'ェ', u'ォ', u'ッ', u'ャ', u'ュ', u'ョ',
    u'。', u'、', u'・', u'゛', u'゜', u'「', u'」', u'ー'
)

KANA_HANKAKU_CHARS = (
    u'ｱ', u'ｲ', u'ｳ', u'ｴ', u'ｵ', u'ｶ', u'ｷ', u'ｸ', u'ｹ', u'ｺ',
    u'ｻ', u'ｼ', u'ｽ', u'ｾ', u'ｿ', u'ﾀ', u'ﾁ', u'ﾂ', u'ﾃ', u'ﾄ',
    u'ﾅ', u'ﾆ', u'ﾇ', u'ﾈ', u'ﾉ', u'ﾊ', u'ﾋ', u'ﾌ', u'ﾍ', u'ﾎ',
    u'ﾏ', u'ﾐ', u'ﾑ', u'ﾒ', u'ﾓ', u'ﾔ', u'ﾕ', u'ﾖ',
    u'ﾗ', u'ﾘ', u'ﾙ', u'ﾚ', u'ﾛ', u'ﾜ', u'ｦ', u'ﾝ',
    u'ｧ', u'ｨ', u'ｩ', u'ｪ', u'ｫ', u'ｯ', u'ｬ', u'ｭ', u'ｮ',
    u'｡', u'､', u'･', u'ﾞ', u'ﾟ', u'｢', u'｣', u'ｰ'
)

DIGIT_ZENKAKU_CHARS = (
    u'０', u'１', u'２', u'３', u'４', u'５', u'６', u'７', u'８', u'９'
)

DIGIT_HANKAKU_CHARS = (
    u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9'
)

KANA_TEN_MAP = (
    (u'ガ', u'ｶ'), (u'ギ', u'ｷ'), (u'グ', u'ｸ'), (u'ゲ', u'ｹ'), (u'ゴ', u'ｺ'),
    (u'ザ', u'ｻ'), (u'ジ', u'ｼ'), (u'ズ', u'ｽ'), (u'ゼ', u'ｾ'), (u'ゾ', u'ｿ'),
    (u'ダ', u'ﾀ'), (u'ヂ', u'ﾁ'), (u'ヅ', u'ﾂ'), (u'デ', u'ﾃ'), (u'ド', u'ﾄ'),
    (u'バ', u'ﾊ'), (u'ビ', u'ﾋ'), (u'ブ', u'ﾌ'), (u'ベ', u'ﾍ'), (u'ボ', u'ﾎ'),
    (u'ヴ', u'ｳ')
)

KANA_MARU_MAP = (
    (u'パ', u'ﾊ'), (u'ピ', u'ﾋ'), (u'プ', u'ﾌ'), (u'ペ', u'ﾍ'), (u'ポ', u'ﾎ')
)


def convert_value(value: str, mode: ConversionMode = ConversionMode.HALF_WIDTH, ascii=True, digit=True, kana=True, non_convert_chars=None) -> str:
    """
    文字列を変換(半角/全角/大文字/小文字)

    Args:
        value (str): 変換する文字列
        mode (ConversionMode, optional): 変換モード. デフォルトはConversionMode.HALF_WIDTH.
        ascii (bool, optional): ASCII文字の変換を有効にするかどうか. デフォルトはTrue.
        digit (bool, optional): 数字の変換を有効にするかどうか. デフォルトはTrue.
        kana (bool, optional): カナ文字の変換を有効にするかどうか. デフォルトはTrue.
        non_convert_chars (str or list[str], optional): 変換しない文字列. デフォルトはNone.

    Returns:
        str: 変換後の文字列

    Raises:
        ValueError: 無効な変換モードが指定された場合
    """

    if non_convert_chars is None:
        non_convert_chars = []
    elif isinstance(non_convert_chars, str):
        non_convert_chars = [non_convert_chars]

    if mode in [ConversionMode.UPPER, ConversionMode.LOWER]:
        temp = []
        for c in value:
            if c in non_convert_chars:
                temp.append(c)
            else:
                temp.append(c.upper() if mode ==
                            ConversionMode.UPPER else c.lower())
        return ''.join(temp)

    tables = {
        'ascii_zh_table': {},
        'ascii_hz_table': {},
        'kana_zh_table': {},
        'kana_hz_table': {},
        'digit_zh_table': {},
        'digit_hz_table': {},
        'kana_ten_zh_table': {},
        'kana_ten_hz_table': {},
        'kana_maru_zh_table': {},
        'kana_maru_hz_table': {},
    }

    for (z, h) in zip(ASCII_ZENKAKU_CHARS, ASCII_HANKAKU_CHARS):
        tables['ascii_zh_table'][z] = h
        tables['ascii_hz_table'][h] = z

    for (z, h) in zip(KANA_ZENKAKU_CHARS, KANA_HANKAKU_CHARS):
        tables['kana_zh_table'][z] = h
        tables['kana_hz_table'][h] = z

    for (z, h) in zip(DIGIT_ZENKAKU_CHARS, DIGIT_HANKAKU_CHARS):
        tables['digit_zh_table'][z] = h
        tables['digit_hz_table'][h] = z

    for (z, h) in KANA_TEN_MAP:
        tables['kana_ten_zh_table'][z] = h
        tables['kana_ten_hz_table'][h] = z

    for (z, h) in KANA_MARU_MAP:
        tables['kana_maru_zh_table'][z] = h
        tables['kana_maru_hz_table'][h] = z

    temp = []
    prev = ''
    for c in value:
        if c in non_convert_chars:
            temp.append(c)
            prev = c
            continue

        if mode == ConversionMode.HALF_WIDTH:
            if ascii and c in tables['ascii_zh_table']:
                temp.append(tables['ascii_zh_table'][c])
            elif digit and c in tables['digit_zh_table']:
                temp.append(tables['digit_zh_table'][c])
            elif kana and c in tables['kana_zh_table']:
                temp.append(tables['kana_zh_table'][c])
            elif kana and c in tables['kana_ten_zh_table']:
                temp.append(tables['kana_ten_zh_table'][c])
                temp.append('ﾞ')
            elif kana and c in tables['kana_maru_zh_table']:
                temp.append(tables['kana_maru_zh_table'][c])
                temp.append('ﾟ')
            else:
                temp.append(c)
        elif mode == ConversionMode.FULL_WIDTH:
            if ascii and c in tables['ascii_hz_table']:
                temp.append(tables['ascii_hz_table'][c])
            elif digit and c in tables['digit_hz_table']:
                temp.append(tables['digit_hz_table'][c])
            elif kana and c == 'ﾞ' and prev in tables['kana_ten_hz_table']:
                temp.pop()
                temp.append(tables['kana_ten_hz_table'][prev])
            elif kana and c == 'ﾟ' and prev in tables['kana_maru_hz_table']:
                temp.pop()
                temp.append(tables['kana_maru_hz_table'][prev])
            elif kana and c in tables['kana_hz_table']:
                temp.append(tables['kana_hz_table'][c])
            else:
                temp.append(c)
        else:
            raise ValueError("Invalid conversion mode")
        prev = c
    return ''.join(temp)


def base64_convert(value: str, mode: Base64Mode = Base64Mode.ENCODE, encoding: str = 'utf-8') -> str:
    """
    文字列のBase64エンコードまたはデコードを行います。

    Args:
        value (str): エンコードまたはデコードする文字列
        mode (Base64Mode, optional): 処理モード. デフォルトはBase64Mode.ENCODE.
        encoding (str, optional): エンコードに使用する文字エンコーディング. デフォルトは'utf-8'.

    Returns:
        str: エンコードまたはデコード後の文字列

    Raises:
        ValueError: 無効な処理モードが指定された場合
    """
    if mode == Base64Mode.ENCODE:
        encoded_bytes = value.encode(encoding)
        encoded_value = base64.b64encode(encoded_bytes).decode(encoding)
        return encoded_value
    elif mode == Base64Mode.DECODE:
        decoded_bytes = base64.b64decode(value.encode(encoding))
        decoded_value = decoded_bytes.decode(encoding)
        return decoded_value
    else:
        raise ValueError("Invalid base64 mode")


def hash_value(value: str, mode: HashMode = HashMode.MD5, encoding: str = 'utf-8') -> str:
    """
    文字列のハッシュ計算を行います。

    Args:
        value (str): ハッシュ計算する文字列
        mode (HashMode, optional): ハッシュモード. デフォルトはHashMode.MD5.
        encoding (str, optional): 文字列のエンコーディング. デフォルトは'utf-8'.

    Returns:
        str: ハッシュ値の16進数表現

    Raises:
        ValueError: 無効なハッシュモードが指定された場合
    """
    if mode == HashMode.MD5:
        hash_object = hashlib.md5()
    elif mode == HashMode.SHA1:
        hash_object = hashlib.sha1()
    elif mode == HashMode.SHA256:
        hash_object = hashlib.sha256()
    elif mode == HashMode.SHA512:
        hash_object = hashlib.sha512()
    else:
        raise ValueError("Invalid hash mode")

    hash_object.update(value.encode(encoding))
    return hash_object.hexdigest()


class DictToFieldConverter:
    """
    This class converts a dictionary into field values.

    Args:
        dictionary (dict): The dictionary to convert.

    Attributes:
        dictionary (dict): The dictionary being converted.

    Raises:
        AttributeError: If a requested field does not exist in the dictionary.

    Example:
        # Create a dictionary
        dictionary = {'name': 'John', 'age': 30, 'city': 'Tokyo'}

        # Create an instance of DictToFieldConverter
        converter = DictToFieldConverter(dictionary)

        # Access field values
        name = converter.name
        age = converter.age
        city = converter.city

        print(name)  # Output: 'John'
        print(age)   # Output: 30
        print(city)  # Output: 'Tokyo'
    """

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __getattr__(self, field_name):
        if field_name in self.dictionary:
            return self.dictionary[field_name]
        else:
            raise AttributeError(
                f"'DictToFieldConverter' object has no attribute '{field_name}'")


def get_temp_dir_path():
    """
    Get the path to a temporary dir path.

    Returns:
        str: The path to the temporary path.
    """
    temp_dir = os.path.join(
        tempfile.gettempdir(),
        "python_{}".format(flaretool.__name__),
    )
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def is_file_fresh(file_path: str, days: int) -> bool:
    """
    Check if the given file has been modified within the specified number of days.

    Args:
        file_path (str): The path to the file.
        days (int): The number of days to check for freshness.

    Returns:
        bool: True if the file is fresh, False otherwise.
    """
    try:
        file_modified_time = os.path.getmtime(file_path)
        current_time = time.time()
        time_difference = current_time - file_modified_time
        return time_difference <= (days * 24 * 60 * 60)
    except FileNotFoundError:
        return False

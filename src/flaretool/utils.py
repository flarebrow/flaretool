"""汎用ユーティリティ関数群(文字列変換/ハッシュ/Base64/一時ディレクトリなど)."""

import base64
import hashlib
import tempfile
import time
from pathlib import Path

import flaretool
from flaretool.enums import Base64Mode, ConversionMode, HashMode

# fmt: off
ASCII_ZENKAKU_CHARS = (
    'ａ', 'ｂ', 'ｃ', 'ｄ', 'ｅ', 'ｆ', 'ｇ', 'ｈ', 'ｉ', 'ｊ', 'ｋ',
    'ｌ', 'ｍ', 'ｎ', 'ｏ', 'ｐ', 'ｑ', 'ｒ', 'ｓ', 'ｔ', 'ｕ', 'ｖ',
    'ｗ', 'ｘ', 'ｙ', 'ｚ',
    'Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ', 'Ｋ',
    'Ｌ', 'Ｍ', 'Ｎ', 'Ｏ', 'Ｐ', 'Ｑ', 'Ｒ', 'Ｓ', 'Ｔ', 'Ｕ', 'Ｖ',
    'Ｗ', 'Ｘ', 'Ｙ', 'Ｚ',
    '！', '”', '＃', '＄', '％', '＆', '’', '（', '）', '＊', '＋',
    '，', '－', '．', '／', '：', '；', '＜', '＝', '＞', '？', '＠',
    '［', '￥', '］', '＾', '＿', '‘', '｛', '｜', '｝', '～', '　'
)

ASCII_HANKAKU_CHARS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
    'W', 'X', 'Y', 'Z',
    '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+',
    ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
    '[', '¥', ']', '^', '_', '`', '{', '|', '}', '~', ' '
)

KANA_ZENKAKU_CHARS = (
    'ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク', 'ケ', 'コ',
    'サ', 'シ', 'ス', 'セ', 'ソ', 'タ', 'チ', 'ツ', 'テ', 'ト',
    'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
    'マ', 'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ',
    'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヲ', 'ン',
    'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ッ', 'ャ', 'ュ', 'ョ',
    '。', '、', '・', '゛', '゜', '「', '」', 'ー'
)

KANA_HANKAKU_CHARS = (
    'ｱ', 'ｲ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｸ', 'ｹ', 'ｺ',
    'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 'ﾀ', 'ﾁ', 'ﾂ', 'ﾃ', 'ﾄ',
    'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾉ', 'ﾊ', 'ﾋ', 'ﾌ', 'ﾍ', 'ﾎ',
    'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾖ',
    'ﾗ', 'ﾘ', 'ﾙ', 'ﾚ', 'ﾛ', 'ﾜ', 'ｦ', 'ﾝ',
    'ｧ', 'ｨ', 'ｩ', 'ｪ', 'ｫ', 'ｯ', 'ｬ', 'ｭ', 'ｮ',
    '｡', '､', '･', 'ﾞ', 'ﾟ', '｢', '｣', 'ｰ'
)

DIGIT_ZENKAKU_CHARS = (
    '０', '１', '２', '３', '４', '５', '６', '７', '８', '９'
)

DIGIT_HANKAKU_CHARS = (
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
)

KANA_TEN_MAP = (
    ('ガ', 'ｶ'), ('ギ', 'ｷ'), ('グ', 'ｸ'), ('ゲ', 'ｹ'), ('ゴ', 'ｺ'),
    ('ザ', 'ｻ'), ('ジ', 'ｼ'), ('ズ', 'ｽ'), ('ゼ', 'ｾ'), ('ゾ', 'ｿ'),
    ('ダ', 'ﾀ'), ('ヂ', 'ﾁ'), ('ヅ', 'ﾂ'), ('デ', 'ﾃ'), ('ド', 'ﾄ'),
    ('バ', 'ﾊ'), ('ビ', 'ﾋ'), ('ブ', 'ﾌ'), ('ベ', 'ﾍ'), ('ボ', 'ﾎ'),
    ('ヴ', 'ｳ')
)

KANA_MARU_MAP = (
    ('パ', 'ﾊ'), ('ピ', 'ﾋ'), ('プ', 'ﾌ'), ('ペ', 'ﾍ'), ('ポ', 'ﾎ')
)
# fmt: on

# 変換テーブル(モジュール読み込み時に一度だけ構築)
_ASCII_ZH_TABLE = dict(zip(ASCII_ZENKAKU_CHARS, ASCII_HANKAKU_CHARS, strict=True))
_ASCII_HZ_TABLE = dict(zip(ASCII_HANKAKU_CHARS, ASCII_ZENKAKU_CHARS, strict=True))
_KANA_ZH_TABLE = dict(zip(KANA_ZENKAKU_CHARS, KANA_HANKAKU_CHARS, strict=True))
_KANA_HZ_TABLE = dict(zip(KANA_HANKAKU_CHARS, KANA_ZENKAKU_CHARS, strict=True))
_DIGIT_ZH_TABLE = dict(zip(DIGIT_ZENKAKU_CHARS, DIGIT_HANKAKU_CHARS, strict=True))
_DIGIT_HZ_TABLE = dict(zip(DIGIT_HANKAKU_CHARS, DIGIT_ZENKAKU_CHARS, strict=True))
_KANA_TEN_ZH_TABLE = dict(KANA_TEN_MAP)
_KANA_TEN_HZ_TABLE = {h: z for z, h in KANA_TEN_MAP}
_KANA_MARU_ZH_TABLE = dict(KANA_MARU_MAP)
_KANA_MARU_HZ_TABLE = {h: z for z, h in KANA_MARU_MAP}

# 全角→半角は前後の文字に依存しないため、全フラグ有効時は str.translate で一括変換できる
_FULL_TO_HALF_TRANSLATE_TABLE = str.maketrans(
    _ASCII_ZH_TABLE
    | _DIGIT_ZH_TABLE
    | _KANA_ZH_TABLE
    | {z: h + "ﾞ" for z, h in _KANA_TEN_ZH_TABLE.items()}
    | {z: h + "ﾟ" for z, h in _KANA_MARU_ZH_TABLE.items()}
)


def convert_value(
    value: str,
    mode: ConversionMode = ConversionMode.HALF_WIDTH,
    ascii: bool = True,
    digit: bool = True,
    kana: bool = True,
    non_convert_chars: str | list[str] | None = None,
) -> str:
    """
    文字列を変換(半角/全角/大文字/小文字/ひらがな/カタカナ)<br>
    ひらがな/カタカナの変換は全角に変換されます

    Args:
        value (str): 変換する文字列
        mode (ConversionMode, optional): 変換モード. デフォルトはConversionMode.HALF_WIDTH.
        ascii (bool, optional): ASCII文字の変換を有効にするかどうか. デフォルトはTrue.
        digit (bool, optional): 数字の変換を有効にするかどうか. デフォルトはTrue.
        kana (bool, optional): カナ文字の変換を有効にするかどうか. デフォルトはTrue.
        non_convert_chars (str or list[str], optional): 変換しない文字列. デフォルトはNone.
            全角変換時、保護された文字は直後の濁点/半濁点との合成対象になりません
            (例: 'ｶﾞ' で 'ｶ' を保護すると 'ガ' に合成されず 'ｶ゛' になります).

    Returns:
        str: 変換後の文字列

    Raises:
        ValueError: 無効な変換モードが指定された場合
    """
    if non_convert_chars is None:
        non_convert_chars = []
    elif isinstance(non_convert_chars, str):
        non_convert_chars = [non_convert_chars]
    exclude_chars = frozenset(non_convert_chars)

    if mode == ConversionMode.HIRAGANA:
        value = convert_value(
            value, ConversionMode.FULL_WIDTH, non_convert_chars=non_convert_chars
        )
        return "".join(
            char
            if char in exclude_chars
            else (chr(ord(char) - 96) if "ァ" <= char <= "ヶ" else char)
            for char in value
        )

    if mode == ConversionMode.KATAKANA:
        value = convert_value(
            value, ConversionMode.FULL_WIDTH, non_convert_chars=non_convert_chars
        )
        return "".join(
            char
            if char in exclude_chars
            else (chr(ord(char) + 96) if "ぁ" <= char <= "ゖ" else char)
            for char in value
        )

    if mode in (ConversionMode.UPPER, ConversionMode.LOWER):
        return "".join(
            c
            if c in exclude_chars
            else (c.upper() if mode == ConversionMode.UPPER else c.lower())
            for c in value
        )

    if (
        mode == ConversionMode.HALF_WIDTH
        and not exclude_chars
        and ascii
        and digit
        and kana
    ):
        return value.translate(_FULL_TO_HALF_TRANSLATE_TABLE)

    temp: list[str] = []
    prev = ""
    prev_protected = False  # 直前の文字が non_convert_chars で保護されていたか
    for c in value:
        if c in exclude_chars:
            temp.append(c)
            prev = c
            prev_protected = True
            continue

        if mode == ConversionMode.HALF_WIDTH:
            if ascii and c in _ASCII_ZH_TABLE:
                temp.append(_ASCII_ZH_TABLE[c])
            elif digit and c in _DIGIT_ZH_TABLE:
                temp.append(_DIGIT_ZH_TABLE[c])
            elif kana and c in _KANA_ZH_TABLE:
                temp.append(_KANA_ZH_TABLE[c])
            elif kana and c in _KANA_TEN_ZH_TABLE:
                temp.append(_KANA_TEN_ZH_TABLE[c])
                temp.append("ﾞ")
            elif kana and c in _KANA_MARU_ZH_TABLE:
                temp.append(_KANA_MARU_ZH_TABLE[c])
                temp.append("ﾟ")
            else:
                temp.append(c)
        elif mode == ConversionMode.FULL_WIDTH:
            if ascii and c in _ASCII_HZ_TABLE:
                temp.append(_ASCII_HZ_TABLE[c])
            elif digit and c in _DIGIT_HZ_TABLE:
                temp.append(_DIGIT_HZ_TABLE[c])
            elif kana and c == "ﾞ" and not prev_protected and prev in _KANA_TEN_HZ_TABLE:
                temp.pop()
                temp.append(_KANA_TEN_HZ_TABLE[prev])
            elif (
                kana and c == "ﾟ" and not prev_protected and prev in _KANA_MARU_HZ_TABLE
            ):
                temp.pop()
                temp.append(_KANA_MARU_HZ_TABLE[prev])
            elif kana and c in _KANA_HZ_TABLE:
                temp.append(_KANA_HZ_TABLE[c])
            else:
                temp.append(c)
        else:
            raise ValueError("Invalid conversion mode")
        prev = c
        prev_protected = False
    return "".join(temp)


def base64_convert(
    value: str, mode: Base64Mode = Base64Mode.ENCODE, encoding: str = "utf-8"
) -> str:
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
    match mode:
        case Base64Mode.ENCODE:
            return base64.b64encode(value.encode(encoding)).decode(encoding)
        case Base64Mode.DECODE:
            return base64.b64decode(value.encode(encoding)).decode(encoding)
        case _:
            raise ValueError("Invalid base64 mode")


def hash_value(
    value: str, mode: HashMode = HashMode.MD5, encoding: str = "utf-8"
) -> str:
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
    if not isinstance(mode, HashMode):
        raise ValueError("Invalid hash mode")
    return hashlib.new(mode.name.lower(), value.encode(encoding)).hexdigest()


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

    def __init__(self, dictionary: dict) -> None:
        self.dictionary = dictionary

    def __getattr__(self, field_name: str):
        if field_name in self.dictionary:
            return self.dictionary[field_name]
        raise AttributeError(
            f"'DictToFieldConverter' object has no attribute '{field_name}'"
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.dictionary!r})"


def get_temp_dir_path() -> str:
    """
    Get the path to a temporary dir path.

    Returns:
        str: The path to the temporary path.
    """
    temp_dir = Path(tempfile.gettempdir()) / f"python_{flaretool.__name__}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return str(temp_dir)


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
        file_modified_time = Path(file_path).stat().st_mtime
    except FileNotFoundError:
        return False
    return (time.time() - file_modified_time) <= days * 24 * 60 * 60

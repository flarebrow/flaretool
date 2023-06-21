import unittest
from flaretool.utills import *


class UtillsTestCase(unittest.TestCase):

    def test_convert_value_half(self):
        test_cases = [
            ("ｱｲｳｴｵ", "アイウエオ"),
            ("ｶﾞｷﾞｸﾞｹﾞｺﾞ", "ガギグゲゴ"),
            ("ﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟ", "パピプペポ"),
            ("0123", "０１２３"),
            ("abcABC", "ａｂｃＡＢＣ"),
            ("#?!¥", "＃？！￥"),
            ("あいうえお", "あいうえお"),
            ("DEF", "ＤＥＦ"),
            ("xyzXYZ", "ｘｙｚＸＹＺ"),
            ("漢字", "漢字"),
            ("1234", "12３４"),
            ("@#$%", "＠＃＄％"),
            ("ｶﾀｶﾅ", "カタカナ"),
            ("ｱﾍﾞｺｺﾞ", "アベコゴ"),
            ("12345", "１２３４５"),
            ("abCD", "ａｂＣＤ"),
            ("亜伊宇江於", "亜伊宇江於"),
            ("!@#$%", "!＠＃＄％"),
            ("World", "Ｗｏｒｌｄ"),
        ]

        for expected, text in test_cases:
            result = convert_value(text, ConversionMode.HALF_WIDTH)
            self.assertEqual(result, expected)

    def test_convert_value_mode(self):
        # テストケース1: デフォルトの変換モード (半角に変換)
        assert convert_value("Ｈｅｌｌｏ") == "Hello"
        assert convert_value("１２３４５") == "12345"
        assert convert_value("カタカナ") == "ｶﾀｶﾅ"

        # テストケース2: フルウィズモード (全角に変換)
        assert convert_value(
            "Hello", mode=ConversionMode.FULL_WIDTH) == "Ｈｅｌｌｏ"
        assert convert_value(
            "12345", mode=ConversionMode.FULL_WIDTH) == "１２３４５"
        assert convert_value(
            "ｶﾀｶﾅ", mode=ConversionMode.FULL_WIDTH) == "カタカナ"

        # テストケース3: 変換しない文字列を指定
        assert convert_value(
            "Ｈｅｌｌｏ", non_convert_chars="ｏ") == "Hellｏ"  # 'ｏ' は変換しない
        assert convert_value("Ｈｅｌｌｏ", non_convert_chars=[
            "Ｈ", "ｅ"]) == "Ｈｅllo"  # 'Ｈ', 'ｅ' は変換しない

    def test_zen_to_han_ascii(self):
        text = "ＡＢＣａｂｃ１２３"
        expected = "ABCabc１２３"
        result = convert_value(
            text, ascii=True, digit=False, kana=False)
        self.assertEqual(result, expected)

    def test_han_to_zen_ascii(self):
        text = "ABCabc123"
        expected = "ＡＢＣａｂｃ123"
        result = convert_value(
            text, ConversionMode.FULL_WIDTH, ascii=True, digit=False, kana=False)
        self.assertEqual(result, expected)

    def test_zen_to_han_digit(self):
        text = "０１２３４５６７８９"
        expected = "0123456789"
        result = convert_value(text, ascii=False, digit=True, kana=False)
        self.assertEqual(result, expected)

    def test_han_to_zen_digit(self):
        text = "0123456789"
        expected = "０１２３４５６７８９"
        result = convert_value(
            text, ConversionMode.FULL_WIDTH, ascii=False, digit=True, kana=False)
        self.assertEqual(result, expected)

    def test_zen_to_han_kana(self):
        text = "アイウエオガギグゲゴ"
        expected = "ｱｲｳｴｵｶﾞｷﾞｸﾞｹﾞｺﾞ"
        result = convert_value(text, ascii=False, digit=False, kana=True)
        self.assertEqual(result, expected)

    def test_han_to_zen_kana(self):
        text = "ｱｲｳｴｵｶﾞｷﾞｸﾞｹﾞｺﾞ"
        expected = "アイウエオガギグゲゴ"
        result = convert_value(
            text, ConversionMode.FULL_WIDTH, ascii=False, digit=False, kana=True)
        self.assertEqual(result, expected)

    def test_zen_to_han_all(self):
        text = "ＡＢＣａｂｃ１２３０１２３４５６７８９アイウエオガギグゲゴ"
        expected = "ABCabc1230123456789ｱｲｳｴｵｶﾞｷﾞｸﾞｹﾞｺﾞ"
        result = convert_value(text, ascii=True, digit=True, kana=True)
        self.assertEqual(result, expected)

    def test_han_to_zen_all(self):
        text = "ABCabc1230123456789ｱｲｳｴｵｶﾞｷﾞｸﾞｹﾞｺﾞﾊﾟ"
        expected = "ＡＢＣａｂｃ１２３０１２３４５６７８９アイウエオガギグゲゴパ"
        result = convert_value(
            text, ConversionMode.FULL_WIDTH, ascii=True, digit=True, kana=True)
        self.assertEqual(result, expected)

    def test_lower(self):
        text = "ABCabc"
        expected = "abcabc"
        result = convert_value(
            text, ConversionMode.LOWER)
        self.assertEqual(result, expected)

    def test_upper(self):
        text = "ABCabc"
        expected = "ABCABC"
        result = convert_value(
            text, ConversionMode.UPPER)
        self.assertEqual(result, expected)

    def test_convert_value_raise(self):
        with self.assertRaises(ValueError):
            convert_value("test", "test")

    def test_base64_convert(self):
        # Base64Mode.ENCODEの場合
        result = base64_convert("Hello, World!", Base64Mode.ENCODE)
        self.assertEqual(result, "SGVsbG8sIFdvcmxkIQ==")

        # Base64Mode.DECODEの場合
        result = base64_convert("SGVsbG8sIFdvcmxkIQ==", Base64Mode.DECODE)
        self.assertEqual(result, "Hello, World!")

        # error
        with self.assertRaises(ValueError):
            base64_convert("test", "test")

    def test_hash_value(self):
        # HashMode.MD5の場合
        result = hash_value("Hello, World!", HashMode.MD5)
        self.assertEqual(result, "65a8e27d8879283831b664bd8b7f0ad4")

        # HashMode.SHA1の場合
        result = hash_value("Hello, World!", HashMode.SHA1)
        self.assertEqual(result, "0a0a9f2a6772942557ab5355d76af442f8f65e01")

        # HashMode.SHA256の場合
        result = hash_value("Hello, World!", HashMode.SHA256)
        self.assertEqual(
            result, "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f")

        # HashMode.SHA512の場合
        result = hash_value("Hello, World!", HashMode.SHA512)
        self.assertEqual(
            result, "374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387")

        # error
        with self.assertRaises(ValueError):
            hash_value("test", "test")

    def test_dict_to_field_converter(self):
        dictionary = {'name': 'John', 'age': 30, 'city': 'Tokyo'}
        converter = DictToFieldConverter(dictionary)

        assert converter.name == 'John'
        assert converter.age == 30
        assert converter.city == 'Tokyo'

        try:
            assert converter.gender
        except AttributeError as e:
            assert str(
                e) == "'DictToFieldConverter' object has no attribute 'gender'"

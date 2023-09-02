import os
import shutil
import tempfile
import time
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

        text = "ABCabc"
        expected = "aBcabc"
        result = convert_value(
            text, ConversionMode.LOWER, non_convert_chars="B")
        self.assertEqual(result, expected)

    def test_upper(self):
        text = "ABCabc"
        expected = "ABCABC"
        result = convert_value(
            text, ConversionMode.UPPER)
        self.assertEqual(result, expected)

        text = "ABCabc"
        expected = "ABCaBc"
        result = convert_value(
            text, ConversionMode.UPPER, non_convert_chars=["a", "c"])
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

        self.assertEqual(converter.name, 'John')
        self.assertEqual(converter.age, 30)
        self.assertEqual(converter.city, 'Tokyo')

        with self.assertRaises(AttributeError) as e:
            converter.gender
        self.assertEqual(
            str(e.exception), "'DictToFieldConverter' object has no attribute 'gender'")

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # テストで作成した一時ディレクトリを削除
        # os.rmdir(self.temp_dir)
        shutil.rmtree(self.temp_dir)

    def test_get_temp_dir_path(self):
        temp_path = get_temp_dir_path()

        # パスが存在することを確認
        self.assertTrue(os.path.exists(temp_path))

        # 正しいディレクトリが作成されたことを確認
        expected_dir = os.path.join(
            tempfile.gettempdir(),
            "python_{}".format(flaretool.__name__),
        )
        self.assertEqual(temp_path, expected_dir)

    def test_is_file_fresh(self):
        # テスト用のファイルを作成
        file_path = os.path.join(self.temp_dir, "test_file.txt")
        with open(file_path, 'w') as file:
            file.write("Test content")

        # ファイルが存在し、現在の時間から24時間以内に変更されていることを確認
        self.assertTrue(is_file_fresh(file_path, days=1))

        # ファイルを24時間以上前に変更
        file_modified_time = os.path.getmtime(file_path)
        os.utime(file_path, (file_modified_time - 2 * 24 * 60 *
                 60, file_modified_time - 2 * 24 * 60 * 60))

        # ファイルが24時間以内に変更されていないことを確認
        self.assertFalse(is_file_fresh(file_path, days=1))

        # ファイルが存在しない場合も考慮
        self.assertFalse(is_file_fresh(
            "non_existent_file.txt", days=1))
